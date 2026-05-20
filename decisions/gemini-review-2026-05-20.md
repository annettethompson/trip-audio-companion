# Gemini Adversarial Review — 2026-05-20

Scope: `src/main.py`, `src/trip_config.py`, `src/duration_guard.py`, `src/tts_microsoft.py`, `src/audio_stitcher.py`, `src/quality_check.py`

Note: Gemini CLI was unavailable in this environment. Review performed by direct code analysis of all 6 files in full. The 7 issues already found by Codex are excluded.

---

## New Critical Issues

- **`audio_stitcher.py` line 36-39 — ID3 tags silently lost on new files:** The `except` branch creates `tags = ID3()` (no path arg), then calls `tags.save(str(output_path))`. In mutagen, `ID3()` with no path creates an in-memory object not bound to any file. `save()` on such an object with a filename arg does write, but only if no `ID3NoHeaderError` was raised — the real fix is `ID3(); tags.save(str(output_path))` should be `tags = ID3(); tags.save(str(output_path))` where `output_path` is passed to `save`. In practice the except branch writes nothing. Episode tags (title, artist) are silently dropped every time the stitched file is fresh.

- **`audio_stitcher.py` line 21-30 — empty segment list exports silent 0-byte MP3:** `stitch_segments([])` calls `AudioSegment.empty().export(...)` with no error. The file is written, `check_post_tts` then reads 0-second duration, returns `passes: False` with a deficit of 60 min, but no exception is raised. The caller has no way to distinguish "TTS produced no segments" from "segments too short."

- **`trip_config.py` lines 33 and 37 — dual conflicting word-count targets:** `target_words: int = 10000` (field) and `target_word_count` property returns `target_minutes * words_per_minute = 65 * 145 = 9425`. Two different values answer "how many words do we need?" Any caller using the wrong one will either over-generate or under-generate by ~575 words (~4 minutes of audio).

- **`duration_guard.py` line 39 — unhandled exception on missing or corrupt MP3:** `MP3(str(mp3_path))` raises `MutagenError` or `FileNotFoundError` if the file doesn't exist or has no valid header. `check_post_tts` has no try/except, so the raw exception propagates instead of returning a structured result dict. The `verify-duration` CLI command crashes with a traceback rather than a clean error message.

---

## New Warnings

- **`audio_stitcher.py` line 57 — silent chapter truncation on length mismatch:** `zip(segment_paths, chapter_names)` truncates silently if the two lists differ in length. If the pipeline produces 8 segments but only 7 chapter names are passed (or vice versa), one chapter is dropped with no warning.

- **`quality_check.py` line 29 — `passes` threshold inconsistent with displayed table:** `passes` requires `word_count >= 9000` (= ~62.1 min at 145 WPM). The table row "Estimated >= 60 min" uses a separate 60-min check. A script with 8700 words (60.0 min) shows a green checkmark in the table row but `passes: False`. The two checks tell different stories; callers relying on the table display will think they passed when they haven't.

- **`tts_microsoft.py` line 36 — `asyncio.run()` breaks inside an existing event loop:** `synthesize_segment` wraps the async function with `asyncio.run()`. This raises `RuntimeError: This event loop is already running` if called from any async context (future pipeline orchestrator, Jupyter, or pytest-asyncio). The project is clearly heading toward async orchestration; this wrapper is a time-bomb.

- **`quality_check.py` line 12 — Wikipedia substring check will match false contexts:** `if b in citations_text.lower()` matches any citation block containing the string `wikipedia.org` anywhere, including a paper title like "Study of Wikipedia's citation reliability at doi.org/..." No real-world risk today, but the check has no anchor to actual URLs.

- **`trip_config.py` lines 22-23 — `start_date`/`end_date` accept any string, no format validation:** Pydantic accepts `"banana"` for both fields. Downstream code that parses these as dates will fail at runtime with an unrelated error, not at config load time.

---

## Verdict: NEEDS MORE FIXES

Critical count: 4 new (plus 7 from Codex = 11 total before first run). The ID3 tag silent-drop and the conflicting word-count targets are the highest priority — both cause silent wrong behavior with no error surface.
