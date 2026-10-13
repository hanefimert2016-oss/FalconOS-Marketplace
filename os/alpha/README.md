# FalconOS Alpha Insider channel

FalconOS desktop users can enroll via **System Updates -> Alpha** (or
`update channel alpha`). The host bridge only accepts the fixed URL:

`updates/os/alpha/latest.fosup`

No Alpha release is published yet. Do not upload a placeholder manifest:
the native updater intentionally displays "No published build" until a
real independently tested, SHA-256-verified Alpha ISO is released.

To publish, upload an immutable ISO to a GitHub Release tagged
`os-vMAJOR.MINOR.PATCH-alpha`, then add the reviewed
`FOSUP/1` manifest referencing that exact ISO and checksum.
Never replace a Release asset without updating the digest and version.
Alpha is experimental: opt-in, no silent restart, retain recovery ISO.
