# External sources — full links and link status

Every non-FAOSTAT source cited anywhere in this track, with the live URL and its HTTP status as
checked **2026-09-01**. Use this for the deck's citations slide.

**Status legend**
- ✅ **200** — resolves
- ⚠️ **403** — refuses automated requests (bot-filtering). Almost certainly fine in a browser;
  `fas.usda.gov` returns 403 even at its own domain root, so this is a blanket filter, not a dead page.
- ❌ **404** — dead. Must be replaced before use.

---

## 1. Primary data source (the analysis itself)

All production/area/yield numbers in notebooks 01–07 come from **FAOSTAT bulk downloads**, reused from
the sibling `grow-eda` / `sustain-eda` tracks — not re-downloaded here. Domains: QCL, QI, QV, RL.

- FAOSTAT: https://www.fao.org/faostat/en/#data ✅
- QCL metadata: https://www.fao.org/faostat/en/#data/QCL/metadata
- QI metadata: https://www.fao.org/faostat/en/#data/QI/metadata
- QV metadata: https://www.fao.org/faostat/en/#data/QV/metadata

---

## 2. Sourced external inputs (numbers that reach the deck)

| Source | Link | Status | Used for |
|---|---|---|---|
| **World Bank Commodity Markets ("Pink Sheet")** | https://www.worldbank.org/en/research/commodity-markets | ✅ 200 | Monthly wheat price → the slide-8 `$ saved` column (task E3). Take *Monthly prices* → `CMO-Historical-Data-Monthly.xlsx`. **The download URL rotates a vintage token — scrape the current link off this page, never hardcode it.** Vintage used: *Updated on August 04, 2026*. |
| **FAO GIEWS — Indonesia Country Brief** | https://www.fao.org/giews/countrybrief/country.jsp?code=IDN | ✅ 200 | nb 07 §2 counterpoint (2025 paddy area planted above the 5-yr average); near-record 11.5 MMT wheat imports; 1.5 MMT maize imports. Reference date used: **29-January-2026**. PDF: `https://www.fao.org/giews/countrybrief/country/IDN/pdf/IDN.pdf` ✅ |
| **USDA FAS GAIN — Indonesia Grain and Feed Annual, ID2026-0010** | https://fas.usda.gov/data/gain-report/2026/04 (portal) | ⚠️ 403 | Wheat demand 9.8 MMT food / 11.6 MMT total; imports 10.45 → 12.3 MMT; feed wheat 1.1 → 2.1 MMT; supplier shares (Australia 37.8% / Ukraine 18.3% / Canada 16.1%, Jul'25–Jan'26); **p.20** ATR/BPN paddy-conversion statement; **pp.1, 4, 13** paddy→corn switching. Local copy: `OtherDetails/2026-09-01/Grain and Feed Annual_Jakarta_Indonesia_ID2026-0010.pdf` |

### Access-blocked (documented gaps, no numbers taken)

| Source | Link | Status | Note |
|---|---|---|---|
| **Kementan — Statistik Lahan Pertanian** | https://satudata.pertanian.go.id/assets/docs/publikasi/Statistik_Lahan_Pertanian_Tahun_2015-2019.pdf | ❌ 403 Cloudflare | Task E2's intended primary source. Blocked on both the PDF and the portal root, with and without a browser user-agent. **No ha/yr conversion figure was taken from it.** |
| **BPS — provincial crop statistics** | https://www.bps.go.id/en/statistics-table?subject=557 | — | Task E1. Rice (table 119) and maize (table 137) provincial harvested area only — **no cassava**; 2019–2025; behind an account/API gate. |

---

## 3. Crop-calendar reference (nb 03 only — **not** FAOSTAT-derived)

**Why hand-compiled:** Indonesia is **not covered by FAO's own Crop Calendar tool**
(https://www.fao.org/agriculture/seed/cropcalendar/ ✅ 200 — covers ~58 countries, mostly
Africa/Central Asia/Latin America). So the table was assembled from published secondary sources.

**Nothing downstream consumes this** — no other notebook, no FINDINGS entry, not in the slide-8
material. No conclusion in the analysis rests on it.

| Crop | Harvest | Source | Link | Status |
|---|---|---|---|---|
| Rice — wet season | Feb–Apr | FAO GIEWS (legacy archive) | https://www.fao.org/4/y6611E/pays/ins0204e.htm | ✅ 200 |
| " | " | VOI (Indonesian news site) | https://voi.id/en/economy/415574 | ✅ 200 |
| Rice — dry season | Jul–Aug | *same sources as above* | — | — |
| Maize — rainy season | Jan–Feb | Paper: *Maize in Indonesia: Production Systems, Constraints and Research Priorities* (ResearchGate-hosted) | https://www.researchgate.net/publication/242469500_Maize_in_Indonesia_Production_Systems_Constraints_and_Research_Priorities | ⚠️ 403 |
| " | " | USDA FAS — Indonesia Grain and Feed Update | https://www.fas.usda.gov/data/indonesia-grain-and-feed-update-3 | ⚠️ 403 |
| Maize — dry season | Jul | *same sources as above* | — | — |
| Cassava | ~8–12 months after planting | FAO doc `x5032e` | https://www.fao.org/4/x5032e/x5032e01.htm | ✅ 200 |
| Sugar cane | May–Oct (Java milling) | USDA FAS — Indonesia Sugar Annual | https://www.fas.usda.gov/data/indonesia-sugar-annual | ⚠️ 403 |
| Oil palm | year-round | Musim Mas (palm-oil **company** blog) | https://www.musimmas.com/resources/blogs/what-is-palm-oil-from-seed-to-harvest/ | ✅ 200 |
| Cocoa | Feb–May + Aug–Sep | Indonesia Investments (commercial portal) | https://www.indonesia-investments.com/business/commodities/cocoa/item241 | ✅ 200 |
| Coffee — Robusta (Java) | May–Aug | Willkin Green Coffee (**retailer**) | https://greencoffee.willkinsales.com/indonesia-coffee-harvest-season/ | ❌ **404 — DEAD SITE** |
| Coffee — Arabica (N. Sumatra) | Mar–May + Oct–Dec | *same source* | — | ❌ **DEAD** |

### Required fixes before this table is used anywhere

1. **Coffee (2 rows) is now unsourced.** `greencoffee.willkinsales.com` returns 404 **at its domain
   root**, not just the cited page — the whole site is gone. Replace with **USDA FAS *Indonesia
   Coffee Annual*** (`fas.usda.gov/data`, search "Indonesia Coffee Annual") or drop both rows.
2. **Oil palm and cocoa** rest on a producer-company blog and a commercial portal. This fails the
   repo's own provenance rule (`CLAUDE.md`: cite the primary portal, *"not the aggregator that
   reported it"*). Re-source to USDA FAS annuals or label them clearly as trade-press orientation.
3. **ResearchGate is a hosting platform, not a publisher** — cite the paper itself (authors, journal,
   year), since ResearchGate both bot-blocks and sometimes gates content behind login.
4. **The FAO GIEWS rice link sits under FAO's `/4/` legacy document archive.** It resolves, but may be
   old for something as changeable as a planting calendar. Verify the vintage before quoting.

**Rows that are properly sourced today:** rice, maize, sugar cane (FAO GIEWS + USDA FAS). If the
calendar has to appear in the deck on short notice, keep those three and cut the rest.

---

## 4. Housekeeping note

`CLAUDE.md` and `CONTEXT.md` refer to `bps.go.id`, `satudata.pertanian.go.id` and
`worldbank.org/en/research/commodity-markets` as bare domains in backticks, without the `https://`
scheme, so they aren't clickable and don't show up in a URL scan. The full URLs are in §2 above.
