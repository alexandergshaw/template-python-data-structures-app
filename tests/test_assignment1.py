"""Unit tests for Assignment 1 data structures (``array`` and ``linked_list``).

The methods under test are shells that initially raise ``NotImplementedError``.
The behaviour tests are marked ``xfail`` so the suite stays green until the
assignment is implemented; once a method is filled in, its test will pass.
"""

import pytest

from data_structures.assignment1 import array, linked_list


# -- array tests --


class TestArray:
    def test_new_array_is_empty(self):
        arr = array(5)
        assert len(arr) == 0
        assert arr.capacity == 5

    @pytest.mark.xfail(reason="array.append not yet implemented")
    def test_append_increases_length(self):
        arr = array(3)
        arr.append(10)
        assert len(arr) == 1

    @pytest.mark.xfail(reason="array.get not yet implemented")
    def test_get_returns_stored_value(self):
        arr = array(3)
        arr.append(10)
        assert arr.get(0) == 10

    @pytest.mark.xfail(reason="array.set not yet implemented")
    def test_set_updates_value(self):
        arr = array(3)
        arr.append(10)
        arr.set(0, 99)
        assert arr.get(0) == 99


# -- linked_list tests --


class TestLinkedList:
    def test_new_list_is_empty(self):
        ll = linked_list()
        assert len(ll) == 0
        assert ll.head is None

    @pytest.mark.xfail(reason="linked_list.append not yet implemented")
    def test_append_increases_length(self):
        ll = linked_list()
        ll.append(1)
        ll.append(2)
        assert len(ll) == 2

    @pytest.mark.xfail(reason="linked_list.prepend not yet implemented")
    def test_prepend_sets_head(self):
        ll = linked_list()
        ll.prepend(1)
        ll.prepend(2)
        assert ll.head.value == 2
        assert len(ll) == 2

    @pytest.mark.xfail(reason="linked_list.find not yet implemented")
    def test_find_locates_value(self):
        ll = linked_list()
        ll.append(1)
        ll.append(2)
        assert ll.find(2) is True
        assert ll.find(99) is False
