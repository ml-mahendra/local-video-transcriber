# Architecture

## Pipeline

1. `cli.py` parses arguments or prompts for a path.
2. `transcriber.py:discover()` finds media inputs for batch mode.
3. CLI preflight checks that inputs exist and transcript outputs will not be overwritten accidentally.
4. CLI loads a Whisper model **once**.
5. `transcriber.py:transcribe()` invokes Whisper and its built-in `all` writer.
6. The application verifies that TXT, SRT, JSON, VTT, and TSV exist and prints paths.

## Design decisions

- **Local inference:** no cloud transcription API is used.
- **One folder per recording:** output directory uses the source filename without extension.
- **Non-destructive:** original input files remain in place.
- **Batch efficiency:** a model is loaded once per invocation.
- **Simple module separation:** CLI handles user interaction; transcriber handles file discovery and transcription.

## Scope

This is audio transcription, not multimodal video understanding. It does not interpret mouse clicks, menus, or screenshots. A later enhancement could add optional frame extraction and visual annotation as a separate feature.
