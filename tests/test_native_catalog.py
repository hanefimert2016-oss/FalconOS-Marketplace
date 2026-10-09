#!/usr/bin/env python3
"""Verify the public static HTTPS catalog is an exact snapshot of reviewed
FAPP source; CI rejects drift, path traversal and digest mismatches."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from build_packages import build_app

root=Path(__file__).resolve().parents[1]
catalog=(root/"site/native/catalog.fcat").read_text()
lines=catalog.splitlines()
assert lines[0]=="FCAT/1" and 1<len(lines)<=49
ids=set()
for line in lines[1:]:
    parts=line.split("|")
    assert len(parts)==6 and parts[0]=="CAT"
    _,app_id,version,name,digest,filename=parts
    assert app_id not in ids and app_id.isascii()
    ids.add(app_id)
    assert filename==f"{app_id}-v{version}.app.pkg"
    assert len(digest)==64 and all(c in "0123456789abcdef" for c in digest)
    entry,expected=build_app(root/"apps"/app_id)
    assert entry["version"]==version and entry["name"]==name
    published=(root/"site/native"/filename).read_bytes()
    assert published==expected
    assert hashlib.sha256(published).hexdigest()==digest
assert ids=={p.name for p in (root/"apps").iterdir() if p.is_dir()}
print(f"PASS: {len(ids)} reviewed FAPP/1 packages exactly match direct-HTTPS catalog and hashes")
