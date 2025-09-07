# Chia Blockchain Development Instructions

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Initial Setup and Installation
- **CRITICAL**: The installation process can take 60+ minutes. NEVER CANCEL builds or installations.
- Bootstrap the development environment:
  - `./install.sh -d` -- installs with development dependencies. Takes 60+ minutes. NEVER CANCEL. Set timeout to 90+ minutes.
  - If network issues occur with PyPI repositories, retry the installation command multiple times
  - Installation creates `.venv/` virtual environment and `venv` symlink
- Activate the environment:
  - `source ./activate` OR `source .venv/bin/activate` 
  - `./activated.py <command>` -- wrapper script that auto-activates environment
  - `./activated.sh <command>` -- shell wrapper that auto-activates environment

### Alternative Installation Methods
- Basic installation (no dev dependencies): `./install.sh` -- takes 45+ minutes. NEVER CANCEL. Set timeout to 75+ minutes.
- Poetry direct: `./setup-poetry.sh` followed by `.penv/bin/poetry install --extras upnp --extras dev`
- **NETWORK ISSUE TROUBLESHOOTING**: If installation fails with PyPI timeouts:
  - Wait and retry the same command (network issues are temporary)
  - Check that both pypi.org and pypi.chia.net are accessible
  - Installation can be resumed by re-running the same `./install.sh` command

### Build and Test Process
- **Build verification**: No separate build step required. Installation handles compilation.
- **Test suite**: 
  - `pytest chia/_tests/` -- runs full test suite. Takes 30+ minutes. NEVER CANCEL. Set timeout to 60+ minutes.
  - `pytest chia/_tests/some_specific_test.py` -- run specific tests
  - **Note**: Tests may fail with ConsensusConstants compatibility issues between source and chia_rs package
- **Development tools validation**:
  - `ruff format --check .` -- format checking (~0.25 seconds)
  - `ruff check --fix --statistics .` -- linting and auto-fixes (~0.1 seconds) 
  - `mypy chia/types/` -- type checking subset (~3 seconds)
  - `./activated.py python manage-mypy.py build-mypy-ini` -- build mypy config (~0.1 seconds)

### Running the Application
- **Basic chia commands**: 
  - `PYTHONPATH=. ./activated.py python -c "import chia; print('Import successful')"` -- verify installation
  - **Note**: Full CLI may have ConsensusConstants compatibility issues requiring dependency updates
- **Test basic functionality**:
  - `PYTHONPATH=. python -c "import chia; print('✓ Chia import successful')"` -- verify basic imports
  - **Note**: Many chia utilities require chia_rs package which may have compatibility issues

## Validation
- **Pre-commit validation**:
  - `pre-commit install` -- install hooks
  - `pre-commit run --all-files` -- run all hooks (~10 seconds)
  - `./activated.py pre-commit run --all-files ruff_format` -- specific hook (~2 seconds)
- **ALWAYS run validation before committing**:
  - `ruff format .` -- format code (~0.25 seconds)
  - `ruff check --fix .` -- lint and fix (~0.1 seconds)
  - `./activated.py python manage-mypy.py build-mypy-ini` -- update mypy config
  - **Note**: Full mypy validation may fail due to version compatibility issues
- **Manual testing scenarios**:
  - Verify chia module imports work: `PYTHONPATH=. python -c "import chia; print('✓ Success')"`
  - **Note**: Many specific utilities require chia_rs package with version compatibility
  - **Cannot fully test CLI or advanced features due to dependency version conflicts** -- document this limitation

## Common Tasks

### Development Workflow
- **Before making changes**:
  - Run `./install.sh -d` if first time (60+ minutes. NEVER CANCEL)
  - Activate environment: `source ./activate` 
  - Verify installation: `PYTHONPATH=. python -c "import chia"`
- **After making changes**:
  - Format: `ruff format .` 
  - Lint: `ruff check --fix .`
  - Test basic imports: `PYTHONPATH=. python -c "import chia; print('✓ Basic imports work')"`
  - **Note**: Full pytest and advanced functionality may fail due to dependency issues

### Repository Structure
```
.
├── install.sh              # Main installation script (60+ min runtime)
├── setup-poetry.sh         # Poetry setup (part of install.sh)
├── activated.py/activated.sh # Environment activation wrappers
├── chia/                   # Main chia blockchain source code
│   ├── cmds/              # CLI commands (may have compatibility issues)
│   ├── consensus/         # Consensus logic
│   ├── types/             # Data types and structures  
│   ├── util/              # Utility functions
│   └── _tests/            # Test suite
├── pyproject.toml         # Poetry project configuration
├── pytest.ini            # Test configuration
├── ruff.toml             # Ruff linter configuration
└── .pre-commit-config.yaml # Pre-commit hooks

```

### Timing Expectations and Critical Timeouts
- **NEVER CANCEL**: Installation: 60+ minutes (use 90+ minute timeout)
- **NEVER CANCEL**: Basic installation: 45+ minutes (use 75+ minute timeout)  
- **NEVER CANCEL**: Full test suite: 30+ minutes (use 60+ minute timeout)
- Ruff format check: ~0.25 seconds
- Ruff lint/fix: ~0.1 seconds
- MyPy (subset): ~3 seconds
- Pre-commit hooks: ~2-10 seconds

### Known Issues and Limitations
- **Network Dependencies**: Installation requires access to pypi.org and pypi.chia.net
- **Version Compatibility**: ConsensusConstants compatibility issues between source code and chia_rs package versions
- **CLI Limitations**: Full `chia` CLI may not work due to dependency version mismatches
- **Testing Limitations**: pytest may fail on configuration loading due to ConsensusConstants issues
- **Workaround**: Use `PYTHONPATH=.` for direct Python imports and testing of individual modules

### Emergency Troubleshooting
- If installation fails with timeouts: wait and retry the exact same command
- If chia imports fail: check PYTHONPATH and virtual environment activation
- If tests fail with ConsensusConstants errors: this is a known compatibility issue
- If network errors persist: check firewall and DNS settings for PyPI access

## Important Notes
- This is a Python 3.9+ cryptocurrency blockchain project using Poetry for dependency management
- Has extensive CI/CD workflows and comprehensive development tooling
- Requires significant build time due to cryptographic dependencies (chiapos, chiavdf, etc.)
- **Always allow full completion time for installations and builds**
- Development tools (ruff, mypy, pre-commit) work reliably for code quality checks