# Setup Guide

Step-by-step instructions for non-coders. You do not need to know Python or the command line beyond copying and pasting the commands here.

**Time required:** About 10-15 minutes the first time.

---

## What you need before starting

- A computer running Windows, Mac, or Linux
- An internet connection (for the initial install)
- A text editor (Notepad works on Windows; TextEdit on Mac)

---

## Step 1: Install Python 3.10 or higher

Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest version.

**Windows:** Run the installer. On the first screen, check the box that says **"Add Python to PATH"** before clicking Install. This is easy to miss and important.

**Mac:** The installer from python.org works. Alternatively: `brew install python` if you use Homebrew.

**Linux:** Python is likely already installed. Check with `python3 --version`. If not: `sudo apt install python3 python3-pip`

**Verify it worked:**
Open a terminal (on Windows: search for "Command Prompt" or "PowerShell") and type:

```
python --version
```

You should see something like `Python 3.12.3`. Any version 3.10 or higher is fine.

---

## Step 2: Get the code

**Option A -- if you have git installed:**

```bash
git clone https://github.com/annettethompson/trip-audio-companion.git
cd trip-audio-companion
```

**Option B -- download as ZIP:**

1. Go to [github.com/annettethompson/trip-audio-companion](https://github.com/annettethompson/trip-audio-companion)
2. Click the green **Code** button
3. Click **Download ZIP**
4. Extract the ZIP file somewhere convenient (your Desktop is fine)
5. Open a terminal and navigate to the folder: `cd ~/Desktop/trip-audio-companion`

---

## Step 3: Install Python dependencies

In your terminal, make sure you're in the `trip-audio-companion` folder, then run:

```bash
pip install -r requirements.txt
```

This downloads and installs everything the project needs. It takes 1-3 minutes depending on your internet speed. You'll see a lot of text scroll by -- that's normal.

---

## Step 4: Install ffmpeg

ffmpeg is the audio engine that stitches your chapter files into a single MP3. It's free and open source.

**Windows:**

Option 1 (easiest -- Windows Package Manager):
```
winget install ffmpeg
```

Option 2 (manual):
1. Go to [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Under Windows, click the gyan.dev link and download the "release full" build
3. Extract the ZIP
4. Copy the `bin` folder contents somewhere permanent (e.g. `C:\ffmpeg\bin\`)
5. Add `C:\ffmpeg\bin\` to your PATH: search Windows for "Environment Variables", edit the PATH variable, add that folder

**Mac:**

```bash
brew install ffmpeg
```

If you don't have Homebrew: [brew.sh](https://brew.sh)

**Ubuntu/Debian Linux:**

```bash
sudo apt install ffmpeg
```

**Fedora/RHEL Linux:**

```bash
sudo dnf install ffmpeg
```

**Verify it worked:**

```
ffmpeg -version
```

You should see version information, not an error.

---

## Step 5: Copy the trip template

```bash
cp config/trip-template.yaml config/my-trip.yaml
```

On Windows (Command Prompt):

```
copy config\trip-template.yaml config\my-trip.yaml
```

---

## Step 6: Fill in your trip details

Open `config/my-trip.yaml` in a text editor. Every field has a comment (lines starting with `#`) explaining what it does.

The key sections to fill in:

**Trip name and dates:**
```yaml
trip_name: "Pacific Coast Highway Drive"
start_date: "2026-08-10"
end_date: "2026-08-17"
```

**Your travelers** (add as many as you like):
```yaml
travelers:
  - name: Sarah
    background: "Marine biologist, loves coastal ecology and tide pools"
    interests:
      - geology
      - birds
      - rivers_aquatic
```

**Your route:**
```yaml
route:
  origin: "San Francisco, CA"
  destinations:
    - date: "2026-08-10"
      city: "Monterey"
      notes: "Cannery Row, Point Lobos, kelp forests"
    - date: "2026-08-11"
      city: "Big Sur"
      notes: "Bixby Bridge, Pfeiffer Beach, McWay Falls"
```

**Interest IDs** come from `config/interests_catalog.yaml`. The available IDs are:
`geology`, `plants_botany`, `birds`, `mammals_wildlife`, `insects_butterflies`, `trees_forests`, `rivers_aquatic`, `astronomy`, `altitude_physiology`, `weather_climate`, `indigenous_history`, `mining_industrial`, `railroad_history`, `military_history`, `frontier_colonial`, `architecture_buildings`, `antique_vintage`, `art_galleries`, `literary_history`, `music_history`, `film_tv_locations`, `ghost_towns`, `local_restaurants`, `breweries_wineries`, `farm_food`, `coffee_cafes`, `foraging`, `hiking`, `extreme_sports`, `mountain_biking`, `water_sports`, `equestrian`, `winter_sports`, `fishing`, `hot_springs`, `religious_spiritual`, `wellness_meditation`, `cemetery_history`, `photography_spots`, `scenic_drives`, `covered_bridges`, `waterfalls`, `roadside_attractions`, `cryptids_paranormal`, `world_records`, `space_exploration`, `energy_infrastructure`, `conservation_environment`, `family_activities`, `accessible_travel`, `dog_friendly`

Or add anything you want in free text:
```yaml
custom_interests:
  - "Steinbeck's Cannery Row history"
  - "sea otter behavior and recovery"
  - "lighthouse architecture"
```

---

## Step 7: Generate your script

```bash
python -m src.main generate-script --config config/my-trip.yaml
```

This creates a set of chapter files in `outputs/scripts/`. The process takes a few minutes -- the generator is writing detailed educational content for each destination.

---

## Step 8: Synthesize the audio

```bash
python scripts/synthesize_episode.py --config config/my-trip.yaml
```

This sends each chapter to Microsoft's free neural TTS engine and assembles the results into a single MP3. Expect 5-15 minutes depending on episode length and your connection speed.

Your finished file appears in `outputs/final_mp3s/`.

---

## Step 9: Load it in your car

Transfer the MP3 to your phone and play it through your car's Bluetooth or aux input. A 65-minute episode is about 60-90 MB.

Options for getting it on your phone:
- AirDrop (Mac to iPhone)
- Google Drive or Dropbox -- upload from computer, download on phone
- USB cable -- the MP3 plays in any music app
- Email it to yourself if the file is under your email provider's attachment limit

---

## Troubleshooting

**"python is not recognized" (Windows):** Python wasn't added to PATH during install. Re-run the Python installer, choose "Modify", and check "Add Python to environment variables."

**"pip is not recognized":** Try `pip3` instead of `pip`. Or: `python -m pip install -r requirements.txt`

**"ffmpeg is not recognized":** ffmpeg isn't on your PATH. On Windows, verify the bin folder path and that it's in your Environment Variables. Restart your terminal after adding it.

**"No module named edge_tts":** Run `pip install edge-tts` to install it separately, then try the synthesis step again.

**The audio is too fast or too slow:** Edit `config/voice.yaml` and adjust the `rate` setting. Values like `"+10%"` speed up, `"-10%"` slows down.

**The episode is too short:** Increase `target_minutes` in your trip YAML and re-run both steps. The minimum is 60 minutes.

---

## What the output folder structure looks like

```
outputs/
  scripts/          <- Chapter .md files (the text before audio synthesis)
  audio_segments/   <- Individual chapter MP3s (intermediate files)
  final_mp3s/       <- Your finished episode (this is the file you want)
```

The `scripts/` and `audio_segments/` folders are intermediate -- you only need the final MP3 from `final_mp3s/`.
