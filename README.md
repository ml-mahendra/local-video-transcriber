# Local Video Transcriber

A free, local command-line project that transcribes video and audio with [OpenAI Whisper](https://github.com/openai/whisper). It creates **five output formats** per recording: TXT, SRT, JSON, VTT, and TSV. No account or paid API key is required.

## Features

- **Interactive mode:** run without arguments and paste a file path.
- **Single or multiple files:** pass one or several file paths.
- **Batch mode:** process every supported recording in a directory, optionally recursively.
- **Organised outputs:** create a folder named after each recording, beside the original by default.
- **Five formats:** plain text, timestamped subtitles, JSON, web subtitles, and tab-separated segments.
- **Model selection:** `tiny`, `base`, `small`, `medium`, `large`, or other installed Whisper model names.
- **Language selection:** English by default or `--language auto` for detection.
- **Overwrite protection:** existing outputs cause an error unless `--overwrite` is supplied.
- **Originals untouched:** input recordings are never moved or deleted.
- **Offline processing after setup:** models must be downloaded once; recordings are processed locally.

## Quick start (Ubuntu + Conda)

Install Conda first if needed. From the project root:
```bash
conda env create -f environment.yml
conda activate whisper
local-transcribe
```

If you **already have a Conda environment named `whisper`**, do **not** recreate it. Instead:
```bash
conda activate whisper
conda install -c conda-forge ffmpeg -y
python -m pip install -e .
```

Run from any directory once installed:
```bash
local-transcribe "/home/user/Videos/demo.mkv"
local-transcribe "/home/user/Videos/demo.mkv" --model medium
local-transcribe "/home/user/Videos/demo.mkv" --language auto
local-transcribe --folder "/home/user/Desktop/Video-Transcripts"
local-transcribe --folder ~/Videos --recursive --output-root ~/Transcripts
```

Or run without installing a console command (from the project root, after installing dependencies):
```bash
python -m local_video_transcriber "/path/to/video.mkv"
```

## Output layout

Given `Videos/demo.mkv`, the default output is:

```text
Videos/
├── demo.mkv
└── demo/
    ├── demo.txt
    ├── demo.srt
    ├── demo.json
    ├── demo.vtt
    └── demo.tsv
```
`--output-root /some/path` changes the parent directory for these named folders. **Warning:** two files with the same stem (such as `demo.mp4` and `demo.mkv`) directed to the same output root will conflict; rename inputs or use separate roots.

## Command reference
| Argument | Meaning |
| --- | --- |
| `paths` | Optional file paths; interactive prompt if omitted |
| `--folder DIR` | Transcribe all supported files directly in DIR |
| `--recursive` | Include nested folders with `--folder` |
| `--model NAME` | Whisper model, default `small` |
| `--language NAME` | Language, default `English`; `auto` detects |
| `--output-root DIR` | Parent folder for output folders |
| `--overwrite` | Replace existing transcript outputs |
| `-h`, `--help` | Show help |

Supported input suffixes: `.mkv`, `.mp4`, `.mov`, `.avi`, `.webm`, `.m4v`, `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`. Actual decoding depends on FFmpeg.

## Limitations
- Whisper transcribes **spoken audio**; it does not describe on-screen actions, identify UI buttons, or generate a visual walkthrough.
- Transcription accuracy depends on audio quality, accent, background noise, and model choice. Review critical passages.
- Processing may be slow on CPU; this version sets FP16 off for broad compatibility.
- The first run for a model needs internet access to download model weights; installing dependencies also needs internet.
- Batch mode processes files sequentially and loads the model once. Errors are reported per file.
- Existing output files are protected; a batch containing already-transcribed files will stop at preflight unless `--overwrite` is used.

## Documentation
- [Installation](docs/INSTALLATION.md)
- [Usage and examples](docs/USAGE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Testing](docs/TESTING.md)

## Development
```bash
python -m unittest discover -s tests -v
```

## License
MIT. Whisper and its dependencies have their own licenses.
