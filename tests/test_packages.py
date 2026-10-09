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
            for cmd in ("reboot\n", "echo test; shutdown\n", "echo foo > bar\n", "echo foo | sh\n", "echo hello & reboot\n"):
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


class ExtraValidationTests(unittest.TestCase):
    def temporary_app(self, manifest_version, source):
        td = tempfile.TemporaryDirectory()
        directory = pathlib.Path(td.name) / "test-package"
        directory.mkdir()
        (directory / "manifest.json").write_text(
            '{"id":"test-package","name":"Test Package","version":"'
            + manifest_version + '","summary":"A safely packaged example"}'
        )
        (directory / "main.fsh").write_text(source)
        return td, directory

    def test_version_numeric_and_length_limits(self):
        for ver in ("01.0.0", "4294967296.0.0", "1.0.0-alpha.", "1.0.0-alpha.01",
                    "1.0.0-" + "x" * 30):
            td, directory = self.temporary_app(ver, "echo hello\n")
            with td, self.subTest(version=ver), self.assertRaises(ValueError):
                packager.build_app(directory)

    def test_ascii_controls_and_comment_length_rejected(self):
        for source in ("# control \x1b\n", "echo hello\tworld\n", "# " + "a"*190 + "\n"):
            td, directory = self.temporary_app("1.0.0", source)
            with td, self.subTest(source=repr(source)), self.assertRaises(ValueError):
                packager.build_app(directory)
