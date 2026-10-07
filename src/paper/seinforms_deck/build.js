// Build the SEINFORMS 2026 EV Pulse NC deck (.pptx) from the locked outline.
//
// Usage (from this folder):  npm install && node build.js [output.pptx]
//
// Content source: conferences/seinforms-2026/presentation/deck-outline.md, which
// quotes every number from the SEINFORMS manuscript. Figures are the paper's
// PNGs in output/figures/, used as-is. Photos in assets/ come from the BIDA-670
// capstone deck. The .pptx output is gitignored; it lives in Google Drive.
//
// Copyright © 2026 Wolfgang Sanyer
// Licensed under the Polyform Noncommercial License 1.0.0 (see LICENSE).
const pptxgen = require("pptxgenjs");
const path = require("path");
const QRCode = require("qrcode");

const REPO_URL = "https://github.com/wolfieman/ev-pulse-nc";
let QR_REPO; // data URI, generated in main()

const FIG = path.resolve(__dirname, "../../../output/figures") + path.sep;
const OUT = process.argv[2] || "seinforms-2026-ev-pulse-nc.pptx";

// Palette matched to the showcase / BIDA-670 decks: white, light-blue cards, blue accent, navy text.
const NAVY = "0F2A4A", BLUE = "1F6FC5", CARD = "E3EFFB", CARD2 = "CFE3F8", MUTED = "5B6B7F",
      GREEN_BG = "E4F4E3", GREEN = "2E7D32", WHITE = "FFFFFF";
const FONT = "Calibri";

async function main() {
QR_REPO = "image/png;base64," + (await QRCode.toBuffer(REPO_URL, { width: 600, margin: 1, color: { dark: "#0F2A4A", light: "#FFFFFF" } })).toString("base64");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.title = "EV Pulse NC · SEINFORMS 2026";
pres.author = "Wolfgang Sanyer";
pres.theme = { headFontFace: FONT, bodyFontFace: FONT };

const W = 13.333, M = 0.6;

pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: WHITE },
  objects: [
    { text: { text: "EV Pulse NC · SEINFORMS 2026", options: { x: M, y: 7.05, w: 6, h: 0.3, fontFace: FONT, fontSize: 10, color: MUTED } } },
  ],
  slideNumber: { x: 12.2, y: 7.05, w: 0.6, h: 0.3, fontFace: FONT, fontSize: 10, color: MUTED, align: "right" },
});

function header(s, kicker, title) {
  s.addText(kicker.toUpperCase(), {
    x: M, y: 0.35, w: 6, h: 0.3, fontFace: FONT, fontSize: 11, bold: true, color: BLUE, charSpacing: 1.5, margin: 0, isTextBox: true,
  });
  s.addText(title, {
    x: M, y: 0.68, w: W - 2 * M, h: 0.85, fontFace: FONT, fontSize: 30, bold: true, color: NAVY, margin: 0, valign: "top", isTextBox: true,
  });
}

function card(s, x, y, w, h, fill = CARD) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: fill }, rectRadius: 0.08 });
}

function bullets(s, items, x, y, w, h, size = 17) {
  const runs = items.map((it, i) => {
    const parts = Array.isArray(it) ? it : [{ text: it }];
    return parts.map((p, j) => ({
      text: p.text,
      options: Object.assign(
        { breakLine: j === parts.length - 1 && i < items.length - 1, paraSpaceAfter: 14 },
        p.options || {}
      ),
    }));
  }).flat();
  s.addText(runs, { x, y, w, h, fontFace: FONT, fontSize: size, color: NAVY, valign: "top", margin: 0, isTextBox: true });
}

// Bold helper for inline emphasis: b("x") -> run
const b = (t) => ({ text: t, options: { bold: true } });
const t = (x) => ({ text: x });

function stat(s, x, y, w, h, big, label, bigSize = 34) {
  card(s, x, y, w, h);
  s.addText(big, { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: 0.75, fontFace: FONT, fontSize: bigSize, bold: true, color: BLUE, margin: 0, isTextBox: true });
  s.addText(label, { x: x + 0.2, y: y + 0.95, w: w - 0.4, h: h - 1.1, fontFace: FONT, fontSize: 15, color: NAVY, valign: "top", margin: 0, isTextBox: true });
}

function callout(s, text, y = 6.2, fill = CARD2, color = NAVY) {
  card(s, M, y, W - 2 * M, 0.62, fill);
  s.addText(text, { x: M + 0.25, y, w: W - 2 * M - 0.5, h: 0.62, fontFace: FONT, fontSize: 16, color, valign: "middle", margin: 0, isTextBox: true });
}

// Fit an image (pixel size pw x ph) inside a box, centered.
function fig(s, file, pw, ph, x, y, w, h) {
  const r = pw / ph;
  let iw = w, ih = w / r;
  if (ih > h) { ih = h; iw = h * r; }
  s.addImage({ path: FIG + file, x: x + (w - iw) / 2, y: y + (h - ih) / 2, w: iw, h: ih });
}

const content = () => pres.addSlide({ masterName: "CONTENT", sectionTitle: "Talk" });

// ---------- Slide 1: Title ----------
pres.addSection({ title: "Talk" });
{
  const s = pres.addSlide({ sectionTitle: "Talk" });
  s.background = { color: WHITE };
  s.addImage({ path: path.join(__dirname, "assets", "photo-title.jpg"), x: W - 5.0, y: 0, w: 5.0, h: 7.5 });
  s.addText("SEINFORMS 2026 · MYRTLE BEACH, SC · OCTOBER 2026", { x: M, y: 1.2, w: 7.4, h: 0.35, fontFace: FONT, fontSize: 12, bold: true, color: BLUE, charSpacing: 1.5, margin: 0, isTextBox: true });
  s.addText("EV Pulse NC: A Data-Driven Framework for Equitable and Demand-Driven EV Charging Infrastructure Investment Prioritization in North Carolina", {
    x: M, y: 1.7, w: 7.4, h: 2.9, fontFace: FONT, fontSize: 32, bold: true, color: NAVY, valign: "top", margin: 0, isTextBox: true,
  });
  s.addText([
    { text: "Wolfgang Sanyer", options: { bold: true, breakLine: true } },
    { text: "MBA, Business Analytics · Fayetteville State University", options: { breakLine: true } },
    { text: "Faculty Advisor: Dr. Majed Al-Ghandour", options: { fontSize: 16, color: MUTED } },
  ], { x: M, y: 4.9, w: 7.4, h: 1.3, fontFace: FONT, fontSize: 18, color: NAVY, valign: "top", margin: 0, isTextBox: true });
  s.addNotes("Good morning. I'm Wolfgang Sanyer, an MBA student in business analytics at Fayetteville State. This talk is about how North Carolina could decide where $109 million in federal EV charging money should go, and what the data says about where the real gaps are.");
}

// ---------- Slide 2: The Problem ----------
{
  const s = content();
  header(s, "The problem", "$109 Million. 100 Counties. No Allocation Framework.");
  const y = 1.9, h = 2.0, w = 3.85, g = 0.3;
  stat(s, M, y, w, h, "$109M", "NC's federal NEVI Formula Program funding", 44);
  stat(s, M + w + g, y, w, h, "No framework", "No publicly available, data-driven method for allocating it across counties", 34);
  stat(s, M + 2 * (w + g), y, w, h, "Feb 2026", "NCDOT shifts from 50 interstate-corridor stations toward 16 rural and community locations", 34);
  card(s, M, 4.3, W - 2 * M, 1.5);
  s.addText([
    { text: "Efficiency vs. equity", options: { bold: true, color: BLUE, breakLine: true } },
    { text: "Demand-driven allocation reinforces existing concentration; equity-driven allocation can place stations where use is too low to sustain them." },
  ], { x: M + 0.3, y: 4.4, w: W - 2 * M - 0.6, h: 1.3, fontFace: FONT, fontSize: 18, color: NAVY, valign: "middle", margin: 0, isTextBox: true });
  s.addNotes("North Carolina has $109 million in NEVI formula funding for public charging. What it doesn't have is a published, data-driven way to decide which counties get it. The two obvious approaches pull against each other. Follow demand, and you put chargers where they already are. Follow equity alone, and you can build stations nobody uses. NCDOT itself moved in February 2026, from a corridor-only plan to 16 rural and community sites. So this is a live decision, and the question is whether there's a defensible way to make it.");
}

// ---------- Slide 2a: Research questions (paper §1.3; BIDA-670 deck s5) ----------
{
  const s = content();
  header(s, "Research questions", "Five Questions Drive the Work");
  const qs = [
    ["Forecast Accuracy", "How accurate are SAS Model Studio's county-level BEV forecasts against unseen data?"],
    ["Demand-Supply Gaps", "Where are the largest demand-supply gaps?"],
    ["Sub-County Inequality", "How do ZIP-level density patterns reveal priorities county aggregation obscures?"],
    ["Commuter Flows", "How do commuting flows reshape demand once workplace needs are layered onto residential data?"],
    ["Defensible Rankings", "Can a weighted scoring equation translate these layers into defensible recommendations?"],
  ];
  qs.forEach((q, i) => {
    const y = 1.8 + i * 1.0;
    s.addShape(pres.shapes.OVAL, { x: M, y: y + 0.1, w: 0.7, h: 0.7, fill: { color: BLUE }, line: { color: BLUE } });
    s.addText(String(i + 1), { x: M, y: y + 0.1, w: 0.7, h: 0.7, fontFace: FONT, fontSize: 22, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, isTextBox: true });
    card(s, M + 0.95, y, W - 2 * M - 0.95, 0.9);
    s.addText(q[0], { x: M + 1.2, y, w: 3.2, h: 0.9, fontFace: FONT, fontSize: 19, bold: true, color: BLUE, valign: "middle", margin: 0, isTextBox: true });
    s.addText(q[1], { x: M + 4.5, y, w: W - 2 * M - 4.75, h: 0.9, fontFace: FONT, fontSize: 17, color: NAVY, valign: "middle", margin: 0, isTextBox: true });
  });
  s.addNotes("Five questions drive the work. Can the county forecasts be trusted on data they haven't seen? Where are the biggest gaps between demand and supply? What do ZIP codes show that county averages hide? How does commuting change where charging is needed? And can one weighted score turn all of that into a ranking you can defend? The rest of the talk answers them in order.");
}

// ---------- Slide 3: Demand Signal ----------
{
  const s = content();
  header(s, "Demand signal", "The BEV Fleet Grew 1,727% Since 2018. Ports Have Not Kept Pace.");
  const y = 1.95, h = 3.3, w = 2.85, g = 0.233;
  stat(s, M, y, w, h, "5,165 → 94,371", "BEVs, Sep 2018 → Jun 2025", 26);
  stat(s, M + (w + g), y, w, h, "53.8%", "Compound annual growth", 40);
  stat(s, M + 2 * (w + g), y, w, h, "Gini 0.805", "County-level BEV ownership is highly concentrated; Wake alone holds more BEVs than the bottom 60 counties combined", 32);
  stat(s, M + 3 * (w + g), y, w, h, "16.9", "BEVs per public port (Feb 2026) vs. IEA global benchmark ≈10", 40);
  callout(s, [t("Top 10 counties hold "), b("73%"), t(" of the statewide BEV fleet")], 5.6);
  s.addNotes("Demand isn't the question. The fleet went from 5,165 battery-electric vehicles in 2018 to 94,371 by mid-2025, a 53.8% annual growth rate. It's also very concentrated: a county-level Gini of 0.805, and Wake County alone has more EVs than the bottom 60 counties put together. Supply hasn't kept up. North Carolina has 16.9 EVs per public port, against a global benchmark of about 10. The top 10 counties hold 73% of the fleet, which is why the scoring focuses on them.");
}

// ---------- Slide 4: Pipeline ----------
{
  const s = content();
  header(s, "Method", "Five Analytical Phases, One Scoring Framework");
  const phases = [
    ["Phase 1", "Forecast validation", "NCDOT registrations, Sep 2018–Oct 2025"],
    ["Phase 2", "Infrastructure baseline", "NREL AFDC API, Feb 2026: 1,985 stations, 6,145 connectors"],
    ["Phase 3", "ZIP-level inequality", "Gini + additive Theil-T decomposition"],
    ["Phase 4", "Workplace charging demand", "LEHD LODES 2021"],
    ["Phase 5", "Justice40 equity overlay", "CEJST v2.0, area-weighted tract-to-ZCTA crosswalk"],
  ];
  const y = 1.9, h = 2.9, w = 2.3, g = 0.157;
  phases.forEach((p, i) => {
    const x = M + i * (w + g);
    card(s, x, y, w, h);
    s.addText(p[0].toUpperCase(), { x: x + 0.18, y: y + 0.18, w: w - 0.36, h: 0.3, fontFace: FONT, fontSize: 12, bold: true, color: BLUE, charSpacing: 1, margin: 0, isTextBox: true });
    s.addText(p[1], { x: x + 0.18, y: y + 0.55, w: w - 0.36, h: 0.85, fontFace: FONT, fontSize: 18, bold: true, color: NAVY, valign: "top", margin: 0, isTextBox: true });
    s.addText(p[2], { x: x + 0.18, y: y + 1.45, w: w - 0.36, h: 1.3, fontFace: FONT, fontSize: 14, color: NAVY, valign: "top", margin: 0, isTextBox: true });
  });
  s.addShape(pres.shapes.DOWN_ARROW, { x: W / 2 - 0.3, y: 4.95, w: 0.6, h: 0.45, fill: { color: BLUE }, line: { color: BLUE } });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: W / 2 - 2.6, y: 5.5, w: 5.2, h: 0.7, fill: { color: NAVY }, line: { color: NAVY }, rectRadius: 0.1 });
  s.addText("NEVI Priority Score", { x: W / 2 - 2.6, y: 5.5, w: 5.2, h: 0.7, fontFace: FONT, fontSize: 20, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText("All public data · 8,600 county-month observations · Python + SAS Model Studio", { x: M, y: 6.4, w: W - 2 * M, h: 0.4, fontFace: FONT, fontSize: 15, color: MUTED, align: "center", margin: 0, isTextBox: true });
  s.addNotes("The work runs in five phases. Phase 1 tests the demand forecasts on data they never saw. Phase 2 rebuilds the supply side from a full AFDC pull, all charger levels, not just fast chargers. Phase 3 measures inequality at the ZIP level. Phase 4 adds workplace demand from Census commuter flows. Phase 5 overlays the federal disadvantaged-community designations. Everything feeds one score. Every input is public, and the whole pipeline reruns from the repository.\n\n(Cut candidate for a 15-minute slot: move to backup.)");
}

// Figure + right column helper
function figRight(s, items, size = 16) { bullets(s, items, 8.25, 1.95, W - 8.25 - M, 4.9, size); }

// ---------- Slide 5: Forecast validation ----------
{
  const s = content();
  header(s, "Phase 1 · Forecast validation", "Forecasts Hold Out of Sample, and Adoption Is Accelerating");
  fig(s, "fig-44-validation-scatter.png", 4569, 3669, M, 1.75, 7.3, 5.15);
  figRight(s, [
    [b("MAPE 4.34%"), t(" on a true holdout (n = 400 county-months, Jul–Oct 2025, all 100 counties)")],
    [b("69.00%"), t(" of actuals exceeded forecast (mean bias +18.22 vehicles per county-month)")],
    [b("Chow test: F = 1,268.35, p < 1 × 10⁻⁶"), t(" at the Aug 2022 Inflation Reduction Act passage")],
    [t("95% interval coverage "), b("75.50% raw → 93.75%"), t(" after county bias correction: a centering problem, not a width problem")],
  ]);
  s.addNotes("First question: can we trust the demand forecasts? The SAS models were tested on four months they never saw, all 100 counties, 400 observations. The error was 4.34%, under the 5% usability bar. But look at the scatter: most points sit above the line. In 69% of cases actual registrations beat the forecast. That isn't a broken model. A Chow test puts a strong structural break at the Inflation Reduction Act in August 2022, F of 1,268.35. The models learned a slower world. The intervals are the right width but centered too low, so the fix is an upward buffer of 4 to 5% in planning, which the score carries.");
}

// ---------- Slide 6: Infrastructure gap ----------
{
  const s = content();
  header(s, "Phase 2 · Infrastructure gap", "58.5% of NC ZIP Areas Have No Charging Station");
  bullets(s, [
    [b("499 of 853"), t(" ZCTAs have zero stations: "), b("2.2 million people"), t(" (21.1% of the state)")],
    [t("Charlotte 28202: "), b("78.64"), t(" ports per 10,000 residents")],
    [t("Charlotte 28215, 14 miles east: "), b("0.31"), t(" (64,713 residents, 2 ports)")],
  ], M, 1.95, 6.6, 3.2, 18);
  card(s, M, 5.2, 6.6, 1.0, CARD2);
  s.addText("250-fold gap inside one county", { x: M + 0.25, y: 5.2, w: 6.1, h: 1.0, fontFace: FONT, fontSize: 24, bold: true, color: BLUE, valign: "middle", margin: 0, isTextBox: true });
  fig(s, "fig-24-heatmap-mecklenburg.png", 3384, 3669, 7.5, 1.6, W - 7.5 - 0.4, 5.35);
  s.addNotes("On the supply side, more than half of North Carolina's ZIP areas have no charger at all, covering 2.2 million people. That's not only a rural story. This map is Mecklenburg. Uptown Charlotte, the dark cluster, has 78.64 ports per 10,000 residents. Fourteen miles east, ZIP 28215 has 64,713 people and two ports. That's a 250-fold difference inside one county. Hold on to this picture, because the next slide shows it isn't an outlier.");
}

// ---------- Slide 7: Theil ----------
{
  const s = content();
  header(s, "Phase 3 · The headline finding", "84.5% of Charging Inequality Is Within Counties");
  fig(s, "fig-33-theil-decomposition.png", 4269, 2469, M, 1.75, 7.6, 4.45);
  stat(s, 8.5, 1.85, 2.0, 1.55, "84.5%", "within", 30);
  stat(s, 10.73, 1.85, 2.0, 1.55, "15.5%", "between", 30);
  bullets(s, [
    [t("Theil-T (top 10 counties) = "), b("0.5791"), t(" = between 0.0900 + within 0.4892")],
    [t("Exact additive decomposition (GE(1)); verified to "), b("2.22 × 10⁻¹⁶"), t("; Theil-L check: "), b("82.5%"), t(" within")],
    [t("ZIP-level charging Gini (statewide, population-weighted): "), b("0.566")],
  ], 8.5, 3.6, 4.23, 2.6, 15);
  callout(s, [t("County-only formulas miss most of the problem → "), b("two-tier design: county ranking + ZIP-level targeting")], 6.3);
  s.addNotes("This is the central result. The Gini tells you inequality is high, 0.566 across ZIP codes, but not where it lives. The Theil-T index splits exactly into a between-county part and a within-county part, with no residual. For the top 10 counties, 84.5% of the inequality is within counties, not between them. The Theil-L version gives 82.5%, so it isn't an artifact of the index. Mecklenburg and Wake alone account for about 70% of it. The implication is structural: most state NEVI formulas allocate by county, so they miss most of the problem. That is why the framework has two tiers: rank the counties, then target ZIP codes inside them.");
}

// ---------- Slide 8: Workplace demand ----------
{
  const s = content();
  header(s, "Phase 4 · Workplace demand", "Commuters Shift Demand Toward Employment Centers");
  fig(s, "fig-36-demand-comparison.png", 4269, 3069, M, 1.75, 7.3, 5.15);
  figRight(s, [
    [t("LEHD LODES 2021: 4,198,163 workers → "), b("859,260"), t(" EV-relevant commuters (income filter, ACS $75K household correction, 0.85 remote-work multiplier)")],
    [t("Net daily inflow: Mecklenburg "), b("+194,361"), t(" · Wake "), b("+126,517"), t(" · Durham "), b("+89,450")],
    [t("Union (ranked #1) is a bedroom community: "), b("−36,113"), t(" net per day")],
  ], 17);
  s.addNotes("Registration data tells you where EVs sleep, not where they park during the day. Census commuter flows fill that in. Starting from 4,198,163 workers, I filtered by income, corrected to EV-affordable households, and applied a remote-work adjustment, leaving 859,260 commuters. Mecklenburg takes in 194,361 more workers a day than it sends out. Union, which ends up ranked first, is a bedroom community of Charlotte, with a net outflow of 36,113 commuters a day; its residents drive to Mecklenburg for work. This feeds the cost-effectiveness pillar.\n\n(Cut candidate for a 15-minute slot: move to backup.)");
}

// ---------- Slide 9: Justice40 ----------
{
  const s = content();
  header(s, "Phase 5 · Justice40 overlay", "Where Stations Sit vs. Where Disadvantaged Communities Live");
  fig(s, "fig-42-stations-justice40-overlay.png", 6069, 3733, M, 1.7, 7.9, 4.86);
  bullets(s, [
    [b("43.0%"), t(" of NC census tracts designated disadvantaged (934 of 2,170; CEJST v2.0)")],
    [t("Top 10 counties: "), b("18.5%"), t(" population-weighted disadvantaged rate")],
    [b("24.5%"), t(" of stations (296 of 1,210) sit in disadvantaged tracts: roughly proportional overall, with "), b("strong county-by-county variation")],
    [t("Removing CEJST's climate category: "), b("7 of 10"), t(" study counties unchanged")],
  ], 8.75, 1.9, W - 8.75 - M, 4.7, 15);
  s.addText("CEJST v2.0 as of Jan 21, 2025; tool removed Jan 22, 2025 after EO 14008 was rescinded; data from the EDGI / PEDP archive", {
    x: M, y: 6.6, w: W - 2 * M, h: 0.35, fontFace: FONT, fontSize: 11, italic: true, color: MUTED, margin: 0, isTextBox: true,
  });
  s.addNotes("Phase 5 overlays the federal disadvantaged-community map. Statewide, 43.0% of tracts are designated disadvantaged. In the top 10 EV counties it's 18.5% of the population. About a quarter of stations, 24.5%, sit in those tracts. So in aggregate the siting is roughly proportional. The story is in the variation: some counties site stations in line with their disadvantaged population, others fall well short, and that variation is what drives the equity pillar. One caveat I want to be upfront about: the federal screening tool was taken down in January 2025. I use the archived v2.0 data, and removing its most contested category leaves 7 of 10 counties unchanged.");
}

// ---------- Slide 10: Scoring framework ----------
{
  const s = content();
  header(s, "The framework", "Three Pillars, One Score");
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 1.75, w: W - 2 * M, h: 0.85, fill: { color: NAVY }, line: { color: NAVY }, rectRadius: 0.1 });
  s.addText("NEVI Score = 0.40 × Equity + 0.35 × Utilization + 0.25 × Cost-Effectiveness", { x: M, y: 1.75, w: W - 2 * M, h: 0.85, fontFace: FONT, fontSize: 24, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, isTextBox: true });
  const pillars = [
    ["0.40", "Equity", "Analytical anchor on the Justice40 40% target (EO 14008, rescinded Jan 2025)"],
    ["0.35", "Utilization", "BEVs per port, from validated forecasts (strongest data)"],
    ["0.25", "Cost-Effectiveness", "Workplace demand (most uncertain input)"],
  ];
  const y = 2.9, h = 2.3, w = 3.85, g = 0.3;
  pillars.forEach((p, i) => {
    const x = M + i * (w + g);
    card(s, x, y, w, h);
    s.addText(p[0], { x: x + 0.2, y: y + 0.15, w: 1.3, h: 0.7, fontFace: FONT, fontSize: 36, bold: true, color: BLUE, margin: 0, isTextBox: true });
    s.addText(p[1], { x: x + 1.5, y: y + 0.15, w: w - 1.7, h: 0.7, fontFace: FONT, fontSize: 20, bold: true, color: NAVY, valign: "middle", margin: 0, isTextBox: true });
    s.addText(p[2], { x: x + 0.2, y: y + 0.95, w: w - 0.4, h: 1.25, fontFace: FONT, fontSize: 15, color: NAVY, valign: "top", margin: 0, isTextBox: true });
  });
  s.addText("Weights follow data confidence. Each pillar is a weighted composite of sub-metrics, min-max normalized to 0–1.", { x: M, y: 5.35, w: W - 2 * M, h: 0.5, fontFace: FONT, fontSize: 16, color: NAVY, margin: 0, isTextBox: true });
  callout(s, [t("Pillars are independent: "), b("max VIF 1.41"), t(" (concern threshold 5.0)")], 6.0, GREEN_BG);
  s.addNotes("The score combines three pillars. Each one is built from sub-metrics, all min-max normalized to a 0-to-1 scale. The weights follow data confidence. Equity gets 0.40, anchored on the Justice40 40% target. I treat that as an analytical anchor, not a legal requirement, since the executive order was rescinded in January 2025. Utilization gets 0.35 because it rests on the validated forecasts. Cost-effectiveness gets 0.25 because workplace demand is the least certain input. And the pillars aren't three views of one thing: the highest variance inflation factor is 1.41.");
}

// ---------- Slide 11: Rankings ----------
{
  const s = content();
  header(s, "The rankings", "Top 3: Union, Mecklenburg, Guilford");
  fig(s, "fig-43-nevi-priority-scores.png", 4869, 3369, M, 1.75, 7.3, 5.15);
  const top = [["1", "Union", "0.561"], ["2", "Mecklenburg", "0.548"], ["3", "Guilford", "0.465"]];
  top.forEach((r, i) => {
    const x = 8.25 + i * 1.53;
    card(s, x, 1.85, 1.43, 1.25);
    s.addText(r[2], { x, y: 1.9, w: 1.43, h: 0.6, fontFace: FONT, fontSize: 24, bold: true, color: BLUE, align: "center", margin: 0, isTextBox: true });
    s.addText(`#${r[0]} ${r[1]}`, { x, y: 2.5, w: 1.43, h: 0.5, fontFace: FONT, fontSize: 13, bold: true, color: NAVY, align: "center", margin: 0, isTextBox: true });
  });
  s.addText("Top 3 held across three perturbations:", { x: 8.25, y: 3.3, w: W - 8.25 - M, h: 0.4, fontFace: FONT, fontSize: 16, bold: true, color: NAVY, margin: 0, isTextBox: true });
  bullets(s, [
    "Equity weight 0.30–0.50 (five scenarios)",
    "Cost-effectiveness sub-weight extremes",
    "Remote-work multiplier 0.75 / 0.85 / 0.95 (cancels in normalization)",
  ], 8.25, 3.75, W - 8.25 - M, 1.8, 15);
  card(s, 8.25, 5.65, W - 8.25 - M, 1.15, CARD2);
  s.addText("Wake ranks 5th despite the most BEVs (equity 0.322; 8.1% of tracts disadvantaged)", { x: 8.4, y: 5.65, w: W - 8.25 - M - 0.3, h: 1.15, fontFace: FONT, fontSize: 15, color: NAVY, valign: "middle", margin: 0, isTextBox: true });
  s.addNotes("Here's the result. Union, Mecklenburg, and Guilford come out on top, and each bar shows how much of the score comes from each pillar. The top three held under three separate tests: moving the equity weight from 0.30 to 0.50, the extremes of the cost-effectiveness sub-weights, and the remote-work assumption, which cancels out in the normalization. To be precise about what that means: these are one-factor-at-a-time tests, not a full search over all weight combinations. Notice Wake: the most EVs in the state, but fifth, because its equity burden is low.");
}

// ---------- Slide 12: Archetypes ----------
{
  const s = content();
  header(s, "What the ranking means", "Three County Archetypes");
  const rows = [
    ["Union: utilization-driven", "101.5 BEVs per port, 3× the next county → more stations"],
    ["Mecklenburg & Guilford: equity-driven", "Equity 0.810 and 0.855 → better-targeted stations in underserved ZIPs"],
    ["Orange: low across all pillars", "(0.077) → no priority deployment now"],
  ];
  rows.forEach((r, i) => {
    const y = 1.9 + i * 1.25;
    card(s, M, y, 6.4, 1.1);
    s.addText(r[0], { x: M + 0.25, y: y + 0.1, w: 5.9, h: 0.42, fontFace: FONT, fontSize: 18, bold: true, color: BLUE, margin: 0, isTextBox: true });
    s.addText(r[1], { x: M + 0.25, y: y + 0.52, w: 5.9, h: 0.5, fontFace: FONT, fontSize: 15, color: NAVY, margin: 0, isTextBox: true });
  });
  card(s, M, 5.75, 6.4, 1.0, CARD2);
  s.addText([b("Empty quadrant: "), t("no county is high on both equity and utilization")], { x: M + 0.25, y: 5.75, w: 5.9, h: 1.0, fontFace: FONT, fontSize: 17, color: NAVY, valign: "middle", margin: 0, isTextBox: true });
  fig(s, "fig-45-equity-utilization-archetypes.png", 4869, 4269, 7.3, 1.6, W - 7.3 - 0.4, 5.3);
  s.addNotes("The ranking says where, but not why. Plotting equity against utilization gives three archetypes. Union is utilization-driven: 101.5 EVs per port, more than three times the next county. It needs more stations. Mecklenburg and Guilford are equity-driven. They don't just need more stations, they need them in the right ZIP codes. Orange scores low on everything and doesn't need priority deployment now. Then look at the top-right corner: it's empty. No county is high on both equity and utilization, so every county is a trade-off, and the framework makes that trade-off visible instead of hiding it.");
}

// ---------- Slide 13: Contributions and limitations ----------
{
  const s = content();
  header(s, "What it adds", "Contributions and Limitations");
  const colW = (W - 2 * M - 0.4) / 2;
  card(s, M, 1.8, colW, 4.2);
  s.addText("Contributions", { x: M + 0.3, y: 1.95, w: colW - 0.6, h: 0.45, fontFace: FONT, fontSize: 20, bold: true, color: BLUE, margin: 0, isTextBox: true });
  s.addText([
    { text: "Additive Theil-T decomposition of EV charging inequality, used as a design input to allocation", options: { bullet: { type: "number" }, breakLine: true, paraSpaceAfter: 14 } },
    { text: "Area-weighted CEJST–AFDC crosswalk at ZIP resolution (23 of 23 validation checks)", options: { bullet: { type: "number" }, breakLine: true, paraSpaceAfter: 14 } },
    { text: "Three-pillar NEVI score with VIF-confirmed independence and a robust top 3", options: { bullet: { type: "number" } } },
  ], { x: M + 0.3, y: 2.55, w: colW - 0.6, h: 3.3, fontFace: FONT, fontSize: 19, color: NAVY, valign: "top", margin: 0, isTextBox: true });
  const x2 = M + colW + 0.4;
  card(s, x2, 1.8, colW, 4.2);
  s.addText("Limitations, each with a direction of bias", { x: x2 + 0.3, y: 1.95, w: colW - 0.6, h: 0.45, fontFace: FONT, fontSize: 20, bold: true, color: BLUE, margin: 0, isTextBox: true });
  bullets(s, [
    [t("Top-10 scope (73% of fleet): "), b("bounded")],
    [t("LODES 2021 vintage: "), b("cancels in normalization")],
    [t("Static BEV counts: "), b("understates growth (conservative)")],
    [t("CEJST v2.0 lock, NEVI rule changes: "), b("policy risk")],
  ], x2 + 0.3, 2.55, colW - 0.6, 3.3, 19);
  s.addNotes("Three contributions. First, using the Theil decomposition as a design input, not just a summary number; prior EV work, such as Choi, Xu and Jiao on Austin, reports Theil as a single magnitude. Second, a validated crosswalk that brings the federal equity designations down to ZIP level. Third, a score whose pillars are independent and whose top three survives perturbation. On limitations, I gave each one a direction. The scope covers 73% of the fleet. The 2021 commuting data cancels out in normalization. Static counts understate growth, which makes the scores conservative. None of them overturns the top three.");
}

// ---------- Slide 14: Implications / close ----------
{
  const s = pres.addSlide({ sectionTitle: "Talk" });
  s.background = { color: WHITE };
  s.addImage({ path: path.join(__dirname, "assets", "photo-close.jpg"), x: W - 5.0, y: 0, w: 5.0, h: 7.5 });
  s.addText("IMPLICATIONS AND NEXT STEPS", { x: M, y: 0.6, w: 7.4, h: 0.3, fontFace: FONT, fontSize: 11, bold: true, color: BLUE, charSpacing: 1.5, margin: 0, isTextBox: true });
  s.addText("Decision Support, Not Decision-Making", { x: M, y: 0.95, w: 7.4, h: 0.8, fontFace: FONT, fontSize: 30, bold: true, color: NAVY, margin: 0, isTextBox: true });
  bullets(s, [
    [b("NCDOT / FHWA: "), t("an auditable county ranking (VIF 1.41, MAPE 4.34%, robust top 3)")],
    [b("County planners: "), t("ZIP-level gap analysis for site selection")],
    [b("Next: "), t("all 100 counties · validate against NCDOT's actual NEVI deployments · confidence intervals on composite scores")],
  ], M, 2.0, 7.4, 2.6, 17);
  card(s, M, 4.7, 7.4, 2.15, CARD);
  s.addText([
    { text: "Thank you", options: { fontSize: 28, bold: true, color: NAVY, breakLine: true } },
    { text: "wolfgang.sanyer@gmail.com", options: { fontSize: 15, color: NAVY, breakLine: true } },
    { text: "linkedin.com/in/wolfgangsanyer", options: { fontSize: 15, color: NAVY, breakLine: true } },
    { text: "github.com/wolfieman/ev-pulse-nc", options: { fontSize: 15, color: NAVY, breakLine: true } },
    { text: "sanyer.org/research-lab", options: { fontSize: 15, color: NAVY } },
  ], { x: M + 0.3, y: 4.7, w: 5.2, h: 2.15, fontFace: FONT, valign: "middle", margin: 0, isTextBox: true });
  s.addImage({ data: QR_REPO, x: M + 7.4 - 1.95, y: 4.7 + 0.3, w: 1.55, h: 1.55, altText: "QR code: github.com/wolfieman/ev-pulse-nc" });
  s.addNotes("This isn't meant to replace NCDOT's judgment. Right-of-way, utilities, and politics all matter and aren't in the model. What it gives is an analytical floor: a ranking an auditor can trace, and ZIP-level targets a planner can use. Next steps are extending it to all 100 counties, checking it against NCDOT's actual deployments, and putting confidence intervals on the scores. Thank you, I'm happy to take questions.");
}

// ---------- Backup slides ----------
pres.addSection({ title: "Backup" });
const backup = () => pres.addSlide({ masterName: "CONTENT", sectionTitle: "Backup" });

{
  const s = backup();
  header(s, "Backup B1", "Theil-T Decomposition");
  fig(s, "fig-33-theil-decomposition.png", 4269, 2469, M, 1.8, 6.4, 3.7);
  bullets(s, [
    [t("GE(1) / Theil-T is additively decomposable: "), b("T = T_between + T_within"), t(", with no residual (Bourguignon 1979; Shorrocks 1980)")],
    [t("Top 10 counties: "), b("0.5791 = 0.0900 (15.5%) + 0.4892 (84.5%)")],
    [t("Theil-L (GE(0)) robustness: "), b("82.5%"), t(" within")],
    [t("Within-county contribution: Mecklenburg "), b("41.5%"), t(", Wake "), b("28.1%"), t(", Guilford "), b("7.7%"), t(", Union "), b("0.6%")],
    "Theil is a diagnostic for the architecture (why Tier 2 exists), not an input to either tier's score",
  ], 7.3, 1.85, W - 7.3 - M, 5.0, 15);
}

{
  const s = backup();
  header(s, "Backup B2", "Crosswalk Validation");
  bullets(s, [
    "CEJST v2.0 (2010 tracts) → 2020 ZCTAs, area-weighted in NC State Plane (EPSG:32119), the EPA EJScreen / HUD USPS approach",
    [b("12 checks in 3 tiers, 23 of 23 sub-checks passed"), t("; per-ZCTA area conservation within 1%")],
    "Slivers < 100 m² dropped; border-state tracts (VA, SC, TN, GA) included; 25 zero-population tracts excluded",
    "Known limit: uniform within-tract population (weaker in large rural tracts)",
  ], M, 1.9, W - 2 * M, 4.8, 19);
}

{
  const s = backup();
  header(s, "Backup B3", "Full NEVI Scores (Table 2)");
  const hdr = ["Rank", "County", "NEVI", "Equity", "Utilization", "Cost-Eff."].map((h) => ({ text: h, options: { bold: true, color: WHITE, fill: { color: NAVY } } }));
  const data = [
    ["1", "Union", "0.561", "0.319", "1.000", "0.333"],
    ["2", "Mecklenburg", "0.548", "0.810", "0.067", "0.801"],
    ["3", "Guilford", "0.465", "0.855", "0.103", "0.347"],
    ["4", "New Hanover", "0.341", "0.607", "0.071", "0.293"],
    ["5", "Wake", "0.316", "0.322", "0.130", "0.568"],
    ["6", "Durham", "0.313", "0.469", "0.033", "0.454"],
    ["7", "Forsyth", "0.285", "0.283", "0.156", "0.467"],
    ["8", "Cabarrus", "0.199", "0.228", "0.229", "0.111"],
    ["9", "Buncombe", "0.197", "0.470", "0.000", "0.034"],
    ["10", "Orange", "0.077", "0.059", "0.101", "0.071"],
  ].map((r, i) => r.map((c) => ({ text: c, options: { fill: { color: i % 2 ? WHITE : CARD } } })));
  s.addTable([hdr, ...data], { x: M, y: 1.75, w: W - 2 * M, colW: [1.2, 3.33, 1.9, 1.9, 1.9, 1.9], fontFace: FONT, fontSize: 14, color: NAVY, align: "center", rowH: 0.4, border: { type: "solid", pt: 0.5, color: "C8D6E5" } });
  s.addText("Equity weight 0.30–0.50 sweep: top 3 unchanged; Mecklenburg gains and Union falls as the equity weight rises; Orange stays 10th.", { x: M, y: 6.3, w: W - 2 * M, h: 0.5, fontFace: FONT, fontSize: 15, color: NAVY, margin: 0, isTextBox: true });
}

{
  const s = backup();
  header(s, "Backup B4", "Data Sources and Diagnostics");
  const hdr = ["Source", "Content", "Window"].map((h) => ({ text: h, options: { bold: true, color: WHITE, fill: { color: NAVY } } }));
  const data = [
    ["NCDOT", "Monthly county BEV registrations", "Sep 2018 – Oct 2025"],
    ["NREL AFDC API", "Station inventory, all levels", "Feb 2026 pull"],
    ["U.S. Census ACS + TIGER", "Income, tenure, population; boundaries", "ACS 2022 five-year; TIGER 2020"],
    ["LEHD LODES", "Block-level commuter flows", "2021"],
    ["CEJST v2.0", "Disadvantaged tract designations", "Dec 2024 release (EDGI / PEDP archive)"],
  ].map((r, i) => r.map((c) => ({ text: c, options: { fill: { color: i % 2 ? WHITE : CARD } } })));
  s.addTable([hdr, ...data], { x: M, y: 1.75, w: W - 2 * M, colW: [3.0, 4.6, 4.533], fontFace: FONT, fontSize: 15, color: NAVY, rowH: 0.45, border: { type: "solid", pt: 0.5, color: "C8D6E5" } });
  bullets(s, [
    [t("CSS vs. MLE estimator: forecast difference "), b("< 0.1%")],
    [t("NCDOT counting change (May 2025): ~"), b("0.4%"), t(" of totals, works "), { text: "against", options: { italic: true } }, t(" the underprediction")],
    "Pillar correlations: E–U −0.26 · E–CE +0.48 · U–CE −0.03",
  ], M, 4.75, W - 2 * M, 2.0, 16);
}

const f = await pres.writeFile({ fileName: OUT });
console.log("wrote", f);
}

main().catch((e) => { console.error(e); process.exit(1); });
