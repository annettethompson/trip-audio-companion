# Roadmap

## Goal
Complete all 9 days of the Colorado road trip audio companion, publish every episode to annettethompson.com/trip/[slug]/, and then generalize the pipeline for open-source release and a NotTooOldForAI case study.

## Near-term next steps
- Audit which days (7: valley-view, 8: mt-princeton, 9: leadville) still need scripts written
- Write missing day scripts following the geology-word-budget rules (20 min max at 137.75 WPM)
- Run synthesize_*.py for each remaining day to produce MP3 segments and final episode
- Build and deploy companion pages for any days not yet live on annettethompson.com/trip/
- Verify all 9 companion pages load correctly with sticky audio player

## MVP definition
All 9 episodes have:
- Complete script set (00_intro through final chapter)
- Synthesized final episode MP3 uploaded to GitHub release v1.0.0
- Companion page live at annettethompson.com/trip/[slug]/ with chapter cards and image credits

## Future improvements
- Generalize the pipeline: abstract trip.yaml / route data so any road trip can be scripted, not just this one
- Open-source the engine on GitHub (planned post-MVP)
- NotTooOldForAI case study article: "How I built a personal travel audio guide with AI at 57"
- Add GPS-triggered playback (location-aware, plays chapter when passing the landmark)
- Support multiple voice options beyond en-GB-RyanNeural

## Open questions
- Which days 7-9 still need scripts? Need to audit outputs/ folder more precisely
- Is the trip happening now or still upcoming? (determines urgency)
- Should Days 1-5 companion pages all be verified live before moving to generalization?

## Maintenance notes
- Dependencies: edge-tts, pydub, Pillow, requests (for Wikimedia downloads)
- Synthesis scripts pattern: scripts/synthesize_[slug].py
- Chime file: outputs/audio/chime.mp3 (must exist before any synthesis)
- Image downloads: 8-10 sec delays between Wikimedia API calls
- GitHub release upload: gh release upload v1.0.0 outputs/final_mp3s/[slug]_episode.mp3 --repo annettethompson/trip-audio-companion --clobber
- Companion page push: cd AnnetteThompson, git add -A, git commit, git push origin main
- Cloudflare Pages auto-deploys on main push (1-2 min)
