# Trip Audio Companion

**Generate a 60+ minute educational audio tour for any road trip destination** -- geology, plants, wildlife, history, and local tips -- narrated by a warm AI voice.

No API keys. No subscriptions. Microsoft's neural TTS voices are free.

---

## What you get

- A **single MP3 file**, ready to play in your car (60-90 minutes)
- A **companion webpage** with species cards, trail info, and restaurant picks
- Content shaped to **your interests** (geology lover? historian? birder? all of the above?)
- Content shaped to **your travelers** (each person's priorities woven throughout)

### Example output: Colorado Hot Springs Road Trip

> *"Glenwood Canyon is one of the most dramatic geological formations in North America. The Colorado River has spent the last five to six million years sawing through rock that formed nearly two billion years ago -- Precambrian granite, some of the oldest exposed stone in Colorado..."*

Generated for a couple where one traveler is obsessed with geology and the other loves altitude physiology, horse history, and local restaurants. Sixty-eight minutes of custom audio, voice-narrated, plays like a documentary made specifically for their drive.

---

## What it covers

Choose any combination of 51 built-in interest categories across 10 groups:

| Group | Interests include |
|---|---|
| **Nature & Science** | Geology, Plants & Wildflowers, Birds, Mammals & Wildlife, Rivers & Lakes, Astronomy, Altitude Physiology, Weather & Climate |
| **History & Culture** | Native American History, Mining & Industrial, Railroad History, Ghost Towns, Military History, Architecture, Literary History |
| **Food & Drink** | Local Restaurants, Craft Breweries & Wineries, Farm-to-Table, Wild Food Foraging |
| **Adventure & Sports** | Hiking Trails, Whitewater & Extreme Sports, Mountain Biking, Fly Fishing, Equestrian |
| **Wellness** | Hot Springs & Geothermal, Historic Cemeteries, Spiritual Sites |
| **Photography** | Photography Spots & Golden Hour, Scenic Drives, Waterfalls, Covered Bridges |
| **Quirky & Offbeat** | Roadside Attractions, Folklore & Cryptids, World Records & Superlatives |
| **Science & Tech** | Space Exploration, Energy Infrastructure, Conservation History |
| **Family** | Family-Friendly Stops, Accessible Travel |
| **Pets** | Dog-Friendly Stops |

Add unlimited custom interests in free text: `"narrow gauge railroads"`, `"bat colonies"`, `"Civil War skirmishes"` -- anything.

---

## Quick Start

**You need:** Python 3.10+, ffmpeg, and about 10 minutes of setup.

### 1. Install Python

Download from [python.org](https://www.python.org/downloads/) -- version 3.10 or higher. During install on Windows, check "Add Python to PATH."

### 2. Get the code

```bash
git clone https://github.com/annettethompson/trip-audio-companion.git
cd trip-audio-companion
```

Or download the ZIP from the green "Code" button on GitHub.

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install ffmpeg

ffmpeg is the audio engine that assembles your chapters into a final MP3.

- **Windows:** Download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html), extract, add the `bin/` folder to your PATH. Or use: `winget install ffmpeg`
- **Mac:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo dnf install ffmpeg` (Fedora)

### 5. Create your trip config

```bash
cp config/trip-template.yaml config/my-trip.yaml
```

Open `config/my-trip.yaml` in any text editor. Fill in your destinations, traveler names, and interests. Every field has a comment explaining what it does.

### 6. Generate your script

```bash
python -m src.main generate-script --config config/my-trip.yaml
```

This creates chapter `.md` files in `outputs/scripts/`.

### 7. Synthesize the audio

```bash
python scripts/synthesize_episode.py --config config/my-trip.yaml
```

Your MP3 appears in `outputs/final_mp3s/`.

### 8. Play it

Load the MP3 into your phone, a Bluetooth speaker, or your car's audio system before you leave. Press play when you hit the road.

---

## Voices

The default narrator is **Ryan** (`en-GB-RyanNeural`) -- warm, documentary-quality British male, ideal for road trip audio.

**Browse all 47 voices:** see [VOICES.md](VOICES.md)

**Preview any voice before committing:**

```bash
edge-tts --voice en-GB-RyanNeural --text "Welcome to your road trip." --write-media preview.mp3
```

**Change your voice** in `config/voice.yaml`:

```yaml
edge_tts:
  voice: en-US-JennyNeural   # any ID from VOICES.md
```

Popular picks:

| Voice ID | Description |
|---|---|
| `en-GB-RyanNeural` | British male -- warm, documentary (default) |
| `en-US-JennyNeural` | American female -- friendly, all-rounder |
| `en-US-GuyNeural` | American male -- great for science segments |
| `en-IE-ConnorNeural` | Irish male -- warm storytelling quality |
| `en-AU-NatashaNeural` | Australian female -- clear and professional |
| `en-GB-SoniaNeural` | British female -- authoritative and clear |

> No Scottish voice exists in edge-tts or Microsoft's standard Neural TTS catalog. `en-GB-RyanNeural` is the closest available British accent. See [VOICES.md](VOICES.md) for details.

---

## Customizing Your Trip

Everything lives in your trip YAML file. The key sections:

**`travelers`** -- who's listening. Add name, background, and interests per person. The script generator weights content based on each traveler's profile, so a couple where one person loves geology and the other loves history both get what they came for.

**`interests`** -- pick from the 51 built-in categories (see `config/interests_catalog.yaml`) or add free-text custom interests.

**`route`** -- your destinations in order, with dates and notes. The generator creates one chapter per destination.

**`episode_structure`** -- which sections appear in every chapter (geology open, history, local tips, etc.)

**`target_minutes`** -- default 65. Minimum is 60. You can go up to 90 for an extended deep dive.

See [SETUP.md](SETUP.md) for a complete walkthrough.

---

## Examples

**Colorado Hot Springs Road Trip** (`config/trip.yaml`) -- 11 destinations, 10 days, two travelers. One is a geology enthusiast, the other focuses on altitude physiology, horse history, and local restaurants. Chapters cover Steamboat Springs, Glenwood Canyon, Ridgway, Durango, Pagosa Springs, the San Luis Valley, and Leadville. Each episode runs 65+ minutes.

---

## Coming Soon: Web UI

A browser-based interface where you fill out a form instead of editing YAML. No terminal required.

If you want to help build it, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Credits

- **TTS engine:** [edge-tts](https://github.com/rany2/edge-tts) -- Microsoft Neural TTS voices, accessed free via the Edge browser speech API. No API key required.
- **Audio assembly:** [ffmpeg](https://ffmpeg.org/) + [pydub](https://github.com/jiaaro/pydub)
- **Script generation:** OpenRouter (configurable -- see `.env.example`)

---

## License

MIT -- use it, fork it, build on it.
