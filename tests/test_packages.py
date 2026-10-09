import importlib.util
import pathlib
import tempfile
import unittest

root = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("packager", root / "tools" / "build_packages.py")
packager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)

class PackageTests(unittest.TestCase):
    def test_example_apps(self):
        for d in (root / "apps").iterdir():
            if d.is_dir():
                info, raw = packager.build_app(d)
                self.assertTrue(raw.startswith(b"FAPP/1\n"))
                self.assertLessEqual(len(raw), 4096)
                self.assertEqual(info["id"], d.name)
    def test_unsafe_commands_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            d = pathlib.Path(temp) / "malicious"
            d.mkdir()
            (d / "manifest.json").write_text('{"id":"malicious","name":"Malicious Test","version":"1.0.0","summary":"Security test app"}')
            for cmd in ("reboot\n", "echo test; shutdown\n", "echo foo > bar\n", "echo foo | sh\n"):
                (d / "main.fsh").write_text(cmd)
                with self.assertRaises(ValueError):
                    packager.build_app(d)
    def test_invalid_ids_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            d = pathlib.Path(temp) / "sample"
            d.mkdir()
            (d / "main.fsh").write_text("echo hello\n")
            (d / "manifest.json").write_text('{"id":"../sample","name":"Sample Test","version":"1.0.0","summary":"Security test app"}')
            with self.assertRaises(ValueError):
                packager.build_app(d)
