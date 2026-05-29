"""Unit tests for Assignment 2 data structures (``stack`` and ``queue``).

The methods under test are shells that initially raise ``NotImplementedError``.
The behaviour tests are marked ``xfail`` so the suite stays green until the
assignment is implemented; once a method is filled in, its test will pass.
"""

import pytest

from data_structures.assignment2 import stack, queue


# -- stack tests --


class TestStack:
    def test_new_stack_is_empty(self):
        s = stack()
        assert len(s) == 0

    @pytest.mark.xfail(reason="stack.push not yet implemented")
    def test_push_increases_length(self):
        s = stack()
        s.push(10)
        s.push(20)
        assert len(s) == 2

    @pytest.mark.xfail(reason="stack.pop not yet implemented")
    def test_pop_returns_last_pushed(self):
        s = stack()
        s.push(1)
        s.push(2)
        assert s.pop() == 2
        assert len(s) == 1

    @pytest.mark.xfail(reason="stack.peek not yet implemented")
    def test_peek_returns_top_without_removing(self):
        s = stack()
        s.push(1)
        s.push(2)
        assert s.peek() == 2
        assert len(s) == 2


# -- queue tests --


class TestQueue:
    def test_new_queue_is_empty(self):
        q = queue()
        assert len(q) == 0

    @pytest.mark.xfail(reason="queue.enqueue not yet implemented")
    def test_enqueue_increases_length(self):
        q = queue()
        q.enqueue(10)
        q.enqueue(20)
        assert len(q) == 2

    @pytest.mark.xfail(reason="queue.dequeue not yet implemented")
    def test_dequeue_returns_first_enqueued(self):
        q = queue()
        q.enqueue(1)
        q.enqueue(2)
        assert q.dequeue() == 1
        assert len(q) == 1

    @pytest.mark.xfail(reason="queue.peek not yet implemented")
    def test_peek_returns_front_without_removing(self):
        q = queue()
        q.enqueue(1)
        q.enqueue(2)
        assert q.peek() == 1
        assert len(q) == 2
