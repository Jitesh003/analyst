"""The corpus: SEC 10-K filings from 16 listed D2C/consumer companies.

Downloading, caching and HTML->text. Plumbing, not the skill -- the chunking
that consumes this is yours (Stage 3).

    python -m analyst.corpus          # download everything (~200MB, one-time)
    python -m analyst.corpus --dry    # list what it would fetch

Then:  from analyst.corpus import documents, facts
"""

import json
import os
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DATA = Path(__file__).resolve().parent.parent / "data"
SINCE = "2019-01-01"  # ~7 filings per company; enough to ask "what changed?"

# ticker -> CIK, from https://www.sec.gov/files/company_tickers.json
COMPANIES = {
    "BBWI": 701985,   "CHWY": 1766502,  "CROX": 1334036,  "DECK": 910521,
    "ELF": 1600033,   "ETSY": 1370637,  "FIGS": 1846576,  "HIMS": 1773751,
    "HNST": 1530979,  "LULU": 1397187,  "NKE": 320187,    "PTON": 1639825,
    "TPR": 1116132,   "ULTA": 1403568,  "WRBY": 1504776,  "YETI": 1670592,
}

_last_request = 0.0


def _get(url: str, dest: Path) -> bytes:
    """Fetch, cached on disk. SEC allows 10 req/sec; we stay well under."""
    global _last_request
    if dest.exists():
        return dest.read_bytes()

    ua = os.environ.get("SEC_USER_AGENT")
    if not ua:
        sys.exit("Set SEC_USER_AGENT in .env -- SEC requires 'Name email@host' "
                 "and blocks requests without it.")

    time.sleep(max(0, 0.15 - (time.monotonic() - _last_request)))
    _last_request = time.monotonic()

    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read()

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(body)
    return body


def filings(ticker: str) -> list[tuple[str, str]]:
    """[(filing_date, document_url)] for every 10-K since SINCE."""
    cik = COMPANIES[ticker]
    raw = _get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json",
               DATA / "meta" / f"{ticker}-submissions.json")
    recent = json.loads(raw)["filings"]["recent"]
    out = []
    for i, form in enumerate(recent["form"]):
        date = recent["filingDate"][i]
        if form != "10-K" or date < SINCE:
            continue
        acc = recent["accessionNumber"][i].replace("-", "")
        doc = recent["primaryDocument"][i]
        out.append((date, f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{doc}"))
    return sorted(out)


# ix:header holds inline-XBRL machine metadata -- ~1,300 tags of fasb.org
# URIs that would otherwise land at the top of every document and pollute
# every chunk built from it.
_DROP = ("script", "style", "ix:header")


class _Stripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in _DROP:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in _DROP:
            self.skip = max(0, self.skip - 1)

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def to_text(html: str) -> str:
    p = _Stripper()
    p.feed(html)
    text = "\n".join(p.parts)
    text = re.sub(r"[ \t\xa0]+", " ", text)
    return re.sub(r"\n\s*\n\s*\n+", "\n\n", text).strip()


def facts(ticker: str) -> dict:
    """XBRL financials -- the structured half of the project (Stage 5)."""
    cik = COMPANIES[ticker]
    raw = _get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json",
               DATA / "facts" / f"{ticker}.json")
    return json.loads(raw)


def load(ticker: str, year: int) -> str:
    """One filing's text, by ticker and filing year. Must already be cached."""
    hits = sorted((DATA / "filings").glob(f"{ticker}-{year}-*.htm"))
    if not hits:
        raise FileNotFoundError(f"no cached filing for {ticker} {year}")
    return to_text(hits[0].read_text(encoding="utf-8", errors="replace"))


def documents():
    """Yields (ticker, filing_date, text) for every cached filing."""
    for ticker in sorted(COMPANIES):
        for date, url in filings(ticker):
            dest = DATA / "filings" / f"{ticker}-{date}.htm"
            html = _get(url, dest).decode("utf-8", errors="replace")
            yield ticker, date, to_text(html)


def download() -> None:
    total = 0
    for ticker, date, text in documents():
        words = len(text.split())
        total += words
        print(f"  {ticker:5} {date}  {words:>7,} words")
    for ticker in sorted(COMPANIES):
        facts(ticker)
    print(f"\n{total:,} words across the corpus. Facts cached for "
          f"{len(COMPANIES)} companies in {DATA / 'facts'}.")


if __name__ == "__main__":
    if "--dry" in sys.argv:
        for ticker in sorted(COMPANIES):
            for date, url in filings(ticker):
                print(f"  {ticker:5} {date}  {url}")
    else:
        download()
