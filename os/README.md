# FalconOS System Update program

The embedded OS updater is distinct from the app Marketplace.
It uses COM2 and a host HTTPS verification bridge for QEMU/OVMF guests.

| Program | Fixed updates-branch manifest | Version suffix |
|---|---|---|
| Stable | `os/stable/latest.fosup` | none |
| Beta | `os/latest.fosup` | `-beta` |
| Alpha | `os/alpha/latest.fosup` | `-alpha` |

Beta is published. Stable and Alpha have no approved ISO manifests yet.
The UI must display "No published build" for absent feeds rather
than inventing available updates. Manual checks are supported; automatic
checks do not automatically restart or overwrite the original ISO.
A stronger signing/rollback chain is still required before any real PC
installation or production-grade update service.
