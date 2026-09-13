# cardano-cip1852

> ada · cip-1852 · stake

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)]()

Cardano CIP-1852 derive shell — payment and stake tags.

## Features

- HD derivation along m/1852'/1815'/0' for ADA
- Passphrase-wrapped vault stored as local JSON
- Deterministic address codec (SHA-256 simulation, no live keys)
- Fee estimator with low / medium / high presets
- Balance sync against a stub RPC client
- Click CLI with vault, account and portfolio commands

## Prerequisites

- Python 3.11+
- Git

## Getting Started

```bash
git clone <repo-url>
cd cardano-cip1852
python -m pip install -e .
python -m adacip --help
```

## CLI Usage

```bash
adacip create-vault --name "Main"
# Create an encrypted local vault

adacip list-vaults
# List vault files in the storage directory

adacip add-account --label Savings
# Derive the next HD account

adacip sync
# Refresh stub balances

adacip balance
# Print account table

adacip portfolio
# Show coin + stub USD total
```

## Project Structure

```
adacip/
  crypto/          seed, derive, address
  chain/           stub RPC and fee table
  storage/         vault JSON
  services/        wallet + sync
  cli.py           click entry
tests/             pytest
```

## Configuration

Defaults live in `adacip/config.py` (`WalletConfig`).

| Setting | Default | Description |
|---------|---------|-------------|
| `network` | `mainnet` | mainnet / testnet |
| `rpc_endpoint` | `http://127.0.0.1:8090` | ADA node URL (unused in stub mode) |
| `storage_dir` | `.wallets` | Local vault directory |
| `derivation_path` | `m/1852'/1815'/0'` | BIP path |

## Tests

```bash
python -m pytest -q
```

## Background

ADA Python starters search cip1852, not cosmos-wallet.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.


---

## Topics

![cardano](https://img.shields.io/badge/cardano-111827?style=flat-square) ![cip1852](https://img.shields.io/badge/cip1852-111827?style=flat-square) ![cardano-cip1852](https://img.shields.io/badge/cardano%20cip1852-111827?style=flat-square) ![cryptocurrency](https://img.shields.io/badge/cryptocurrency-111827?style=flat-square) ![wallet](https://img.shields.io/badge/wallet-111827?style=flat-square) ![blockchain](https://img.shields.io/badge/blockchain-111827?style=flat-square) ![web3](https://img.shields.io/badge/web3-111827?style=flat-square) ![bitcoin](https://img.shields.io/badge/bitcoin-111827?style=flat-square)

`cardano` `cip1852` `cardano-cip1852` `cryptocurrency` `wallet` `blockchain` `web3` `bitcoin` `ethereum` `hd-wallet` `open-source` `python`

Search: cardano-cip1852 · ada · cip-1852 · stake · Cardano CIP-1852 derive shell — payment and stake tags.

---

<sub>Cardano CIP-1852 derive shell — payment and stake tags.</sub>
