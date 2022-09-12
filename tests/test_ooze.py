"""Testing ooze dependency injection."""
import os
from io import BytesIO
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


@ooze.factory('config')
def load_config(version):
    return {
        'version': version,
        'url': 'https://github.com/brettschneider/ooze/issues'
    }


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


@ooze.magic
def greet(hostname: str, config: dict):
    return f"Hostname: {hostname}, Version: {config['version']}"


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
    assert exc_info.value.args[0] == 'itza-notta-thera not a valid dependency'


def test_factory():
    # Given
    greeter = ooze.resolve('greeter')

    # When
    result = greeter.version

    # Then
    assert result == '1.0.0'


def test_environment_resolution():
    # Given
    os.environ['URL'] = 'https://github.com/'

    # When
    result = ooze.resolve('url')

    # Then
    assert result == 'https://github.com/'


def test_config_resolution_json(mocker):
    # Given
    mock_open = mocker.patch('ooze.open')
    mock_open.side_effect = [
        BytesIO(bytes('{"json_url": "https://github.com"}', 'utf-8')),
        FileNotFoundError,
        FileNotFoundError
    ]

    # When
    result = ooze.resolve('json_url')

    # Then
    assert result == "https://github.com"
    mock_open.assert_called_with('application_settings.json')


def test_config_resolution_yaml(mocker):
    # Given
    mock_open = mocker.patch('ooze.open')
    mock_open.side_effect = [
        FileNotFoundError,
        BytesIO(bytes("""
        yaml_url: https://github.com
        """, 'utf-8')),
        FileNotFoundError
    ]

    # When
    result = ooze.resolve('yaml_url')

    # Then
    assert result == "https://github.com"
    mock_open.assert_called_with('application_settings.yml')


def test_config_resolution_file_not_found(mocker):
    # Given
    mock_open = mocker.patch('ooze.open')
    mock_open.side_effect = [
        FileNotFoundError,
        FileNotFoundError,
        FileNotFoundError
    ]

    # When
    with pytest.raises(ooze.InjectionError) as exc_info:
        ooze.resolve('fnf_url')

    # Then
    assert exc_info.value.args[0] == 'fnf_url not a valid dependency'


def test_config_resolution_manual_file(mocker):
    # Given
    os.environ['APPLICATION_SETTINGS'] = '/tmp/app.yaml'
    mock_open = mocker.patch('ooze.open')
    mock_open.side_effect = [
        BytesIO(bytes('{"manual_url": "https://github.com"}', 'utf-8')),
        FileNotFoundError,
        FileNotFoundError,
        FileNotFoundError
    ]

    # When
    result = ooze.resolve('manual_url')

    # Then
    assert result == 'https://github.com'
    mock_open.assert_called_with('/tmp/app.yaml')


def test_magic_resolves():
    # Given
    name = 'localhost'

    # When
    result = greet(name)

    # Then
    assert result == 'Hostname: localhost, Version: 1.0.0'


def test_magic_doesnt_resolve():
    # Given
    name = 'localhost'
    config = {'version': '2.0.0'}

    # When
    result = greet(name, config)

    # Then
    assert result == 'Hostname: localhost, Version: 2.0.0'


def test_magic_fails_as_expected():
    # Given

    # When
    with pytest.raises(ooze.InjectionError) as exc_info:
        greet()

    # Then
    assert exc_info.value.args[0] == 'hostname not a valid dependency'
