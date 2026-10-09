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

The browser IDE source lives in `site/index.html`. It can validate, preview, import an existing `.app.pkg`, export a `.app.pkg` or the two required source files, and guide contributors to a GitHub fork/PR. It does not ask for GitHub tokens or merge submissions automatically.

## Enable the website once
The `Publish CodeDium + Marketplace website` workflow saves the static website as an Actions artifact even when Pages is disabled. To serve it publicly, the **repository owner** must open **Settings → Pages → Build and deployment** and select **GitHub Actions** as the source. Re-run the workflow after enabling it. A successful preview-artifact workflow run alone does not mean the public Pages URL is live.

The marketplace web UI lists published GitHub Release assets and exposes each asset's `.sha256` sidecar. Users must verify downloaded files; a checksum is **not** a publisher identity signature. A full guest-local network stack is not currently available. The experimental `feature/marketplace-codedium` FalconOS branch uses a QEMU serial-to-host HTTPS bridge, not direct guest HTTPS.
