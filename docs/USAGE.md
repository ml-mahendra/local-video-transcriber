# Usage

## Interactive

```bash
local-transcribe
```

Paste the absolute path when prompted. Paths containing spaces work.

## One recording

```bash
local-transcribe "/home/rurouni/Desktop/Video-Transcripts/2026-11-03 11-18-54.mkv"
```

## Multiple recordings

```bash
local-transcribe "video one.mkv" "video two.mp4"
```

## Batch folder

```bash
local-transcribe --folder ~/Desktop/Video-Transcripts
```

Add `--recursive` to search subfolders. The scanner recognises only supported media suffixes.

## Custom model and language

```bash
local-transcribe "video.mkv" --model medium --language English
local-transcribe "video.mkv" --language auto
```

## Custom output location

```bash
local-transcribe "video.mkv" --output-root ~/Transcripts
```

Creates `~/Transcripts/video/` containing five outputs.

## Re-run

```bash
local-transcribe "video.mkv" --overwrite
```

Without `--overwrite`, existing transcript outputs cause an error. `--overwrite` replaces transcript files, not original recordings.

## Understanding formats

- **TXT:** readable transcript without timestamps.
- **SRT:** subtitles with numbered segments and time ranges.
- **JSON:** detailed transcription structure including segment timing.
- **VTT:** WebVTT subtitles for browsers.
- **TSV:** tab-separated segment timing and text.

## Exit codes

- `0`: all requested recordings succeeded.
- `1`: one or more recordings failed after processing started.
- `2`: invalid CLI arguments, missing inputs, or preflight errors.
