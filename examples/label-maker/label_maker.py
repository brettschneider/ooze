#!/usr/bin/env python
"""
This example script reads a csv text file that contains contact information
and transforms each row into an address label.  It demonstrates use of the
following Ooze topics:

* Ooze factories (the @ooze.factory decorator)
* Ooze dependency injection (the @ooze.provide decorator)
* Ooze reasing a config file (see filename, default arguement and the
  application_settings.yaml file)
* Ooze partial injection (the @ooze.magic decorator)

This example has no dependencies beyond the Ooze package.  Everything
else that this example relies upon is avaialbel in the Python standard
library.
"""
import ooze
import os
import sys


@ooze.magic
def generate_labels(filename, file_reader, file_mapper):
    """
    Since this method is decorated with the @ooze.magic decorator you
    can call it without passing any arguments.  Ooze will try to 
    find dependencies in the dependency graph and will pass them in
    for you.  See line 101. 
    """
    if not filename:
        return
    file_lines = file_reader(filename)
    file_mapper(file_lines)


@ooze.factory
def filename(defaults):
    """
    This function is decorated with teh @ooze.factory decorator.  Every
    time a 'filename' argument is injected into a class or function,
    Ooze will run this function an pass the output in as the
    dependency.
    """
    if len(sys.argv) != 2:
        return defaults['filename']
    else:
        return sys.argv[1]
    

@ooze.provide
def file_reader(filename: str) -> list:
    """
    This function is decorated wiwith the @ooze.provide decorator.
    Any function or class that has 'filen_reader' in it's arguments will
    get this function passed in by Ooze.
    """
    with open(filename) as infile:
        return [l.strip() for l in infile.readlines()]


@ooze.provide('file_mapper')
class FileMapper:
    """
    @ooze.provide can be used to decorate classes as well as functions.
    In this case when ooze goes to create a instane of this class,
    it will inject the 'line_mapper' depenendecy when instantiating
    the FileMapper.  Also, in this example, the FileMapper class is
    registered as 'file_mapper' (see the decorator line).
    """
    def __init__(self, line_mapper):
        self.line_mapper = line_mapper


    def __call__(self, lines):
        for line in lines:
            print(self.line_mapper(line))


@ooze.provide('line_mapper')
class LineMapper:
    def __init__(self, name_mapper, address_mapper):
        self.name_mapper = name_mapper
        self.address_mapper = address_mapper

    def __call__(self, line):
        fields = [f.strip() for f in line.split(',')]
        return f"{self.name_mapper(fields)}\n{self.address_mapper(fields)}\n"


@ooze.provide
def name_mapper(fields: list) -> str:
    return f"{fields[0]} {fields[1]} {fields[3]}"


@ooze.provide
def address_mapper(fields: list) -> str:
    return f"{fields[10]}, {fields[11]}\n{fields[8]}, {fields[7]} {fields[9]}"


if __name__ == '__main__':
    generate_labels()
