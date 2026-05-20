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
