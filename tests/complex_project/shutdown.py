from typing import Callable

from ooze import provide


@provide
class Shutdown:
    def __init__(self, upper_case: Callable):
        self.upper_case = upper_case

    def close(self):
        return self.upper_case('shutting down system')


