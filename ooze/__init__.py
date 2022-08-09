#!/usr/bin/env python
"""Ooze - A _very_ simple dependency injector"""
import inspect
import sys


class DependencyNotAvailable:
    """Indication that dependency isn't in the graph"""


_STARTUP = DependencyNotAvailable
_INSTANCES = {}
_CLASSES_TO_INSTANTIATE = {}


class InjectionError(Exception):
    """Simple_inject specific exception"""


def run():
    """Look for a STARTUP callable and then run it the application by calling STARTUP."""
    if _STARTUP is DependencyNotAvailable:
        raise InjectionError("No startup function assigned")
    _instantiate_objects()
    _execute(_STARTUP)


def _instantiate_objects():
    """
    As the _provide_ decorators are encountered, if they are decorating classes, the classes
    are placed in an dictionary to be instantiated later.  This function instantiates those
    classes right before the application STARTUP function is called.
    :return:
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
    kwargs = {key: _INSTANCES.get(key, DependencyNotAvailable) for key in needed_args.parameters}
    missing_deps = [dep for dep in kwargs if kwargs[dep] is DependencyNotAvailable]
    if missing_deps:
        name = func.__name__
        raise InjectionError(f"Cannot execute {name} - Missing dependencies: {', '.join(missing_deps)}")
    return func(**kwargs)


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
        class_name = class_to_provide.__name__
        _CLASSES_TO_INSTANTIATE[class_name] = class_to_provide
        return class_to_provide
    elif inspect.isfunction(name_or_item):
        func_to_provide = name_or_item
        func_name = name_or_item.__name__
        _INSTANCES[func_name] = func_to_provide
        return func_to_provide
    else:
        def inner_provide(item):
            name = name_or_item
            if inspect.isclass(item):
                _CLASSES_TO_INSTANTIATE[name] = item
            else:
                _INSTANCES[name] = item
            return item

        return inner_provide
