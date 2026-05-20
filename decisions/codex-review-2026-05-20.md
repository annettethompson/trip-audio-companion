## Critical Bugs (will crash)

- `src/tts_microsoft.py:24` sends the entire `text` argument directly into `edge_tts.Communicate(...)`, and `src/tts_microsoft.py:25` immediately calls `save(...)` with no splitting loop or chunk queue in `src/tts_microsoft.py:17-26`. For a 10,000+ word episode, this is the specific edge-tts long-string failure mode the project must avoid.
- `src/tts_microsoft.py:25` has no timeout, retry, or exception handling around `await communicate.save(...)`; an edge-tts network timeout or service error will bubble out and crash synthesis.
- `src/audio_stitcher.py:30` writes `combined.export(str(output_path), ...)` without creating `output_path.parent`; writing to `outputs/final_mp3s/...` will fail if that directory does not already exist.
- `src/tts_microsoft.py:24-25` writes directly to `output_path`, but `synthesize_segment_async(...)` / `synthesize_segment(...)` never create `output_path.parent` in `src/tts_microsoft.py:17-38`; only `synthesize_chapter(...)` creates a directory at `src/tts_microsoft.py:48`, so direct calls to `synthesize_segment(...)` can crash when `outputs/audio_segments/` is absent.

## Logic Errors (wrong behavior)

- `src/duration_guard.py:18-20` estimates duration from `len(text.split()) / WORDS_PER_MINUTE`, with `WORDS_PER_MINUTE = 145` fixed at `src/duration_guard.py:11`. This does not account for `DEFAULT_VOICE`, `DEFAULT_RATE = "-5%"`, or `DEFAULT_PITCH` in `src/tts_microsoft.py:12-14`, so the pre-TTS duration estimate is not reliable enough to enforce the 60-minute hard rule.
- `src/trip_config.py:31-37` exposes a configurable `words_per_minute` and `target_word_count`, but `src/duration_guard.py:11` and `src/quality_check.py:26` both hard-code 145 WPM instead of using the trip configuration. Changing the config will not change the actual duration checks.
- `src/quality_check.py:26` reports estimated minutes using hard-coded 145 WPM, while `src/quality_check.py:29` marks pre-flight as passing solely on `word_count >= 9000`, citations, and no Wikipedia. The displayed "Estimated >= 60 min" check at `src/quality_check.py:38` is not part of the pass/fail decision at `src/quality_check.py:29`.
- `src/audio_stitcher.py:22-28` builds one growing `AudioSegment` in memory and `src/audio_stitcher.py:25` decodes every MP3 segment with pydub before exporting at `src/audio_stitcher.py:30`. A 60+ minute MP3 is decoded to much larger PCM data in memory, and repeated `combined += segment` can copy the accumulated audio repeatedly.
- `src/audio_stitcher.py:57` uses `zip(segment_paths, chapter_names)`, so extra segments or extra chapter names are silently dropped instead of being rejected; chapter timestamps can become incomplete without an error.
- `src/audio_stitcher.py:69` adds `pause_ms` after every segment when building timestamps, including the final segment, while `stitch_segments(...)` only inserts silence when `i < len(segment_paths) - 1` at `src/audio_stitcher.py:27-28`. The computed end timeline is longer than the actual stitched audio.
- `src/tts_microsoft.py:25-26` returns `output_path` after `save(...)` with no file existence, nonzero-size, or readable-MP3 validation. An empty or corrupt output file can be treated as a successful segment.

## Missing Features (needed for 60-min guarantee)

- `src/main.py:21-23` does not run generation, TTS, stitching, or duration verification; it only prints that the full pipeline is not implemented. There is no CLI path that creates an episode and enforces the 60-minute minimum.
- `src/duration_guard.py:38-50` can detect whether a finished MP3 is under 60 minutes, but there is no repair path that appends or regenerates audio when `passes` is false at `src/duration_guard.py:47`.
- `src/tts_microsoft.py:17-26` has no edge-tts chunking feature: no sentence/paragraph splitter, no maximum character budget, no per-chunk temp files, and no reassembly of chunks before returning.
- `src/audio_stitcher.py:15-41` does not call `check_post_tts(...)` from `src/duration_guard.py:38-50` after export, so the final MP3 can be produced without a hard duration gate.
- `src/quality_check.py:19-30` is a standalone pre-flight check and is not invoked by `src/main.py:14-23`, so script length validation is not enforced by the episode command.
- `src/audio_stitcher.py:33-39` handles fresh MP3s without existing ID3 tags by constructing `ID3()` at `src/audio_stitcher.py:36`, so the specific fresh-tag concern is covered; however, `TALB` and `COMM` are imported at `src/audio_stitcher.py:7` and never written, so album/comment metadata is not implemented.

## Verdict: READY / NEEDS FIXES

NEEDS FIXES - the current code does not implement the episode pipeline, does not chunk long edge-tts input, and does not enforce or repair the 60-minute post-TTS guarantee.
