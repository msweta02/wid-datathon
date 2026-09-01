# Indonesia GROW deep-dive — consolidated analysis record

**Track:** GROW (production side). **Scope:** what Indonesia grows or could grow.
TRADE / EAT / SUSTAIN are out of scope; where their data is needed it is named as a gap.
**Data:** FAOSTAT QCL / QI / QV (production) + RL (land use), 2010–2024, reused from
`../grow-eda` and `../sustain-eda`. See `CLAUDE.md` for loaders, `CONTEXT.md` for the
build queue and deck state.

**Status:** notebooks 01–07 all execute end-to-end, 0 errors. 18 figures, 3 tables.

---

## 1. The thesis, and what the production data does to it

**Deck thesis:** Indonesia is the world's #1 wheat importer and grows zero wheat; the domestic
lever is cassava → MOCAF (fermented cassava flour); the bottleneck is MOCAF processing.

**What GROW data confirms:** the structural zero, the scale of cassava, and the bottleneck's
location.
**What GROW data changes:** the constraint is *not* cassava agronomy. Indonesia is already near
the achievable cassava-yield frontier. The binding constraints are **land retention** and
**processing yield** — and there is a **second route into wheat dependence (maize)** that MOCAF
does not touch at all.

---

## 2. Findings by question

### 2.1 The structural zero (nb 05 §2)
- **Zero wheat records in QCL in every year 2010–2024** — literal absence, not a small number.
- Meanwhile: rice 53.1 Mt, cassava 15.6 Mt, maize 15.1 Mt (2024).
- There is no domestic wheat sector to scale — only a substitution question.

### 2.2 What Indonesia grows, and the shift (nb 02, 03, 07 §2)
- 2024 leaders by tonnage: oil palm fruit 243 Mt, rice 53.1 Mt, sugar cane 32.0 Mt,
  coconuts 18.0 Mt, cassava 15.6 Mt, maize 15.1 Mt.
- By value (QV): oil palm $32.3bn, rice $21.3bn, maize $5.6bn, cassava $4.76bn.
- **Cropping intensity fell 114% (2015) → 96% (2024)** (area harvested ÷ arable land). Dropping
  below 100% means Indonesia stopped double-cropping land it used to double-crop. *Proxy, not a
  calendar — FAOSTAT has no planting/harvest months.*
- **Every food staple lost area; every one raised yield.** Indonesia is not farming worse, it is
  farming less land.

| Crop | Production Δ | Area Δ | Yield Δ |
|---|---|---|---|
| Rice | −10.4% | −14.8% | +5.3% |
| Maize | −17.4% | −38.3% | +33.9% |
| Cassava | −34.7% | −53.2% | +39.6% |
| Soya beans | −74.9% | −79.8% | +24.2% |

### 2.3 Where the land went — the mechanism (nb 07 §2) ★
This was the deck's biggest unbacked link. It is answerable inside GROW.

- **Total cropped area ROSE 3.75M ha** (34.54M → 38.28M ha). Indonesia is **not short of
  cropland**. The staple decline is a **reallocation, not a shortage** — and reallocations
  respond to policy in a way shortages do not.
- **Oil palm took +8.54M ha** (5.78M → 14.32M, **+148%**) while six food staples gave up
  **−5.04M ha**.
  - Oil palm's gain = **1.7×** the six staples' combined loss.
  - Oil palm's gain = **13.6×** cassava's entire area loss (629,597 ha).
- **Therefore the ask is small:** restoring cassava to its 2010 footprint needs **7.4% of the oil
  palm land added since 2010**. This reframes "we need land" as a rounding error.
- Also supports the deck's bottleneck framing: an organised, consolidating plantation sector
  (+148%) beside a fragmenting smallholder staple sector is exactly the organisational asymmetry
  the deck describes — visible in data, not asserted.
- **Limit:** national area coincidence, *not* parcel-level conversion. QCL cannot show a given
  cassava field became oil palm. It **can** rule out "there is no land," which is the objection
  the recommendation must clear. Parcel proof needs land-cover data (SUSTAIN).

### 2.4 Is cassava even the right lever? (nb 07 §3)
Tested rather than assumed. Cassava wins **by elimination** — a stronger claim.

| Candidate | 2024 | Verdict |
|---|---|---|
| Rice | 53.1 Mt | The crop wheat competes with — diverting it moves the shortfall, not solves it |
| **Cassava** | **15.6 Mt** | **Scale + proven MOCAF route + near-frontier yield → the lever** |
| Maize | 15.1 Mt | Already the binding FEED constraint; own area −38% |
| Sweet potato | 1.48 Mt | 9% of cassava's volume; area falling faster (−62%) |
| Potato | 1.27 Mt | Only starch crop growing (+20%) but 8% of cassava, not flour-capable |
| Sago | **no FAOSTAT series** | Real Papua/Maluku staple, **unmeasurable here** — a data gap, not a zero |

### 2.5 Cassava: base, yield gap, and the MOCAF ceiling (nb 05)
- **Base shrinking:** production −34.7% (23.9 → 15.6 Mt), driven by **area −53.2%** against
  **yield +39.6%**; `corr(area, production) = +0.97`. The solution's own input is under pressure.
- **Yield headroom is real but small.** Indonesia is the **#2 cassava yielder of 40 peer
  producers** (≥50k ha): 28.2 t/ha vs India's 35.6 = a **20.6% gap**, and *at parity with the peer
  top-5 mean* (28.1 t/ha). Closing it fully on today's area adds **+4.06 Mt, no new land**.
  → **This is not a "teach them to farm" story.**
- **Area is the 4.4× bigger lever:** the 630k ha already lost, at today's yield, is **+17.8 Mt** —
  more than the entire current crop.
- **Offset ceiling:** all 15.6 Mt → MOCAF = 3.12–5.41 Mt flour = **32–55% of food-wheat demand**
  (9.8 MMT). A ceiling, not a forecast — cassava already feeds food/feed/starch demand.
- **Achievable band (slide 8):** a **10% blend** needs 2.83–4.90 Mt fresh cassava (18–31% of the
  crop), avoids 0.98 Mt wheat, saves **~$0.25–0.34bn/yr** ($250–350/t). A **20% blend** needs
  5.66–9.80 Mt (36–63% of the crop) — out of reach without new land or large diversion.
- **The land-neutral headline:** closing the yield gap alone funds an **8.3–14.3% blend from new
  cassava only**. Which end of the range depends on **processing yield**, not on farmers.

> ⚠ **Correction from the pre-run draft.** Notebook 05 originally used a hardcoded **40,000 kg/ha
> placeholder frontier** (implying a 29% gap). The real peer frontier is **35,574 kg/ha (India)**.
> The *unfiltered* global leader is **Guyana on 2,399 ha** — a garden plot, which would inflate the
> gap to 32%. Notebook 05 now filters to producers ≥50,000 ha. **Net effect: the yield story got
> smaller and the land-retention story got bigger.**

### 2.6 The maize channel — a second route into wheat dependence (nb 07 §4) ★
New. The deck treats feed-wheat growth as a demand quirk; it is a production story.

- Maize area **−38%** (4.13M → 2.55M ha); production **−40% off its 2017 peak** (25.2 → 15.1 Mt).
- Chain: less/dearer domestic corn → feed millers substitute wheat (GAIN: **1.1 → 2.1 MMT** feed
  wheat) → wheat imports rise for reasons unrelated to bread.
- **Scoping consequence:** nb 05 sized MOCAF against the **9.8 MMT food** stream. MOCAF does
  **nothing** for the ~2.1 MMT feed stream. **The deck currently has no lever there at all.**
  Maize land retention is a separate ask on a separate part of the import bill.

### 2.7 Supplier side — who grows Indonesia's wheat, and how reliably (nb 06)
Production-side backing for the deck's supply-fragility argument (slides 3–5).

- **Top 3 = 72.2% of imports:** Australia 37.8%, Ukraine 18.3%, Canada 16.1% (GAIN Jul'25–Jan'26).
- **They are mid-sized producers:** 34.1 / 22.4 / 35.9 Mt = **11.6% of world wheat** combined.
- **All three lost ≥34% of their crop in a single year since 2010:** Australia −34% (2017),
  Canada −37% (2021), Ukraine −36% (2022). Three shocks in fifteen years — not a tail risk.
- **The largest supplier is the least reliable:** Australia CV **26.5%**, the highest of any major
  producer checked, swinging **14.5 → 41.2 Mt** (2.8×).
- **Australia's swing is yield, not area:** yield CV **21.9%** vs area CV **10.1%**;
  `corr(yield, prod) = +0.95` vs `corr(area, prod) = +0.65`. Steady footprint, wildly variable
  harvest ⇒ **weather risk no contract or acreage policy hedges.** ← *this is where the El Niño /
  IOD angle belongs, quantified.* (Keep the deck's correct nuance that 2018–19 was IOD-led.)
- **Shocks are uncorrelated** (Aus–Ukr −0.09, Ukr–Can −0.34, Aus–Can +0.20) and land in different
  years ⇒ diversification is genuinely protective, and now sized:

| Sourcing mix | Supply-pool CV | Worst single year |
|---|---|---|
| Australia only | 26.5% | −34% |
| Actual mix (GAIN) | 14.9% | −20% |
| **Equal-weight top 3** | **11.6%** | **−15%** |

  → rebalancing off Australia-heavy = a further **22% relative** cut in supply volatility.
- **Indonesia is not a marginal buyer:** 10.45 Mt = **31% of Australia's**, **47% of Ukraine's**,
  **29% of Canada's** entire 2024 crop. Mutual dependency (leverage), but no quiet spare capacity.
- **The tradeable pool is ~⅓ of world production.** China + India + Pakistan grow **36%** of world
  wheat and export almost none; the 7 major exporters are **34%**. *"The world grows plenty of
  wheat"* is not a comfort available to Indonesia.
- **Supplier-% reconciliation (deck open item — resolved, nb 06 §1):** slide 4's FAOSTAT
  calendar-2024 split (Australia 25.5% / Ukraine 21.3%) and GAIN's Jul'25–Jan'26 split differ by
  **window, not method** — both are volume; GAIN's marketing year opens right after Australia's
  Nov–Jan harvest, when Australian share peaks. **Quote GAIN** for "who supplies Indonesia today,"
  use slide 4's series only for the historical-instability point, footnote the window on both,
  **don't average them.**

---

## 3. Recommendation — ranked and sized (nb 07 §5)

`outputs/tables/grow_action_levers.csv`

| # | Lever | Actor | Sized effect |
|---|---|---|---|
| **A** | Processing yield 20% → 34.6% MOCAF | Processors | Cuts cassava needed per tonne of wheat by **42%**; no new land, no new crop |
| **B** | Cassava land retention | Policymakers | **+17.8 Mt** cassava; needs **7.4%** of the oil palm land added since 2010 |
| **C** | Close cassava yield gap to India | Producers + extension | **+4.06 Mt**, land-neutral — real but bounded; **don't lead with it** (already #2 of 40) |
| **D** | Maize land retention | Policymakers | The **only** lever on the ~2.1 MMT **feed**-wheat stream |
| **E** | Supplier rebalancing (parallel track) | Policymakers / importers | **−22%** supply-pool volatility; does **not** reduce the volume imported |

**Order for the deck: A → B → C → D**, with E as the parallel non-production track.

**The reframe to put on the slide:** at a realistic **10–20% blend, raw cassava availability is
not the constraint** — retention plus the yield gap would cover it several times over. The
constraints are **processing capacity, conversion yield, and miller/consumer acceptance.**
*Production is not what limits this solution* — which is itself a GROW finding, and the honest
thing for a production-track deck to say.

**Two-track framing:** supplier rebalancing is cheap and fast and worth ~22% less volatility but
cannot reduce the 12.3 Mt Indonesia must buy; cassava → MOCAF reduces the volume but caps at an
8–14% blend on land-neutral terms. **Neither is sufficient alone.**

---

## 4. Deliverables

**Notebooks** (`notebooks/`, run 01→07)

| # | Notebook | Contribution |
|---|---|---|
| 01 | `01_data_loading` | Load + inventory |
| 02 | `02_what_it_grows` | Crop mix by production / area / value; rice decomposition |
| 03 | `03_when_it_grows` | Cropping-intensity proxy; 2015→2024 area decomposition |
| 04 | `04_synthesis` | Consolidated findings + scoped recommendation |
| 05 | `05_cassava_substitution` | Wheat zero; cassava trajectory; peer yield gap; MOCAF blend matrix |
| 06 | `06_supplier_side` | Supplier production, volatility, shock correlation, diversification math |
| 07 | `07_land_and_alternatives` | Land reallocation; substitute bench; maize channel; ranked levers |

**Tables** (`outputs/tables/`)
- `slide8_mocaf_blend_matrix.csv` — blend rate × MOCAF conversion → flour, fresh cassava, % of
  crop, wheat avoided, $ saved, % fundable by the yield gap
- `supplier_diversification_scenarios.csv` — sourcing mix → pool volatility, worst year
- `grow_action_levers.csv` — lever → actor → sized effect

**Key figures** (`outputs/figures/`, 18 total)
- `idn_staples_vs_wheat_zero` — the structural zero
- `idn_land_reallocation` ★ — total area grew while staples shrank; oil palm crossover
- `idn_substitute_candidates` ★ — cassava by elimination
- `idn_maize_channel` ★ — the second route into wheat dependence
- `idn_cassava_yield_vs_peers` — Indonesia already #2 of 40
- `idn_mocaf_blend_requirement` — slide 8 asset
- `idn_supply_supplier_production`, `idn_supply_australia_area_vs_yield`,
  `idn_supply_diversification` — supplier fragility

**Code** (`src/`)
- `load.load_qcl_world(item, elements)` — cross-country QCL slice; drops region aggregates
  (`Area Code >= 5000`) and FAOSTAT's China composite; caches per-item
- `clean.drop_china_composite` — code 351 double-counts `China, mainland`
- `clean.tonnes_only` — `Production` mixes `t` with `1000 No` (eggs); see §5

---

## 5. Corrections made to pre-existing work

1. **Placeholder yield frontier** (nb 05) — 40,000 kg/ha hardcoded → real peer frontier 35,574
   (India), with a ≥50k ha peer-scale filter. Changed the conclusion (see §2.5).
2. **China double-count** (new cross-country code) — FAOSTAT ships `China` (351, composite) beside
   `China, mainland` (41); both appeared in the first cassava peer ranking.
3. **Unit mixing in the tonnage ranking** (nb 02, nb 04) — `Production` reports crops in `t` but
   eggs in `1000 No`. Grouping by `Item` alone summed 146bn eggs with 6.6 Mt and ranked
   **hen eggs as Indonesia's #2 "crop" by production**. Fixed via `clean.tonnes_only`.
4. **Two `''`-in-f-string bugs** (nb 05) — terminated the f-string early, printing literal
   `{cur_area:,.0f}` instead of the value.

---

## 6. Honest limits and remaining gaps

**Cannot be closed with this data**
- **Sub-national / island-level analysis.** FAOSTAT is national-only. Java rice vs
  Sumatra/Kalimantan oil palm is exactly where the land-competition story lives, and a national
  aggregate hides it. Needs Indonesian **BPS provincial** data. *This is the only GROW-rubric item
  not covered.*
- **Sago** — a real regional flour staple with no FAOSTAT Indonesian series. Unsized.
- **Month-level crop calendar** — QCL/QI/QV/RL are annual; nb 03 uses cropping intensity as an
  explicit proxy. Real fix is FAO's Crop Calendar tool.

**Out of scope here, but named because the deck leans on them**
- **Import volumes and supplier shares are external constants** (deck slides 3–4, USDA GAIN) —
  this repo has no FAOSTAT trade domain. Never present a supplier share as if derived here.
  Adding a TM loader is the single highest-value data addition left.
- **$300/t CIF wheat price** in the slide-8 matrix is an assumption; TRADE should replace it with
  observed unit values. (Volume columns don't depend on it.)
- **Parcel-level land conversion** — SUSTAIN land-cover data.
- The nb 06 diversification metric is **production-side only**: it ignores freight, wheat
  protein/quality class (Australian ASW and Canadian CWRS are not interchangeable for every
  miller), and contract availability. "Rebalance to equal weights" is not costless.

**Presentation guardrails**
- MOCAF flour-equivalent figures are **ceilings**, never point forecasts.
- The **77% "blend equivalent"** in nb 07 §5 is **headroom, not a target** — baking functionality
  caps substitution far lower; the working band stays 10–20%.
- **Don't pitch cassava yield as the fix** — Indonesia is already #2 of 40 peers.
- **Don't claim oil palm replaced cassava field-by-field** — national area coincidence only.
