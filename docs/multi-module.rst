.. _multi-module:
==========================================
Multi-module and/or multi-package projects
==========================================

Overview
--------

Ooze will happily work with complex projects that have multiple modules
and packages.  The only stipulation to this is that Ooze has to be
aware of the module and/or packages.  What this means that if you
don't `import` a module or package, Ooze won't know about it.

For example, you may have module `file_reader.py` that has the following code:

.. code-block:: python
    :number-lines:

    import ooze


    @ooze.provide
    class FileReader(datafile):

        def read(self):
            with open(datafile) as infile:
                return infile.read()

You may also have a module named `main.py` that has the following code:

.. code-block:: python
    :number-lines:

    import ooze
    import file_reader          # You gotta import this or Ooze won't see it.


    ooze.provide('datafile')('/tmp/stuff.txt')


    def main_func(filereader):    # Ooze will figure out how to inject even
        print(filereader.read())  # though it's in another module.

    if __name__ == '__main__':
        ooze.run(main_func)

When you run `main.py`, `main_func` will have the `FileReader` injected into it as
you'd expect, but only if the `import file_reader` line is present.  If you were to
fail to import the `file_reader` module, Ooze wouldn't have an opportunity to
add the `FileReader` instance to the dependency graph.

