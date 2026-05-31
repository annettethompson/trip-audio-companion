# Project Status

**Last meaningful work:**
- 2026-05-25 (Day 6 / Joyful Journey episode scripts + synthesis)
- Git history shows active commits through Day 4 (Durango), Day 3 (Ouray/MDH), Day 2 (Ridgway), and a bridge/trail addition. Day 6 (Joyful Journey) scripts and MP3 segments are fully present in outputs/.

**Current stage:** Active

**Project type:** App / Content

**Purpose:**
Generates location-aware audio companion episodes for Bob and Annette's Colorado road trip, with geology, history, and culture scripts synthesized to MP3 using edge-tts, then published to annettethompson.com/trip/[slug]/.

**Current state:**
- 9-day trip planned (Days 1-9): steamboat-springs, ridgway, ouray, durango, pagosa-springs, joyful-journey, valley-view, mt-princeton, leadville
- Day 6 (joyful-journey) has full script set (13 chapters, 00_intro through 12_come_back_for_this) plus synthesized MP3 segments and a final combined episode MP3
- Days 2-4 scripts exist (Ridgway, Ouray, Durango) based on git log
- Day 5 (pagosa-springs) has scripts (05_orvis_hot_springs, 05_southern_ute, etc.)
- scripts/synthesize_joyful_journey.py is the synthesis pipeline
- Companion pages must be built in AnnetteThompson project and pushed for each episode
- MP3s are uploaded to GitHub release v1.0.0 on annettethompson/trip-audio-companion
- Chime file (outputs/audio/chime.mp3) used between all chapters

**Next action:**
Determine which days (1, 7, 8, 9) still need scripts written and synthesized, then generate and publish their companion pages.

**Blockers:**
- Days 7-9 (valley-view, mt-princeton, leadville) may still need scripts written
- Companion page deployment requires AnnetteThompson project git push

**Priority:** High

**Staleness risk:** Low (active work 2026-05-25, trip likely imminent or ongoing)

**Notes for future Claude sessions:**
- Bob loves geology, history, horsemen, and has a 1923 connection (script ch. 11 is named "1923_moment")
- Voice: en-GB-RyanNeural (warm British male)
- Slug mapping in CLAUDE.md: Day 1=steamboat-springs, Day 2=ridgway, Day 3=ouray, Day 4=durango, Day 5=pagosa-springs, Day 6=joyful-journey, Day 7=valley-view, Day 8=mt-princeton, Day 9=leadville
- Companion page template: C:\Users\annet\ClaudeProjects\AnnetteThompson\public\trip\durango\index.html
- Geology word budget: 20 min max at 137.75 WPM per episode
- Wikimedia image downloads need 8-10 sec delays between requests to avoid 429s
- Future plans: open-source generalization post-MVP, NotTooOldForAI case study article
