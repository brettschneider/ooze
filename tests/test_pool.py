"""Unit tests for the ooze.pool module"""

import ooze.pool


class SampleThing:
    def __init__(self):
        self.closed = False
        self.allocated = False


def create_item():
    item = SampleThing()
    item.allocated = True
    return item


def reclaim_item(item):
    item.allocated = False


def teardown_item(item):
    item.closed = True


def test_pool():
    # Given
    sut = ooze.pool.Pool(create_item, reclaim_item, teardown_item)

    # When
    with sut.item() as item:
        assert item.allocated
        assert not item.closed
        assert len(sut.items) == 0
        extra_item_reference = item

    assert not extra_item_reference.allocated

    with sut.item() as item:
        assert not item.closed
        assert len(sut.items) == 0
        extra_item_reference = item

        with sut.item() as item_2:
            assert item_2.allocated
            assert not item_2.closed
            assert len(sut.items) == 0
            extra_item_reference_2 = item_2

    assert len(sut.items) == 2
    assert not extra_item_reference.allocated
    assert not extra_item_reference_2.allocated

    # Then
    del sut
    assert extra_item_reference.closed
    assert extra_item_reference_2.closed


def test_pool_size():
    # Given
    sut = ooze.pool.Pool(create_item, reclaim_item, teardown_item, 1)

    # When
    with sut.item() as _:
        with sut.item() as _:  # Create second item
            pass

    # Then
    assert len(sut.items) == 1  # Assert pool on grew to size 1
