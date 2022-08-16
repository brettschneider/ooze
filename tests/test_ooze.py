"""Testing ooze dependency injection."""
from unittest.mock import call

import pytest

from tests.complex_project.greeter import WelcomeWagon
from tests.complex_project.shutdown import Shutdown
import ooze


@ooze.provide
def upper_case(string: str) -> str:
    return string.upper()


@ooze.provide('lower')
def lower_case(string: str) -> str:
    return string.lower()


ooze.provide_static('address', {
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
        print(self.shutdown.close())
        return 1

    def do_other_job(self):
        print(self.greeter.greet())
        print(self.shutdown.close())
        return 2


@ooze.startup
def tagged_main(system: System):
    return system.do_job()


def untagged_main(system: System):
    return system.do_other_job()


def test_ooze_with_tagged_main(mocker):
    # Given
    mock_print = mocker.patch('builtins.print')

    # When
    result = ooze.run()

    # Then
    assert result == 1
    assert mock_print.call_args_list == [
        call('System version 1.0.0'),
        call('SHUTTING DOWN SYSTEM')
    ]


def test_ooze_with_untagged_main(mocker):
    # Given
    mock_print = mocker.patch('builtins.print')

    # When
    result = ooze.run(untagged_main)

    # Then
    assert result == 2
    assert mock_print.call_args_list == [
        call('hello steve'),
        call('SHUTTING DOWN SYSTEM')
    ]


def test_resolve():
    # Given
    greeter = ooze.resolve('greeter')

    # When
    result = greeter.greet()

    # Then
    assert result == 'hello steve'


def test_resolve_not_present():
    # When
    with pytest.raises(ooze.InjectionError) as exc_info:
        ooze.resolve('itza-notta-thera')

    # Then
    assert exc_info.value.args[0] == 'itza-notta-thera not present in container'
