# 2025 Colts Situational Efficiency Audit: Testing the QB-Injury Narrative

A data analysis project testing whether the popular explanation for the Indianapolis Colts' 2025 offensive decline — their starting quarterback's injury — actually holds up against the timeline.

## Overview

The Colts' offensive struggles late in the 2025 season are commonly attributed to the starting quarterback's injury. **This analysis covers Weeks 1–13, but the QB injury didn't occur until Week 14** — meaning the entire efficiency decline measured here happened *before* the injury that's typically cited as its cause. Using play-by-play data, this project evaluates the Colts' early-down (1st and 2nd down) offensive performance across two in-season segments — **Weeks 1–8** and **Weeks 9–13** — to find out whether the offense was already breaking down independent of personnel changes, and if so, where. The analysis uses **Expected Points Added (EPA)** as the core efficiency metric and adjusts for each week's opponent defensive strength to rule out "tougher schedule" as an alternate explanation.

## Key Questions

- Did the Colts' early-down efficiency (EPA, success rate) decline before Week 14 — i.e., independent of the QB injury commonly cited as the cause?
- Did their run/pass play-calling tendencies shift between the two segments, and did the offense adjust to what was/wasn't working?
- Is any observed decline explained by facing stronger defenses later in the season, or does it persist after normalizing for opponent strength?
- If the decline predates the QB injury, where specifically did it originate?

## Methodology

1. **Data source:** Play-by-play data pulled via [`nfl_data_py`](https://github.com/nflverse/nfl_data_py) and loaded into a local SQLite database.
2. **Querying:** SQL used to aggregate play counts, average EPA, and average yards gained, filtered to Colts offensive plays on 1st and 2nd down.
3. **Segmentation:** Season split into "Early" (Weeks 1–8) and "Late" (Weeks 9–13) to compare performance windows — both entirely before the Week 14 QB injury.
4. **Success rate definition:** A play is marked successful if it gains ≥4 yards on 1st down, or ≥50% of yards-to-go on 2nd down.
5. **Opponent adjustment:** Defensive strength calculated independently for each segment (average EPA allowed per team), then merged against Colts performance per game to separate offensive decline from strength-of-schedule effects.
6. **Run gap analysis:** Runs categorized as "inside" or "outside" based on run location, then compared across segments to isolate whether the decline was uniform or concentrated in a specific part of the run game.
7. **Visualization:** Seaborn/Matplotlib used to build grouped bar charts and a run/pass ratio heatmap by down and segment.

## Key Findings

- **The full decline measured here predates the QB injury (Week 14) by definition** — the dataset only runs through Week 13, so the commonly cited explanation cannot account for any of the regression observed.
- **Early-down success rate dropped from 48.7% (Weeks 1–8) to 37.8% (Weeks 9–13).**
- **1st down passing efficiency collapsed**, with average EPA falling from +0.29 (Early) to -0.19 (Late).
- **1st down run/pass ratio increased** late in the season (0.93 → 1.08) — the offense leaned more on the pass even though passing efficiency dropped.
- The performance decline **persisted after adjusting for opponent defensive strength**, suggesting the drop-off reflects an internal offensive issue rather than simply facing tougher defenses.
- **Breaking runs down by gap (inside vs. outside) isolated where the decline was concentrated:** inside run efficiency stayed roughly flat (+0.059 → +0.046 EPA), while outside run efficiency collapsed from the offense's most productive play type early in the season (+0.205 EPA) to a negative-value play late (-0.098 EPA). This points to a specific breakdown in the outside/perimeter run game — rather than a uniform offensive decline — that the play-calling did not adjust to.

## Tech Stack

- **Python** — pandas, nfl_data_py
- **SQL** — SQLite for querying and aggregation
- **Visualization** — Seaborn, Matplotlib

## Visualizations

- Grouped bar chart: average EPA by down, comparing Early vs. Late season
- Heatmap: run/pass ratio by down and season segment
- Annotated weekly performance chart: Colts EPA vs. opponent defensive strength, Weeks 1–13

## Setup

```bash
pip install nfl_data_py pandas seaborn matplotlib
```

Run the notebook/scripts in order to rebuild the SQLite database, run the queries, and regenerate the visualizations.

## Notes

This analysis is limited to Weeks 1–13 of the 2025 regular season and focuses on early-down (1st/2nd) play-calling. The starting quarterback's Week 14 injury is commonly cited as the cause of the Colts' offensive decline — but since that decline is fully observable in data from before the injury occurred, this analysis suggests the offensive regression has a different, earlier root cause. It is worth noting, the quarterback was playing through a nagging injury in the weeks leading up to Week 14, which sharpens the play-calling question this analysis raises: even as passing efficiency collapsed (+0.29 → -0.19 EPA on 1st down) and inside runs remained the offense's one stable, efficient option (+0.059 → +0.046 EPA), the offense's run/pass ratio shifted *toward* the pass (0.93 → 1.08) despite the quarterback being shaken up. The data doesn't capture injury status on a play-by-play basis, so this is interpretation rather than a verified causal claim — but the trend is consistent with a play-calling staff that didn't adjust to either declining personnel or declining play-type efficiency. Future extensions could include 3rd down conversion analysis, red zone efficiency, specific pass zones, or extending this window past Week 14 to compare performance once the backup QB took over.
