# 2025 Colts Situational Efficiency Audit

A data analysis project investigating whether the Indianapolis Colts' offensive efficiency declined over the course of the 2025 season — and whether that decline holds up once opponent strength is accounted for.

## Overview

Using play-by-play data, this project evaluates the Colts' early-down (1st and 2nd down) offensive performance across two segments of the 2025 season — **Weeks 1–8** and **Weeks 9–13** — to test the hypothesis that the offense regressed as the season progressed. The analysis goes beyond simple counting stats by using **Expected Points Added (EPA)** as the core efficiency metric, and by adjusting for the defensive strength of each week's opponent to rule out "tougher schedule" as the sole explanation.

## Key Questions

- Did the Colts' early-down efficiency (EPA, success rate) change over the season?
- Did their run/pass play-calling tendencies shift between the two segments?
- Is any observed decline explained by facing stronger defenses later in the season, or does it persist after normalizing for opponent strength?

## Methodology

1. **Data source:** Play-by-play data pulled via [`nfl_data_py`](https://github.com/nflverse/nfl_data_py) and loaded into a local SQLite database.
2. **Querying:** SQL used to aggregate play counts, average EPA, and average yards gained, filtered to Colts offensive plays on 1st and 2nd down.
3. **Segmentation:** Season split into "Early" (Weeks 1–8) and "Late" (Weeks 9–13) to compare performance windows.
4. **Success rate definition:** A play is marked successful if it gains ≥4 yards on 1st down, or ≥50% of yards-to-go on 2nd down.
5. **Opponent adjustment:** Defensive strength calculated independently for each segment (average EPA allowed per team), then merged against Colts performance per game to separate offensive decline from strength-of-schedule effects.
6. **Run gap analysis:** Runs categorized as "inside" or "outside" based on run location, then compared across segments to isolate whether the decline was uniform or concentrated in a specific part of the run game.
7. **Visualization:** Seaborn/Matplotlib used to build grouped bar charts and a run/pass ratio heatmap by down and segment.

## Key Findings

- **Early-down success rate dropped from 48.7% (Weeks 1–8) to 37.8% (Weeks 9–13).**
- **1st down passing efficiency collapsed**, with average EPA falling from +0.29 (Early) to -0.19 (Late).
- **1st down run/pass ratio increased** late in the season (0.93 → 1.08) — the offense leaned *more* on the pass even as passing efficiency dropped.
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

This analysis is limited to Weeks 1–13 of the 2025 regular season and focuses on early-down (1st/2nd) play-calling. Future extensions could include 3rd down conversion analysis, red zone efficiency, or extending the opponent-adjustment model league-wide.
