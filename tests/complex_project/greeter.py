from typing import Callable

from ooze import provide


@provide('greeter')
class WelcomeWagon:
    def __init__(self, lower: Callable, address: dict, config):
        self.address = address
        self.lower = lower
        self.config = config

    def greet(self):
        return self.lower(f"Hello {self.address['name']}")

    @property
    def version(self):
        return self.config['version']


