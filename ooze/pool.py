"""Reusable pool context manager"""
import threading
from typing import Callable, Union


class PoolItem:
    def __init__(self, item, pool):
        self.item = item
        self.pool = pool

    def __enter__(self):
        return self.item

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.return_item(self.item)


class Pool:
    def __init__(self, create: Callable,
                 reclaim: Union[Callable, None] = None,
                 teardown: Union[Callable, None] = None,
                 pool_size: int = 5):
        self.create = create
        self.reclaim = reclaim
        self.teardown = teardown
        self.pool_size = pool_size
        self.items = []
        self._lock = threading.RLock()

    def __del__(self):
        with self._lock:
            if self.teardown:
                for item in self.items:
                    self.teardown(item)
            self.items = []

    def item(self):
        with self._lock:
            if self.items:
                return PoolItem(self.items.pop(0), self)
            else:
                return PoolItem(self.create(), self)

    def return_item(self, item):
        with self._lock:
            while len(self.items) >= self.pool_size:
                item = self.items.pop(0)
                if self.teardown:
                    self.teardown(item)
            if self.reclaim:
                self.reclaim(item)
            self.items.append(item)
