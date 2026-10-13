# FalconOS native OS update channel

This repository's **updates** branch owns `os/source.json`, a pinned exact FalconOS source commit. The workflow builds a **real bootable** UEFI ISO, publishes it as an immutable GitHub Release and writes `os/latest.fosup` with an actual SHA-256 hash and size. FalconOS native System Updates reads that manifest over its isolated COM2 updater bridge; the bridge refuses unverified media. New ISO replaces ONLY the QEMU virtual CD medium. Normal guest reboot activates it. **No physical disks are written.** Reverting is done by launching with the old `build/FalconOS.iso`.

The guest also has a built-in native System Updates application; no Marketplace app is required to check, install or enable automatic installation. A FAPP/1 convenience launcher may be published separately. This channel does not contain arbitrary executable updates or silent physical disk flashing.
