# FalconOS Stable channel

FalconOS includes a **Stable** enrollment option, independent of Beta
and Alpha. The manifest URL is fixed to:

`updates/os/stable/latest.fosup`

There is currently **no Stable release**. Do not publish an untested
Beta ISO under Stable just to populate the update screen. Real Stable
releases require hardware safety and storage recovery validation that
FalconOS does not yet have.

When validated, publish an immutable GitHub Release and a manifest
with unsuffixed version, e.g. `2.1.0`.
