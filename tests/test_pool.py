"""Unit tests for the ooze.pool module"""

import ooze.pool


def create():
    return "MY-ITEM"


def teatdown(item):
    print(f"Tearing down item {item}")


def test_pool():
    # Given
    sut = ooze.pool.Pool(create, teatdown)

    # When
    with sut.item() as item:
        assert item == 'MY-ITEM'
        assert len(sut.items) == 0

    with sut.item() as item:
        assert item == 'MY-ITEM'
        assert len(sut.items) == 0

        with sut.item() as item_2:
            assert item == 'MY-ITEM'
            assert len(sut.items) == 0


    # Then
    assert len(sut.items) == 2
