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
// Output directory (default: current folder). Three files are written per run:
//   *-upload.pptx (15 talk slides, sent for the Ex Ordo upload),
//   *-presenter.pptx (talk + backup slides, for the presenter's USB),
//   *-backup.pptx (backup slides only).
const OUT_DIR = process.argv[2] || ".";
const BASE = "ev-pulse-nc-seinforms-2026";

// Palette matched to the showcase / BIDA-670 decks: white, light-blue cards, blue accent, navy text.
const NAVY = "0F2A4A", BLUE = "1F6FC5", CARD = "E3EFFB", CARD2 = "CFE3F8", MUTED = "5B6B7F",
      GREEN_BG = "E4F4E3", GREEN = "2E7D32", WHITE = "FFFFFF";
const FONT = "Calibri";

async function main(VARIANT) {
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

function stat(s, x, y, w, h, big, label, bigSize = 34, bigColor = BLUE) {
  card(s, x, y, w, h);
  s.addText(big, { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: 0.75, fontFace: FONT, fontSize: bigSize, bold: true, color: bigColor, margin: 0, isTextBox: true });
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
  // A bare file name is a paper figure in output/figures/; a full path is a deck asset.
  const src = path.isAbsolute(file) ? file : FIG + file;
  const box = { x: x + (w - iw) / 2, y: y + (h - ih) / 2, w: iw, h: ih };
  s.addImage({ path: src, ...box });
  return box;
}

const content = () => pres.addSlide({ masterName: "CONTENT", sectionTitle: "Talk" });

if (VARIANT !== "backup") {
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
    { text: "Faculty Advisors: Dr. Majed Al-Ghandour, Dr. Burcu Adivar", options: { fontSize: 16, color: MUTED } },
  ], { x: M, y: 4.9, w: 7.4, h: 1.3, fontFace: FONT, fontSize: 18, color: NAVY, valign: "top", margin: 0, isTextBox: true });
  s.addNotes("Good morning. I'm Wolfgang Sanyer, an MBA student in business analytics at Fayetteville State. This talk is about how North Carolina could decide where $109 million in federal EV charging money should go, and what the data says about where the real gaps are. The analysis was completed in spring 2026, using data through February 2026.");
}

// ---------- Slide 2: The Problem ----------
{
  const s = content();
  header(s, "The problem", "$109 Million. 100 Counties. No Data-Driven County Ranking.");
  const y = 1.9, h = 2.3, w = 3.85, g = 0.3;
  stat(s, M, y, w, h, "$109M", "NC's federal National Electric Vehicle Infrastructure (NEVI) Formula Program funding", 44);
  stat(s, M + w + g, y, w, h, "No county ranking", "The NC Department of Transportation (NCDOT) has a federally approved NEVI plan, but no publicly available, data-driven method for ranking counties", 30);
  stat(s, M + 2 * (w + g), y, w, h, "Feb 2026", "NCDOT revises its NEVI plan, narrowing the corridor buildout and shifting funds toward rural and community charging", 34);
  card(s, M, 4.55, W - 2 * M, 1.5);
  s.addText([
    { text: "Efficiency vs. equity", options: { bold: true, color: BLUE, breakLine: true } },
    { text: "Demand-driven allocation reinforces existing concentration; equity-driven allocation can place stations where use is too low to sustain them." },
  ], { x: M + 0.3, y: 4.65, w: W - 2 * M - 0.6, h: 1.3, fontFace: FONT, fontSize: 18, color: NAVY, valign: "middle", margin: 0, isTextBox: true });
  s.addNotes("North Carolina has $109 million in National Electric Vehicle Infrastructure, or NEVI, formula funding for public charging. The two obvious approaches pull against each other. Follow demand, and you put chargers where they already are. Follow equity alone, and you can build stations nobody uses. The North Carolina Department of Transportation, NCDOT, has a federally approved NEVI plan and is building out highway corridors in rounds. In February 2026 it revised that plan, narrowing the corridor buildout and shifting funds toward rural and community charging. What it hasn't published is a data-driven way to rank counties, and that matters most for the community phase still ahead. So this is a live decision, and the question is whether there's a defensible way to make it.");
}

// ---------- Slide 2a: Research questions (paper §1.3; BIDA-670 deck s5) ----------
{
  const s = content();
  header(s, "Research questions", "Five Questions Drive the Work");
  const qs = [
    ["Forecast Accuracy", "How accurate are SAS Model Studio's county-level battery electric vehicle (BEV) forecasts against unseen data?"],
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
  s.addNotes("Five questions drive the work. Can the county forecasts of battery electric vehicles, or BEVs, be trusted on data they haven't seen? Where are the biggest gaps between demand and supply? What do ZIP codes show that county averages hide? How does commuting change where charging is needed? And can one weighted score turn all of that into a ranking you can defend? The rest of the talk follows these questions. The short answer: most of the charging inequality is inside counties, not between them, so the framework works in two tiers, and the top three counties are Union, Mecklenburg, and Guilford.");
}

// ---------- Slide 3: Demand Signal ----------
{
  const s = content();
  header(s, "Demand signal", "The BEV Fleet Grew 1,727% Since 2018. Ports Have Not Kept Pace.");
  const y = 1.95, h = 3.3, w = 2.85, g = 0.233;
  stat(s, M, y, w, h, "5,165 → 94,371", "BEVs, Sep 2018 → Jun 2025", 26);
  stat(s, M + (w + g), y, w, h, "53.8%", "Compound annual growth", 40);
  stat(s, M + 2 * (w + g), y, w, h, "Gini 0.805", "County-level BEV ownership is highly concentrated; Wake alone holds more BEVs than the bottom 60 counties combined", 32);
  stat(s, M + 3 * (w + g), y, w, h, "16.9", "BEVs per public port (Feb 2026) vs. International Energy Agency (IEA) global benchmark ≈10", 40);
  callout(s, [t("Top 10 counties hold "), b("73%"), t(" of the statewide BEV fleet")], 5.6);
  s.addText("Data as of Feb 2026: NCDOT registrations through Oct 2025; Alternative Fuels Data Center (AFDC) stations as of Feb 2026", { x: M, y: 6.4, w: W - 2 * M, h: 0.35, fontFace: FONT, fontSize: 12, italic: true, color: MUTED, margin: 0, isTextBox: true });
  s.addNotes("Start with the backdrop: demand isn't in doubt. The fleet went from 5,165 battery-electric vehicles in 2018 to 94,371 by mid-2025, a 53.8% annual growth rate. It's also very concentrated: a Gini coefficient of 0.805 across counties, on a scale where 0 is perfectly even and 1 is everything in one place. Wake County alone has more BEVs than the bottom 60 counties put together. Supply hasn't kept up. North Carolina has 16.9 BEVs per public port, against the International Energy Agency's global benchmark of about 10. The top 10 counties hold 73% of the fleet, which is why the scoring focuses on them.");
}

// ---------- Slide 4: Pipeline ----------
{
  const s = content();
  header(s, "Method", "Five Analytical Phases, One Scoring Framework");
  const phases = [
    ["Phase 1 · Q1", "Forecast validation", "NCDOT registrations, Sep 2018–Oct 2025"],
    ["Phase 2 · Q2", "Infrastructure baseline", "NREL AFDC API, Feb 2026: 1,985 stations, 6,145 connectors"],
    ["Phase 3 · Q3", "ZIP-level inequality", "Gini + additive Theil-T decomposition"],
    ["Phase 4 · Q4", "Workplace charging demand", "LEHD LODES 2021"],
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
  s.addText("NEVI Priority Score  →  Q5", { x: W / 2 - 2.6, y: 5.5, w: 5.2, h: 0.7, fontFace: FONT, fontSize: 20, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText("All public data · 8,600 county-month observations · SAS Model Studio forecasts (fall 2025), validated in Python (spring 2026)", { x: M, y: 6.25, w: W - 2 * M, h: 0.35, fontFace: FONT, fontSize: 14, color: MUTED, align: "center", margin: 0, isTextBox: true });
  s.addText("NREL: National Renewable Energy Laboratory · AFDC: Alternative Fuels Data Center · API: application programming interface · LEHD LODES: Longitudinal Employer-Household Dynamics Origin-Destination Employment Statistics · CEJST: Climate and Economic Justice Screening Tool · ZCTA: ZIP Code Tabulation Area", { x: M, y: 6.6, w: W - 2 * M, h: 0.45, fontFace: FONT, fontSize: 10.5, color: MUTED, align: "center", valign: "top", margin: 0, isTextBox: true });
  s.addNotes("The work runs in five phases. Phase 1 tests the demand forecasts on data they never saw. Phase 2 rebuilds the supply side from the Department of Energy's Alternative Fuels Data Center, all charger levels, not just fast chargers. Phase 3 measures inequality at the ZIP level. Phase 4 adds workplace demand from Census commuting data. Phase 5 overlays the federal disadvantaged-community designations. Everything feeds one score, every input is public, and the whole pipeline reruns from the repository.\n\n(Cut candidate for a 15-minute slot: move to backup.)");
}

// Figure + right column helper
function figRight(s, items, size = 16) { bullets(s, items, 8.25, 1.95, W - 8.25 - M, 4.9, size); }

// ---------- Slide 5: Forecast validation ----------
{
  const s = content();
  header(s, "Phase 1 · Forecast validation", "Forecasts Hold Out of Sample, and Adoption Accelerated After 2022");
  // Talk version of Fig 44 (fig44_talk.py): same data, projector styling.
  fig(s, path.join(__dirname, "assets", "fig-44-validation-scatter-talk.png"), 2224, 1624, M, 1.75, 7.3, 5.15);
  figRight(s, [
    [b("Mean absolute percentage error (MAPE) 4.34%"), t(" on a true holdout (n = 400 county-months, Jul–Oct 2025, all 100 counties)")],
    [b("69.00%"), t(" of actuals exceeded forecast (mean bias +18.22 vehicles per county-month)")],
    [b("Chow test: F = 1,268.35, p < 1 × 10⁻⁶"), t(" at the Aug 2022 Inflation Reduction Act passage")],
    [t("95% interval coverage "), b("75.50% raw → 93.75%"), t(" after county bias correction: a centering problem, not a width problem")],
  ]);
  s.addNotes("First question: can we trust the demand forecasts? The SAS models were tested on four months they never saw: all 100 counties, 400 observations. Each dot is one county in one month, forecast across, actual up, on a log scale because counties range from a handful of BEVs to tens of thousands. The colors are the model type SAS picked for each county. Dots on the dashed line are perfect forecasts. The mean absolute percentage error, or MAPE, was 4.34%, under the 5% usability bar. On this log scale the misses are hard to see, but 69% of them go the same way: actual registrations beat the forecast. The circled point is Mecklenburg in October 2025: its actual exceeded the forecast by 975 vehicles in a single month. That isn't a broken model. A Chow test, which checks whether a trend changed at a specific date, finds a strong break at the Inflation Reduction Act in August 2022. The models learned a slower world. Their 95% ranges caught only 75.5% of the actual counts, but after shifting each county's forecast up by its own average miss, 93.75%. So the ranges were the right width, just centered too low, and planners should add an upward buffer of 4 to 5 percent.");
}

// ---------- Slide 6: Infrastructure gap ----------
{
  const s = content();
  header(s, "Phase 2 · Infrastructure gap", "A 250-Fold Charging Gap Inside One County");
  bullets(s, [
    [b("58.5%"), t(" of NC ZIP areas (499 of 853) have zero stations: "), b("2.2 million people"), t(" (21.1% of the state)")],
    [t("Charlotte 28202: "), b("78.64"), t(" ports per 10,000 residents")],
    [t("Charlotte 28215, 14 miles east: "), b("0.31"), t(" (64,713 residents, 2 ports)")],
  ], M, 1.95, 6.6, 3.2, 18);
  card(s, M, 5.2, 6.6, 1.0, CARD2);
  s.addText("The gap is not rural alone", { x: M + 0.25, y: 5.2, w: 6.1, h: 1.0, fontFace: FONT, fontSize: 24, bold: true, color: BLUE, valign: "middle", margin: 0, isTextBox: true });
  const mb = fig(s, "fig-24-heatmap-mecklenburg.png", 3384, 3669, 7.5, 1.6, W - 7.5 - 0.4, 5.35);
  // Overlays on the paper's map (image unchanged). ZIP positions come from
  // fig24_labels.py (raw ZCTA boundaries, same projection as the map script).
  const L = require(path.join(__dirname, "assets", "fig24-labels.json"));
  const at = (k) => ({ x: mb.x + L[k][0] * mb.w, y: mb.y + L[k][1] * mb.h });
  // Cover the paper's small legend and the corner box (its population and port
  // counts are not quoted in the paper text), then draw a projector-size legend.
  s.addShape(pres.shapes.RECTANGLE, { x: mb.x + 0.55 * mb.w, y: mb.y + 0.055 * mb.h, w: 0.29 * mb.w, h: 0.095 * mb.h, fill: { color: WHITE }, line: { color: WHITE } });
  s.addShape(pres.shapes.RECTANGLE, { x: mb.x + 0.015 * mb.w, y: mb.y + 0.875 * mb.h, w: 0.205 * mb.w, h: 0.105 * mb.h, fill: { color: WHITE }, line: { color: WHITE } });
  s.addText([
    { text: "▲ ", options: { color: "E53935", bold: true } },
    { text: "DC fast-charging stations", options: { breakLine: true } },
    { text: "■ ", options: { color: "1F6FC5", bold: true } },
    { text: "Color: all charging ports", options: { breakLine: true } },
    { text: "▨ ", options: { color: "9E9E9E", bold: true } },
    { text: "No charging stations" },
  ], { x: mb.x + 0.555 * mb.w, y: mb.y + 0.06 * mb.h, w: W - M - (mb.x + 0.555 * mb.w), h: 0.78, fontFace: FONT, fontSize: 11, color: NAVY, valign: "top", margin: 0.04, fill: { color: WHITE }, line: { color: "C8D6E5", width: 0.75 }, isTextBox: true });
  // ZIP callouts: a ring on the ZIP, a leader line, and a label.
  const callout = (k, text, lx, ly, lw) => {
    const p = at(k);
    s.addShape(pres.shapes.OVAL, { x: p.x - 0.11, y: p.y - 0.11, w: 0.22, h: 0.22, fill: { color: WHITE, transparency: 100 }, line: { color: "E53935", width: 2.25 } });
    const ex = lx + lw / 2, ey = ly + 0.42;
    s.addShape(pres.shapes.LINE, { x: Math.min(p.x, ex), y: Math.min(p.y, ey), w: Math.abs(ex - p.x) || 0.01, h: Math.abs(ey - p.y) || 0.01, flipH: (ex - p.x) * (ey - p.y) < 0, line: { color: "E53935", width: 1.5 } });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: lx, y: ly, w: lw, h: 0.42, fill: { color: NAVY }, line: { color: NAVY }, rectRadius: 0.06 });
    s.addText(text, { x: lx, y: ly, w: lw, h: 0.42, fontFace: FONT, fontSize: 12, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, isTextBox: true });
  };
  // Labels sit in the map's empty lower corners, clear of the colour bar.
  callout("28202", "28202 Uptown: 78.64", mb.x + 0.02 * mb.w, mb.y + 0.885 * mb.h, 1.75);
  callout("28215", "28215: 0.31", mb.x + 0.50 * mb.w, mb.y + 0.885 * mb.h, 1.25);
  s.addNotes("On the supply side, more than half of North Carolina's ZIP areas have no charger at all, covering 2.2 million people. That's not only a rural story. This map zooms into one county, Mecklenburg. The color is all charging ports per 10,000 residents, darker means more; gray hatching means no stations at all; the red triangles mark fast-charging stations. Uptown Charlotte, ZIP 28202, has 78.64 ports per 10,000 residents. Fourteen miles east, ZIP 28215 has 64,713 people and two ports. That's a 250-fold difference inside one county. Hold on to this picture, because the next slide shows it isn't an outlier.");
}

// ---------- Slide 7: Theil ----------
{
  const s = content();
  header(s, "Phase 3 · The headline finding", "84.5% of Charging Inequality Is Within Counties");
  // Native chart of the paper's Fig 33 values (§6.3): between 0.0900, within
  // 0.4892, total 0.5791. Replaces the print image (its title and subtitle overlap).
  s.addChart(pres.charts.BAR, [
    { name: "Between counties", labels: ["Top 10 counties"], values: [0.09] },
    { name: "Within counties", labels: ["Top 10 counties"], values: [0.4892] },
  ], {
    x: M, y: 1.75, w: 7.6, h: 4.4, barDir: "bar", barGrouping: "stacked", barGapWidthPct: 40,
    chartColors: ["9AA5B1", "1F6FC5"], // between muted, within (the finding) in the accent blue
    showValue: true, dataLabelPosition: "ctr", dataLabelFormatCode: "0.0000", dataLabelColor: "FFFFFF",
    dataLabelFontSize: 20, dataLabelFontBold: true, dataLabelFontFace: FONT,
    showTitle: true, title: "Theil-T inequality index, top 10 counties (total = 0.5791)", titleFontSize: 18, titleColor: NAVY, titleFontFace: FONT,
    showLegend: true, legendPos: "b", legendFontSize: 16, legendFontFace: FONT, legendColor: NAVY,
    catAxisHidden: true,
    valAxisMinVal: 0, valAxisMaxVal: 0.6, valAxisMajorUnit: 0.1, valAxisLabelFormatCode: "0.0",
    valAxisLabelFontSize: 14, valAxisLabelFontFace: FONT, valAxisLabelColor: MUTED,
    valAxisTitle: "Theil-T index value", showValAxisTitle: true, valAxisTitleFontSize: 14, valAxisTitleColor: MUTED, valAxisTitleFontFace: FONT,
    valGridLine: { color: "D9E2EC", size: 0.75 }, catGridLine: { style: "none" },
  });
  stat(s, 8.5, 1.85, 2.0, 1.55, "84.5%", "within", 30);
  stat(s, 10.73, 1.85, 2.0, 1.55, "15.5%", "between", 30, MUTED);
  bullets(s, [
    [t("Exact additive decomposition (generalized entropy index GE(1)); verified to "), b("2.22 × 10⁻¹⁶"), t("; Theil-L check: "), b("82.5%"), t(" within")],
    [t("ZIP-level charging Gini (statewide, population-weighted): "), b("0.566")],
  ], 8.5, 3.6, 4.23, 2.6, 15);
  callout(s, [t("County-only formulas miss most of the problem → "), b("two-tier design: county ranking + ZIP-level targeting")], 6.3);
  s.addNotes("This is the central result. A second Gini, this time for charging ports across ZIP codes, is 0.566: inequality is high, but that doesn't tell you where it lives. The Theil index measures how unevenly ports are spread relative to where people live; zero would mean every ZIP code has the same access per person. The Theil-T version splits exactly into a between-county part and a within-county part, with no residual. If every county had the same average access but big differences between its own ZIP codes, all the inequality would be within counties. That's essentially what we see: for the top 10 counties, 84.5% of the inequality is within counties. The Theil-L version gives 82.5%, so it isn't an artifact of the index. Mecklenburg alone contributes 41.5% of it. Most state NEVI formulas allocate by county, so they miss most of the problem. That is why the framework has two tiers: rank the counties, then target ZIP codes inside them.");
}

// ---------- Slide 8: Workplace demand ----------
{
  const s = content();
  header(s, "Phase 4 · Workplace demand", "Commuters Shift Demand Toward Employment Centers");
  // Native diverging bar of net daily commuters (paper §6.4; the four counties
  // the paper reports). One unit throughout: commuters per day, in minus out.
  s.addChart(pres.charts.BAR, [
    { name: "Job centers: net inflow", labels: ["Mecklenburg", "Wake", "Durham", "Union"], values: [194361, 126517, 89450, 0] },
    { name: "Bedroom community: net outflow", labels: ["Mecklenburg", "Wake", "Durham", "Union"], values: [0, 0, 0, -36113] },
  ], {
    x: M, y: 1.75, w: 7.4, h: 4.95, barDir: "bar", barGrouping: "stacked", barGapWidthPct: 45,
    chartColors: ["1F6FC5", "F39C12"],
    catAxisOrientation: "maxMin", catAxisLabelFontSize: 16, catAxisLabelFontFace: FONT, catAxisLabelColor: NAVY,
    catAxisLabelPos: "low",
    showValue: true, dataLabelPosition: "inEnd", dataLabelFormatCode: "+#,##0;−#,##0;;", dataLabelColor: "FFFFFF",
    dataLabelFontSize: 15, dataLabelFontBold: true, dataLabelFontFace: FONT,
    showTitle: true, title: "Net daily commuters, selected counties (in minus out)", titleFontSize: 17, titleColor: NAVY, titleFontFace: FONT,
    showLegend: true, legendPos: "b", legendFontSize: 14, legendFontFace: FONT, legendColor: NAVY,
    valAxisMinVal: -50000, valAxisMaxVal: 200000, valAxisMajorUnit: 50000, valAxisLabelFormatCode: "#,##0",
    valAxisLabelFontSize: 13, valAxisLabelFontFace: FONT, valAxisLabelColor: MUTED,
    valGridLine: { color: "D9E2EC", size: 0.75 }, catGridLine: { style: "none" },
  });
  figRight(s, [
    [b("U.S. Census commuting data"), t(" (Longitudinal Employer-Household Dynamics Origin-Destination Employment Statistics, LEHD LODES, 2021): 4,198,163 workers → "), b("859,260 adjusted commuters"), t(" after income and remote-work filters")],
    [b("Union"), t(" sends more commuters out than it takes in: a bedroom community of Charlotte")],
    [t("Feeds the "), b("cost-effectiveness pillar"), t(": Mecklenburg scores highest ("), b("0.801"), t(")")],
  ], 16);
  s.addNotes("That's where the inequality is. Next, where the demand is during the day. Registration data tells you where EVs sleep, not where they sit during the workday. For the workday I used Census commuting data, LODES, for 2021: 4,198,163 workers, filtered to EV-affordable incomes and adjusted for remote work, leaving 859,260 commuters. The chart shows net daily commuters. Mecklenburg takes in 194,361 more workers a day than it sends out, and Wake and Durham are job centers too. Union is the opposite: 36,113 more people leave each day than arrive. It's a bedroom community: people live there and drive to Charlotte for work. That daytime demand feeds the cost-effectiveness part of the score I'll show in a moment, where Mecklenburg scores highest.\n\n(Cut candidate for a 15-minute slot: move to backup.)");
}

// ---------- Slide 9: Justice40 ----------
{
  const s = content();
  header(s, "Phase 5 · Justice40 overlay", "Roughly Proportional Overall, with Strong County-by-County Variation");
  // Left: stations and residents together (paper §6.5): roughly proportional.
  const tile = (x, big, label) => {
    card(s, x, 1.85, 2.75, 2.05);
    s.addText(big, { x: x + 0.2, y: 1.95, w: 2.35, h: 0.8, fontFace: FONT, fontSize: 40, bold: true, color: BLUE, margin: 0, isTextBox: true });
    s.addText(label, { x: x + 0.2, y: 2.8, w: 2.35, h: 1.0, fontFace: FONT, fontSize: 15, color: NAVY, valign: "top", margin: 0, isTextBox: true });
  };
  tile(M, "24.5%", "of stations in the top 10 counties sit in disadvantaged tracts (296 of 1,210)");
  tile(M + 2.95, "18.5%", "of residents in the top 10 counties live in those tracts");
  s.addText("Roughly proportional overall", { x: M, y: 4.05, w: 5.7, h: 0.45, fontFace: FONT, fontSize: 19, bold: true, color: BLUE, margin: 0, isTextBox: true });
  bullets(s, [
    [t("Statewide: "), b("43.0%"), t(" of NC census tracts designated disadvantaged (934 of 2,170; CEJST v2.0)")],
    [t("Removing CEJST's climate category: "), b("7 of 10"), t(" study counties unchanged")],
  ], M, 4.6, 5.7, 1.7, 15);
  // Right: county-by-county dot plot of residents in disadvantaged tracts
  // (§6.5), with the top-10 average as a dashed reference line.
  const X0 = 8.6, X1 = 12.45, VMAX = 35, px = (v) => X0 + (v / VMAX) * (X1 - X0);
  s.addText("Residents in disadvantaged tracts, by county", { x: 6.85, y: 1.8, w: 5.9, h: 0.4, fontFace: FONT, fontSize: 16, bold: true, color: NAVY, margin: 0, isTextBox: true });
  const rows = [["Guilford", 29.2], ["New Hanover", 28.8], ["Durham", 26.6], ["Mecklenburg", 23.7], ["Wake", 8.1], ["Orange", 4.9]];
  const avgX = px(18.5);
  s.addShape(pres.shapes.LINE, { x: avgX, y: 2.45, w: 0, h: 3.05, line: { color: "9AA5B1", width: 1.5, dashType: "dash" } });
  s.addText("Top-10 average 18.5%", { x: avgX - 1.2, y: 2.18, w: 2.4, h: 0.27, fontFace: FONT, fontSize: 12, color: MUTED, align: "center", margin: 0, isTextBox: true });
  rows.forEach(([name, v], k) => {
    const y = 2.72 + k * 0.52;
    s.addText(name, { x: 6.85, y: y - 0.17, w: 1.6, h: 0.34, fontFace: FONT, fontSize: 15, color: NAVY, align: "right", margin: 0, isTextBox: true });
    s.addShape(pres.shapes.LINE, { x: X0, y, w: px(v) - X0, h: 0, line: { color: "D9E2EC", width: 2 } });
    s.addShape(pres.shapes.OVAL, { x: px(v) - 0.13, y: y - 0.13, w: 0.26, h: 0.26, fill: { color: BLUE }, line: { color: BLUE } });
    s.addText(`${v.toFixed(1)}%`, { x: px(v) + 0.17, y: y - 0.17, w: 0.8, h: 0.34, fontFace: FONT, fontSize: 14, bold: true, color: NAVY, margin: 0, isTextBox: true });
  });
  s.addShape(pres.shapes.LINE, { x: X0, y: 5.6, w: X1 - X0, h: 0, line: { color: "9AA5B1", width: 1 } });
  [0, 10, 20, 30].forEach((v) => {
    s.addShape(pres.shapes.LINE, { x: px(v), y: 5.6, w: 0, h: 0.07, line: { color: "9AA5B1", width: 1 } });
    s.addText(`${v}%`, { x: px(v) - 0.3, y: 5.7, w: 0.6, h: 0.27, fontFace: FONT, fontSize: 12, color: MUTED, align: "center", margin: 0, isTextBox: true });
  });
  s.addText("CEJST v2.0 as of Jan 21, 2025; tool removed Jan 22, 2025 after Executive Order (EO) 14008 was rescinded; data from the Environmental Data & Governance Initiative (EDGI) / Public Environmental Data Partners (PEDP) archive", {
    x: M, y: 6.45, w: W - 2 * M, h: 0.5, fontFace: FONT, fontSize: 11, italic: true, color: MUTED, valign: "top", margin: 0, isTextBox: true,
  });
  s.addNotes("Phase 5 brings in equity. The federal Climate and Economic Justice Screening Tool, CEJST, flags a census tract as disadvantaged when it's low-income and also burdened on at least one of eight environmental, health, or infrastructure measures. In the top 10 counties, 18.5% of residents live in those tracts, and 24.5% of stations sit in them. Those are the two numbers on the left: in aggregate the siting is roughly proportional. The story is in the variation, on the right. Each dot is a county's share of residents in disadvantaged tracts; the dashed line is the 18.5% average. Guilford is at 29.2%; Wake is at only 8.1%, and Orange at 4.9%. That share is the largest input to the equity pillar; the others are how unevenly chargers are spread inside each county and how many ZIP codes are underserved. And as the Theil result showed, proportional in total doesn't mean well served inside each county: Mecklenburg has plenty of chargers, but they're concentrated in Uptown. One caveat: the federal screening tool was taken down in January 2025. I use the archived version 2.0 data, and removing its most contested category, climate, leaves 7 of 10 counties unchanged.\n\n(Cut candidate: trim first at rehearsal if the talk runs long.)");
}

// ---------- Slide 10: Scoring framework ----------
{
  const s = content();
  header(s, "The framework", "Three Pillars, One Score");
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 1.75, w: W - 2 * M, h: 0.85, fill: { color: NAVY }, line: { color: NAVY }, rectRadius: 0.1 });
  s.addText("NEVI Priority Score = 0.40 × Equity + 0.35 × Utilization + 0.25 × Cost-Effectiveness", { x: M, y: 1.75, w: W - 2 * M, h: 0.85, fontFace: FONT, fontSize: 22, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, isTextBox: true });
  const pillars = [
    ["0.40", "Equity", "Disadvantaged residents, within-county charging Gini, underserved ZIPs; anchored on the Justice40 40% target (EO 14008, rescinded Jan 2025)"],
    ["0.35", "Utilization", "BEVs per port; demand data validated out of sample (strongest data)"],
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
  callout(s, [b("Pillars measure different things: "), t("max variance inflation factor (VIF) 1.41 (concern threshold 5.0)")], 6.0, GREEN_BG);
  s.addNotes("Those three layers, demand, workplace, and equity, now go into one score with three pillars. Each pillar is built from several measures, and every measure is min-max normalized: rescaled so the lowest county gets 0 and the highest gets 1, so measures in different units can be added together. The weights follow data confidence. Equity gets 0.40. It's anchored on Justice40, a 2021 federal goal that 40% of certain federal benefits, NEVI included, flow to disadvantaged communities. I treat that as an analytical anchor, not a legal requirement, since the executive order was rescinded in January 2025. Utilization, which is BEVs per charging port, gets 0.35 because its demand data passed the out-of-sample test. Cost-effectiveness gets 0.25 because workplace demand is the least certain input. The highest variance inflation factor is 1.41, well under the usual concern threshold of 5, so the pillars overlap only modestly and each adds its own information.");
}

// ---------- Slide 11: Rankings ----------
{
  const s = content();
  header(s, "The rankings", "Top 3: Union, Mecklenburg, Guilford");
  // Native bar of the composite scores, copied from Table 2 (§6.6); no derived
  // values. The paper's Fig 43 (pillar breakdown) moves to backup B7.
  const counties = ["Union", "Mecklenburg", "Guilford", "New Hanover", "Wake", "Durham", "Forsyth", "Cabarrus", "Buncombe", "Orange"];
  const scores = [0.561, 0.548, 0.465, 0.341, 0.316, 0.313, 0.285, 0.199, 0.197, 0.077];
  s.addChart(pres.charts.BAR, [
    { name: "Top 3", labels: counties, values: scores.map((v, i) => (i < 3 ? v : 0)) },
    { name: "Others", labels: counties, values: scores.map((v, i) => (i < 3 ? 0 : v)) },
  ], {
    x: M, y: 1.75, w: 7.3, h: 5.15, barDir: "bar", barGrouping: "stacked", barGapWidthPct: 35,
    chartColors: [BLUE, "9AA5B1"],
    catAxisOrientation: "maxMin", catAxisLabelFontSize: 15, catAxisLabelFontFace: FONT, catAxisLabelColor: NAVY,
    showValue: true, dataLabelPosition: "inEnd", dataLabelFormatCode: "0.000;;;", dataLabelColor: WHITE,
    dataLabelFontSize: 14, dataLabelFontBold: true, dataLabelFontFace: FONT,
    showTitle: true, title: "NEVI Priority Score, top 10 counties (Table 2)", titleFontSize: 17, titleColor: NAVY, titleFontFace: FONT,
    showLegend: false, valAxisHidden: true, valAxisMinVal: 0, valAxisMaxVal: 0.6,
    valGridLine: { style: "none" }, catGridLine: { style: "none" },
  });
  const top = [["1", "Union", "0.561"], ["2", "Mecklenburg", "0.548"], ["3", "Guilford", "0.465"]];
  top.forEach((r, i) => {
    const x = 8.25 + i * 1.53;
    card(s, x, 1.85, 1.43, 1.25);
    s.addText(r[2], { x, y: 1.9, w: 1.43, h: 0.6, fontFace: FONT, fontSize: 24, bold: true, color: BLUE, align: "center", margin: 0, isTextBox: true });
    s.addText(`#${r[0]} ${r[1]}`, { x, y: 2.5, w: 1.43, h: 0.5, fontFace: FONT, fontSize: 13, bold: true, color: NAVY, align: "center", margin: 0, isTextBox: true });
  });
  s.addText("Top-3 set held; order shifts:", { x: 8.25, y: 3.3, w: W - 8.25 - M, h: 0.4, fontFace: FONT, fontSize: 16, bold: true, color: NAVY, margin: 0, isTextBox: true });
  bullets(s, [
    "Equity weight 0.30–0.50 (five scenarios): Mecklenburg gains and Union falls as the equity weight rises",
    "Remote-work multiplier 0.75 / 0.85 / 0.95: cancels in min-max normalization, so the rankings are identical by construction",
  ], 8.25, 3.75, W - 8.25 - M, 1.8, 15);
  card(s, 8.25, 5.65, W - 8.25 - M, 1.15, CARD2);
  s.addText("Wake ranks 5th despite the most BEVs (equity 0.322; 8.1% of residents in disadvantaged tracts)", { x: 8.4, y: 5.65, w: W - 8.25 - M - 0.3, h: 1.15, fontFace: FONT, fontSize: 15, color: NAVY, valign: "middle", margin: 0, isTextBox: true });
  s.addNotes("Here's the result. Union, Mecklenburg, and Guilford come out on top. Each bar is a county's total score, and the top three are in blue. The same three stay on top as the equity weight moves from 0.30 to 0.50, though the order shifts: Mecklenburg gains as equity counts more. The remote-work assumption can't change the ranking at all, because a uniform multiplier cancels in the normalization, so I treat it as an invariance, not a test. And this is one factor at a time, not a full search of all weight combinations. Notice Wake: the most BEVs in the state, but fifth, because its equity burden is low.");
}

// ---------- Slide 12: Archetypes ----------
{
  const s = content();
  header(s, "What the ranking means", "Three County Archetypes");
  const rows = [
    ["Union: utilization-driven", "101.5 BEVs per port, more than 3× the next county → more stations"],
    ["Mecklenburg & Guilford: equity-driven", "Equity 0.810 and 0.855 → better-targeted stations in underserved ZIPs"],
    ["Orange: low across all pillars", "Lowest overall score (0.077) → no priority deployment now"],
  ];
  rows.forEach((r, i) => {
    const y = 1.9 + i * 1.25;
    card(s, M, y, 6.4, 1.1);
    s.addText(r[0], { x: M + 0.25, y: y + 0.1, w: 5.9, h: 0.42, fontFace: FONT, fontSize: 18, bold: true, color: BLUE, margin: 0, isTextBox: true });
    s.addText(r[1], { x: M + 0.25, y: y + 0.52, w: 5.9, h: 0.5, fontFace: FONT, fontSize: 15, color: NAVY, margin: 0, isTextBox: true });
  });
  card(s, M, 5.75, 6.4, 1.0, CARD2);
  s.addText([b("Empty quadrant: "), t("no county is high on both equity and utilization")], { x: M + 0.25, y: 5.75, w: 5.9, h: 1.0, fontFace: FONT, fontSize: 17, color: NAVY, valign: "middle", margin: 0, isTextBox: true });
  // Native equity x utilization chart from Table 2 (§6.6), replacing the paper's
  // Fig 45 image, whose labels sit on the wrong bubbles. Points are plotted
  // straight from the table; quadrants split at 0.5 as in the paper's figure.
  {
    const X0 = 7.95, X1 = 12.55, YT = 1.75, YB = 6.2;
    const gx = (e) => X0 + e * (X1 - X0), gy = (u) => YB - u * (YB - YT);
    const quad = (x0, y0, x1, y1, color) => s.addShape(pres.shapes.RECTANGLE, { x: gx(x0), y: gy(y1), w: gx(x1) - gx(x0), h: gy(y0) - gy(y1), fill: { color }, line: { color } });
    quad(0, 0.5, 0.5, 1, "FDF1DC");   // utilization-driven
    quad(0.5, 0.5, 1, 1, "FFFFFF");   // high on both (empty)
    quad(0, 0, 0.5, 0.5, "EEF1F4");   // low across pillars
    quad(0.5, 0, 1, 0.5, "E3EFFB");   // equity-driven
    s.addShape(pres.shapes.RECTANGLE, { x: gx(0.5), y: gy(1), w: gx(1) - gx(0.5), h: gy(0.5) - gy(1), fill: { color: WHITE, transparency: 100 }, line: { color: "9AA5B1", width: 1, dashType: "dash" } });
    const qlabel = (text, x, y, color, align = "left") => s.addText(text, { x, y, w: 2.2, h: 0.3, fontFace: FONT, fontSize: 12, bold: true, color, align, margin: 0, isTextBox: true });
    qlabel("Utilization-driven", gx(0.02), gy(0.98), "B26B00");
    qlabel("High on both: none", gx(0.98) - 2.2, gy(0.98), MUTED, "right");
    qlabel("Low across pillars", gx(0.02), gy(0.48), MUTED);
    qlabel("Equity-driven", gx(0.98) - 2.2, gy(0.48), BLUE, "right");
    // Axes
    s.addShape(pres.shapes.LINE, { x: X0, y: YB, w: X1 - X0, h: 0, line: { color: "9AA5B1", width: 1 } });
    s.addShape(pres.shapes.LINE, { x: X0, y: YT, w: 0, h: YB - YT, line: { color: "9AA5B1", width: 1 } });
    [0, 0.5, 1].forEach((v) => {
      s.addText(v.toFixed(1), { x: gx(v) - 0.3, y: YB + 0.04, w: 0.6, h: 0.25, fontFace: FONT, fontSize: 11, color: MUTED, align: "center", margin: 0, isTextBox: true });
      s.addText(v.toFixed(1), { x: X0 - 0.42, y: gy(v) - 0.12, w: 0.36, h: 0.25, fontFace: FONT, fontSize: 11, color: MUTED, align: "right", margin: 0, isTextBox: true });
    });
    s.addText("Equity pillar score (0–1) →", { x: X0, y: YB + 0.3, w: X1 - X0, h: 0.3, fontFace: FONT, fontSize: 13, color: NAVY, align: "center", margin: 0, isTextBox: true });
    s.addText("Utilization pillar score (0–1) →", { x: X0 - 2.88, y: (YT + YB) / 2 - 0.15, w: 4.45, h: 0.3, fontFace: FONT, fontSize: 13, color: NAVY, align: "center", rotate: 270, margin: 0, isTextBox: true });
    // Counties (Table 2: equity, utilization); top three highlighted.
    const pts = [
      ["Union", 0.319, 1.0, "F39C12", 0.12, -0.12, "left"],
      ["Mecklenburg", 0.81, 0.067, BLUE, -1.15, 0.12, "right"],
      ["Guilford", 0.855, 0.103, BLUE, 0.05, -0.38, "left"],
      ["New Hanover", 0.607, 0.071, "9AA5B1", -0.6, -0.4, "center"],
      ["Wake", 0.322, 0.13, "9AA5B1", 0.13, -0.28, "left"],
      ["Durham", 0.469, 0.033, "9AA5B1", -1.42, -0.3, "right"],
      ["Forsyth", 0.283, 0.156, "9AA5B1", -1.05, -0.3, "right"],
      ["Cabarrus", 0.228, 0.229, "9AA5B1", -0.6, -0.4, "center"],
      ["Buncombe", 0.47, 0.0, "9AA5B1", -1.42, -0.06, "right"],
      ["Orange", 0.059, 0.101, "9AA5B1", 0.13, -0.13, "left"],
    ];
    pts.forEach(([name, e, u, color, dx, dy, align]) => {
      const cx = gx(e), cy = gy(u), top3 = color !== "9AA5B1";
      const d = top3 ? 0.26 : 0.18;
      s.addShape(pres.shapes.OVAL, { x: cx - d / 2, y: cy - d / 2, w: d, h: d, fill: { color }, line: { color: WHITE, width: 1 } });
      s.addText(name, { x: cx + dx, y: cy + dy, w: align === "center" ? 1.2 : 1.3, h: 0.26, fontFace: FONT, fontSize: top3 ? 13 : 11, bold: top3, color: top3 ? NAVY : MUTED, align, margin: 0, isTextBox: true });
    });
  }
  s.addNotes("The ranking says where, but not why. Plotting equity against utilization gives three archetypes. Equity runs left to right, utilization bottom to top, and the top three counties are in color. Union is utilization-driven: 101.5 BEVs per port, more than three times the next county. It needs more stations. One caveat: Union is so far ahead that min-max scaling puts it at 1.0 and squeezes the other nine counties to 0.229 or below on utilization. The gap is real, not a data artifact, but the scoring is sensitive to an extreme value like this. Mecklenburg and Guilford are equity-driven. Mecklenburg's equity score is high not only because of its disadvantaged residents, but because its chargers are so unevenly spread across its ZIP codes, the Uptown gap. They need better-targeted stations. Orange is low on everything and isn't a priority now. And the top-right corner is empty: no county is high on both equity and utilization, so every county is a trade-off, which the framework makes visible.");
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
    { text: "Area-weighted CEJST–AFDC crosswalk at ZIP resolution (12 checks, 23 of 23 sub-checks passed)", options: { bullet: { type: "number" }, breakLine: true, paraSpaceAfter: 14 } },
    { text: "Three-pillar NEVI score with pillars that measure different things (VIF 1.41) and a robust top 3", options: { bullet: { type: "number" } } },
  ], { x: M + 0.3, y: 2.55, w: colW - 0.6, h: 3.3, fontFace: FONT, fontSize: 19, color: NAVY, valign: "top", margin: 0, isTextBox: true });
  const x2 = M + colW + 0.4;
  card(s, x2, 1.8, colW, 4.2);
  s.addText("Limitations, each with a direction of bias", { x: x2 + 0.3, y: 1.95, w: colW - 0.6, h: 0.45, fontFace: FONT, fontSize: 20, bold: true, color: BLUE, margin: 0, isTextBox: true });
  bullets(s, [
    [t("Top-10 scope (73% of fleet): "), b("bounded")],
    [t("LODES 2021 vintage: "), b("cancels in normalization")],
    [t("Static BEV counts: "), b("understates growth (conservative)")],
    [t("CEJST v2.0 lock, NEVI rule changes: "), b("direction unknown (policy risk)")],
  ], x2 + 0.3, 2.55, colW - 0.6, 3.3, 19);
  s.addNotes("So what does this add, and where is it weak? Three contributions. First, using the Theil decomposition as a design input, not just a summary number. To my knowledge, it's the first state-level application, and the first to use the split to design the allocation itself. Second, a validated crosswalk that brings the federal equity designations down to ZIP level. Third, a score whose pillars measure different things and whose top three holds across the equity-weight sweep. Each limitation comes with its direction of bias. The scope covers 73% of the fleet. The 2021 commuting data cancels out in normalization. Static counts understate growth, which makes the scores conservative. And federal policy changes are a risk whose direction we can't know yet. None of them directly undermines the headline rankings.");
}

// ---------- Slide 14: Implications / close ----------
{
  const s = pres.addSlide({ sectionTitle: "Talk" });
  s.background = { color: WHITE };
  s.addImage({ path: path.join(__dirname, "assets", "photo-close.jpg"), x: W - 5.0, y: 0, w: 5.0, h: 7.5 });
  s.addText("IMPLICATIONS AND NEXT STEPS", { x: M, y: 0.6, w: 7.4, h: 0.3, fontFace: FONT, fontSize: 11, bold: true, color: BLUE, charSpacing: 1.5, margin: 0, isTextBox: true });
  s.addText("A Ranking to Inform NCDOT's Decisions, and What Comes Next", { x: M, y: 0.95, w: 7.4, h: 1.05, fontFace: FONT, fontSize: 28, bold: true, color: NAVY, margin: 0, isTextBox: true });
  // Takeaways stay on screen through Q&A (tell them what you told them).
  const mark = (n) => ({ text: n + "  ", options: { bold: true, color: BLUE, paraSpaceBefore: 8 } });
  s.addText([
    mark("①"), { text: "84.5% of charging inequality is within counties: ", options: { bold: true } },
    { text: "county rankings for where to invest, ZIP-level targeting for whom", options: { breakLine: true } },
    mark("②"), { text: "Top 3: ", options: { bold: true } },
    { text: "Union 0.561 · Mecklenburg 0.548 · Guilford 0.465", options: { breakLine: true } },
    mark("③"), { text: "Forecasts hold out of sample (MAPE 4.34%) but run low: ", options: { bold: true } },
    { text: "plan an upward buffer of 4 to 5%", options: { breakLine: true } },
    { text: "Next: ", options: { bold: true, color: BLUE, paraSpaceBefore: 6 } },
    { text: "all 100 counties · validate against NCDOT's actual NEVI deployments · confidence intervals on composite scores", options: { color: MUTED } },
  ], { x: M, y: 2.1, w: 7.4, h: 2.5, fontFace: FONT, fontSize: 16, color: NAVY, valign: "top", margin: 0, isTextBox: true });
  card(s, M, 4.7, 7.4, 2.15, CARD);
  s.addText([
    { text: "Thank you", options: { fontSize: 28, bold: true, color: NAVY, breakLine: true } },
    { text: "wolfgang.sanyer@gmail.com", options: { fontSize: 15, color: NAVY, breakLine: true } },
    { text: "linkedin.com/in/wolfgangsanyer", options: { fontSize: 15, color: NAVY, breakLine: true } },
    { text: "github.com/wolfieman/ev-pulse-nc", options: { fontSize: 15, color: NAVY, breakLine: true } },
    { text: "sanyer.org/research-lab", options: { fontSize: 15, color: NAVY } },
  ], { x: M + 0.3, y: 4.7, w: 5.2, h: 2.15, fontFace: FONT, valign: "middle", margin: 0, isTextBox: true });
  s.addImage({ data: QR_REPO, x: M + 7.4 - 1.95, y: 4.7 + 0.3, w: 1.55, h: 1.55, altText: "QR code: github.com/wolfieman/ev-pulse-nc" });
  s.addNotes("This ranking is meant to inform NCDOT's decisions, not replace them. Right-of-way, utilities, and politics all matter and aren't in the model. What it gives is an analytical floor: a ranking an auditor can trace, and ZIP-level targets a planner can use. And NCDOT's community phase, which is still ahead, is exactly where a county ranking can help. Next: all 100 counties, a check against NCDOT's actual deployments, and confidence intervals on the scores. If you remember one thing: most of the charging gap is inside counties, so allocation has to work county first, then neighborhood. I'd like to thank my faculty advisors, Dr. Al-Ghandour and Dr. Adivar. Thank you, I'm happy to take questions.");
}

} // end talk slides

if (VARIANT !== "upload") {
// ---------- Backup slides ----------
pres.addSection({ title: "Backup" });
const backup = () => pres.addSlide({ masterName: "CONTENT", sectionTitle: "Backup" });

{
  const s = backup();
  header(s, "Backup B1", "Theil-T Decomposition");
  s.addNotes("If asked how the decomposition works, or who drives the within-county share. The Theil-T index splits exactly into a between-county and a within-county part, with no residual: 0.5791 = 0.0900 + 0.4892. The Theil-L version gives 82.5% within, so the result doesn't depend on the index. Mecklenburg alone contributes 41.5% of the within-county part and Wake 28.1%, together roughly 70%. Theil explains why Tier 2 exists; it isn't an input to either score.");
  // Native chart of each county's share of within-county inequality, the four
  // counties §6.3 reports (replaces the Fig 33 image, whose title overlaps).
  s.addChart(pres.charts.BAR, [
    { name: "Share of within-county inequality", labels: ["Mecklenburg", "Wake", "Guilford", "Union"], values: [41.5, 28.1, 7.7, 0.6] },
  ], {
    x: M, y: 1.75, w: 6.4, h: 4.6, barDir: "bar", barGapWidthPct: 40, chartColors: [BLUE],
    catAxisOrientation: "maxMin", catAxisLabelFontSize: 15, catAxisLabelFontFace: FONT, catAxisLabelColor: NAVY,
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0.0"%"', dataLabelColor: NAVY,
    dataLabelFontSize: 15, dataLabelFontBold: true, dataLabelFontFace: FONT,
    showTitle: true, title: "Share of within-county inequality (the four counties reported in §6.3)", titleFontSize: 14, titleColor: NAVY, titleFontFace: FONT,
    showLegend: false, valAxisHidden: true, valAxisMinVal: 0, valAxisMaxVal: 50,
    valGridLine: { style: "none" }, catGridLine: { style: "none" },
  });
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
  s.addNotes("If asked how CEJST tracts get down to ZIP level. CEJST uses 2010 census tracts; ZIP areas are 2020. I area-weighted the tracts into ZIP areas in the NC State Plane projection, the approach EPA's EJScreen and HUD's USPS crosswalk use. Twelve checks in three tiers, 23 of 23 sub-checks passed, with area conserved within 1% per ZIP area. The known limit: it assumes population is spread evenly within a tract, which is weaker in large rural tracts.");
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
  s.addNotes("If asked about a specific county, or for the full table. All ten counties, with each pillar score. Union leads utilization at 1.000; Guilford and Mecklenburg lead equity; Mecklenburg leads cost-effectiveness at 0.801. Orange is last at 0.077. Across the equity-weight sweep from 0.30 to 0.50, the top three stay the same: Mecklenburg gains and Union falls as the equity weight rises, and Orange stays tenth.");
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
  s.addNotes("If asked about data vintages, the estimator, or pillar correlations. All five sources are public; the vintages are in the table. Two diagnostics: SAS's default ARIMA estimator versus exact maximum likelihood changes forecasts by less than 0.1%, and NCDOT's May 2025 counting change is about 0.4% of totals and works against the underprediction. Equity and cost-effectiveness correlate +0.48; the other pairs are −0.26 and −0.03. So the pillars measure different things, but they aren't independent.");
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

{
  const s = backup();
  header(s, "Backup B5", "Workplace Demand by County (Paper Fig 36)");
  s.addNotes("If asked how large workplace demand is, county by county. Blue is registered BEVs in the county; orange adds the adjusted commuters who work there. The orange bar isn't an EV count: it shows where daytime demand concentrates. Port need in the paper uses a 30% charging adoption rate and a 15-to-1 port ratio.");
  fig(s, "fig-36-demand-comparison.png", 4269, 3069, M, 1.75, 7.3, 5.15);
  bullets(s, [
    [b("Blue:"), t(" registered BEVs in the county (residential demand)")],
    [b("Orange:"), t(" residential BEVs plus adjusted commuters who work in the county")],
    [t("The orange bar adds commuters to EVs: it shows "), b("where daytime demand concentrates"), t(", not an EV count. Port need uses a 30% charging adoption rate and a 15:1 port ratio (§6.4).")],
  ], 8.25, 1.95, W - 8.25 - M, 4.9, 15);
}

{
  const s = backup();
  header(s, "Backup B6", "Stations on Justice40 Tracts (Paper Fig 42)");
  s.addNotes("If asked where stations sit relative to disadvantaged areas. Pink tracts are disadvantaged under CEJST; blue dots are Level 2 stations and orange triangles are fast chargers. These colors differ from slide 7's map. Of 1,210 stations in the ten counties, 24.5% sit in disadvantaged tracts, against 18.5% of residents: roughly proportional overall, with strong variation county by county.");
  fig(s, "fig-42-stations-justice40-overlay.png", 6069, 3733, M, 1.7, 8.2, 5.0);
  bullets(s, [
    [b("Pink:"), t(" disadvantaged census tracts (CEJST v2.0)")],
    [b("Blue dots:"), t(" Level 2 (L2) charging stations")],
    [b("Orange triangles:"), t(" DC fast-charging (DCFC) stations")],
    [t("1,210 stations in the 10 study counties; 24.5% in disadvantaged tracts (§6.5)")],
  ], 9.05, 1.9, W - 9.05 - M, 4.8, 14);
}

{
  const s = backup();
  header(s, "Backup B7", "Pillar Contributions to the NEVI Score (Paper Fig 43)");
  s.addNotes("If asked what drives a county's score, e.g. Union's. This is the paper's breakdown of each total into weighted pillar contributions. Union's bar is dominated by utilization, its 1.000 normalized score; Mecklenburg's and Guilford's are dominated by equity. It's the archetype story from slide 13, shown as parts of each score.");
  fig(s, "fig-43-nevi-priority-scores.png", 4869, 3369, M, 1.7, 8.2, 5.15);
  bullets(s, [
    [b("Blue:"), t(" equity (weight 0.40)")],
    [b("Orange:"), t(" utilization (weight 0.35)")],
    [b("Green:"), t(" cost-effectiveness (weight 0.25)")],
    "Union's bar is dominated by utilization; Mecklenburg's and Guilford's by equity (§6.7)",
  ], 9.05, 1.9, W - 9.05 - M, 4.8, 14);
}

{
  const s = backup();
  header(s, "Backup B8", "Tier 2: ZIP-Level Targeting");
  s.addNotes("If asked \"where's the ZIP-level tier?\" The talk shows why it exists: the 84.5% within-county finding and the 250-fold gap in Mecklenburg. Tier 2 ranks ZIPs within each county on population, disadvantaged status, and station density. The top 20 underserved ZIPs hold 732,892 residents served by 58 ports, 15 have zero fast chargers, and Mecklenburg and Guilford each have five of them.");
  bullets(s, [
    [b("What Tier 2 uses: "), t("population, disadvantaged-community status, and station density, ranking ZIPs within each county (§4.4)")],
    [b("Its output: "), t("the top 20 underserved ZIPs hold "), b("732,892 residents served by 58 ports"), t("; "), b("15"), t(" have zero DC fast chargers (§6.2)")],
    [t("Mecklenburg and Guilford each contribute "), b("5 ZIPs"), t(" to the top 20: the state's two most infrastructure-rich counties also hold some of its worst gaps (§6.2)")],
    [t("Theil justifies Tier 2 but is "), b("not an input"), t(" to either tier's score (§4.4)")],
  ], M, 1.9, W - 2 * M, 4.8, 19);
}

{
  const s = backup();
  header(s, "Backup B9", "Glossary of Abbreviations");
  const rows = [
    ["ACS", "American Community Survey"], ["AFDC", "Alternative Fuels Data Center"],
    ["API", "Application programming interface"], ["ARIMA", "Autoregressive integrated moving average"],
    ["BEV", "Battery electric vehicle"], ["CEJST", "Climate and Economic Justice Screening Tool"],
    ["CSS / MLE", "Conditional sum of squares / maximum likelihood estimation"], ["DCFC", "DC fast charging"],
    ["E / U / CE", "Equity / Utilization / Cost-Effectiveness pillars"], ["EDGI", "Environmental Data & Governance Initiative"],
    ["EO", "Executive Order"], ["EPA EJScreen", "U.S. Environmental Protection Agency environmental justice screening tool"],
    ["EPSG", "Standard ID code for a map projection (here, NC State Plane)"], ["ESM", "Exponential smoothing model"],
    ["FHWA", "Federal Highway Administration"], ["GE(0) / GE(1)", "Generalized entropy index, alpha = 0 (Theil-L) / alpha = 1 (Theil-T)"],
    ["HUD USPS", "Dept. of Housing and Urban Development / U.S. Postal Service ZIP crosswalk"], ["IEA", "International Energy Agency"],
    ["IRA", "Inflation Reduction Act"], ["Justice40", "Federal goal (EO 14008, 2021): 40% of certain federal benefits to disadvantaged communities; rescinded Jan 2025"],
    ["L2", "Level 2 charging"], ["LEHD LODES", "Longitudinal Employer-Household Dynamics Origin-Destination Employment Statistics"],
    ["MAPE", "Mean absolute percentage error"], ["NCDOT", "North Carolina Department of Transportation"],
    ["NEVI", "National Electric Vehicle Infrastructure (Formula Program)"], ["NREL", "National Renewable Energy Laboratory"],
    ["PEDP", "Public Environmental Data Partners"], ["TIGER", "Census Topologically Integrated Geographic Encoding and Referencing (boundaries)"],
    ["UCM", "Unobserved components model"], ["VIF", "Variance inflation factor"],
    ["ZCTA", "ZIP Code Tabulation Area"],
  ];
  // Two side-by-side tables so the list clears the footer at a readable size.
  const half = Math.ceil(rows.length / 2), g = 0.3, tw = (W - 2 * M - g) / 2;
  [rows.slice(0, half), rows.slice(half)].forEach((part, k) => {
    const hdr = ["Abbreviation", "Meaning"].map((h) => ({ text: h, options: { bold: true, color: WHITE, fill: { color: NAVY } } }));
    const data = part.map((r, i) => r.map((c) => ({ text: c, options: { fill: { color: i % 2 ? WHITE : CARD } } })));
    s.addTable([hdr, ...data], { x: M + k * (tw + g), y: 1.6, w: tw, colW: [1.45, tw - 1.45], fontFace: FONT, fontSize: 12, color: NAVY, rowH: 0.29, margin: 0.04, border: { type: "solid", pt: 0.5, color: "C8D6E5" } });
  });
}
} // end backup slides

const f = await pres.writeFile({ fileName: path.join(OUT_DIR, `${BASE}-${VARIANT}.pptx`) });
console.log("wrote", f);
}

(async () => {
  for (const v of ["upload", "presenter", "backup"]) await main(v);
})().catch((e) => { console.error(e); process.exit(1); });
