"""Unit tests for Assignment 8 advanced tree structures.

The methods under test are shells that initially raise ``NotImplementedError``.
The behaviour tests are marked ``xfail`` so the suite stays green until the
assignment is implemented; once a method is filled in, its test will pass.
"""

import pytest

from data_structures.assignment8 import avl_tree, trie


# -- avl_tree tests --


class TestAVLTree:
    def test_new_tree_is_empty(self):
        t = avl_tree()
        assert len(t) == 0
        assert t.root is None

    @pytest.mark.xfail(reason="avl_tree.insert not yet implemented")
    def test_insert_increases_size(self):
        t = avl_tree()
        t.insert(10)
        t.insert(20)
        assert len(t) == 2

    @pytest.mark.xfail(reason="avl_tree.contains not yet implemented")
    def test_contains_finds_inserted_values(self):
        t = avl_tree()
        for v in [10, 20, 5, 6, 15]:
            t.insert(v)
        assert t.contains(15) is True
        assert t.contains(99) is False

    @pytest.mark.xfail(reason="avl_tree.insert must keep tree balanced")
    def test_tree_stays_balanced_on_sorted_insert(self):
        t = avl_tree()
        for v in range(1, 8):  # 7 ascending inserts would be linear w/o balancing
            t.insert(v)
        # A balanced tree with 7 nodes has height 3.
        assert t.height() == 3


# -- trie tests --


class TestTrie:
    def test_new_trie_is_empty(self):
        t = trie()
        assert len(t) == 0

    @pytest.mark.xfail(reason="trie.insert not yet implemented")
    def test_insert_increases_size(self):
        t = trie()
        t.insert("cat")
        t.insert("car")
        assert len(t) == 2

    @pytest.mark.xfail(reason="trie.contains not yet implemented")
    def test_contains_finds_full_words_only(self):
        t = trie()
        t.insert("cat")
        assert t.contains("cat") is True
        assert t.contains("ca") is False

    @pytest.mark.xfail(reason="trie.starts_with not yet implemented")
    def test_starts_with_finds_prefixes(self):
        t = trie()
        t.insert("cat")
        assert t.starts_with("ca") is True
        assert t.starts_with("do") is False
