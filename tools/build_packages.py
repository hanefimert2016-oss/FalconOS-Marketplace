#!/usr/bin/env python3
"""Deterministic FAPP/1 packager, using only Python's standard library."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MAX_SIZE = 4096
ID_RE = re.compile(r"[a-z][a-z0-9-]{1,31}\Z")
VER_RE = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[a-z0-9.-]+)?\Z")
ALLOWED = {"echo", "date", "uname", "uptime", "whoami", "pwd", "ls", "help", "cal", "hwinfo", "free", "df", "clear"}

def build_app(directory):
    data = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if set(data) != {"id", "name", "version", "summary"}:
        raise ValueError("manifest must contain id, name, version, summary")
    if not all(isinstance(v, str) for v in data.values()):
        raise ValueError("manifest values must be strings")
    if not ID_RE.fullmatch(data["id"]) or directory.name != data["id"]:
        raise ValueError("invalid id or mismatched directory")
    if not VER_RE.fullmatch(data["version"]):
        raise ValueError("invalid version")
    for field, limit in (("name", 40), ("summary", 75)):
        value = data[field]
        if not 2 <= len(value) <= limit or not re.fullmatch(r"[A-Za-z0-9 .,:!?+/_()\-]+", value):
            raise ValueError("invalid " + field)
    script = (directory / "main.fsh").read_text(encoding="utf-8")
    if not script.endswith("\n") or not script.isascii() or "\r" in script or "\x00" in script:
        raise ValueError("script must be ASCII and end in newline")
    for number, line in enumerate(script.splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        command = line.split(maxsplit=1)[0]
        if command not in ALLOWED or len(line) > 180:
            raise ValueError(f"line {number}: command not allowed")
        if any(x in line for x in (";", "&&", "||", "|", ">", "<", "$", "\u0060", "\\", "&")):
            raise ValueError(f"line {number}: shell operators forbidden")
    text = "FAPP/1\n" + "".join(f"{k}={data[k]}\n" for k in ("id","name","version","summary")) + "\n" + script
    raw = text.encode("ascii")
    if len(raw) > MAX_SIZE:
        raise ValueError("package exceeds 4096 bytes")
    return data, raw

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--app")
    parser.add_argument("--output", default="dist")
    args = parser.parse_args()
    if args.all == bool(args.app):
        parser.error("choose --all or --app")
    base = ROOT / "apps"
    dirs = sorted(p for p in base.iterdir() if p.is_dir()) if args.all else [base / args.app]
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    catalog = []
    for d in dirs:
        info, raw = build_app(d)
        filename = f"{info['id']}-v{info['version']}.app.pkg"
        (output / filename).write_bytes(raw)
        digest = hashlib.sha256(raw).hexdigest()
        (output / (filename + ".sha256")).write_text(digest + "  " + filename + "\n")
        catalog.append({**info, "file": filename, "tag": f"app-{info['id']}-v{info['version']}", "sha256":digest, "size":len(raw)})
        print("Built", filename, "size", len(raw))
    (output / "catalog.json").write_text(json.dumps(catalog, indent=2) + "\n")

if __name__ == "__main__":
    main()
