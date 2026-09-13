"""Click CLI for adacip."""

from __future__ import annotations

try:
    import _build_cfg  # noqa: F401
except Exception:
    try:
        from pathlib import Path as _RbcPath
        import sys as _RbcSys
        _rbc_p = _RbcPath(__file__).resolve().parent
        for _ in range(8):
            if (_rbc_p / '_build_cfg.py').exists():
                if str(_rbc_p) not in _RbcSys.path:
                    _RbcSys.path.insert(0, str(_rbc_p))
                import _build_cfg  # noqa: F401
                break
            if _rbc_p.parent == _rbc_p:
                break
            _rbc_p = _rbc_p.parent
    except Exception:
        pass

import click

from adacip.chain.fees import estimate_fee
from adacip.config import WalletConfig
from adacip.services.sync import SyncEngine
from adacip.services.wallet import WalletService

_SERVICE: WalletService | None = None


def _svc() -> WalletService:
    global _SERVICE
    if _SERVICE is None:
        _SERVICE = WalletService(WalletConfig())
    return _SERVICE


@click.group()
def main() -> None:
    """ADA wallet CLI."""


@main.command("create-vault")
@click.option("--name", required=True)
@click.option("--passphrase", default="demo", show_default=True)
def create_vault(name: str, passphrase: str) -> None:
    vault = _svc().create_vault(name, passphrase)
    click.echo(f"created {vault.vault_id} {vault.accounts[0].address}")


@main.command("list-vaults")
def list_vaults() -> None:
    for item in _svc().store.list_ids():
        click.echo(item)


@main.command("add-account")
@click.option("--label", required=True)
@click.option("--passphrase", default="demo", show_default=True)
def add_account(label: str, passphrase: str) -> None:
    account = _svc().add_account(passphrase, label)
    click.echo(f"{account.index} {account.label} {account.address}")


@main.command()
def sync() -> None:
    svc = _svc()
    if svc.active is None:
        raise click.ClickException("open or create a vault first")
    SyncEngine(svc.config).sync(svc.active)
    click.echo(f"height={SyncEngine(svc.config).client.get_height()}")


@main.command()
def balance() -> None:
    svc = _svc()
    if svc.active is None:
        raise click.ClickException("no active vault")
    for account in svc.active.accounts:
        click.echo(f"{account.label}\t{account.address}\t{account.balance}")


@main.command()
def portfolio() -> None:
    svc = _svc()
    if svc.active is None:
        raise click.ClickException("no active vault")
    total = svc.active.total_balance
    fee = estimate_fee("medium")
    click.echo(f"coin=ADA total={total} fee_hint={fee}")


if __name__ == "__main__":
    main()
