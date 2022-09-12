#!/usr/bin/env python
"""Ooze - A _very_ simple dependency injector"""
import functools
import inspect
import os

import yaml


class DependencyNotAvailable:
    """Indication that dependency isn't in the graph"""


_STARTUP = DependencyNotAvailable
_INSTANCES = {}
_CLASSES_TO_INSTANTIATE = {}
_FACTORIES = {}


class InjectionError(Exception):
    """Error related to inject failures"""


class ConfigurationError(Exception):
    """Error related to reading configuration(s)"""


def run(startup_callable=None):
    """Look for a STARTUP callable and then run it the application by calling STARTUP."""
    startup_to_run = startup_callable if startup_callable else _STARTUP
    if startup_to_run is DependencyNotAvailable:
        raise InjectionError("No startup function assigned")
    _instantiate_objects()
    return _execute(startup_to_run)


def _instantiate_objects():
    """
    As the _provide_ decorators are encountered, if they are decorating classes, the classes
    are placed in an dictionary to be instantiated later.  This function instantiates those
    classes right before the application STARTUP function is called.
    """
    while True:
        new_objs = []
        for name in _CLASSES_TO_INSTANTIATE:
            requested_class = _CLASSES_TO_INSTANTIATE[name]
            try:
                obj = _execute(requested_class)
                _INSTANCES[name.lower()] = obj
                new_objs.append(name)
            except:
                pass
        if new_objs:
            for name in new_objs:
                del _CLASSES_TO_INSTANTIATE[name]
        else:
            break
    if _CLASSES_TO_INSTANTIATE:
        raise InjectionError(
            f"The following classes have missing dependencies: {', '.join(_CLASSES_TO_INSTANTIATE.keys())}")


def _execute(func):
    """Figure out what the func needs to run and then run it."""
    needed_args = inspect.signature(func)
    kwargs = {key: _resolve_dependency(key) for key in needed_args.parameters}
    missing_deps = [dep for dep in kwargs if kwargs[dep] is DependencyNotAvailable]
    if missing_deps:
        name = func.__name__
        raise InjectionError(f"Cannot execute {name} - Missing dependencies: {', '.join(missing_deps)}")
    return func(**kwargs)


def _resolve_dependency(dep_name: str):
    """Attempts to resolve the dependency"""
    resolvers = [_resolve_dependency_os_env, _resolve_dependency_instance, _resolve_dependency_factory,
                 _resolve_dependency_config]
    dep = DependencyNotAvailable
    for resolver in resolvers:
        dep = resolver(dep_name)
        if dep is not DependencyNotAvailable:
            break
    if dep is DependencyNotAvailable:
        raise InjectionError(f"{dep_name} not a valid dependency")
    return dep


def _resolve_dependency_instance(dep_name: str):
    return _INSTANCES.get(dep_name, DependencyNotAvailable)


def _resolve_dependency_factory(dep_name: str):
    factory_func = _FACTORIES.get(dep_name, DependencyNotAvailable)
    if factory_func is DependencyNotAvailable:
        return factory_func
    return _execute(factory_func)


def _resolve_dependency_os_env(dep_name: str):
    dep = os.environ.get(dep_name, DependencyNotAvailable)
    if dep is DependencyNotAvailable:
        dep = os.environ.get(dep_name.upper(), DependencyNotAvailable)
    if dep is DependencyNotAvailable:
        dep = os.environ.get(dep_name.lower(), DependencyNotAvailable)
    return dep


def _resolve_dependency_config(dep_name: str):
    filenames = ['application_settings.json', 'application_settings.yml', 'application_settings.yaml']
    if 'APPLICATION_SETTINGS' in os.environ:
        filenames = [os.environ['APPLICATION_SETTINGS']] + filenames
    for filename in filenames:
        try:
            with open(filename) as infile:
                extension = os.path.splitext(filename)[1]
                if extension in ['.json', '.yml', '.yaml']:
                    config = yaml.safe_load(infile)
                else:
                    raise ConfigurationError(f"Configuration files with {extension} extension not supported")
                if dep_name in config:
                    return config[dep_name]
        except FileNotFoundError:
            pass
    return DependencyNotAvailable


def startup(func):
    """A decorator that marks what the startup function should be in the app."""
    global _STARTUP
    if not callable(func):
        raise InjectionError('Startup must be callable')
    _STARTUP = func
    return func


def provide(name_or_item):
    """ A decorator to add a class, function or static value to the dependency graph."""
    if inspect.isclass(name_or_item):
        class_to_provide = name_or_item
        class_name = class_to_provide.__name__.lower()
        _CLASSES_TO_INSTANTIATE[class_name] = class_to_provide
        return class_to_provide
    elif inspect.isfunction(name_or_item):
        func_to_provide = name_or_item
        func_name = name_or_item.__name__.lower()
        _INSTANCES[func_name] = func_to_provide
        return func_to_provide
    else:
        def inner_provide(item):
            name = name_or_item.lower()
            if inspect.isclass(item):
                _CLASSES_TO_INSTANTIATE[name] = item
            else:
                _INSTANCES[name] = item
            return item

        return inner_provide


def provide_static(name: str, item):
    """Convenience method to add static values"""
    provide(name)(item)


def factory(name_or_item):
    """A decorator to add a factory to the dependency graph."""
    if callable(name_or_item):
        factory_func = name_or_item
        factory_name = factory_func.__name__.lower()
        _FACTORIES[factory_name] = factory_func
        return factory_func
    else:
        def inner_factory(item):
            inner_factory_func = item
            inner_factory_name = name_or_item
            _FACTORIES[inner_factory_name] = inner_factory_func
            return inner_factory_func

        return inner_factory


def resolve(name):
    """Retrieve an item from the dependency graph from outside a provided callable"""
    _instantiate_objects()
    return _resolve_dependency(name)


def magic(func):
    """Decorator that injects any parameters that aren't given by the non-ooze caller."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        needed_args = inspect.signature(func)
        if len(needed_args.parameters) <= len(args) + len(kwargs):
            return func(*args, **kwargs)
        ooze_kwargs = {}
        for idx, key in enumerate(needed_args.parameters.keys()):
            if idx < len(args):
                ooze_kwargs[key] = args[idx]
            elif key in kwargs:
                ooze_kwargs[key] = kwargs[key]
            else:
                ooze_kwargs[key] = resolve(key)
        return func(*[], **ooze_kwargs)

    return wrapper


class OozeBottlePlugin:
    api = 2

    def apply(self, callback, _):
        args = inspect.signature(callback)
        dependencies = {}

        for kw in args.parameters:
            try:
                dependencies[kw] = resolve(kw)
            except InjectionError:
                # Ignore injection error because other Bottle plugins may satisfy
                pass
        if not dependencies:
            return callback

        def wrapper(*args, **kwargs):
            kwargs = kwargs | dependencies
            return callback(*args, **kwargs)

        return wrapper
