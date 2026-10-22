# 2025 Colts Offense: Soft Schedule or Real Decline?

A data analysis project testing why the Indianapolis Colts' 2025 offense fell off after a hot start. My hypothesis: the early success came from facing easier defenses, and the offense regressed once the schedule got tougher. The second question: how much of the late-season collapse comes from starting QB Daniel Jones' Week 14 injury instead?

## Overview

Using play-by-play data, this project evaluates the Colts' early-down (1st and 2nd down) offense across three segments of the 2025 regular season:

| Segment | Weeks | Starting QB |
|---|---|---|
| Early | 1–8 | Daniel Jones |
| Late | 9–13 | Daniel Jones |
| Post-injury | 14–18 | Riley Leonard / Philip Rivers |

Efficiency is measured with **Expected Points Added (EPA)** and **success rate**. Each opponent is rated by the EPA its defense allowed to the rest of the league, which shows both how tough the schedule was and how the Colts performed relative to what each defense usually gave up.

## Key Questions

- Were the Colts' early opponents easier than their later ones?
- Was the hot start real, or a product of the schedule?
- How much of the decline survives after adjusting for opponent strength?
- How much of the collapse lines up with the QB injury instead of the schedule?
- Where did the offense change, and did play-calling follow what was working?

## Methodology

1. **Data source:** Play-by-play data pulled with [`nflreadpy`](https://github.com/nflverse/nflreadpy) and loaded into a local SQLite database (`ingest.py`).
2. **Segmentation:** SQL filters to Colts 2025 regular-season run/pass plays on 1st and 2nd down and tags each play with its segment. One shared segment definition with explicit week bounds is used everywhere, and a sanity check confirms each segment contains only its own weeks.
3. **QB timeline check:** Dropbacks by passer and week confirm Jones started Weeks 1–13 and left Week 14 after 7 dropbacks.
4. **Opponent ratings:** Each defense is rated by its full-season average early-down EPA allowed, counting only games against other teams, then ranked 1–32 with a SQL window function. Each Colts game is compared with its opponent's rating: `EPA over expected = Colts EPA − opponent's EPA allowed`.
5. **Success rate definition:** A play is successful if it gains ≥4 yards on 1st down, or ≥50% of yards-to-go on 2nd down.
6. **Run gap analysis:** Runs to the middle are classed as inside runs and runs to the left or right as outside runs. Plays with no recorded location are excluded.
7. **Visualization:** Seaborn/Matplotlib weekly chart of Colts EPA against each opponent's rating, grouped bar charts by down and play type, and a run/pass ratio heatmap.

## Key Findings

| Segment | Avg opponent defense rank (1 = best) | Colts EPA/play | Colts vs. expected | Success rate |
|---|---|---|---|---|
| Weeks 1–8 | 16.6 | +0.202 | +0.189 | 57.8% |
| Weeks 9–13 | 11.3 | +0.031 | +0.077 | 56.1% |
| Weeks 14–18 | 9.6 | −0.184 | −0.140 | 42.2% |

- **The schedule did get tougher.** Opponents went from middle-of-the-league defenses to top-10-caliber ones.
- **But the hot start wasn't a soft schedule.** Early opponents were average, and the Colts beat what those defenses usually allowed by +0.189 EPA per play, including Denver (#2) and the Chargers (#4).
- **Schedule explains about a third of the Weeks 9–13 decline.** After adjusting for opponents, the offense still slipped from +0.189 to +0.077 over expected.
- **The injury explains the collapse.** Weeks 9–13 and 14–18 had equally tough opponents, yet the Colts fell from +0.031 to −0.184 EPA per play once the backups took over.
- **The pre-injury slide was in the passing game.** 1st-down pass EPA fell from +0.292 to +0.107 and 2nd-down pass EPA from +0.186 to −0.196, while 2nd-down runs and inside runs improved.
- **Play-calling moved toward the weaker option.** The run/pass ratio dropped on both 1st down (0.93 → 0.80) and 2nd down (0.77 → 0.65) in Weeks 9–13, meaning more passing even as the pass game faded.

**Bottom line:** my hypothesis was partly right. The schedule got harder and that cost the offense some efficiency, but the early success was real, and the collapse lines up with the QB injury, not the schedule.

## Tech Stack

- **Python:** pandas, nflreadpy
- **SQL:** SQLite for filtering, segmentation, aggregation, and window-function rankings
- **Visualization:** Seaborn, Matplotlib

## Setup

```bash
pip install -r requirements.txt
python ingest.py          # builds nfl_data.db (2023–2025 play-by-play)
jupyter notebook analysis.ipynb
```

`analysis.html` is a rendered copy of the notebook with all outputs.

## Notes and Limitations

Weeks 9–13 is only four games (187 early-down plays) and Weeks 14–18 is five, so single games move segment averages a lot. The manageable 2nd-down splits in the notebook are 15–27 plays per group. Defensive ratings use early-down EPA only. Jones was reportedly playing through injury in the weeks before Week 14, which could explain part of the pre-injury passing decline, but the data doesn't capture injury status play by play.

Future extensions: 3rd down conversion analysis, red zone efficiency, pass depth/location splits, and comparing the Leonard and Rivers starts.
