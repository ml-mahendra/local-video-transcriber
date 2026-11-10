# Installation

## Requirements

- Ubuntu/Linux, macOS, or Windows with Conda
- Python 3.10+ (3.11 recommended)
- FFmpeg available on PATH
- Disk space for the Whisper model and transcripts

## Fresh Conda environment

From the project root:

```bash
conda env create -f environment.yml
conda activate whisper
local-transcribe --help
```

If an environment named `whisper` already exists, use the existing-environment steps instead.

## Existing Conda environment

```bash
conda activate whisper
conda install -c conda-forge ffmpeg -y
python -m pip install -e .
local-transcribe --help
```

Check `ffmpeg -version` and `python -c "import whisper; print('Whisper ready')"` if needed.

## Troubleshooting

- `conda: command not found`: initialise Conda for your shell and reopen the terminal.
- `local-transcribe: command not found`: activate the correct environment and run `python -m pip install -e .` from the project root.
- `ffmpeg` missing: install it with `conda install -c conda-forge ffmpeg`.
- Slow transcription: choose `--model base` or `--model tiny`; CPU execution can take time.
- Download failures: retry when online; the first run of a new model downloads weights.
