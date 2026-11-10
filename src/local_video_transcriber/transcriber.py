"""Transcription core: validate paths, run Whisper, write five formats."""
from pathlib import Path

FORMATS = ("txt", "srt", "json", "vtt", "tsv")
SUPPORTED = {".mkv", ".mp4", ".mov", ".avi", ".webm", ".m4v", ".mp3", ".wav", ".m4a", ".flac", ".ogg"}


def discover(directory: Path, recursive: bool = False) -> list[Path]:
    """Find supported input files, sorted for reproducibility."""
    if not directory.is_dir():
        raise ValueError(f"Input directory does not exist: {directory}")
    iterator = directory.rglob("*") if recursive else directory.iterdir()
    return sorted((p for p in iterator if p.is_file() and p.suffix.lower() in SUPPORTED), key=str)


def output_paths(source: Path, output_root: Path | None = None) -> tuple[Path, list[Path]]:
    base = (output_root or source.parent).expanduser().resolve()
    target = base / source.stem
    return target, [target / f"{source.stem}.{ext}" for ext in FORMATS]


def transcribe(source: Path, *, model, language: str = "English", output_root: Path | None = None,
               overwrite: bool = False) -> list[Path]:
    source = source.expanduser().resolve()
    if not source.is_file():
        raise ValueError(f"Input file not found: {source}")
    if source.suffix.lower() not in SUPPORTED:
        raise ValueError(f"Unsupported file type: {source.suffix}")
    target, expected = output_paths(source, output_root)
    existing = [p for p in expected if p.exists()]
    if existing and not overwrite:
        raise FileExistsError(f"Existing outputs for {source.name}: {', '.join(str(p) for p in existing)}. Use --overwrite.")
    target.mkdir(parents=True, exist_ok=True)
    from whisper.utils import get_writer
    options = {"verbose": False, "fp16": False}
    if language.lower() != "auto":
        options["language"] = language
    result = model.transcribe(str(source), **options)
    get_writer("all", str(target))(result, str(source))
    missing = [p for p in expected if not p.is_file()]
    if missing:
        raise RuntimeError(f"Whisper did not produce: {', '.join(str(p) for p in missing)}")
    return expected
