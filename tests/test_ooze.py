"""Testing ooze dependency injection."""
from unittest.mock import call

from tests.complex_project.greeter import WelcomeWagon
from tests.complex_project.shutdown import Shutdown
import ooze


@ooze.provide
def upper_case(string: str) -> str:
    return string.upper()


@ooze.provide('lower')
def lower_case(string: str) -> str:
    return string.lower()


ooze.provide('address')({
    "name": "Steve",
    "age": 50
})

ooze.provide('version')('1.0.0')


@ooze.provide
class System:
    def __init__(self, version: str, greeter: WelcomeWagon, shutdown: Shutdown):
        self.version = version
        self.greeter = greeter
        self.shutdown = shutdown

    def do_job(self):
        print(f"System version {self.version}")
        print(self.greeter.greet())
        print(self.shutdown.close())


@ooze.startup
def main(system: System):
    system.do_job()


def test_ooze(mocker):
    # Given
    mock_print = mocker.patch('builtins.print')

    # When
    ooze.run()

    # Then
    assert mock_print.call_args_list == [
        call('System version 1.0.0'),
        call('hello steve'),
        call('SHUTTING DOWN SYSTEM')
    ]
