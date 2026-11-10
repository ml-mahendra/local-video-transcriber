"""Command-line interface."""
import argparse
from pathlib import Path
from .transcriber import discover, output_paths, transcribe


def make_parser():
    parser = argparse.ArgumentParser(description="Transcribe videos/audio locally into TXT, SRT, JSON, VTT and TSV")
    parser.add_argument("paths", nargs="*", help="One or more input files; prompts if omitted")
    parser.add_argument("--folder", type=Path, help="Process all supported files in a directory")
    parser.add_argument("--recursive", action="store_true", help="Search subdirectories when using --folder")
    parser.add_argument("--model", default="small", help="Whisper model (default: small)")
    parser.add_argument("--language", default="English", help="Spoken language (default: English; auto to detect)")
    parser.add_argument("--output-root", type=Path, help="Parent directory for per-video transcript folders")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing outputs")
    return parser


def main(argv=None):
    parser = make_parser()
    args = parser.parse_args(argv)
    if args.folder and args.paths:
        parser.error("Use either file paths or --folder, not both")
    try:
        if args.folder:
            sources = discover(args.folder.expanduser().resolve(), args.recursive)
        elif args.paths:
            sources = [Path(p.strip().strip('"').strip("'")) for p in args.paths]
        else:
            entered = input("Enter video/audio file path: ").strip().strip('"').strip("'")
            if not entered:
                parser.error("No input path supplied")
            sources = [Path(entered)]
        if not sources:
            parser.error("No supported media files found")
        # Preflight before downloading the model.
        for source in sources:
            source = source.expanduser().resolve()
            if not source.is_file():
                parser.error(f"Input file not found: {source}")
            target, expected = output_paths(source, args.output_root)
            if any(p.exists() for p in expected) and not args.overwrite:
                parser.error(f"Outputs already exist in {target}. Use --overwrite to replace")
        import whisper
        print(f"Loading Whisper model: {args.model}")
        model = whisper.load_model(args.model)
        failed = 0
        for index, source in enumerate(sources, 1):
            print(f"\n[{index}/{len(sources)}] Transcribing: {source}")
            try:
                paths = transcribe(source, model=model, language=args.language,
                                   output_root=args.output_root, overwrite=args.overwrite)
                print("Saved:")
                for p in paths:
                    print(f"  {p}")
            except Exception as exc:
                failed += 1
                print(f"ERROR: {source}: {exc}")
        print(f"\nCompleted: {len(sources) - failed} succeeded, {failed} failed")
        return 1 if failed else 0
    except (ValueError, OSError, ImportError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
