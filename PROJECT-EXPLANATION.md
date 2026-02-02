# EV Pulse NC: Project Explanation for Dr. Al-Ghandour

**Audience:** Dr. Majed Al-Ghandour, BIDA 670 Instructor
**Purpose:** Clarify project structure, baseline vs. extensions, and methodological innovation
**Date:** January 30, 2026

---

## Project Overview

North Carolina faces a critical infrastructure challenge: electric vehicle (EV) adoption is outpacing the deployment of public charging infrastructure, creating geographic inequalities that threaten equitable access to electric mobility. Between September 2018 and June 2025, the state's battery electric vehicle (BEV) fleet exploded from 5,165 vehicles to 94,371—a 1,727% increase with a 53.8% compound annual growth rate. Meanwhile, public charging infrastructure has struggled to keep pace, with approximately 16.9 BEVs per charging port compared to the national benchmark of 10-15 BEVs per port.

This project analyzes the alignment between EV adoption and infrastructure deployment across all 100 North Carolina counties over 82 months of time series data (September 2018 through June 2025). The dataset comprises 8,200 county-month observations on the demand side (NCDOT BEV registration data) and 1,725 individual charging connectors across 355 stations on the supply side (AFDC infrastructure snapshot from July 2024). The core research question addresses resource allocation: where should North Carolina's $109 million in NEVI Formula Program funding be deployed to maximize infrastructure equity and efficiency?

What makes this analysis distinctive is its granularity and temporal depth. While most EV infrastructure studies operate at the state or metropolitan level using snapshot data, this project examines county-level dynamics over nearly seven years. The supply-side analysis operates at the connector level—1,725 individual charging units rather than 355 aggregate stations—providing 4.85 times more analytical precision. This combination of temporal breadth (82 months) and spatial detail (100 counties, 1,725 connectors) creates a uniquely comprehensive view of North Carolina's EV infrastructure landscape.

---

## Baseline Analysis - Completed Last Semester

The baseline analysis established the analytical foundation through a comprehensive five-phase framework: exploratory, descriptive, diagnostic, predictive, and prescriptive analysis. This work was completed during Fall 2025 and provides the validated foundation for this semester's extension work.

On the demand side, the analysis processed NCDOT's complete time series of BEV registrations: 8,200 observations spanning 100 counties across 82 months (September 2018 through June 2025). The data reveals extreme geographic concentration, with a Gini coefficient of 0.805 indicating that the top 10 counties account for 72% of all BEVs while the bottom 50 counties combined hold just 4.8% of the fleet. The Research Triangle counties (Wake, Durham, Orange) alone represent 35.2% of the statewide total. This concentration creates a tension between efficiency (deploying infrastructure where demand already exists) and equity (ensuring rural and disadvantaged communities have access to charging infrastructure).

On the supply side, the analysis incorporated AFDC's July 2024 snapshot of North Carolina's charging infrastructure: 355 stations containing 1,725 individual charging ports. The connector-level detail enables capacity-weighted analysis that accounts for charging power levels. For example, Tesla's network represents only 24.8% of stations but 60.5% of all charging connectors, primarily through high-powered Supercharger locations. This granularity matters because a station with two 7kW Level 2 chargers serves far fewer vehicles per day than a station with eight 250kW DC fast chargers. The capacity-weighted analysis reveals that 80.5% of infrastructure provides 150kW or higher charging speeds, indicating a strategic focus on high-turnover corridor charging rather than destination charging.

The predictive component employed county-level ARIMA forecasting to project BEV adoption through June 2028. Rather than building a single statewide model, the analysis fitted 100 separate ARIMA models—one per county—to capture heterogeneous adoption trajectories. Urban counties like Wake and Mecklenburg exhibit sustained exponential growth, while rural counties show sporadic adoption patterns with high volatility. The weighted mean absolute percentage error (MAPE) across all counties was 2.73%, indicating strong historical predictive accuracy. These forecasts project that North Carolina's BEV fleet will reach approximately 150,000 vehicles by mid-2028, requiring an estimated 10,000-15,000 public charging ports to maintain adequate infrastructure ratios.

The gap analysis methodology compared demand (BEVs per county) to supply (charging ports per county) using both simple ratios (BEVs per port) and capacity-weighted metrics (BEVs per kilowatt of charging capacity). The statewide average of 16.9 BEVs per port exceeds the national benchmark range of 10-15 BEVs per port, but county-level variation is dramatic. Wake County hosts 54.7 BEVs per port while some rural counties have zero infrastructure despite modest BEV populations. This analysis classified counties into three tiers: well-aligned (adequate infrastructure for current demand), emerging strain (approaching capacity constraints), and high strain (demand significantly outpacing supply).

The baseline analysis established several key findings. First, infrastructure deployment has dramatically accelerated, with 47.6% of all current infrastructure added during 2024-2025 alone—likely reflecting federal funding incentives including NEVI Formula Program dollars and Inflation Reduction Act tax credits. Second, geographic inequality in access is extreme, with the Gini coefficient of 0.805 comparable to highly unequal wealth distributions. Third, the infrastructure gap is widening despite rapid deployment, as demand growth (53.8% CAGR) consistently outpaces supply expansion. Fourth, zero-infrastructure counties—those with BEV registrations but no public charging stations—represent critical equity concerns, particularly in rural eastern North Carolina.

This baseline work established credibility through methodological rigor, comprehensive data coverage, and validated forecasting accuracy. The predictive models performed well on historical backtesting, the data cleaning process documented and resolved inconsistencies, and the analytical framework progressed systematically from exploratory profiling through prescriptive recommendations. Having established this foundation, the extension work this semester adds strategic depth without replacing or undermining the baseline analysis.

---

## The Extension Framework - This Semester

The baseline analysis proved the project's viability and established analytical credibility. This semester's work builds on that foundation through four targeted extensions that enhance rather than replace the county-level temporal analysis. The extension logic follows a clear principle: start with validation to confirm the baseline's accuracy, then add analytical dimensions that address stakeholder questions the baseline could not answer.

The extensions are prioritized based on analytical value, data availability, and integration potential. Priority #1 (validation) must be completed first because it establishes confidence in the forecasting methodology that underpins all subsequent work. Priority #5 (infrastructure data update) provides the current baseline that Priorities #2 and #3 depend upon. Priority #2 (ZIP code analysis) and Priority #3 (workplace charging via CTPP) can proceed in parallel once the updated infrastructure baseline is available. This sequencing ensures that each extension builds logically on validated prior work.

The extensions share a common analytical philosophy: acknowledge limitations transparently, report ranges rather than false precision, and frame findings as proof-of-concept methodologies that future work can refine. Unlike the baseline analysis, which aimed for comprehensive state coverage, the extensions apply strategic selectivity—focusing analytical effort where data quality supports meaningful insights. For example, ZIP code analysis targets the top 100-120 urban ZIP codes rather than attempting to analyze all 800 statewide, and workplace charging analysis focuses on the top 15 employment centers rather than modeling all 10,000 possible county-to-county commute pairs.

---

## Extension Slice #1: Validation (Priority #1)

The validation extension addresses a fundamental question: how accurate are the ARIMA forecasts used to project future infrastructure needs? The baseline analysis reported strong historical fit (MAPE of 2.73%), but this measures in-sample performance—how well models fit the data used to train them. Out-of-sample validation tests whether models maintain accuracy when predicting genuinely new data they have never seen.

The methodology leverages a fortunate timing advantage. The baseline analysis used data through June 2025 to build forecasting models. In the months since project completion, NCDOT has published July through October 2025 actual BEV registration counts. These four months of new data provide an out-of-sample testing window. The validation process compares what the ARIMA models predicted for July-October 2025 against what actually occurred, calculating accuracy metrics (MAPE, mean absolute error, root mean squared error) to quantify forecast performance.

This validation employs an accuracy spectrum interpretation rather than a binary pass-fail threshold. If aggregate MAPE across counties remains below 5%, this indicates strong validation—the models can be used confidently for policy recommendations through 2028. If MAPE falls between 5-10%, this suggests moderate validation requiring wider confidence intervals and cautious interpretation. If MAPE exceeds 10%, this signals weak validation requiring diagnostic work to identify failure modes (structural breaks, non-stationarity, specification errors) before proceeding with extensions.

The innovation here is methodological transparency. Most infrastructure planning studies deploy forecasts with minimal validation, assuming models trained on historical data will perform adequately on future projections. By explicitly testing forecast accuracy before making policy recommendations, this extension demonstrates scientific rigor and builds stakeholder confidence. If validation reveals weaknesses, the analysis includes remediation strategies: bias correction factors, hybrid approaches combining ARIMA with external growth factors, or migration to alternative forecasting methodologies.

---

## Extension Slice #2: ZIP Code Analysis (Priority #2) + Infrastructure Update (Priority #5)

County-level aggregation obscures critical intra-county variation, particularly in large urban counties. Wake County, for example, spans 857 square miles and contains approximately 28 ZIP codes with dramatically different BEV adoption densities. Aggregating infrastructure needs to the county level is appropriate for state-level policy but inadequate for site selection—the specific question of where within Wake County to deploy the next 50 charging stations. ZIP code analysis provides sub-county precision that enables targeted deployment strategies.

The challenge is data availability. While NCDOT publishes comprehensive county-level BEV registration data (the foundation of the baseline analysis), they do not publish ZIP code-level adoption statistics. This is a deliberate policy choice, likely reflecting privacy concerns (small geographic units risk revealing individual vehicle owners) and administrative convenience (ZIP codes change boundaries more frequently than counties, complicating time series analysis). Requests to NCDOT for ZIP-level data have been unsuccessful, and commercial alternatives (IHS Markit, Experian) require expensive licenses beyond project resources.

The solution is an infrastructure-only ZIP code analysis for urban areas. While BEV adoption data is unavailable at the ZIP level, charging station data inherently contains ZIP codes (stations have street addresses). The extension geocodes all 1,725 charging connectors to their associated ZIP codes, then calculates infrastructure density metrics: ports per square mile, ports per capita, and spatial clustering patterns. This analysis identifies which ZIP codes within major urban counties have adequate charging coverage and which represent infrastructure deserts despite high population density.

This work integrates tightly with Priority #5, the infrastructure data update. The baseline analysis used AFDC's July 2024 infrastructure snapshot, which is now six months stale. Recent deployment has been rapid—47.6% of all infrastructure was added during 2024-2025—so staleness creates meaningful distortion. A six-month lag means the numerator (current BEV population) is up-to-date while the denominator (infrastructure count) is outdated, systematically overstating gaps by 15-22%.

Rather than simply replacing the July 2024 snapshot with a January 2026 update, the extension employs a dual-snapshot approach that transforms a data weakness into an analytical strength. By retaining both snapshots, the analysis calculates infrastructure growth rates: which counties saw the fastest deployment between July 2024 and January 2026, what types of chargers were added (Level 2 vs. DC fast charging), and whether new infrastructure went to gap counties or amplified existing disparities by concentrating in already well-served urban areas.

The dual-snapshot methodology enables a unique research question that snapshot-only analyses cannot address: are market forces and existing public funding closing infrastructure gaps, or are they widening inequalities? If new stations disproportionately deployed in already-served counties (following market demand), this strengthens the equity case for targeted NEVI funding in underserved areas. If deployment preferentially targeted gap counties, this indicates that existing incentives are working and NEVI dollars can focus on maintenance and expansion rather than gap-filling.

For ZIP code analysis, the January 2026 infrastructure snapshot provides current spatial distribution data essential for urban sub-county targeting. The analysis will focus on approximately 100-120 ZIP codes within the top 10 urban counties, representing roughly 80% of the state's BEV population. Rather than attempting to forecast ZIP-level adoption (data unavailable), the extension uses county-level forecasts as constraints and examines infrastructure distribution within those county totals. The value proposition is site selection precision: "deploy 50 stations in ZIP codes 27603, 27607, and 27615 in Wake County" provides actionable guidance that "deploy in Wake County" does not.

---

## Extension Slice #3: Workplace Charging (Priority #3)

The baseline analysis treated BEV demand as a residential phenomenon—vehicles are registered to home addresses, and most charging occurs at home (approximately 80% of all EV charging). This residential focus is accurate but incomplete. Electric vehicles also require charging at workplaces, particularly for commuters with long distances or those living in multi-family housing without home charging access. The workplace charging extension adds a second analytical dimension by incorporating inter-county commuting patterns.

The data source is the Census Transportation Planning Products (CTPP), a specialized dataset derived from the American Community Survey (ACS) that provides county-to-county commuting flow matrices. For each North Carolina county, CTPP reports how many workers commute in from every other county and how many residents commute out to work elsewhere. This creates a 100×100 matrix of commuting flows capturing approximately 1,500-2,500 meaningful pairs (flows with more than 100 workers).

The methodology identifies employment centers by calculating net commuting effects: inbound workers minus outbound residents. Wake County, for example, has approximately 450,000 total workers but only 350,000 residents employed within the county, indicating a net positive commuting effect—roughly 100,000 people commute into Wake County for work daily. These net inbound commuters represent workplace charging demand that residential analysis misses entirely.

The inference chain applies EV adoption rates to commuting flows. If Wake County draws 10,000 daily commuters from Johnston County, and Johnston County's BEV adoption rate is 1.8%, this implies approximately 180 EV commuters traveling from Johnston to Wake daily. Applying a workplace charging propensity rate (30%, based on ChargePoint utilization data) suggests that roughly 54 of these commuters charge at work regularly. Aggregating across all inbound commuting pairs sizes Wake County's workplace infrastructure gap.

The key insight from this analysis is efficiency asymmetry: workplace charging infrastructure serves far more vehicles per port than residential public charging. The baseline analysis found that residential public chargers average 7.5 BEVs per port, while preliminary workplace estimates suggest 15 BEVs per port—double the efficiency. This occurs because workplace chargers have consistent demand (same commuters Monday through Friday) and long dwell times (8-hour workdays) that maximize utilization. A parking garage with 20 Level 2 workplace chargers can serve 300 regular users across the week, while a public charger in a retail area serves more variable, transient demand.

The dual-dimension model reveals that employment centers need 2-3 times more infrastructure than residential analysis alone suggests. Wake County's residential demand (based on 25,000 registered BEVs) requires approximately 1,700-2,500 public residential ports. Adding workplace demand (approximately 8,400 net EV commuters) increases total needs to 2,200-3,100 ports. Without CTPP data, investment plans would systematically underfund employment centers and overfund bedroom communities.

The challenge is data vintage. CTPP is based on 2016-2020 ACS data, making it 6-10 years old. More critically, these data predate COVID-19 remote work shifts that fundamentally altered commuting patterns. The solution applies sector-specific remote work adjustment factors: technology hubs like Wake County receive a 0.75 multiplier (25% reduction in commuting), traditional manufacturing counties like Guilford receive a 0.85 multiplier (15% reduction), and rural counties receive a 0.90 multiplier (10% reduction). These adjustments account for the reality that while remote work reduced commuting volumes, remaining commuters are charging more intensively at work (sessions per user increased 64% between 2023-2024 according to ChargePoint data).

The workplace extension explicitly acknowledges uncertainty through sensitivity ranges rather than point estimates. Rather than claiming "Wake County needs exactly 158 workplace ports," the analysis reports "Wake County needs 90-239 workplace ports depending on remote work adjustment assumptions, EV adoption rate variation, and workplace charging propensity." This range-based reporting maintains analytical honesty while still providing actionable order-of-magnitude guidance for infrastructure planning.

---

## Integration Logic

The extensions connect through a logical dependency chain. Validation (Priority #1) establishes confidence in the ARIMA forecasting methodology that underpins the baseline analysis. If validation is strong (MAPE below 5%), the county-level forecasts can be used reliably as constraints for ZIP code allocation and workplace demand calculations. If validation reveals weaknesses, extensions proceed with appropriately wider uncertainty intervals.

The AFDC infrastructure update (Priority #5) provides the current baseline that subsequent extensions require. ZIP code analysis needs January 2026 station locations to calculate sub-county infrastructure density. Workplace charging analysis needs current station type classifications (workplace-accessible vs. residential public) to measure existing workplace supply. Without updated infrastructure data, extensions would compound the 6-month staleness problem present in the baseline analysis.

ZIP code analysis (Priority #2) and CTPP workplace charging (Priority #3) operate at different analytical scales but complement each other. ZIP code analysis provides intra-county spatial detail: within Wake County, which ZIP codes have the highest BEV density and lowest charging access? CTPP analysis provides inter-county commuting flows: how many EV drivers cross from Johnston County into Wake County for work, creating workplace charging demand that isn't visible in Wake County's residential registration data? Together, these extensions create a triple-layer analytical model: county-level totals (baseline), sub-county spatial patterns (ZIP codes), and cross-county commuting flows (CTPP).

The extensions are not replacing county-level work but adding strategic detail where it matters most. The baseline analysis remains the foundation: 100 counties, 82 months, 8,200 observations, validated ARIMA forecasts. Extensions enhance this by answering questions the baseline could not address: Where within Wake County? (ZIP code analysis) Who is charging at work? (CTPP analysis) How fast is infrastructure actually growing? (dual-snapshot AFDC update) How accurate are our forecasts? (validation analysis).

---

## Methodological Innovation Summary

This project introduces several analytical innovations that distinguish it from typical EV infrastructure studies:

**County-level granularity over 82 months:** Most EV infrastructure research operates at state or metropolitan levels using snapshot data. This project examines all 100 North Carolina counties across nearly seven years of monthly observations, enabling time series forecasting that captures heterogeneous adoption trajectories rather than assuming uniform statewide trends.

**Connector-level infrastructure detail:** The supply-side analysis operates on 1,725 individual charging connectors rather than 355 aggregate stations—4.85 times more granular. This enables capacity-weighted analysis accounting for charging power levels (a 250kW DC fast charger serves far more vehicles daily than a 7kW Level 2 charger). Most studies treat all stations equally, ignoring capacity heterogeneity.

**Dual-snapshot infrastructure growth analysis:** Rather than simply updating stale data, the dual-snapshot approach (July 2024 + January 2026) treats temporal evolution as a research question itself. Calculating infrastructure deployment rates and spatial patterns of growth reveals whether market forces are closing gaps or amplifying disparities—a unique analytical contribution enabled by retaining both baselines.

**Dual-dimension demand model:** Combining residential BEV registrations (baseline) with workplace commuting flows (CTPP extension) creates a more complete demand picture. Employment centers like Wake County serve both residents and net inbound commuters, while bedroom communities primarily serve residents. This distinction matters for infrastructure type allocation: workplace chargers in employment centers, residential public chargers in bedroom communities.

**Validation-first approach:** Explicitly testing forecast accuracy with out-of-sample data before making policy recommendations demonstrates scientific rigor uncommon in applied infrastructure planning. Most studies deploy forecasts without validation, assuming historical fit guarantees future accuracy. This project treats validation as a prerequisite, not an afterthought, and commits to reporting accuracy limitations transparently.

---

## Conclusion

EV Pulse NC addresses a critical infrastructure planning challenge: how should North Carolina allocate $109 million in NEVI Formula Program funding to maximize both efficiency and equity? The baseline analysis completed last semester established a comprehensive county-level understanding of the demand-supply gap using 82 months of time series data and connector-level infrastructure detail. This semester's extensions enhance that foundation by validating forecast accuracy (Priority #1), updating infrastructure data with a dual-snapshot growth analysis (Priority #5), adding sub-county spatial precision in urban areas (Priority #2), and incorporating workplace charging demand through commuting flow analysis (Priority #3).

The project's methodological innovations—temporal depth, connector-level granularity, dual-snapshot evolution tracking, and dual-dimension demand modeling—collectively provide stakeholders with actionable insights at multiple scales: statewide trends for policy, county-level forecasts for regional planning, ZIP code detail for site selection, and workplace demand sizing for employment center targeting. By combining comprehensive baseline analysis with strategically targeted extensions, the project delivers both breadth and depth without sacrificing analytical rigor.

---

**Project Team:**
Wolfgang Sanyer & Braeden Baker<BR>
MBA Candidates, Business & Data Analytics Concentration<BR>
Fayetteville State University

**Faculty Advisor:** Dr. Majed Al-Ghandour<BR>
**Course:** BIDA 670 - Advanced Analytics Capstone<BR>
**Semester:** Spring 2026
