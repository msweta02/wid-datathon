# Build direction — Indonesia wheat-vulnerability / cassava-substitution

Companion to `CLAUDE.md`. That file owns the **infrastructure** (loaders, data
provenance, conventions, FAOSTAT gotchas) — don't duplicate it here. This file owns
the **thesis, deliverable state, and build queue**. The findings section below is filled from
an actual notebook-05 run — if you re-run with a newer FAOSTAT release, re-fill it rather than
leaving stale numbers in the deck.

## Thesis
Indonesia is the world's #1 wheat importer and grows **zero** wheat (tropical climate).
Demand is inelastic and rising. The domestic lever is **cassava -> MOCAF** (fermented
cassava flour), constrained on the production and processing sides. The deck argues:
**Problem (import vulnerability) -> Mechanism (why substitution fails today) -> Solution
(data-driven recommendation).**

## Reference numbers (from USDA GAIN ID2026-0010 — use these, don't re-derive from FAOSTAT)
- Indonesia grows no wheat — fully import-dependent.
- Wheat imports: 10.45 MMT (2024/25) -> 12.3 MMT forecast (2025/26).
- Wheat food consumption ~9.8 MMT; total ~11.6 MMT (2025/26).
- Feed wheat ~doubled (~1.1 -> 2.1 MMT) as millers substitute wheat for costly corn.
- Team's FAOSTAT import trend: ~+0.48 Mt/yr, R^2~=0.82 (2010–2024).
- Supplier fragility: Ukraine share ~26.8% -> 1.8% in one year (2021->2022 war);
  Australia (top-3 supplier) drought/El-Nino exposed.
- MOCAF conversion yields: ~20% community sun-dried, ~34.6% lab tape-yeast.
- Live 2026 angle: BMKG 50–60% moderate El Nino mid-2026; Citi raising wheat targets.

## Filled findings from notebook 05 (RUN 2026-09-01, FAOSTAT 2010-2024 — no brackets left)
- **Cassava base is shrinking.** Production **-34.7%** (23.9 -> 15.6 Mt), driven by **area -53.2%**
  (1.18M -> 0.55M ha) against **yield +39.6%**; corr(area, production) = +0.97.
- **Yield gap is real but small.** Indonesia is the **#2 cassava yielder of 40 peer producers**
  (>=50k ha harvested): 28.2 t/ha vs the frontier **India 35.6 t/ha** = a **20.6% gap**, and
  *at parity with the peer top-5 mean (28.1 t/ha)*. Closing it on today's area adds
  **+4.06 Mt, no new land**.
- **Area is the 4.4x bigger lever.** The 630k ha lost since 2010, at today's yield, is **+17.8 Mt** —
  more than the entire current crop. Yield alone cannot carry the substitution story.
- **Offset ceiling.** All 15.6 Mt -> MOCAF = 3.12-5.41 Mt flour = **32-55% of food-wheat demand**
  (9.8 MMT). Ceiling, not forecast.
- **Achievable band.** **10% blend**: 2.83-4.90 Mt fresh cassava (**18-31%** of crop), 0.98 Mt wheat
  avoided, worth **~$0.26bn/yr** at the sourced 2010-2026 mean ($265/t FOB) — range **$0.18bn** soft
  market to **$0.35bn** tight, **$0.51bn** at the 2022 peak (E3; supersedes the old "$0.25-0.34bn
  ($250-350/t)" assumption). **20% blend**: 5.66-9.80 Mt (**36-63%** of crop) — out of reach without
  new land or large diversion.
- **The land-neutral headline (best deck line).** Closing the yield gap alone funds an
  **8.3-14.3% blend from new cassava only** — no new land, no diversion. Processing yield
  (20% sun-dried vs 34.6% lab tape-yeast) decides which end of the range.

Correction worth knowing: the pre-run draft used a **40,000 kg/ha placeholder frontier** (=> a 29% gap).
The real peer frontier is 35,574 kg/ha and the raw global ranking is topped by micro-producers
(Guyana, 2,399 ha). Notebook 05 now filters to producers >=50k ha so the frontier is one Indonesia
could copy. Net effect: the yield story got *smaller*, and the land-retention story got bigger.

## Filled findings from notebook 06 — supplier side (RUN 2026-09-01)
Production-side backing for the deck's supply-chain-fragility argument (slides 3-5).
- **Suppliers are mid-sized, not giants.** Australia 34.1 Mt, Canada 35.9 Mt, Ukraine 22.4 Mt (2024)
  = **11.6% of world wheat** between them. Indonesia's security rests on a narrow slice.
- **All three top suppliers have lost >=34% of their crop in a single year since 2010**:
  Australia **-34%** (2017), Canada **-37%** (2021), Ukraine **-36%** (2022). Three shocks in
  fifteen years, one per supplier — not a tail risk.
- **The largest supplier is the least reliable.** Australia CV **26.5%** (highest of any major
  producer checked), swinging **14.5 -> 41.2 Mt** (2.8x).
- **Australia's swing is yield, not area** (yield CV 21.9% vs area CV 10.1%; corr(yield, prod)
  = +0.95 vs corr(area, prod) = +0.65). Steady footprint, wildly variable harvest => weather risk
  that no contract or acreage policy hedges. **This is where the El Nino / IOD angle belongs.**
- **Shocks are uncorrelated** (Aus-Ukr **-0.09**, Ukr-Can **-0.34**, Aus-Can **+0.20**) and land in
  different years => diversification is genuinely protective, and now quantified:
  Australia-only CV **26.5%** -> actual GAIN mix **14.9%** -> equal-weight top-3 **11.6%**
  (a further **22% relative** cut; worst single year -20% -> -15%).
- **Indonesia is not a marginal buyer.** 10.45 Mt = **31% of Australia's**, **47% of Ukraine's**,
  **29% of Canada's** entire 2024 crop. Mutual dependency = leverage, but no quiet spare capacity.
- **The tradeable pool is ~1/3 of world production.** China+India+Pakistan grow **36%** of world
  wheat and export almost none; the 7 major exporters are **34%**. "The world grows plenty of
  wheat" is not a comfort available to Indonesia.

**Two-track framing this unlocks:** supplier rebalancing is cheap/fast and worth a **~22% cut in
supply volatility** but cannot reduce the 12.3 Mt Indonesia must buy; cassava->MOCAF reduces the
volume but is bounded at an **8-14% blend** land-neutral. Present as two tracks with the volatility
number on one and the blend band on the other. Neither is sufficient alone.

## Filled findings from notebook 07 — land use + substitute bench (RUN 2026-09-01)
Closes the two gaps this file previously called the deck's weakest links.
- **Indonesia is NOT short of cropland.** Total area harvested across all crops **rose 3.75M ha**
  (34.54M -> 38.28M ha, 2010->2024). The staple decline is a **reallocation, not a shortage** —
  and reallocations respond to policy in a way shortages do not.
- **Oil palm took 8.54M ha** (5.78M -> 14.32M, **+148%**) while 6 food staples gave up **5.04M ha**.
  Oil palm's gain = **1.7x** the staples' combined loss, **13.6x** cassava's entire area loss.
- **The ask is small:** restoring cassava to its 2010 footprint needs **7.4% of the oil palm land
  ADDED since 2010**. Use this framing — it converts "we need land" into a rounding error.
- *Limit:* area coincidence, not parcel-level conversion. Rules out "no land available" (the
  objection the recommendation must clear); proving the pathway needs SUSTAIN land-cover data.
- **Cassava survives the substitute test by ELIMINATION** (stronger than assumption): rice is the
  crop wheat competes with; maize is the binding feed constraint and lost 38% of its area;
  sweet potato is 9% of cassava's volume and shrinking faster (-62% area); potato is the only
  growing starch crop (+20%) but 8% of cassava and not flour-capable. **Sago** is a real regional
  staple with **no FAOSTAT Indonesian series** — name it as a data gap, don't silently omit it.
- **NEW MECHANISM — the maize channel.** Maize area **-38%**, production **-40% off its 2017 peak**
  (25.2 -> 15.1 Mt). Less/dearer domestic corn -> feed millers substitute wheat (GAIN: 1.1 -> 2.1 MMT).
  So there are **two independent routes** into wheat dependence, and **MOCAF only addresses the food
  stream (9.8 MMT)** — it does nothing for the ~2.1 MMT feed stream. The deck currently has no lever
  there at all. Maize land retention is a separate ask.
- **Ranked action set** (`outputs/tables/grow_action_levers.csv`): **A** processing yield 20->34.6%
  (cuts cassava needed per tonne of wheat by 42%, no land) -> **B** cassava land retention
  (+17.8 Mt) -> **C** close yield gap (+4.06 Mt, land-neutral, bounded) -> **D** maize retention
  (the only feed-side lever). Order the deck A, B, C, D.
- **Key reframe:** at a realistic 10-20% blend the binding constraint is **not raw cassava
  availability** — retention + yield gap alone would cover it several times over. It is processing
  capacity, conversion yield, and miller/consumer acceptance. *Production is not what limits this
  solution*, which is itself a GROW finding.

## Deliverable state (`Indonesia.pptx`, 11 slides — spine locked)
Open items, ranked:
1. ~~**Slide 8 (MOCAF blending/savings matrix)**~~ — **ASSET BUILT 2026-09-01.**
   `outputs/figures/idn_slide8_blend_and_savings.png` (two panels: cassava cost | USD saved) backed by
   `outputs/tables/slide8_mocaf_blend_matrix.csv`. **Takeaway on the slide:** *"A 10% wheat-flour blend
   is reachable on cassava's yield gap alone — 20% is not."*
   Five decisions taken against the DRAFT slide, all reversible but each with a reason:
   - **Baseline = GAIN food-wheat 9.8 MMT**, not the draft's `8.25M t` (which matches no sourced figure:
     not GAIN total 11.6, food 9.8, imports 10.45/12.3, nor GIEWS 11.5 — it appears unsourced).
   - **Baseline is the FOOD stream, not total imports.** The draft's declining "remaining wheat imports"
     line implies 1:1 substitution against all imports; MOCAF cannot touch the ~2.1 MMT feed stream
     (nb 07 §4), so that framing overstates.
   - **USD, not Rp trillion.** Rp would stack an FX assumption on top of the FOB/CIF one.
   - **Capped at 20%.** The draft ran to 30%; our own numbers say 20% already needs 36-63% of the entire
     crop, so showing 30% would contradict the analysis.
   - **Added the two strongest things the draft omitted:** the **conversion-yield axis** (20% sun-dried vs
     34.6% lab nearly halves the cassava needed — lever A) and the **yield-gap headroom line**
     (+4.06 Mt), which is what makes the 10%-vs-20% verdict visible.
   **Pre-build verification signed off** — `outputs/slide8_verification.md` (matrix FOB-clean, headline
   traceable, both cassava ranks confirmed #6-by-volume / #2-of-40-by-yield). Deck copy in
   `outputs/slide8_copy.md`.
   Residual: draft title reads "MOCA**G**" and the subtitle has a stray leading "A" — fix in the deck.
   Deck edit itself (.pptx) NOT done — `python-pptx` isn't installed and `OtherDetails/` is gitignored,
   so the deck is unversioned; back it up before any programmatic edit.
2. **El Nino angle** — now has a data home: nb 06 §4 shows Australia's production is yield-driven
   (yield CV 2.2x area CV), so climate variance *is* the supply risk. Pair the BMKG 50-60% moderate
   El Nino mid-2026 forecast with that chart rather than leaving it as background colour. Keep the
   deck's correct nuance that the 2018-19 drought was IOD-led, not El Nino.
3. ~~**Supplier % reconciliation**~~ — **resolved in nb 06 §1.** Slide 4's FAOSTAT calendar-2024
   split (Australia 25.5% / Ukraine 21.3%) and GAIN's Jul'25-Jan'26 split (37.8 / 18.3 / 16.1) are
   both *volume* bases; they differ by **window, not method** — GAIN's marketing year opens right
   after Australia's Nov-Jan harvest, which is when Australian share peaks. **Quote GAIN** for
   "who supplies Indonesia today", use slide 4's series only for the historical-instability point,
   footnote the window on both, and don't average them.
4. **Forecast caveat** — linear-only is fine for 15 points; keep the overfitting note visible.
5. **New: reframe the "grow more cassava" ask.** The data does not support a pure yield pitch —
   Indonesia is already #2 of 40 peers. Slide language should be land retention + processing yield.

## Build queue (for Claude Code)
Done (2026-09-01):
- ~~Notebook 05 frontier cell~~ — `src/load.py` now has **`load_qcl_world(item, elements)`**, reading
  grow-eda's `QCL_2010_2024.parquet` / `QCL_long.parquet`, dropping region aggregates (Area Code
  >= 5000) and FAOSTAT's China composite (code 351, was double-counting `China, mainland`).
  Real frontier wired in; peer-scale filter `PEER_MIN_AREA_HA = 50_000`.
- ~~Populate `04_synthesis`~~ — rewritten around the cassava recommendation, with a code cell that
  recomputes the headline numbers rather than restating them in prose.
- ~~Slide-8 savings model~~ — nb 05 §6: full matrix + $ saved + price sensitivity ($250/300/350/t),
  exported to `outputs/tables/slide8_mocaf_blend_matrix.csv`, plus the blend-requirement figure.
- Also fixed: two `''`-in-f-string bugs in nb 05 that were printing literal `{cur_area:,.0f}`.
- Also fixed (nb 02 + nb 04): **unit mixing in the tonnage ranking**. `Production` reports crops in
  `t` but eggs in `1000 No`, and `Hen eggs in shell, fresh` appears under both -> grouping by `Item`
  ranked **hen eggs as Indonesia's #2 crop by production** (146bn eggs summed with 6.6 Mt). New
  helper `clean.tonnes_only`. Corrected top-5: oil palm, rice, sugar cane, coconuts, cassava.
- **`FINDINGS.md` added** — consolidated record of all results, deliverables, corrections, limits.

Still open:
1. ~~**Replace the $300/t CIF wheat-price assumption**~~ — **done via E3** (World Bank Pink Sheet,
   sourced FOB basis + labelled CIF row). Residual: a true **CIF Indonesia** series would still be
   better than FOB-plus-assumed-freight, and would come from the TRADE track's import unit values.
2. ~~**Why did cassava area fall 53%?**~~ — **largely answered in nb 07 §2 without leaving GROW.**
   Total cropped area grew 3.75M ha while staples lost 5.04M ha and oil palm gained 8.54M ha, so it
   is reallocation rather than shortage. What remains for SUSTAIN is only the *parcel-level*
   conversion pathway; the "is there land?" question is settled.
3. **Download FAOSTAT trade (TM / detailed trade matrix).** Now the biggest data gap on this track:
   nb 06 has to carry supplier shares in as constants, so it cannot verify the deck's own two bases
   or compute Indonesia-specific import concentration (HHI) directly. Would also let the $/t import
   price in item 1 come from observed unit values.
4. **Optional GROW extensions** — cassava production concentration (supply security of the substitute
   itself); QV value angle (cassava worth more as flour than tapioca? QV has cassava at $4.76bn);
   tie land-conversion (SUSTAIN) to the cassava area decline in nb 03/05.

## Enrichment tasks (source-anchored — research done, do NOT re-research; fetch the named endpoint)
These came out of the official-sources research (2026-09-01). Each names a primary source, the figure
to pull, a guardrail, and the expected output. Verify every number at the primary portal before it
lands in a notebook or the deck (some were surfaced via aggregators — see CLAUDE.md provenance rule).
Ranked by analytical value. None changes the thesis; all harden it against a judge's probing.

- **E1 — Provincial reallocation overlay (BPS). ATTEMPTED 2026-09-01 — BLOCKED, NOT DONE.**
  **This is now the top remaining data gap on the track.** Documented here so it reads as a scoped
  limitation with known cost, not an oversight.
  - *Still the highest-value gap:* nb 07 §2 establishes reallocation as a **national-total coincidence**.
    Province-level data would test spatial co-location — if staple-area decline concentrates in the same
    provinces as oil-palm expansion, the mechanism moves from "both happened nationally" to "happened in
    the same places". It would also surface the honest complication that cassava land (Lampung, Java) and
    palm land (Sumatra, Kalimantan) may simply not be the same land.
  - *Why blocked — exact source state as checked:*
    - **BPS** exposes provincial **harvested area for rice (table 119) and maize (table 137) only** —
      **no cassava**, which is the crop the whole thesis turns on. Coverage is **2019–2025** (not the
      2010–2024 window the internal analysis uses) and single-year, behind an **account/API gate**.
      Landing page: `bps.go.id/en/statistics-table?subject=557`.
    - **Kementan's** fuller provincial series (`satudata.pertanian.go.id`) is **Cloudflare-blocked**
      (HTTP 403 on both the file and the portal root, with and without a browser user-agent).
    - Net: the accessible half (rice + maize, 2019–2025) cannot answer a **cassava** reallocation
      question, and the half that could is not reachable. Pulling it was judged not worth the effort.
  - *What it would take to unblock:* a BPS account/API key for the provincial tables **plus** a cassava
    provincial series (provincial BPS offices publish these separately), or manual retrieval of the
    Kementan PDF from a browser session.
  - *Guardrail if it is ever done:* BPS rice methodology breaks at **KSA (2018)** and moved to monthly
    tables (Mar 2025) — verify vintage across the window, never splice methods silently. BPS totals
    differ from FAOSTAT (different method) — label which is which.
  - *Consequence for the deck:* no island/province claim may come from this repo. Say "national data
    cannot localise this" rather than implying the reallocation is spatially proven.

- ~~**E2 — Land-conversion corroboration**~~ — **CLOSED 2026-09-01, partially: mechanism corroborated,
  magnitude not.** The named primary source was unreachable, so the scope was cut honestly rather than
  approximated. Added as a referenced markdown section at the end of **nb 07 §2**.
  - *What went in (all verified at origin, quotes checked):*
    - **USDA GAIN ID2026-0010, p. 20** — **ATR/BPN**, reiterating a BPS report, attributes ongoing paddy
      area loss to **conversion to non-agricultural uses (housing, industrial, infrastructure)**,
      concentrated on **Java** (60% of population). On-point corroboration of §2's structural mechanism.
    - **GAIN pp. 1, 4, 13** — paddy harvested area forecast to **decline in 2025/26 and 2026/27** as
      farmers switch paddy->corn under a potential moderate El Nino, *"since most corn and paddy are grown
      in the same fields"*. External confirmation that cropland is **substitutable between crops at field
      level** — the premise the reallocation reading needs. Also links El Nino to land use, not just to
      supplier risk (nb 06).
  - *A source that DISAGREES, reported not buried:* **FAO GIEWS Indonesia Country Brief (ref.
    29-Jan-2026)** gives the opposite near-term sign — 2026 First paddy crop *"area planted ... above the
    five-year average"*, and 2025 paddy 59 Mt (~9% above average) *"reflecting a price-driven expansion in
    the area planted"*. Two reconciliations, neither settled here: **planted vs harvested area** are
    different metrics (drought raises abandonment between them), and **both sources describe the 2025–27
    margin**, not the 2010–2024 structural trend. **Do not put "official sources confirm paddy area is
    falling" on a slide** — one of them says the opposite.
  - *Bonus corroboration of the wider thesis (GIEWS, same brief):* wheat imports forecast at a
    **near-record 11.5 MMT** in 2025/26 *"driven by population growth and increasing domestic consumption
    of wheat-based food products"*, and **maize imports 1.5 MMT**, well above average, *"reflecting strong
    demand by the domestic poultry industry"* — independent support for both the wheat dependence AND
    nb 07 §4's maize/feed channel.
  - *Guardrail honoured:* **no hectares-per-year conversion figure was stated.** The `~60-80k ha/yr` and
    `~79,600 ha (2019-2024)` figures previously listed in this file were **not** verifiable at the primary
    portal (see below), so they were kept out of the notebook entirely.
  - *Access gap, documented in the notebook itself:* Kementan *Statistik Lahan Pertanian* on
    `satudata.pertanian.go.id` returns **HTTP 403 (Cloudflare)** on both the PDF and the portal root;
    `www.pertanian.go.id` soft-404s the same path. So the conversion mechanism is corroborated **only at
    second hand** (GAIN -> ATR/BPN -> BPS), and the magnitude is unsourced.
  - *Correction to this file's own prior numbers:* the two figures staged for E2 **did not reconcile** —
    six years at 60-80k ha/yr is 360-480k ha, not ~79,600 ha (which implies ~13.3k ha/yr, ~5x lower).
    GAIN p. 20 carries the **60-80k ha/yr** rate but says nothing about a 79,600 ha cumulative; that
    cumulative figure appears spurious or differently scoped and should not be used.

- ~~**E3 — Wheat-price fix (World Bank Pink Sheet)**~~ — **DONE 2026-09-01.** Verified at origin
  (HRW Jul-2026 = $310.00/mt exactly, vintage "Updated on August 04, 2026").
  - *Built:* `src/load.load_wheat_prices()` (graceful fallback; vintage persisted as a column since
    `attrs` doesn't survive parquet). Workbook committed at `data/raw/CMO-Historical-Data-Monthly.xlsx`
    so the vintage is pinned. `openpyxl` added to `requirements.txt`. New figure
    `idn_wheat_price_history.png`. Matrix column renamed `saved_USDbn_FOB_mean` — basis is in the name.
  - *Headline result (matters for the deck):* the old **$300/t sat at the 70th percentile** of observed
    2010–2026 months, so the previous $-saved figures were **flattering, not conservative**. Sourced
    HRW mean is **$265/t**; observed range **$142 (2016M12) – $522 (2022M05)**, a **3.7x** swing.
    A 10% blend avoids 0.98 Mt of wheat = **~$0.26bn/yr at the 2010–2026 mean**, $0.18bn in a soft
    market, $0.35bn tight, $0.51bn at the 2022 war peak. **Replaces the old "$0.25–0.34bn ($250–350/t)".**
  - *Guardrail honoured, and widened:* the stated guardrail was FOB-vs-CIF. In fact the file carries
    **only US SRW/HRW** — so origin/route and wheat class differ too (see CLAUDE.md). Per decision,
    headline $ is reported **on the sourced FOB basis with the basis in the column name**, plus a
    clearly-labelled **assumed** +$25–55/t freight row (approx CIF $290–320/t) as a magnitude check only.
  - *Also found:* the Pink Sheet download URL rotates its vintage token and an old token serves data
    that stops years early. Don't hardcode the URL.

Build order status: ~~E3 done~~ → ~~E2 closed (mechanism only)~~ → **E1 blocked, top remaining gap.**
Enrichment is now CLOSED — no further source-chasing. Next work is deck build (slide 8). If short on time
before the deadline, E2+E3 are cheap and defensible; E1 is the one that adds genuinely new insight but
needs BPS data pulled and the methodology break handled.

## Intellectual-honesty guardrails (keep in the story, don't smooth over)
- Cassava **area is declining** — the solution's raw material is itself under pressure.
  Name it; it's what points policy at yield + land-retention.
- MOCAF flour-equivalent numbers are **ceilings** (cassava already has food/feed/starch
  uses) — present as a bounded band, never a point forecast.
- FAOSTAT is national-only — island/province claims come from external sources, not this data.
- **Don't pitch cassava yield as the fix.** Indonesia is already #2 of 40 peer producers and at the
  peer top-5 mean. The honest version is "the remaining gap is worth +4.06 Mt and funds an 8-14%
  blend on no new land" — real, bounded, and 4.4x smaller than the area already lost.
- Any yield "frontier" must be **peer-scale filtered**. The unfiltered global leader is Guyana on
  2,399 ha; using it inflates the gap and the whole opportunity.
- **Supplier shares are not ours.** They come from the deck/GAIN, not from this repo's data (no trade
  domain downloaded). Label them as external wherever they appear.
- **Don't claim oil palm "replaced" cassava field-by-field.** nb 07 shows area coincidence at the
  national level, which rules out a land shortage but is not parcel-level conversion evidence.
- **Don't present the 77% "blend equivalent" from nb 07 §5 as a target.** It is headroom. Baking
  functionality caps substitution far lower; the working band stays 10-20%.
- The nb 06 diversification metric is **production-side only** — it ignores freight, wheat
  protein/quality class (Australian ASW vs Canadian CWRS aren't interchangeable for every miller),
  and contract availability. Don't present "rebalance to equal weights" as costless.
- **Enrichment sources are external and must be cited at origin.** BPS / Kementan / World Bank data
  (tasks E1–E3) is not FAOSTAT and not this repo's — label it, and cite the primary `.go.id` / World
  Bank portal, never the aggregator that surfaced the figure. Same discipline as supplier shares.
- **Provincial co-location is not parcel conversion either.** Even if E1 shows staple loss and palm
  gain in the same provinces, that is province-level correlation, not field-level proof — a step up
  from national coincidence, not the end of the caveat. Keep the SUSTAIN land-cover gap named.
- **Never quote a Pink Sheet dollar figure without its basis.** The series is **FOB US Gulf, US HRW** —
  not CIF Indonesia, not Indonesia's suppliers (no AUS/UKR/CAN series exists in the file), not
  Indonesia's wheat class. The matrix column is named `saved_USDbn_FOB_mean` for exactly this reason;
  the CIF row is an **assumption** and is labelled as one. Don't let the label fall off in the deck.
- **Check the Pink Sheet vintage before quoting.** The download URL rotates a vintage token and an old
  token serves data that stops years early; `load_wheat_prices` carries `attrs["vintage"]` for this.
- **ENSO forecasts conflict across authorities and are probabilistic.** If the El Niño angle uses them,
  present BMKG and NOAA/IRI as a sourced range with dates, not a settled point forecast.
