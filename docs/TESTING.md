# Testing

Run unit tests from the project root:

```bash
python -m unittest discover -s tests -v
```

Tests do not download Whisper models or transcribe real media; they verify file discovery, output paths, and overwrite safety with mocks. For an end-to-end smoke test, run `local-transcribe /path/to/short-test-video.mkv --model tiny` and inspect all five outputs.
