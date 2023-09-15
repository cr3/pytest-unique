"""Unit tests for the count module."""
import pytest

from pytest_unique.count import file_count, memory_count


@pytest.fixture
def countfile(tmp_path):
    """Create a file in a temp dir."""
    path = tmp_path / "countdir"
    path.mkdir()
    yield path / "countfile"


def test_file_count_next(countfile):
    """Next should return the next count from file."""
    count = file_count(countfile)
    assert next(count) == 0
    assert next(count) == 1


def test_file_count_error(countfile):
    """Next should raise a ValueError exception with an invalid countfile."""
    countfile.write_text("test")
    count = file_count(countfile)
    with pytest.raises(ValueError):
        next(count)


def test_memory_count_next():
    """Next should return the next count from memory."""
    count = memory_count()
    assert next(count) == 0
    assert next(count) == 1
