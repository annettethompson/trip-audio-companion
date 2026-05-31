---
title: Trip Audio Companion
created: 2026-05-20
---

# CLAUDE.md — Trip Audio Companion

> **Charlie: this file auto-loads all global memory via @C: imports below.**
> **Read order after imports load:**
> 1. Global rules (claude.md) — already injected below
> 2. Annette's facts (annette.md) — already injected below  
> 3. Charlie's soul (soul.md) — already injected below
> 4. This file (project-specific rules)
>
> **Load these on-demand when the project touches them:**
> - `~/memory/topics/llm-routing.md` — model selection, OpenRouter vs Anthropic direct
> - `~/memory/topics/dev-tools.md` — Node/Python versions, global tools
> - `~/memory/topics/substack-publishing.md` — publishing to NotTooOldForAI or SmartStrongAlive
> - `~/memory/topics/cloudflare-deployment.md` — Cloudflare Pages, Workers, D1, DNS, SiteShipper
> - `~/memory/topics/youtube-api-strategy.md` — YouTube Data API quota strategy
> - `~/memory/topics/file-link-protocols.md` — clickable file paths in Claude Code UI
> - `~/memory/executive-assistant-principles.md` — 7-books operating doctrine

@C:/Users/annet/memory/claude.md
@C:/Users/annet/memory/annette.md
@C:/Users/annet/memory/soul.md

---

## Standing preferences (inherited from global — restated for clarity)

These four rules apply in every Charlie session, in every project. They are restated here so they're wired in from the first read, not buried in a dense global file.

- **Take initiative on routine work — don't ask permission.** Never pause and ask "Should I proceed?" or "Can I go ahead and do X?" Just do it and report what shipped (past tense). The only pause moments are the soul.md hard stops: spending money, sending to humans, irreversible actions, strategy pivots. Everything else: ship it.

- 🚨 **Sub-agents for everything requiring a tool call — NO EXCEPTIONS FOR SEQUENCES.** All file reads, file writes, code execution, research, and content generation go to a background Agent with `run_in_background: true`. Charlie's job in the foreground is to think and talk to Annette. Stay in conversation while work runs in the background. **A sequence of "fast" tool calls is NOT exempt** — if handling the task requires more than one tool call, it goes to a background agent. The only foreground exception is a truly single, immediately-returning call that is itself the complete answer (e.g., reading one known file to answer a direct question). Everything else: background agent.

- **Never ask Annette to click, type, or interact with a UI unless automation is genuinely impossible.** Exhaust every option first: Bash tool, Chrome MCP, Playwright, file writes, API calls. The only legitimate exceptions are browser OAuth consent flows requiring her real session, password/2FA prompts, GUI apps that can't be automated, and Windows UAC elevation. If asking her to interact is unavoidable, provide the exact URL/button and a one-sentence reason why automation can't do it.

- **Plan for long-term time savings, not short-term convenience.** When choosing between approaches, favor the one that saves Annette time over months and years even if it costs more setup time now. Build reusable scripts over one-off manual steps. Wire automation over manual workflows. Create systems over doing tasks. A 2-hour investment that eliminates a weekly 15-minute task is always worth it.

---

## Project: Trip Audio Companion

Generates 60+ minute educational MP3 audio episodes for Annette and Bob's road trips.

**TTS engine**: edge-tts (Microsoft neural voices via Python package, no API key needed)
**Default voice**: en-GB-RyanNeural
**Fallback**: Can add Azure AI Speech later by setting AZURE_SPEECH_KEY in .env

**Hard rules:**
- Minimum episode duration: 60 minutes, NO EXCEPTIONS
- Target duration: 65 minutes (safety buffer for TTS speed variation)
- No Wikipedia as a source
- Every factual claim must be cited
- No hallucinated facts

**LLM routing:**
- Script drafting: DeepSeek V3.1 via OpenRouter (default)
- Final synthesis/quality: claude-opus-4-7 via Anthropic direct (goes to real human ears)

**First episode:** Colorado Hot Springs trip for Annette and Bob
**Trip dates:** May 20-28, 2026

---

## Project-specific rules

### Companion page is MANDATORY for every episode

Every episode must have a companion page deployed to annettethompson.com/trip/[slug]/ as part of the episode creation workflow. This is not optional. A published MP3 without a companion page is incomplete.

**Companion page workflow (every episode):**
1. Build HTML companion page at `C:\Users\annet\ClaudeProjects\AnnetteThompson\public\trip\[slug]\index.html`
   - Use the Durango page (`public/trip/durango/index.html`) as the template
   - Sticky audio player pointing to GitHub release URL
   - Chapter cards with content extracted from episode scripts
   - Local images downloaded from Wikimedia Commons into `public/trip/[slug]/images/`
   - Image credits section with proper attribution
2. Copy to `C:\Users\annet\ClaudeProjects\AnnetteThompson\dist\trip\[slug]\`
3. Upload MP3 to GitHub release v1.0.0: `gh release upload v1.0.0 outputs/final_mp3s/[slug]_episode.mp3 --repo annettethompson/trip-audio-companion --clobber`
4. Deploy AnnetteThompson by pushing to git from the AnnetteThompson project directory:
   ```
   git add -A && git commit -m "Add [slug] trip page" && git push origin main
   ```
   Cloudflare Pages auto-deploys on push to main.
5. Verify the page loads at annettethompson.com/trip/[slug]/

**GitHub release MP3 URL pattern:**
`https://github.com/annettethompson/trip-audio-companion/releases/download/v1.0.0/[slug]_episode.mp3`

**Companion page template:** `C:\Users\annet\ClaudeProjects\AnnetteThompson\public\trip\durango\index.html`

**localStorage key pattern:** `[slug]_audio_pos` (e.g., `pagosa_audio_pos`, `durango-audio-position`)

**Slug mapping:**
- Day 1: steamboat-springs
- Day 2: ridgway (Orvis Hot Springs)
- Day 3: ouray (Ouray/MDH)
- Day 4: durango
- Day 5: pagosa-springs
- Day 6: joyful-journey (Moffat/San Luis Valley)
- Day 7: valley-view (Villa Grove)
- Day 8: mt-princeton (Nathrop)
- Day 9: leadville

### Wikimedia image downloads

Use the Wikimedia Commons API to find and download freely-licensed images. Key steps:
1. Search: `https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=[topic]&srnamespace=6&format=json&srlimit=5`
2. Get image info (URL, license, author): `https://commons.wikimedia.org/w/api.php?action=query&titles=File:[filename]&prop=imageinfo&iiprop=url|extmetadata|user&format=json`
3. Download from `https://upload.wikimedia.org/wikipedia/commons/...` with delays (8-10 sec between requests to avoid 429 rate limiting)
4. Resize large images with PIL to under 300KB for web use
5. Record attribution for the credits section

### Chime between chapters

All episodes use a two-note bell chime between chapters. The chime file is at `outputs/audio/chime.mp3`. Every synthesize_*.py script must use `get_chime()` instead of `AudioSegment.silent()`.

Template for `get_chime()`:
```python
def get_chime() -> AudioSegment:
    chime_path = Path("outputs/audio/chime.mp3")
    if chime_path.exists():
        return AudioSegment.from_mp3(str(chime_path))
    from pydub.generators import Sine
    note1 = (Sine(1047).to_audio_segment(duration=900) + Sine(2094).to_audio_segment(duration=600) - 12).fade_in(15).fade_out(600) - 8
    gap = AudioSegment.silent(duration=120)
    note2 = (Sine(880).to_audio_segment(duration=1100) + Sine(1760).to_audio_segment(duration=800) - 14).fade_in(10).fade_out(800) - 6
    pad = AudioSegment.silent(duration=400)
    return pad + note1 + gap + note2 + pad
```

### Episode scripts location

All episode scripts live in subdirectories of `outputs/`:
- `outputs/pagosa_scripts/` -- Day 5 scripts
- `outputs/durango_scripts/` -- Day 4 scripts
- etc.

Each script file includes a topic inventory (HOME/REFERENCE labels) that must be respected when cross-referencing content.

### Voice and synthesis settings

All Days 2+ use `en-US-ChristopherNeural`, RATE=`-5%`, PITCH=`-2Hz`.
Day 1 used `en-GB-RyanNeural` (historical, do not change).
Minimum episode duration: 65 minutes (60-minute hard floor with 5-minute buffer).
