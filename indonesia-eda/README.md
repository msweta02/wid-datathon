# Indonesia Deep-Dive — GROW Track

**The question:** Indonesia is the world's largest wheat importer and produces **zero wheat** — not
a rounding error, literally absent from FAOSTAT in every year 2010–2024. It is also the world's
**#6 cassava producer**, and it invented **MOCAF** (fermented cassava flour), which substitutes for
wheat flour. So why hasn't substitution happened, and how far could it realistically go?

**The answer this track supports:**

> A **10% wheat-flour blend is reachable on cassava's yield gap alone — no new land, no diversion
> of today's crop. A 20% blend is not.**

The binding constraints are **land retention** and **processing yield**, not agronomy. Indonesia is
already the **#2 cassava yielder among the 40 countries that grow it at scale**, so "farm better"
is not a credible ask. Notebooks 01–07 establish that, bound it, and price it.

---

## Headline findings

| Finding | Number |
|---|---|
| Wheat produced domestically | **0** QCL records, every year 2010–2024 |
| Cassava production, 2010→2024 | **−34.7%** (23.9 → 15.6 Mt) |
| …driven by area | **−53.2%** (1.18M → 0.55M ha) — against yield **+39.6%** |
| Cassava yield rank | **#2 of 40** producers ≥50,000 ha (28.2 t/ha vs India's 35.6) |
| Yield-gap headroom on today's land | **+4.06 Mt**, funding an **8.3–14.3%** blend |
| Total cropped area, 2010→2024 | **+3.75M ha** — so the staple decline is *reallocation, not shortage* |
| Oil palm area gained | **+8.54M ha** (+148%) vs six staples' **−5.04M ha** |
| Restoring cassava's lost area would need | **7.4%** of the oil palm land added since 2010 |
| Supplier concentration | Australia 37.8% · Ukraine 18.3% · Canada 16.1% — and **all three lost ≥34% of their crop in a single year** since 2010 |
| Rebalancing to an even split | cuts supply volatility **CV 15.0% → 11.6%** (shocks are uncorrelated) |

Full detail, including every caveat: **[`FINDINGS.md`](FINDINGS.md)**.

---

## The four documents, and what each owns

This track keeps its prose in strict lanes. Read the one you need:

| File | Owns | Read it when |
|---|---|---|
| **[`FINDINGS.md`](FINDINGS.md)** | **Results** — every finding, number, correction, limit | You want to know *what we found* |
| **[`CLAUDE.md`](CLAUDE.md)** | **Infrastructure** — loaders, conventions, FAOSTAT gotchas | You're going to run or extend the code |
| **[`CONTEXT.md`](CONTEXT.md)** | **Build queue & deck state** — what's done, what's open | You're picking up the work |
| `README.md` (this) | **Orientation** | You just arrived |

---

## Notebooks

Run in order. All are committed **with outputs** — you can read the whole analysis without
executing anything.

| # | Notebook | What it does |
|---|---|---|
| 01 | `01_data_loading` | Load QCL/QI/QV filtered to Indonesia; inventory items, elements, years; flag quality |
| 02 | `02_what_it_grows` | Crop mix by production / area / value; rice area-vs-yield decomposition |
| 03 | `03_when_it_grows` | Cropping intensity as a multi-season proxy (114% in 2015 → 96% in 2024); which crops gave up the area. **States the month-data gap up front** |
| 04 | `04_synthesis` | 01–03 + 05 into one findings page and a scoped recommendation |
| 05 | `05_cassava_substitution` | **The thesis bridge.** Structural wheat-zero; cassava trajectory; peer-scale yield gap; MOCAF flour-equivalent; the blend × conversion decision matrix |
| 06 | `06_supplier_side` | Who actually grows Indonesia's wheat and how reliably — volatility, shock correlation, quantified diversification benefit |
| 07 | `07_land_and_alternatives` | Where the staple land went (oil palm); is cassava even the right lever (tested against the alternatives); the maize→feed-wheat channel; the ranked action set |

**Every trend or comparison table has a companion plot immediately after it, and the table stays.**
If you add a table, add its plot.

---

## Data

**No downloads of its own.** `src/load.py` reads the sibling tracks' already-downloaded FAOSTAT
bulk CSVs, filters to `Area == "Indonesia"` and 2010–2024, and caches a small parquet slice here —
so it never re-melts the ~4M-row global CSV twice.

- **QCL / QI / QV** ← `../grow-eda/data/raw/` (prefers grow-eda's own 2010–2024 cache if present)
- **RL — Land Use** ← `../sustain-eda/data/raw/` (for the cropping-intensity proxy)

grow-eda's notebooks are untouched: the 2010–2024 slice is an **additive** cache, not a replacement.
Run grow-eda's `01_data_loading` first, or just make sure those `_All_Data.csv` files exist.

### The one external download

Wheat prices come from the **World Bank Pink Sheet**, not FAOSTAT:

1. Go to <https://www.worldbank.org/en/research/commodity-markets>
2. Download *Monthly prices* → `CMO-Historical-Data-Monthly.xlsx`
3. Drop it in `data/raw/`

> The download URL embeds a rotating vintage token — **scrape the current link off that page, never
> hardcode it.** Stale tokens serve truncated data. The loader records the workbook's own vintage
> string so you can always check what you're quoting.

`load_wheat_prices()` returns `None` with a clear message if the workbook is absent; the notebook
degrades gracefully rather than inventing a price.

---

## Loaders

```python
from src.load import load_indonesia, load_landuse_indonesia, load_qcl_world, load_wheat_prices

qcl  = load_indonesia("QCL")        # Area, Item, Element, Unit, year, value, flag — 2010–2024
land = load_landuse_indonesia()     # None if sustain-eda's RL CSV isn't present
cas  = load_qcl_world("Cassava, fresh", ["Yield", "Production", "Area harvested"])   # all countries
px   = load_wheat_prices()          # World Bank Pink Sheet; None if the workbook is absent
```

Column names match grow-eda's raw convention, so code copies between tracks without renames.

### Two rules that are load-bearing

**Peer-scale filter — required, not optional.** Any cross-country yield "frontier" must be
restricted to producers at comparable scale (`>= 50_000 ha`). Unfiltered, the global cassava-yield
leader is **Guyana on 2,399 ha** — a garden plot, not an agronomic target — which inflates
Indonesia's apparent gap from 20.6% to 32%.

**`Production` mixes units.** Crops are in tonnes, eggs in `1000 No`, and `Hen eggs in shell,
fresh` appears under *both*. Grouping by `Item` alone summed 146bn eggs into the tonnage and ranked
eggs as Indonesia's #2 "crop". Always `clean.tonnes_only(df)` before a tonnage ranking.

`CLAUDE.md` carries the rest of the gotchas.

---

## Pre-flight check

```bash
python tools/check_stale_numbers.py       # exit 1 if a retired number survives anywhere
python tools/check_stale_numbers.py -v    # also list the intentional, allowlisted mentions
```

Several figures here were **superseded** during the analysis. The risk isn't that they were wrong —
they're fixed — it's that a stale copy survives in one notebook's prose and gets read out on a
slide. This makes that mechanical instead of a memory test, and it has already caught two.

Tracked: the `$300/t` wheat assumption, the `$0.29bn` / `$0.25–0.34bn` figures derived from it, the
`40,000 kg/ha` frontier placeholder, the `41`-peer count, and the `14.4%` blend bound.
**When you retire a number, add it to `RETIRED` in that script.**

---

## Outputs

```
outputs/
├── figures/                             24 charts
├── tables/
│   ├── slide8_mocaf_blend_matrix.csv    blend × conversion → cassava needed, wheat avoided, $ saved
│   ├── supplier_diversification_scenarios.csv   sourcing mix → volatility, worst year
│   └── grow_action_levers.csv           lever → actor → sized effect
├── slide8_copy.md                       deck copy: title, body, footnotes, speaker notes
├── slide8_verification.md               pre-build sign-off on the slide-8 numbers
└── sources.md                           every external source, with live link status
```

The deck asset is `figures/idn_slide8_blend_and_savings.png` (200 dpi).

---

## Honest limits

- **FAOSTAT is national-only.** No island or province claim can come from this repo. Java rice vs
  Sumatra/Kalimantan oil palm is exactly where the land story lives, and a national aggregate hides
  it. Provincial data was attempted and **blocked** — BPS publishes rice and maize provincial area
  but **not cassava**; Kementan's fuller series is Cloudflare-blocked. This is the top remaining gap.
- **Area coincidence is not parcel-level conversion.** Notebook 07 shows total cropped area grew
  while staples shrank, which rules out "there is no land." It cannot show that a *specific* cassava
  field became oil palm. That needs land-cover data.
- **No trade data.** Supplier shares and import volumes are carried in as **sourced external
  constants** (USDA GAIN, deck slides), never derived here. A FAOSTAT trade-domain loader is the
  single highest-value addition left.
- **The `$ saved` column is FOB, not CIF.** Sourced from the Pink Sheet's US HRW series — a global
  benchmark, not Indonesia's landed cost, and not even Indonesia's suppliers. The basis label must
  travel with the number everywhere.
- **Flour-equivalent figures are ceilings, not forecasts.** Cassava already serves food, feed and
  starch demand, so a blend competes with existing uses.
- **One near-term claim is contested.** USDA GAIN forecasts Indonesian paddy area declining; FAO
  GIEWS reports 2025 area planted *above* the five-year average. Notebook 07 §2 reports both rather
  than picking the convenient one. **Don't claim official sources confirm paddy area is falling.**
- **No month-level crop calendar exists in this data.** Notebook 03 uses cropping intensity as a
  genuine proxy and says so. Indonesia isn't covered by FAO's own Crop Calendar tool, so the
  reference table in 03 is compiled from published sources — several of which are weak, and one of
  which is now a dead link. See `outputs/sources.md` before citing any of it.
