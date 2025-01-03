"""Unit tests for the unique module."""

import string
from uuid import UUID

import pytest
from hamcrest import (
    assert_that,
    is_,
    matches_regexp,
)

from pytest_unique.unique import (
    Unique,
    unique_bytes,
    unique_digits,
    unique_email,
    unique_float,
    unique_integer,
    unique_password,
    unique_text,
    unique_uuid,
)


def test_unique_get_plugin_with_match():
    """Getting a plugin with a match should return a plugin."""
    unique = Unique(registry={"pytest_unique": {"test": lambda u: "test"}})
    plugin = unique.get_plugin("test")
    assert plugin() == "test"


def test_unique_get_plugin_without_match():
    """Getting a plugin without a match in the registry should raise."""
    with pytest.raises(KeyError):
        Unique(registry={"pytest_unique": {}}).get_plugin("test")


def test_unique_get_plugin_without_plugins():
    """Getting a plugin without plugins in the registry should raise."""
    with pytest.raises(KeyError):
        Unique(registry={}).get_plugin("test")


@pytest.mark.parametrize(
    "name, matches",
    [
        ("bytes", is_(bytes)),
        ("digits", matches_regexp(r"^\d+$")),
        ("email", matches_regexp(r".*@.*")),
        ("float", is_(float)),
        ("integer", is_(int)),
        ("password", is_(str)),
        ("text", is_(str)),
        ("uuid", is_(UUID)),
    ],
)
def test_unique_types(name, matches, unique):
    """Unique fixtures should return expected types."""
    assert_that(unique(name), matches)


@pytest.mark.parametrize(
    "plugin",
    [
        pytest.param(unique_bytes, id="bytes"),
        pytest.param(unique_digits, id="digits"),
        pytest.param(unique_email, id="email"),
        pytest.param(unique_float, id="float"),
        pytest.param(unique_integer, id="integer"),
        pytest.param(unique_password, id="password"),
        pytest.param(unique_text, id="text"),
        pytest.param(unique_uuid, id="uuid"),
    ],
)
def test_unique_plugin_twice(plugin, unique):
    """Calling any plugin twice should not return the same value."""
    assert plugin(unique) != plugin(unique)


@pytest.mark.parametrize(
    "plugin",
    [
        pytest.param(unique_bytes, id="bytes"),
        pytest.param(unique_digits, id="digits"),
        pytest.param(unique_email, id="email"),
        pytest.param(unique_float, id="float"),
        pytest.param(unique_integer, id="integer"),
        pytest.param(unique_text, id="text"),
        pytest.param(unique_uuid, id="uuid"),
    ],
)
def test_unique_plugin_sequential(plugin, unique):
    """Calling most plugins twice should return sequential values."""
    assert plugin(unique) < plugin(unique)


def test_unique_bytes_encoding(unique):
    """Unique bytes should raise when decoded to UTF-8."""
    with pytest.raises(UnicodeDecodeError):
        unique("bytes").decode("utf-8")


def test_unique_email_prefix(unique):
    """A unique email with a prefix should start with that prefix."""
    email = unique_email(unique, prefix="with-my-prefix")
    assert email.startswith("with-my-prefix")


def test_unique_email_suffix(unique):
    """A unique email with a suffix should use suffix before domain."""
    email = unique_email(unique, suffix="with-my-suffix")
    assert email.endswith("with-my-suffix@example.com")


def test_unique_integer_args(unique):
    """A unique integer with bits should be within that number of bits."""
    base = 1
    mod = 2
    for _ in range(mod + 1):
        integer = unique_integer(unique, base=base, mod=mod)
        assert integer >= base
        assert integer < base + mod


@pytest.mark.parametrize(
    "kwargs, chars",
    [
        pytest.param({"lowercase": 1}, string.ascii_lowercase, id="lowercase"),
        pytest.param({"uppercase": 1}, string.ascii_uppercase, id="uppercase"),
        pytest.param({"digits": 1}, string.digits, id="digits"),
        pytest.param({"punctuation": 1}, string.punctuation, id="punctuation"),
    ],
)
def test_unique_password(kwargs, chars, unique):
    """A unique password with a type of character should contain it."""
    password = unique_password(unique, **kwargs)
    assert set(password).intersection(chars)


def test_unique_text_prefix(unique):
    """Unique text with a prefix should start with that prefix."""
    text = unique_text(unique, prefix="with-my-prefix")
    assert text.startswith("with-my-prefix")


def test_unique_text_suffix(unique):
    """Unique text with a suffix should end with that suffix."""
    text = unique_text(unique, suffix="with-my-suffix")
    assert text.endswith("with-my-suffix")


def test_unique_text_separator(unique):
    """Unique text with a separator should use it."""
    text = unique_text(unique, separator="*")
    assert "*" in text


@pytest.mark.parametrize(
    "limit",
    [
        1,
        2,
        4,
        8,
    ],
)
def test_unique_text_fields(limit, unique):
    """Unique text with a limit should truncate the text."""
    text = unique_text(unique, limit=limit)
    assert len(text) == limit


def test_unique_uuid_fields(unique):
    """A unique UUID should have all fields set to 0 except the last one."""
    uuid = unique_uuid(unique)
    for field in uuid.fields[:-2]:
        assert field == 0
    assert uuid.fields[-1] != 0


def test_unique_uuid_integer(unique):
    """A unique UUID with an integer should use that integer."""
    uuid = unique_uuid(unique, 0)
    assert str(uuid) == "00000000-0000-0000-0000-000000000000"


def test_unique_name_argument():
    """A unique plugin should be able to pass a `name` argument."""
    unique = Unique(registry={"pytest_unique": {"test": lambda u, name: name}})
    assert unique("test", name="test") == "test"
