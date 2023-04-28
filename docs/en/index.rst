====
Ooze
====
---------------------------------------
A brain-dead simple dependency injector
---------------------------------------

Overview
--------
Injecting dependencies makes organizing and reorganizing code easier and more
efficient.  Additionally injecting dependencies makes testing your code and
writing unit-tests much easier.  Unfortunately, manually injecting dependencies
can rappidly become tedious and error prone.   That's where dependency
injectors (DI) come in.  Dependency injectors automate standing up your object
graphs by automatically injecting dependencies into your functions and class
instances.

Ooze is an attempt to do dependency injection in Python in the simplest
way possible.  It embraces Python decorators to leverage what classes,
functions, and even static values are included in the dependency
injection graph.  You can get started in two easy steps:

- decorate your functions, classes and/or variable items to add them to
  dependency graph
- call ooze's `run()`, passing in your callable

That's it!  Here's a quick example:

.. code:: python
    :number-lines:

    import ooze

    @ooze.provide                       # Add to graph as 'upper_case' since a name wasn't specified
    def upper_case(string):
        return string.upper()


    ooze.provide_static('address', {    # Add a static dictionary to the graph, naming it 'address'
        "name": "Steve",
        "title": "Developer"
    })


    @ooze.provide('greeter')            # Add to graph as 'greeter'
    class WelcomeWagon:
        def __init__(self, upper_case, address):
            self.address = address
            self.upper = upper_case

        def greet(self):
            return self.upper(f"Hello {self.address['name']}")


    def main(greeter):
        print(greeter.greet())


    ooze.run(main)


Installing Ooze
---------------
Installing Ooze is as simple as using pip:

.. code:: sh
    :number-lines:

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
