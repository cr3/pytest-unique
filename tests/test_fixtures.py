"""Unit tests for the fixtures module."""


def test_unique_in_memory(unique_in_memory):
    """The unique in-memory fixture should return unique values."""
    assert unique_in_memory("bytes") != unique_in_memory("bytes")


def test_unique_in_file(unique_in_file):
    """The unique in-file fixture should return unique values."""
    assert unique_in_file("bytes") != unique_in_file("bytes")
