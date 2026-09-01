#!/usr/bin/env python
"""
Pre-flight guard: stop RETIRED numbers reaching the deck.

Several figures in this track have been superseded (a placeholder yield frontier, an
unsourced wheat price, a miscounted peer set). The risk is not that they were wrong —
they are fixed — but that a stale copy survives in one notebook's prose and gets read
out on a slide. This grep-with-an-allowlist makes that mechanical instead of a memory test.

Usage
-----
    python tools/check_stale_numbers.py            # scan notebooks/, exit 1 on unexpected hits
    python tools/check_stale_numbers.py --all      # also scan CLAUDE/CONTEXT/FINDINGS
    python tools/check_stale_numbers.py -v         # also list the allowlisted (intentional) hits

Design
------
Every retired figure gets a RetiredNumber entry: what it was, what replaced it, and an
explicit `allow` set of (notebook stem, substring-that-must-appear-on-the-line) pairs.
An allowlist entry is a *documented decision* — e.g. nb 05 deliberately keeps "$300/t"
next to the word "retired" to show the size of the correction. Anything not allowlisted
is reported as STALE and the script exits 1.

Deliberately NOT clever: it does not try to infer intent from nearby words. If a hit is
intentional, someone adds a line here and thereby records why. That is the point.

Docs are excluded by default: CONTEXT.md's E3 block and FINDINGS.md's corrections section
are *supposed* to quote the retired values. --all is there for an occasional manual look.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"
DOC_FILES = ("CLAUDE.md", "CONTEXT.md", "FINDINGS.md")


@dataclass(frozen=True)
class RetiredNumber:
    label: str
    pattern: str
    was: str
    now: str
    # (file stem, substring that must appear on the same line) -> intentional
    allow: tuple[tuple[str, str], ...] = field(default=())

    def regex(self) -> re.Pattern:
        return re.compile(self.pattern)

    def allowed(self, stem: str, line: str) -> bool:
        return any(stem == s and marker.lower() in line.lower() for s, marker in self.allow)


RETIRED = [
    RetiredNumber(
        label="wheat price $300/t (unsourced CIF assumption)",
        pattern=r"\$300\b|\b300\s*/\s*t\b|(IMPORT_PRICE_USD_T|OLD_ASSUMPTION_USD_T)\s*=\s*300",
        was="$300/t, described as a CIF assumption",
        now="World Bank Pink Sheet, US HRW FOB US Gulf; 2010-2026 mean $265/t (E3)",
        allow=(
            # nb 05 §6 shows the retired value on purpose, to size the correction.
            ("05_cassava_substitution", "used to rest on"),
            ("05_cassava_substitution", "OLD_ASSUMPTION_USD_T"),
            # nb 04 names it as retired when recording that the gap is closed.
            ("04_synthesis", "retired"),
        ),
    ),
    RetiredNumber(
        label="savings $0.29bn/yr (derived from the $300 assumption)",
        pattern=r"0\.29\s*bn",
        was="~$0.29bn/yr at a 10% blend",
        now="~$0.26bn/yr at the sourced $265/t FOB mean",
    ),
    RetiredNumber(
        label="savings band $0.25-0.34bn / $250-350/t",
        pattern=r"0\.25\s*[–-]\s*0\.34|\$250\b|\$350\b|\[\s*250\s*,\s*300\s*,\s*350\s*\]",
        was="a hand-picked $250/$300/$350 band",
        now="observed percentiles: p10 $180, mean $265, p90 $359, peak $522",
    ),
    RetiredNumber(
        label="cassava yield frontier 40,000 kg/ha (placeholder)",
        pattern=r"FRONTIER_YIELD_KG_HA\s*=\s*40|40[,_]?000(\.0)?\s*kg",
        was="40,000 kg/ha hardcoded placeholder (implied a 29% gap)",
        now="peer-scale frontier: India 35,574 kg/ha, a 20.6% gap",
    ),
    RetiredNumber(
        label="peer producer count 41",
        pattern=r"\b41 peers?\b|\bof 41\b",
        was="41 peer cassava producers",
        now="40, after dropping FAOSTAT's China composite (code 351)",
    ),
    RetiredNumber(
        label="gap-funded blend upper bound 14.4%",
        pattern=r"14\.4\s*%",
        was="8.3-14.4% blend",
        now="8.3-14.3% (nb 05 computes 14.35% -> 14.3%)",
    ),
]


def iter_notebook_lines(path: Path):
    """Yield (cell_index, cell_type, line_no, line) for a notebook's SOURCE only.

    Outputs are skipped on purpose: a stale number in a stored output is a signal the
    notebook needs re-running, not a prose edit, and would drown the report in noise.
    """
    nb = json.loads(path.read_text(encoding="utf-8"))
    for i, cell in enumerate(nb.get("cells", [])):
        src = "".join(cell.get("source", []))
        for ln, line in enumerate(src.splitlines(), 1):
            yield i, cell.get("cell_type", "?"), ln, line


def iter_doc_lines(path: Path):
    for ln, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        yield None, "markdown", ln, line


def scan(paths, verbose: bool) -> int:
    stale, intentional = [], []
    for path in paths:
        walker = iter_notebook_lines if path.suffix == ".ipynb" else iter_doc_lines
        for cell_i, cell_type, ln, line in walker(path):
            for retired in RETIRED:
                if retired.regex().search(line):
                    where = (f"cell {cell_i} ({cell_type}) line {ln}"
                             if cell_i is not None else f"line {ln}")
                    rec = (path.name, where, retired, line.strip())
                    (intentional if retired.allowed(path.stem, line) else stale).append(rec)

    if stale:
        print(f"STALE — {len(stale)} retired number(s) still present:\n")
        for name, where, retired, line in stale:
            print(f"  {name} :: {where}")
            print(f"    retired : {retired.label}")
            print(f"    was     : {retired.was}")
            print(f"    now     : {retired.now}")
            print(f"    line    : {line[:150]}\n")
    else:
        print("OK — no unexpected retired numbers found.")

    if intentional:
        print(f"({len(intentional)} allowlisted mention(s) — retired values kept on purpose"
              f"{'' if verbose else '; -v to list'})")
        if verbose:
            for name, where, retired, line in intentional:
                print(f"  ~ {name} :: {where} [{retired.label}]")
                print(f"      {line[:150]}")

    return 1 if stale else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true",
                    help="also scan CLAUDE.md / CONTEXT.md / FINDINGS.md (they quote retired "
                         "values by design, so expect hits)")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="list allowlisted mentions too")
    args = ap.parse_args()

    paths = sorted(NOTEBOOK_DIR.glob("*.ipynb"))
    if not paths:
        print(f"no notebooks found under {NOTEBOOK_DIR}", file=sys.stderr)
        return 2
    if args.all:
        paths += [ROOT / f for f in DOC_FILES if (ROOT / f).exists()]

    print(f"scanning {len(paths)} file(s) for {len(RETIRED)} retired number(s)\n")
    return scan(paths, args.verbose)


if __name__ == "__main__":
    raise SystemExit(main())
