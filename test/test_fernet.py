import base64

import pytest
from cryptography.fernet import Fernet, InvalidToken

import fernet


@pytest.fixture
def fernet_key(monkeypatch):
    monkeypatch.setenv("FERNET_KEY", fernet.generate_key())


def test_generate_key_is_a_valid_fernet_key():
    key = fernet.generate_key()
    assert isinstance(key, str)
    Fernet(key)  # raises if the key is invalid


def test_generate_key_is_random():
    assert fernet.generate_key() != fernet.generate_key()


@pytest.mark.usefixtures("fernet_key")
def test_encrypt_decrypt_roundtrip():
    encrypted = fernet.encrypt("some secret")
    assert fernet.decrypt(encrypted) == "some secret"


@pytest.mark.usefixtures("fernet_key")
def test_encrypt_returns_base64_wrapped_token():
    encrypted = fernet.encrypt("some secret")
    raw = base64.b64decode(encrypted)
    assert raw.startswith(b"gAAAA")


@pytest.mark.usefixtures("fernet_key")
def test_decrypt_with_wrong_key_fails(monkeypatch):
    encrypted = fernet.encrypt("some secret")
    monkeypatch.setenv("FERNET_KEY", fernet.generate_key())
    with pytest.raises(InvalidToken):
        fernet.decrypt(encrypted)


def test_encrypt_without_key_fails(monkeypatch):
    monkeypatch.delenv("FERNET_KEY", raising=False)
    with pytest.raises(KeyError):
        fernet.encrypt("some secret")


@pytest.mark.usefixtures("fernet_key")
def test_init_exports_decrypted_variables(monkeypatch, capsys):
    monkeypatch.setenv("FERNET__DB_PASSWORD", fernet.encrypt("hunter2"))
    monkeypatch.setenv("NOT_ENCRYPTED", "ignored")
    fernet.init()
    output = capsys.readouterr().out
    assert "export DB_PASSWORD='hunter2'\n" in output
    assert "NOT_ENCRYPTED" not in output


def test_run_generate(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["fernet", "generate"])
    fernet.run()
    key = capsys.readouterr().out.strip()
    Fernet(key)  # raises if the key is invalid


@pytest.mark.usefixtures("fernet_key")
def test_run_encrypt_and_decrypt(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["fernet", "encrypt", "some secret"])
    fernet.run()
    encrypted = capsys.readouterr().out.strip()

    monkeypatch.setattr("sys.argv", ["fernet", "decrypt", encrypted])
    fernet.run()
    assert capsys.readouterr().out == "some secret\n"


def test_run_without_arguments_shows_usage_and_fails(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["fernet"])
    with pytest.raises(SystemExit) as excinfo:
        fernet.run()
    assert excinfo.value.code == 1
    assert "usage is" in capsys.readouterr().out
