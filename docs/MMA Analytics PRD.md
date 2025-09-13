# MVP PRD — UFC Video + Stats Analytics for Camp Prep (Local, Offline)

## 0) One-liner

A local, offline Jupyter workflow (RTX 3090) that (1) predicts pre-fight win probabilities from stats (with SHAP drivers), (2) ingests broadcast live commentary and post-fight pundit/YouTuber analysis (speech-to-text + NLP) as an additional analytic signal, and (3) mines UFC broadcast footage to surface coach-ready insights: **stance switching %, pressure time, top combos, top vulnerabilities (incl. high-guard vs low-guard exposure), dominant-position time**, plus **highlight clips**. It also infers **stance styles** (boxing vs kickboxing vs karate) and compares **success rates** across styles on historical data.

---

## 1) Goals & Non-Goals

### Goals (MVP)

1. **Stats predictor (pre-fight)**

   * Leak-free features + **betting odds**.
   * Metrics: **Accuracy ≥ 70%**, **Brier ≤ 0.20**.
   * **SHAP** explanations per matchup.

2. **Live commentary & pundit mining**

   * Ingest broadcast commentary audio and public post-fight pundit/YouTuber videos, transcribe (ASR), diarize speakers, and extract time-stamped claims and sentiment.
   * Correlate commentator claims with detected video events to surface validated vs unsupported commentary and to provide coach-ready quotes with clips.

3. **Video pattern miner (post-fight, offline)**

   * **Strike classes (initial):** **jab, cross, hook, uppercut, low kick, roundhouse kick (body), teep kick, head kick**.
   * **Action recognition:** n-gram combos and sequence patterns from strike timelines.
   * **Pose-lite signals:** stance labeling + **stance switching %**; motion-field–based **pressure time**.
   * **Grappling positions (coarse 4-class):** guard / side control / mount / back control.
   * **Vulnerabilities:** emphasis on **high-guard vs low-guard** exposure to specific strikes (esp. hooks/uppercuts/head kicks).
   * **Stance style inference:** classify fighters into **boxing / kickboxing / karate** style buckets and compute **win-rate by style** (overall and by matchup).
   * Export **2–6s** highlight clips for each detected pattern.

4. **Coach-facing Jupyter report**

   * One-click notebook producing visuals + embedded clips + CSV/JSON exports.

### Non-Goals (MVP)

* Real-time inference during events.
* Multi-view / physics-based 3D pose (single-camera UFC footage only).
* Fine-grained grappling techniques (sub types, specific takedown families) beyond the 4 coarse positions.

---

## 2) Users & Use Cases

* **Head coaches / analysts:** pre-camp scouting, post-fight breakdown, opponent dossiers.
* **Use cases:**

  * “Show me Volkanovski’s stance switching %, pressure map, top combos, and where his guard leaks vs hooks.”
  * “Across the roster, which **stance style** wins more often after controlling for age/reach/odds?”

---

## 3) Success Metrics (Acceptance)

### Stats model

* **Accuracy ≥ 70%**, **Brier ≤ 0.20**, AUC reported.
* SHAP top-5 drivers per matchup.

### Video models

* **Strike precision ≥ 85% for jab/cross/hook**; **≥ 75% precision for uppercut/low-kick/roundhouse/head-kick**.
* **Grappling positions ≥ 75% accuracy** (4-class).
* **Coach usefulness ≥ 4/5** (internal rubric after reviewing reports/clips).
* Report **stance switching %, pressure %, top-5 combos, top-5 vulnerabilities**, dominant-position time, with **clips**.

---

## 4) Data & Ingestion

### 4.1 Structured stats

* UFCStats scrape/CSV, merged with **closing odds**.
* Pre-fight features (leak-free): physical diffs; career + recent form; SLpM/SApM; acc/def; TD/sub metrics; odds features (implied prob, log-odds).
* Target: winner.

### 4.2 Video (UFC broadcast style)

* Local MP4s (Fight Pass / YouTube). Normalize to **25–30 FPS, 720/1080p**.
* Round-wise segmentation; audio track kept for cues and transcription.
* **Labeling budget:** **\~300–500 short clips** (active-learning prioritized). Everything else via **transfer learning + pseudo-labels**.

### 4.3 Broadcast commentary & external pundit data

* Keep and transcribe the broadcast audio track (speech-to-text / ASR) for every fight; store time-aligned transcripts and word-level timestamps.
* Ingest public post-fight pundit/YouTuber videos (where licensing allows) as an external data source: download, normalize audio, generate transcripts, and store video+transcript pairs under `data/commentary/`.
* Speaker diarization to separate ring announcers, commentators, analysts, and crowd noise.
* Derived artifacts: timestamped "claims", sentiment, topical tags, and ranked claims by confidence and repetition across pundits.
* Use pundit transcripts as weak labels / features for pattern discovery and coach-facing summarization.

---

## 5) Video Signals & Algorithms

### 5.1 Strike classification (7 classes)

* **Backbone:** **VideoMAE-S** (ViT-Small) fine-tuned on a seed set (public boxing/kick clips) → adapt on UFC pseudo-labels + your 300–500 curated clips.
* **Windows:** 32–64 frames; sliding inference; NMS to de-duplicate.
* **Left/Right handling:** orientation normalization + horizontal-flip augmentation.
* **Outputs:** per-strike timestamps, confidence.

### 5.2 Action recognition (combos & sequences)

* Build strike **n-grams** (len 2–4); rank by frequency and on-target rate.
* Optional temporal encoder (TCN/Transformer) for named patterns (e.g., “1-2-low kick”).
* **Vulnerabilities:** conditional patterns **opponent→fighter** (e.g., “gets hooked when guard is low,” “eats head kick off southpaw switch”). Rank by conditional P(strike lands | context).

### 5.3 Pose-lite stance & switching

* **Keypoints:** lightweight MMPose/MediaPipe (shoulders, hips, wrists, head).
* **Stance per frame:** derive by lead-hand/lead-foot geometry + strike handedness; median filter.
* **Switching %:** count stable stance segments and transitions / minute.

### 5.4 Pressure time

* **Tracking:** per-fighter bboxes (ByteTrack/DeepSORT).
* **Center/fence:** octagon ellipse fit; compute territory control & forward velocity vs opponent.
* **Pressure definition:** (advancing velocity + center dominance + opponent near fence) > threshold.
* **Output:** % time pressuring / retreating; round splits; ring-map heat.

### 5.5 Grappling positions (4-class)

* **Features:** pose keypoints of both fighters + frame crops → small CNN+MLP; temporal smoothing (HMM/TCN).
* **Output:** position segments, durations; transitions per round.

### 5.6 Guard height & vulnerability (high-guard vs low-guard)

* **Guard metric:** wrist/forearm y-level relative to chin/temple keypoints; forearm angle vs vertical; per-frame classification (**high / mid / low**) with hysteresis.
* **Stability:** temporal smoothing; ignore during active punching frames.
* **Vulnerability mining:** correlate **guard state** with **landed strike types** (esp. hooks/uppercuts/head kicks).

  * e.g., P(hook lands | guard=low within −400..+200 ms window).
  * Produce **Top-5 vulnerabilities** with effect sizes + clips.

### 5.7 Stance style inference (boxing vs kickboxing vs karate)

* **Feature set (per fighter):**

  * **Torso yaw** (side-on vs square), average **distance** to opponent, **bounce cadence** (vertical oscillation), **kick ratio** (kicks / total strikes), **guard height distribution**, **stance switching rate**, **combo profile** (straight-dominant vs kick-heavy), **pressure profile**.
* **Classifier:** start with **semi-supervised clustering** (HDBSCAN/K-Means on standardized features), then small supervised head using a few hand-labeled exemplars per style (seed set you approve).
* **Outputs:** per-fighter style probabilities; **style vs win-rate** tables overall, by weight class, and by **style-vs-style** matchup.

### 5.8 Commentary & post-fight analysis mining

* **ASR & diarization:** run a robust speech-to-text (e.g., Whisper/local transformer ASR) and speaker diarization (pyannote/speechbrain) to produce time-aligned transcripts with speaker labels and confidence scores.
* **Claim extraction:** apply NLP (NER + relation extraction + rule-based patterns) and transformer classifiers to pull out short "claims" or observations (e.g., "opponent struggles vs overhand left", "fights better off pressure").
* **Alignment:** align extracted claims to detected video events (strikes, guard drops, transitions) using the transcript timestamps to validate or refute claims within ±1s windows and rate claim support.
* **Aggregation:** rank claims by frequency, speaker authority, and cross-source corroboration (broadcast commentators vs YouTubers) to surface coach-useful insights and suspicious/misleading claims.
* **Use cases:** auto-generate a "commentary timeline" that shows what commentators said at each key video event, provide quick links to the clip and the original pundit timestamp, and surface consensus vs contested narratives.

---

## 6) Evaluation

### 6.1 Stats model

* Time-aware rolling CV; hold-out = most recent year.
* Report Accuracy, Brier, AUC, calibration curves; **with/without odds**; SHAP plots.

### 6.2 Video models

* Split **by fight**, no leakage of clips.
* **Strikes:** per-class P/R/F1; targets: **≥85% precision** (jab/cross/hook) and **≥75% precision** (uppercut/low/roundhouse/head-kick).
* **Grappling 4-class:** accuracy ≥ 75%; segment IoU on a small hand-labeled subset.
* **Guard/vulnerability:** sanity tests (precision of hook/uppercut/head-kick events around low-guard windows), plus coach review.
* **Stance styles:** silhouette score for clusters; confusion (if supervised) on seed set; **success analysis**: win rate by style controlling for confounders.

### 6.3 Commentary & ASR evaluation

* **ASR quality:** report WER (word error rate) on a held-out set of broadcast transcripts and YouTuber transcripts; target WER ≤ 10–15% for broadcast audio (clean feed) and ≤ 20% for noisy sources.
* **Diarization:** speaker-attribution accuracy for primary commentators vs other speakers.
* **Claim extraction:** precision/recall for extracted claims on a small hand-labeled set of pundit statements.
* **Alignment accuracy:** percentage of claims correctly time-aligned to detected video events within a tolerance window (e.g., ±1s).

---

## 7) Explainability & Reporting (Jupyter)

**Inputs:** fighter names or fight IDs + local video paths.
**Outputs (sections):**

1. **Pre-fight prediction:** win prob; SHAP top-5; odds comparison.
2. **Commentary & pundit insights:**

   * **Commentary timeline:** time-aligned transcripts and speaker labels, headline pundit claims, claim support/conflict flags, and links to original pundit timestamps with clips.
   * **Pundit consensus view:** aggregated sentiment and top-5 agreed claims across broadcasters and YouTubers for the fight.

3. **Video insights:**

   * **Stance switching %** timeline.
   * **Pressure %** + ring heatmap.
   * **Top-5 combos** (freq + success) **with clips**.
   * **Top-5 vulnerabilities** (esp. guard-linked) **with clips**.
   * **Dominant positions** bars per round + clips.
   * **Guard profile** (time high/mid/low), **strike-on-guard** matrix (e.g., hooks vs guard state).

4. **Stance style analysis:** style probabilities; **win-rate by style** (global & by division); **style-vs-style** table.

5. **Exports:** CSV (events, features), JSON (patterns), MP4/WebM clips folder, per-fight transcripts (SRT/JSON), claim lists (CSV/JSON), and a `commentary_clips/` folder with short video segments paired with the original commentator audio.

---

## 8) Engineering Plan (3090-friendly)

* **Strike model:** VideoMAE-S, AMP, bs=8–16, clip 32–64, lr warmup+cosine; train on mixed source (public → UFC pseudo-labels) + **300–500** curated clips via **active learning** (uncertainty sampling).
* **Guard/stance/pressure:** fast pose + tracking (CPU/GPU light), vectorized post-processing.
* **Grappling 4-class:** start from BJJ positions data (domain adapt), then fine-tune with \~100–200 UFC frames hand-labeled.
* **Style classifier:** feature pipeline + clustering; small supervised head after you bless seed exemplars.
* **Clips:** ffmpeg-python to cut 2–6s around events; dedupe near-duplicates.

* **Commentary stack:** local ASR (Whisper-large-v2 or a comparable on-device model configured for batch inference), speaker diarization (pyannote), and an NLP pipeline (transformers) for claim extraction, sentiment, and topic tagging. Store transcripts with timestamps and link to video event indices.
* **YouTuber ingestion:** optional pipeline to fetch public post-fight analysis videos, transcribe, and extract claims; use as weak supervision for claim ranking and for stylistic analysis of pundit commentary.

---

## 9) Repository Layout

```
repo/
  data/ (stats_raw, stats_proc, videos_raw, videos_proc, clips)
  notebooks/
    01_stats_dataset.ipynb
    02_train_stats_model.ipynb
    03_video_prep_clips.ipynb
    04_train_strike_model.ipynb
    05_guard_stance_pressure.ipynb
    06_grappling_positions.ipynb
    07_style_inference.ipynb
    08_report_matchup.ipynb   <-- MAIN
    09_commentary_mining.ipynb
    10_youtuber_analysis.ipynb
  src/
    stats_pipeline/ models_stats/
    video_io/ video_models/
    analytics/ (stance, pressure, combos, vulnerabilities, style)
    commentary/ (asr, diarize, claims)
    viz/
  models/ (stats, strike, grappling, style)
  data/commentary/ (transcripts_raw, transcripts_proc, pundit_videos)
  docs/ (README, demo_deck)
  environment.yml
```

**Key deps:** pytorch + timm, xgboost/lightgbm, scikit-learn, shap, mmpose/mediapipe, opencv, ffmpeg-python, numpy/pandas, matplotlib/plotly, mmcv/mmtracking (optional), moviepy, pyannote-audio (for diarization), transformers (for NLP/claim extraction), speechbrain (ASR alternative).

---

## 10) Risks & Mitigations

* **Overlap in kick taxonomy (low vs roundhouse vs head):** define **mutually exclusive labels** by target region + trajectory; prioritize precision on low/head; body roundhouse may start lower precision—improve via more exemplars.
* **Guard ambiguity during exchanges:** mask frames ±N around punches thrown by that fighter; use forearm angle + wrist-to-chin height; apply temporal hysteresis.
* **Left/right confusion:** normalize by opponent bearing; symmetric augmentation.
* **Style inference bias:** control for confounders (age/reach/odds) via logistic regression when reporting **style success**; present raw and adjusted win rates.
* **Label budget constraint:** active learning + curriculum (start with jab/cross/hook; add kicks in passes).

* **Commentary ethics & privacy:** Ensure compliance with fair use and copyright laws when ingesting YouTuber/post-fight videos; anonymize speaker data if redistributing transcripts; flag low-confidence ASR regions as "uncertain" to avoid misleading claims.

---

## 11) Showcase: Holloway vs Volkanovski

* Run full report for I, II, III.
* Emphasize: **stance switching**, **pressure**, **combo evolution**, and **guard-linked vulnerabilities** (esp. hooks/head kicks).
* Include side-by-side clips per bout to illustrate tactical shifts.

---

## 12) Next Steps (post-MVP)

* Add **method-of-victory** model; expand kick/ elbow/ knee taxonomy; robustness to camera zoom/cuts; optional multi-view capture for gym footage; finer grappling (takedowns/submissions).

---
