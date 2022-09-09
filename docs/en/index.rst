====
Ooze
====
---------------------------------------
A brain-dead simple dependency injector
---------------------------------------

Overview
--------
Ooze is an attempt to do dependency injection in Python in the simplest
way possible.  It embraces Python decorators to leverage what classes,
functions, and even static values are included in the dependency
injection graph.  You can get started in three easy steps:

- decorate your functions, classes and/or variable items
- assign a startup function
- call ooze's `run()` function

That's it!  Here's a quick example:

.. code:: python

    import ooze

    @ooze.provide                       # Inject as 'upper_case' since a name wasn't specified
    def upper_case(string):
        return string.upper()


    ooze.provide_static('address', {    # Inject a static dictionary, naming it 'address'
        "name": "Steve",
        "gender": "male"
    })


    @ooze.provide('greeter')            # Inject as 'greeter'
    class WelcomeWagon:
        def __init__(self, upper_case, address):
            self.address = address
            self.upper = upper_case

        def greet(self):
            return self.upper(f"Hello {self.address['name']}")


    @ooze.startup                       # Define where ooze should start running your program
    def main(greeter):
        print(greeter.greet())


    if __name__ == '__main__':
        ooze.run()


Installing Ooze
---------------
Installing Ooze is as simple as using pip:

.. code:: sh

    $ pip install ooze


User Guide
------------

1. `How injection works in Ooze <./how_injection_works.rst>`_

2. `The @ooze.provide decorator <./ooze_provide.rst>`_

3. `The ooze.provide_static function <./ooze_provide_static.rst>`_

4. `The @ooze.startup decorator <./ooze_startup.rst>`_

5. `The @ooze.factory decorator <./ooze_factory.rst>`_

6. `The @ooze.magic decorator <./ooze_magic.rst>`_

7. `OS Environment variables <./ooze_os_environment_variables.rst>`_

8. `Configuration files <./ooze_configuration_files.rst>`_

9. `Ooze pools <./ooze_pools.rst>`_

10. `Multi-module, multi-package Python projects <./multi-module.rst>`_

11. `Using Ooze with Bottle.py <./ooze_bottle.rst>`_
