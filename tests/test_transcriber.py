import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from local_video_transcriber.transcriber import discover, output_paths, transcribe, FORMATS


class TranscriberTests(unittest.TestCase):
    def test_output_names(self):
        source = Path("/tmp/a video.mkv")
        target, paths = output_paths(source)
        self.assertEqual(target.name, "a video")
        self.assertEqual([p.suffix for p in paths], ["." + x for x in FORMATS])

    def test_discover_nonrecursive(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "one.mkv").touch()
            (root / "notes.txt").touch()
            (root / "sub").mkdir()
            (root / "sub" / "two.mp4").touch()
            self.assertEqual([p.name for p in discover(root)], ["one.mkv"])
            self.assertEqual(len(discover(root, recursive=True)), 2)

    def test_existing_outputs_are_protected(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "sample.mkv"
            source.touch()
            target, expected = output_paths(source)
            target.mkdir()
            expected[0].touch()
            with self.assertRaises(FileExistsError):
                transcribe(source, model=object())


if __name__ == "__main__":
    unittest.main()
