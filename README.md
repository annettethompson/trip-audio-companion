# Trip Audio Companion

Generates 60+ minute educational MP3 audio episodes for road trips.

## Quick start

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your OpenRouter and Anthropic keys

# Create first episode
python -m src.main create-episode --trip config/trip.yaml --topic "Colorado Hot Springs Geology"

# Verify duration of any MP3
python -m src.main verify-duration outputs/final_mp3s/episode.mp3
```

## Choosing Your Voice

The default narrator is `en-GB-RyanNeural` — a warm, documentary-quality British male voice ideal for road-trip audio.

**Browse the full voice catalog** (47 English voices across 14 locales):
```
config/voices_catalog.yaml
```
Voices are organized by region (US, UK, Ireland, Australia, Canada, New Zealand, India, South Africa, and more) and gender, with style notes for each.

**List all voices available on your edge-tts install:**
```bash
python -m edge_tts --list-voices | grep "^en-"
```

**Preview any voice before committing:**
```bash
edge-tts --voice en-GB-RyanNeural --text "Welcome to your trip audio companion" --write-media preview.mp3
```
Swap `en-GB-RyanNeural` for any voice ID from the catalog — for example `en-IE-ConnorNeural`, `en-AU-NatashaNeural`, or `en-US-JennyNeural`.

**Change your voice** in `config/voice.yaml`:
```yaml
edge_tts:
  voice: en-US-JennyNeural   # replace with any catalog ID
```

> **Note on Scottish voices:** No dedicated Scottish locale exists in edge-tts or the standard Microsoft Neural TTS catalog as of 2026. `en-GB-RyanNeural` and `en-GB-ThomasNeural` are the closest available British accents.

---

## Rules

- Minimum episode duration: **60 minutes, no exceptions**
- Target: 65 minutes (buffer for TTS speed variation)
- No Wikipedia sources
- Every factual claim must be cited

## TTS

Default: `edge-tts` with `en-GB-RyanNeural` voice (free, no API key needed).
Optional: Azure AI Speech (set `AZURE_SPEECH_KEY` in `.env`).

## First episode

Colorado Hot Springs trip for Annette and Bob, May 2026.

## Roadmap: Open-Source Generalization

This project is designed for public release. Planned adaptations:

### Voice options
Users will choose from Microsoft neural voice samples:
- `en-GB-RyanNeural` — warm British male (current default)
- `en-US-JennyNeural` — friendly American female
- `en-US-AriaNeural` — professional American female
- `en-US-GuyNeural` — American male
- `en-AU-WilliamNeural` — Australian male
- `en-GB-SoniaNeural` — British female

### Duration options
- 30 min — summary episode
- 45 min — standard
- 60 min — full (current default minimum)
- 90 min — extended deep dive

### Interest categories (user-configurable)
Any combination of: geology, plants/botany, wildlife, history, art/architecture,
culinary/food, photography spots, hiking, extreme sports, genealogy, music history,
religious/spiritual sites, literary history, medical/wellness, astronomy

### Example trip configs (coming)
- `config/examples/colorado-hot-springs.yaml` (this project)
- `config/examples/california-coastal.yaml`
- `config/examples/appalachian-trail.yaml`
- `config/examples/national-parks-southwest.yaml`
- `config/examples/historical-cities-east-coast.yaml`
