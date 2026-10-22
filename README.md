# 2025 Colts Situational Efficiency Audit: Testing the QB-Injury Narrative

A data analysis project testing the popular explanation for the Indianapolis Colts' late-2025 offensive decline, which blames starting quarterback Daniel Jones' Week 14 injury, against play-by-play data.

## Overview

The Colts' offensive struggles late in the 2025 season are commonly attributed to Jones' injury. This project evaluates the Colts' early-down (1st and 2nd down) offense across three segments of the regular season to find out *when* the offense actually broke down, and where:

| Segment | Weeks | Starting QB |
|---|---|---|
| Early | 1–8 | Daniel Jones |
| Late | 9–13 | Daniel Jones |
| Post-injury | 14–18 | Riley Leonard / Philip Rivers |

The analysis uses **Expected Points Added (EPA)** and **success rate** as the core efficiency metrics, and adjusts each game for the opponent's defensive strength to rule out "tougher schedule" as an alternate explanation.

## Key Questions

- Did early-down efficiency decline before Week 14, while Jones was still healthy?
- How does any pre-injury decline compare with performance after the injury?
- Did run/pass play-calling shift between segments, and did it follow what was working?
- Is any decline explained by facing stronger defenses, or does it persist after adjusting for opponent strength?

## Methodology

1. **Data source:** Play-by-play data pulled with [`nflreadpy`](https://github.com/nflverse/nflreadpy) and loaded into a local SQLite database (`ingest.py`).
2. **Querying:** SQL filters to Colts 2025 regular-season run/pass plays on 1st and 2nd down and tags each play with its segment. One shared segment definition with explicit week bounds is used everywhere, and a sanity check confirms each segment contains only its own weeks.
3. **QB timeline check:** Dropbacks by passer and week confirm Jones started Weeks 1–13 and left Week 14 after 7 dropbacks.
4. **Success rate definition:** A play is successful if it gains ≥4 yards on 1st down, or ≥50% of yards-to-go on 2nd down.
5. **Opponent adjustment:** For each defense, average early-down EPA allowed to every team *except* the Colts, computed separately per segment. Each Colts game is matched to its opponent's baseline for that segment, and `EPA over expected = Colts EPA − opponent's typical EPA allowed`.
6. **Run gap analysis:** Runs to the middle are classed as inside runs and runs to the left or right as outside runs. Plays with no recorded location are excluded.
7. **Visualization:** Seaborn/Matplotlib grouped bar charts, a run/pass ratio heatmap, and a weekly chart of Colts EPA against each opponent's baseline.

## Key Findings

| Segment | Early-down EPA/play | Success rate | Opponent-adjusted EPA |
|---|---|---|---|
| Weeks 1–8 | +0.205 | 57.8% | +0.217 |
| Weeks 9–13 | +0.036 | 56.1% | +0.087 |
| Weeks 14–18 | −0.191 | 42.2% | −0.155 |

- **There was a real slide before the injury, but not a collapse.** EPA fell sharply in Weeks 9–13 while success rate barely moved. The offense was still staying on schedule but lost its big plays and gave up more costly negative ones.
- **The collapse came after Week 14.** With the backups at QB, both EPA and success rate fell off a cliff. The injury narrative is mostly right about *when* the offense fell apart.
- **Schedule doesn't explain it.** Weeks 9–13 opponents were only slightly tougher than Weeks 1–8, and the decline persists after adjustment.
- **The pre-injury slide was in the passing game.** 1st-down pass EPA fell from +0.292 to +0.107 and 2nd-down pass EPA from +0.186 to −0.196. The run game held up: 2nd-down runs (+0.211 → +0.354) and inside runs (+0.059 → +0.231) both improved.
- **Play-calling moved toward the weaker option.** In Weeks 9–13 the run/pass ratio dropped on both 1st down (0.93 → 0.80) and 2nd down (0.77 → 0.65), meaning more passing even as the pass game faded. On manageable 2nd downs (≤6 yards to go), passes averaged −0.582 EPA against +0.266 for runs.

## Tech Stack

- **Python:** pandas, nflreadpy
- **SQL:** SQLite for filtering, segmentation, and aggregation
- **Visualization:** Seaborn, Matplotlib

## Setup

```bash
pip install -r requirements.txt
python ingest.py          # builds nfl_data.db (2023–2025 play-by-play)
jupyter notebook analysis.ipynb
```

`analysis.html` is a rendered copy of the notebook with all outputs.

## Notes and Limitations

Weeks 9–13 is only four games (187 early-down plays), and one game (Week 9 at Pittsburgh, −0.403 EPA) pulls that segment's average down noticeably. The manageable 2nd-down splits are 15–27 plays per group. Findings about the pre-injury passing slide and play-calling should be read as signals worth investigating, not proof. Jones was reportedly playing through injury in the weeks before Week 14, which could explain the passing decline, but the data doesn't capture injury status play by play.

Future extensions: 3rd down conversion analysis, red zone efficiency, pass depth/location splits, and comparing the Leonard and Rivers starts.
