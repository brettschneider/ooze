from typing import Callable

from ooze import provide


@provide('greeter')
class WelcomeWagon:
    def __init__(self, lower: Callable, address: dict):
        self.address = address
        self.lower = lower

    def greet(self):
        return self.lower(f"Hello {self.address['name']}")


