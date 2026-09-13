from adacip.crypto.address import public_key_to_address, validate_address
from adacip.crypto.keys import derive_key, fingerprint, seed_from_mnemonic
from adacip.crypto.mnemonic import generate_mnemonic, validate_mnemonic


def test_seed_is_stable() -> None:
    assert seed_from_mnemonic("demo") == seed_from_mnemonic("demo")


def test_seed_changes_with_passphrase() -> None:
    assert seed_from_mnemonic("demo", "a") != seed_from_mnemonic("demo", "b")


def test_seed_length() -> None:
    assert len(seed_from_mnemonic("hello")) == 64


def test_derive_is_stable() -> None:
    seed = seed_from_mnemonic("demo")
    assert derive_key(seed, 0, "m/0") == derive_key(seed, 0, "m/0")


def test_derive_index_changes_key() -> None:
    seed = seed_from_mnemonic("demo")
    a, _ = derive_key(seed, 0, "m/0")
    b, _ = derive_key(seed, 1, "m/0")
    assert a != b


def test_fingerprint_length() -> None:
    assert len(fingerprint(b"abc")) == 8


def test_address_roundtrip() -> None:
    seed = seed_from_mnemonic("round")
    _, pub = derive_key(seed, 0, "m/0")
    address = public_key_to_address(pub)
    assert validate_address(address)


def test_mnemonic_generate_12() -> None:
    phrase = generate_mnemonic(12, "vault")
    assert len(phrase.split()) == 12
    assert validate_mnemonic(phrase)
