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
│   ├── apis.py            # Shared API utilities
│   ├── cmds/              # CLI commands and entry points
│   ├── consensus/         # Proof of Space/Time consensus engine
│   │   ├── blockchain.py  # Core blockchain state management
│   │   ├── difficulty_adjustment.py # Dynamic difficulty algorithm
│   │   └── constants.py   # Network consensus parameters
│   ├── daemon/            # Background service coordination
│   ├── data_layer/        # On-chain key-value database system
│   ├── farmer/            # Block creation and farming rewards
│   │   ├── farmer.py      # Main farmer implementation
│   │   └── farmer_api.py  # Farmer RPC interface
│   ├── full_node/         # Complete blockchain validation
│   │   ├── full_node.py   # Full node implementation
│   │   ├── mempool.py     # Transaction pool management
│   │   ├── block_store.py # Persistent block storage
│   │   └── coin_store.py  # UTXO set management
│   ├── harvester/         # Plot scanning and proof generation
│   │   ├── harvester.py   # Main harvester implementation
│   │   └── harvester_api.py # Harvester RPC interface
│   ├── plotting/          # Plot creation and management
│   │   ├── create_plots.py # Plot generation workflow
│   │   ├── manager.py     # Plot lifecycle management
│   │   └── cache.py       # Plot metadata caching
│   ├── plotters/          # Multiple plotter implementations
│   │   ├── chiapos.py     # Reference plotter
│   │   ├── bladebit.py    # GPU-accelerated plotter
│   │   └── madmax.py      # High-performance CPU plotter
│   ├── pools/             # Decentralized pooling protocol
│   ├── protocols/         # Network communication protocols
│   │   ├── full_node_protocol.py # Block/transaction propagation
│   │   ├── farmer_protocol.py    # Farming coordination
│   │   └── wallet_protocol.py    # Wallet synchronization
│   ├── rpc/               # RPC server implementations
│   ├── server/            # Network server infrastructure
│   ├── timelord/          # Verifiable Delay Function services
│   │   ├── timelord.py    # VDF computation and verification
│   │   └── timelord_launcher.py # Timelord process management
│   ├── types/             # Core data structures and formats
│   │   ├── blockchain_format/ # Fundamental blockchain types
│   │   │   ├── coin.py    # UTXO coin representation
│   │   │   ├── program.py # CLVM program execution
│   │   │   └── proof_of_space.py # PoS proof structures
│   │   └── coin_spend.py  # Transaction spending format
│   ├── util/              # Shared utility functions
│   │   ├── hash.py        # Cryptographic hash functions
│   │   └── keychain.py    # Key management utilities
│   ├── wallet/            # Wallet and smart contract system
│   │   ├── wallet.py      # Standard XCH wallet
│   │   ├── singleton.py   # Singleton puzzle implementation
│   │   ├── cat_wallet/    # Chia Asset Token wallets
│   │   ├── nft_wallet/    # NFT wallet implementation
│   │   ├── did_wallet/    # Decentralized Identity wallets
│   │   ├── trading/       # Peer-to-peer offer system
│   │   │   └── offer.py   # Atomic swap implementation
│   │   ├── puzzles/       # Smart contract puzzle library
│   │   └── util/          # Wallet-specific utilities
│   └── _tests/            # Comprehensive test suite
│       ├── blockchain/    # Blockchain core tests
│       ├── consensus/     # Consensus mechanism tests
│       ├── wallet/        # Wallet functionality tests
│       └── plot_sync/     # Plot synchronization tests
├── chia-blockchain-gui/   # Electron-based GUI (submodule)
├── build_scripts/         # Platform-specific build tools
├── tools/                 # Development and maintenance tools
├── pyproject.toml         # Poetry project configuration
├── pytest.ini            # Test framework configuration
├── ruff.toml             # Code linting configuration
├── mypy.ini.template     # Type checking configuration
└── .pre-commit-config.yaml # Git hook automation

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

## Technical Development Workflows

### Working with Plotting System
- **Plot Creation Testing**:
  ```bash
  # Test plot creation (small k25 for development only)
  PYTHONPATH=. python -m chia.plotting.create_plots --size 25 --num 1 --tmp_dir /tmp/plots --final_dir /tmp/plots
  
  # Check plot validity
  PYTHONPATH=. python -m chia.plotting.check_plots /tmp/plots/*.plot
  ```
- **Plot Management Development**:
  - Files: `chia/plotting/manager.py`, `chia/plotting/cache.py`
  - Key classes: `PlotManager`, `PlotCache`
  - Test: `chia/_tests/plotting/`

### Working with Wallet and Smart Contracts
- **Singleton Development**:
  ```bash
  # Test singleton puzzle creation
  PYTHONPATH=. python -c "from chia.wallet.singleton import create_singleton_puzzle; print('Singleton utilities available')"
  ```
  - Files: `chia/wallet/singleton.py`
  - Key functions: `create_singleton_puzzle()`, `get_singleton_id_from_puzzle()`
  - Test: `chia/_tests/wallet/test_singleton.py`

- **Offer System Development**:
  ```bash
  # Test offer utilities
  PYTHONPATH=. python -c "from chia.wallet.trading.offer import Offer; print('Offer system available')"
  ```
  - Files: `chia/wallet/trading/offer.py`, `chia/wallet/trade_manager.py`
  - Key classes: `Offer`, `TradeManager`
  - Test: `chia/_tests/wallet/trading/`

### Working with Consensus and Blockchain
- **Consensus Development**:
  ```bash
  # Test consensus utilities
  PYTHONPATH=. python -c "from chia.consensus.blockchain import Blockchain; print('Blockchain core available')"
  ```
  - Files: `chia/consensus/blockchain.py`, `chia/consensus/difficulty_adjustment.py`
  - Key classes: `Blockchain`, `BlockRecord`
  - Test: `chia/_tests/consensus/`

- **Full Node Development**:
  ```bash
  # Test full node components
  PYTHONPATH=. python -c "from chia.full_node.full_node import FullNode; print('Full node available')"
  ```
  - Files: `chia/full_node/full_node.py`, `chia/full_node/mempool.py`
  - Key classes: `FullNode`, `Mempool`
  - Test: `chia/_tests/full_node/`

### Working with Cryptographic Components
- **Hash Function Development**:
  ```bash
  # Test hashing utilities
  PYTHONPATH=. python -c "from chia.util.hash import std_hash; print('Hash utilities available')"
  ```
  - Files: `chia/util/hash.py`, `chia/types/blockchain_format/tree_hash.py`
  - Key functions: `std_hash()`, `sha256()`

- **Key Management Development**:
  ```bash
  # Test key derivation
  PYTHONPATH=. python -c "from chia.wallet.derive_keys import master_sk_to_farmer_sk; print('Key derivation available')"
  ```
  - Files: `chia/wallet/derive_keys.py`, `chia/util/keychain.py`

### Working with Network Protocols
- **Protocol Development**:
  ```bash
  # Test protocol utilities
  PYTHONPATH=. python -c "from chia.protocols.full_node_protocol import RequestBlock; print('Protocols available')"
  ```
  - Files: `chia/protocols/`, `chia/server/`
  - Key classes: Protocol message types, server implementations

### Working with Data Structures
- **Blockchain Format Development**:
  ```bash
  # Test core data structures
  PYTHONPATH=. python -c "from chia.types.blockchain_format.coin import Coin; print('Blockchain types available')"
  ```
  - Files: `chia/types/blockchain_format/`
  - Key classes: `Coin`, `Program`, `ProofOfSpace`

### Testing Specific Components
- **Component-Specific Testing**:
  ```bash
  # Test specific components (faster than full test suite)
  pytest chia/_tests/wallet/test_singleton.py -v
  pytest chia/_tests/consensus/test_blockchain.py -v
  pytest chia/_tests/plotting/ -v
  pytest chia/_tests/util/test_hash.py -v
  ```

### Performance Optimization Workflows
- **Profiling Setup**:
  ```bash
  # Install profiling tools if needed
  pip install cProfile memory_profiler
  
  # Profile specific functions
  PYTHONPATH=. python -m cProfile -s tottime -m chia.plotting.create_plots --help
  ```

### Common Technical Debugging
- **Import Testing**: Always test imports before developing
- **Component Isolation**: Test individual components before integration
- **Mock Dependencies**: Use pytest fixtures for complex component testing
- **Simulation Mode**: Use `chia.simulator` for blockchain testing without full network

## Important Notes
- This is a Python 3.9+ cryptocurrency blockchain project using Poetry for dependency management
- Has extensive CI/CD workflows and comprehensive development tooling
- Requires significant build time due to cryptographic dependencies (chiapos, chiavdf, etc.)
- **Always allow full completion time for installations and builds**
- Development tools (ruff, mypy, pre-commit) work reliably for code quality checks

## Chia Blockchain Architecture Deep Dive

### Core Blockchain Components

#### Consensus and Blockchain Core
- **Consensus Engine**: `/chia/consensus/` - Proof of Space and Time consensus implementation
  - `blockchain.py` - Main blockchain state management
  - `difficulty_adjustment.py` - Dynamic difficulty adjustment algorithm
  - `pos_quality.py` - Proof of Space quality validation
  - `pot_iterations.py` - Proof of Time iteration calculations
- **Full Node**: `/chia/full_node/` - Complete blockchain validation and network participation
  - `full_node.py` - Main full node implementation
  - `mempool.py` - Transaction pool management
  - `block_store.py` - Persistent block storage
  - `coin_store.py` - UTXO set management
- **Data Structures**: `/chia/types/blockchain_format/` - Core blockchain data types
  - `coin.py` - UTXO coin representation
  - `program.py` - CLVM program execution
  - `proof_of_space.py` - PoS proof structures
  - `tree_hash.py` - Merkle tree hashing utilities

#### Cryptographic Framework
- **Hashing**: `/chia/util/hash.py` - SHA256 and other cryptographic hash functions
- **Signatures**: BLS aggregate signatures using chia_rs Rust library
- **Key Derivation**: `/chia/wallet/derive_keys.py` - Hierarchical deterministic key generation
- **Puzzle Hashes**: Address system based on puzzle hash commitments

### Plotting and Storage Architecture

#### Plot Creation and Management
- **Plot Creation**: `/chia/plotting/create_plots.py` - Plot generation workflow
  - Supports multiple plotter backends: chiapos, bladebit, madmax
  - Plot sizes: k32 (101.4 GiB), k33 (208.8 GiB), k34 (429.8 GiB)
  - Uses hard drive space for Proof of Space farming
- **Plot Formats**: 
  - **Standard Plots**: Traditional plot format with full tables
  - **Compressed Plots**: Space-efficient plots using compression algorithms
  - **Plot Compression**: `/chia/wallet/util/puzzle_compression.py` - Compression utilities
- **Plot Plotters**: `/chia/plotters/` - Multiple plotter implementations
  - `chiapos.py` - Reference plotter implementation
  - `bladebit.py` - High-performance GPU plotter
  - `madmax.py` - Fast CPU plotter
- **Plot Management**: `/chia/plotting/manager.py` - Plot lifecycle management
- **Plot Caching**: `/chia/plotting/cache.py` - Plot metadata caching for performance

#### Hard Drive and Storage Requirements
- **Storage Architecture**: Plots stored as large files on traditional hard drives
- **I/O Patterns**: Sequential write during plotting, random read during harvesting
- **Recommended Hardware**:
  - **Plotting**: NVMe SSDs for temporary files, high-core-count CPUs
  - **Farming**: Large capacity HDDs (8TB+), reliable storage controllers
  - **Network**: Gigabit+ internet for full node synchronization
- **Plot Directory Structure**: Configurable plot directories for distributed storage

#### Harvesting and Farming
- **Harvester**: `/chia/harvester/harvester.py` - Plot scanning and proof generation
  - Scans local plots for valid proofs
  - Communicates with farmer via local network protocols
  - Supports remote harvester configurations
- **Farmer**: `/chia/farmer/farmer.py` - Block creation and reward management
  - Receives proofs from harvesters
  - Creates blocks when winning challenges
  - Manages pool participation and payouts
- **Plot Sync**: `/chia/plot_sync/` - Distributed plot management system

### Advanced Blockchain Features

#### Singleton Puzzles and Smart Contracts
- **Singletons**: `/chia/wallet/singleton.py` - Unique, non-duplicatable on-chain objects
  - Used for NFTs, DIDs, and state-holding smart contracts
  - Guaranteed uniqueness through cryptographic lineage proofs
  - Inner puzzle customization for complex logic
- **Puzzle Architecture**: Chialisp-based smart contract system
  - **Outer Puzzles**: Standard wrappers (CAT, NFT, singleton)
  - **Inner Puzzles**: Custom business logic
  - **Puzzle Drivers**: `/chia/wallet/puzzle_drivers.py` - Automated puzzle solving
- **CLVM**: Chialisp Virtual Machine for smart contract execution
  - Functional programming language optimized for blockchain
  - Deterministic execution and cost calculation
  - Support for complex conditions and state transitions

#### Offer System (Peer-to-Peer Trading)
- **Offer Files**: `/chia/wallet/trading/offer.py` - Atomic swap implementation
  - Self-contained trading contracts
  - Support for XCH, CATs, NFTs, and custom assets
  - Cryptographically secure without trusted intermediaries
- **Offer Format**: Compressed, shareable offer data structures
- **Trade Management**: `/chia/wallet/trade_manager.py` - Offer lifecycle handling
- **Settlement**: Automatic execution when conditions are met

#### Timelord Infrastructure
- **Timelord**: `/chia/timelord/timelord.py` - Verifiable Delay Function (VDF) computation
  - Provides proof-of-time for blockchain security
  - Creates sequential, unpredictable randomness
  - Prevents short-range attacks and ensures fairness
- **VDF Implementation**: Uses chiavdf C++ library for performance
- **Network Coordination**: Multiple timelords coordinate for redundancy

### Network Architecture and Protocols

#### Peer-to-Peer Network
- **Protocols**: `/chia/protocols/` - Network communication protocols
  - `full_node_protocol.py` - Block and transaction propagation
  - `farmer_protocol.py` - Farming communication
  - `harvester_protocol.py` - Harvester coordination
  - `wallet_protocol.py` - Wallet synchronization
- **Network Stack**: Custom protocol over TCP with message authentication
- **Peer Discovery**: DNS seeding and peer exchange protocols
- **Node Types**: Full nodes, farmers, harvesters, wallets, timelords

#### RPC and API Architecture
- **RPC Services**: RESTful APIs for all major components
  - Full Node RPC: Block queries, mempool status, network info
  - Wallet RPC: Transaction creation, balance queries, key management
  - Farmer RPC: Farming status, reward tracking
  - Harvester RPC: Plot management, proof generation stats
- **WebSocket**: Real-time blockchain event streaming
- **Authentication**: Certificate-based mutual TLS authentication

### Frontend and User Interface

#### CLI Interface
- **Main CLI**: `/chia/cmds/chia.py` - Primary command-line interface
- **Component CLIs**: Dedicated CLIs for each service
  - `chia wallet` - Wallet operations
  - `chia farm` - Farming management
  - `chia plots` - Plot management
  - `chia keys` - Key management
  - `chia rpc` - Direct RPC access
- **Interactive Features**: Status displays, configuration management

#### GUI Architecture
- **Separate Repository**: `chia-blockchain-gui` (Electron-based)
- **Technology Stack**: React, TypeScript, Electron
- **API Integration**: Communicates with chia daemon via RPC
- **Features**: Wallet management, farming dashboard, plot creation

### Development Framework and Extensibility

#### Language and Technology Stack
- **Primary Language**: Python 3.9+ for core blockchain logic
- **Performance Components**: Rust (chia_rs) for cryptographic operations
- **Smart Contracts**: Chialisp functional programming language
- **Cryptographic Libraries**:
  - `chiapos` - Proof of Space implementation
  - `chiavdf` - Verifiable Delay Functions
  - `chia_rs` - Core cryptographic primitives
- **Database**: SQLite for local storage, efficient querying

#### Extensibility Points
- **Wallet Types**: Extensible wallet system for new asset types
  - Standard Wallet (XCH)
  - CAT Wallets (Chia Asset Tokens)
  - NFT Wallets
  - DID Wallets (Decentralized Identity)
  - VC Wallets (Verifiable Credentials)
- **RPC Extensions**: Custom RPC endpoints for specialized functionality
- **Plot Formats**: Pluggable plotter backend system
- **Consensus Rules**: Soft fork capability for protocol upgrades

#### Configuration and Deployment
- **Configuration**: YAML-based configuration system
- **Service Architecture**: Modular services with independent lifecycle
- **Deployment**: Docker support, systemd services, cross-platform installers
- **Monitoring**: Comprehensive logging and metrics collection

### Data Layer and Advanced Features

#### Data Layer
- **Distributed Database**: `/chia/data_layer/` - On-chain key-value storage
- **Merkle Trees**: Cryptographically verifiable data structures
- **Synchronization**: Multi-party data synchronization protocol

#### Pool Protocol
- **Pool Architecture**: `/chia/pools/` - Decentralized pooling system
- **Partial Proofs**: Low-difficulty proof submission
- **Payout System**: Fair reward distribution mechanisms

### Testing and Quality Assurance

#### Test Architecture
- **Unit Tests**: `/chia/_tests/` - Comprehensive test coverage
- **Integration Tests**: Full system integration testing
- **Simulation**: `/chia/simulator/` - Blockchain simulation for development
- **Performance Tests**: Load testing and benchmarking tools

#### Code Quality Tools
- **Linting**: ruff for code style enforcement
- **Type Checking**: mypy for static type analysis
- **Formatting**: ruff format for consistent code formatting
- **Pre-commit Hooks**: Automated quality checks