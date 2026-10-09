# FalconOS Marketplace

Source registry and automatic GitHub Releases distributor for **FalconOS**.

## .app.pkg packages
Every app consists of `apps/<app-id>/manifest.json` and `main.fsh`.
The builder generates `<id>-v<version>.app.pkg` containing a valid FAPP/1 UTF-8 (ASCII) script
and `<id>-v<version>.app.pkg.sha256` for integrity checking.
Each *version* receives its own immutable GitHub Release, tagged `app-<id>-v<version>`.

## Publish
1. Develop your FAPP/1 app with CodeDium Studio or edit its source files manually.
2. Submit the app's source via a Pull Request to this repository.
3. Review and merge the PR to the `main` branch.
4. GitHub Actions validates, builds and publishes a release asset for each newly tagged version.
5. QEMU FalconOS can download packages through the companion host bridge and verify SHA-256.

To update an app, increment `version` in the manifest. Existing releases are never replaced.

## Limitations
GitHub Releases have storage policies; they are *not unlimited storage*.
GitHub Docs currently says each release asset must be under 2 GiB, up to 1000 assets per release,
with no stated total release-size or bandwidth limit. Our **current FAPP/1 app limit is 4096 bytes**,
independent of those release limits. Native ELF binaries, full browser networking and persistent
app filesystem are not yet supported by FalconOS. This store distributes small safe scripts.

Build and test locally:
```bash
python3 tools/build_packages.py --all --output dist
python3 -m unittest discover -s tests -v
```

The browser IDE source lives in `site/index.html`. It can export .app.pkg and open PRs.
