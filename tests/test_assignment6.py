"""Unit tests for Assignment 6 ``hash_table``.

The methods under test are shells that initially raise ``NotImplementedError``.
The behaviour tests are marked ``xfail`` so the suite stays green until the
assignment is implemented; once a method is filled in, its test will pass.
"""

import pytest

from data_structures.assignment6 import hash_table


class TestHashTable:
    def test_new_table_is_empty(self):
        t = hash_table()
        assert len(t) == 0
        assert t.capacity == 16

    @pytest.mark.xfail(reason="hash_table.put not yet implemented")
    def test_put_increases_size(self):
        t = hash_table()
        t.put("a", 1)
        t.put("b", 2)
        assert len(t) == 2

    @pytest.mark.xfail(reason="hash_table.get not yet implemented")
    def test_get_returns_stored_value(self):
        t = hash_table()
        t.put("a", 1)
        assert t.get("a") == 1

    @pytest.mark.xfail(reason="hash_table.get not yet implemented")
    def test_get_missing_key_returns_none(self):
        t = hash_table()
        assert t.get("missing") is None

    @pytest.mark.xfail(reason="hash_table.put not yet implemented")
    def test_put_updates_existing_key(self):
        t = hash_table()
        t.put("a", 1)
        t.put("a", 99)
        assert t.get("a") == 99
        assert len(t) == 1

    @pytest.mark.xfail(reason="hash_table.remove not yet implemented")
    def test_remove_returns_true_when_present(self):
        t = hash_table()
        t.put("a", 1)
        assert t.remove("a") is True
        assert t.get("a") is None
        assert len(t) == 0

    @pytest.mark.xfail(reason="hash_table.remove not yet implemented")
    def test_remove_returns_false_when_absent(self):
        t = hash_table()
        assert t.remove("missing") is False
