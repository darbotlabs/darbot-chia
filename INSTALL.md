# Installation

Install instructions have been moved to the [INSTALL](https://github.com/Chia-Network/chia-blockchain/wiki/INSTALL) section of the repository [Wiki](https://github.com/Chia-Network/chia-blockchain/wiki).

After installing, follow the remaining instructions in the
[Quick Start Guide](https://github.com/Chia-Network/chia-blockchain/wiki/Quick-Start-Guide)
to run the software.

## Local source install and lockfile

For a source install on this fork, initialize the `mozilla-ca` submodule and use the repository's locked Poetry environment:

```powershell
git submodule update --init --recursive
poetry install
```

Set `POETRY_DYNAMIC_VERSIONING_BYPASS=2.5.4` during the install/build when package metadata is not available from a normal Git checkout. Do not substitute `uv pip install -e .`: it does not honor `poetry.lock` and can select an incompatible `chia_rs` release.
