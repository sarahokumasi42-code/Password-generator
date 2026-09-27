import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pytest
from password_generator import (
    generate_password,
    generate_passphrase,
    password_strength,
)


def test_default_length():
    assert len(generate_password()) == 12


def test_custom_length():
    assert len(generate_password(length=32)) == 32


def test_contains_all_selected_types():
    pwd = generate_password(length=20)
    assert any(c.islower() for c in pwd)
    assert any(c.isupper() for c in pwd)
    assert any(c.isdigit() for c in pwd)
    assert any(not c.isalnum() for c in pwd)


def test_only_digits():
    pwd = generate_password(
        length=10, use_lowercase=False, use_uppercase=False, use_symbols=False
    )
    assert pwd.isdigit()


def test_invalid_length_raises():
    with pytest.raises(ValueError):
        generate_password(length=2)
    with pytest.raises(ValueError):
        generate_password(length=200)


def test_no_charset_raises():
    with pytest.raises(ValueError):
        generate_password(
            use_lowercase=False,
            use_uppercase=False,
            use_digits=False,
            use_symbols=False,
        )


def test_exclude_ambiguous():
    for _ in range(50):
        pwd = generate_password(length=20, exclude_ambiguous=True)
        assert not any(c in "il1Lo0O" for c in pwd)


def test_passwords_are_unique():
    passwords = {generate_password() for _ in range(100)}
    assert len(passwords) == 100


def test_passphrase():
    phrase = generate_passphrase(word_count=5)
    assert len(phrase.split("-")) == 5


def test_strength_weak():
    result = password_strength("abc")
    assert result["label"] in ("Very Weak", "Weak")


def test_strength_strong():
    result = password_strength("Abcd1234!@#$")
    assert result["label"] in ("Strong", "Very Strong")