# 2025 Colts Offense: Soft Schedule or Real Decline?

A data analysis project testing why the Indianapolis Colts' 2025 offense fell off after a hot start. My hypothesis: the early success came from facing easier defenses, and the offense regressed once the schedule got tougher. Two follow-up questions: how much of the late-season collapse comes from starting QB Daniel Jones' Week 14 injury instead, and did the play-calling keep favoring passes even when runs were working better?

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
- In Weeks 9–13, did the play-calling keep favoring passes even when runs were more effective?

## Methodology

1. **Data source:** Play-by-play data pulled with [`nflreadpy`](https://github.com/nflverse/nflreadpy) and loaded into a local SQLite database (`ingest.py`).
2. **Segmentation:** SQL filters to Colts 2025 regular-season run/pass plays on 1st and 2nd down and tags each play with its segment. One shared segment definition with explicit week bounds is used everywhere, and a sanity check confirms each segment contains only its own weeks.
3. **Called plays:** Plays are classified by what was called, not how they ended. Every dropback (including sacks and scrambles) counts as a pass, and only designed runs count as runs. This matters because the raw data labels QB scrambles as runs.
4. **QB timeline check:** Pass plays by passer and week confirm Jones started Weeks 1–13 and left Week 14 after 7 pass plays.
5. **Opponent ratings:** Each defense is rated by its full-season average early-down EPA allowed, counting only games against other teams, then ranked 1–32 with a SQL window function. Each Colts game is compared with its opponent's rating: `EPA over expected = Colts EPA − opponent's EPA allowed`.
6. **Play-calling test:** Early downs are split into 1st down, 2nd & short (≤6 yards), and 2nd & long (7+). In each situation, called runs are compared with called passes and with league-wide averages, and pass share is tracked across segments. A bootstrap (10,000 resamples) measures how confident the 2nd-down run vs. pass gap is.
7. **Success rate definition:** A play is successful if it gains ≥4 yards on 1st down, or ≥50% of yards-to-go on 2nd down.
8. **Run gap analysis:** Designed runs to the middle are classed as inside runs and runs to the left or right as outside runs. Plays with no recorded location are excluded.
9. **Visualization:** Seaborn/Matplotlib weekly chart of Colts EPA against each opponent's rating, grouped bar charts by down and play call, and a run/pass ratio heatmap.

## Key Findings

| Segment | Avg opponent defense rank (1 = best) | Colts EPA/play (avg of games) | Colts vs. expected | Success rate |
|---|---|---|---|---|
| Weeks 1–8 | 16.6 | +0.202 | +0.189 | 57.8% |
| Weeks 9–13 | 11.3 | +0.031 | +0.077 | 56.1% |
| Weeks 14–18 | 9.6 | −0.184 | −0.140 | 42.2% |

**Schedule and injury**
- **The schedule did get tougher.** Opponents went from middle-of-the-league defenses to defenses ranked around 10th on average.
- **But the hot start wasn't a soft schedule.** Early opponents were league-average, and the Colts beat what those defenses usually allowed by +0.189 EPA per play, including Denver (#2) and the Chargers (#4).
- **Schedule explains about a third of the Weeks 9–13 decline.** After adjusting for opponents, the offense still slipped from +0.189 to +0.077 over expected.
- **The injury explains the collapse.** Weeks 9–13 and 14–18 had equally tough opponents, yet the Colts fell from +0.031 to −0.184 EPA per play once the backups took over.

**What changed in Weeks 9–13**
- **The biggest slide was in the 2nd-down passing game.** On 1st down, both play types slipped (passes +0.296 → +0.104, designed runs +0.104 → −0.029). On 2nd down they split apart: pass EPA fell from +0.191 to −0.129 while designed runs improved from +0.206 to +0.306.
- **On 2nd down, the play-calling leaned toward the weaker option.** On 2nd & short, runs averaged +0.270 EPA and passes −0.535, yet the pass share rose from 27.9% to 38.1%. Across all 2nd downs, runs averaged +0.306 and passes −0.129, while the run/pass ratio fell from 0.72 to 0.53.
- **On 1st down, passing more was the right call.** Passes still beat runs (+0.104 vs −0.029), matching the league-wide pattern, so the small rise in 1st-down pass share (55.0% → 57.5%) was reasonable.
- **Confidence:** in a bootstrap of 2nd-down plays, runs came out ahead in 90% of resamples. The 95% range for the gap still includes zero, so this is a strong signal from a small sample, not proof.

**Bottom line:** my schedule hypothesis was partly right. The schedule got harder and that cost the offense some efficiency, but the early success was real, and the collapse lines up with the QB injury, not the schedule. Before the injury, the play-calling kept leaning on the pass on 2nd down even though runs were working better.

## Tech Stack

- **Python:** pandas, NumPy, nflreadpy
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

Weeks 9–13 is only four games (187 early-down plays) and Weeks 14–18 is five, so single games move segment averages a lot. In Weeks 9–13, 2nd & short has only 26 runs and 16 passes, and there were only 2 designed runs on 2nd & long in Weeks 9–13, so that situation can't be judged. Defensive ratings use early-down EPA only. Jones was reportedly playing through injury in the weeks before Week 14, which could explain part of the pre-injury passing decline, but the data doesn't capture injury status play by play.

Future extensions: 3rd down conversion analysis, red zone efficiency, pass depth/location splits, and comparing the Leonard and Rivers starts.
