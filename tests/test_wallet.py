from adacip.chain.fees import estimate_fee
from adacip.chain.rpc import RpcClient
from adacip.services.sync import SyncEngine
from adacip.services.wallet import WalletService


def test_create_vault_has_one_account(service: WalletService) -> None:
    vault = service.create_vault("test", "password")
    assert vault.name == "test"
    assert len(vault.accounts) == 1
    assert vault.accounts[0].address


def test_open_vault(service: WalletService) -> None:
    created = service.create_vault("test", "password")
    opened = service.open_vault(created.vault_id, "password")
    assert opened is not None
    assert opened.vault_id == created.vault_id


def test_open_missing(service: WalletService) -> None:
    assert service.open_vault("missing", "x") is None


def test_add_account(service: WalletService) -> None:
    service.create_vault("test", "password")
    account = service.add_account("password", "Savings")
    assert account.index == 1
    assert len(service.active.accounts) == 2


def test_add_without_vault_raises(service: WalletService) -> None:
    try:
        service.add_account("password", "Fail")
    except RuntimeError:
        return
    raise AssertionError("expected RuntimeError")


def test_unique_addresses(service: WalletService) -> None:
    service.create_vault("test", "password")
    service.add_account("password", "A")
    service.add_account("password", "B")
    addrs = {a.address for a in service.active.accounts}
    assert len(addrs) == 3


def test_sync_sets_balances(service: WalletService) -> None:
    vault = service.create_vault("test", "password")
    SyncEngine(service.config).sync(vault)
    assert vault.accounts[0].balance >= 0


def test_rpc_height(service: WalletService) -> None:
    height = RpcClient(service.config).get_height()
    assert height > 0


def test_fee_presets() -> None:
    assert estimate_fee("low") < estimate_fee("high")
