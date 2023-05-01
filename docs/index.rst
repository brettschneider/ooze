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
can rapidly become tedious and error prone.   That's where dependency
injectors (DI) come in.  Dependency injectors automate standing up your object
graphs by automatically injecting dependencies into your functions and class
instances.

Ooze is an attempt to do dependency injection in Python in the simplest
way possible.  It embraces Python decorators to leverage what classes,
functions, and even static values are included in the dependency
injection graph.

Since Ooze is implemented as a set of pure Python decorators, it works
seamlessly with any number of other packages and frameworks such as: Bottle,
Flast and FastAPI.

You can get started in two easy steps:

- decorate your functions, classes and/or variable items to add them to
  dependency graph
- call ooze's `run()`, passing in your callable

That's it!  Here's a quick example:

.. code:: python
    :number-lines:

    import ooze

    @ooze.provide                       # Add the upper_case function to the dependency graph
    def upper_case(string):
        return string.upper()

    ooze.provide_static('address', {    # Add a static dictionary to the dependency graph
        "name": "Steve",
        "title": "Developer"
    })

    @ooze.provide('greeter')            # Add to the dependency graph, naming it 'greeter'
    class WelcomeWagon:
        def __init__(self, upper_case, address):   # Automatically injected by Ooze
            self.address = address
            self.upper = upper_case

        def greet(self):
            return self.upper(f"Hello {self.address['name']}")

    def main(greeter):                  # Ooze will automatically inject the greeter
        print(greeter.greet())


    ooze.run(main)  # Ooze takes care of getting 'main' to run, injecting whatever is needed.


Installing Ooze
---------------
Installing Ooze is as simple as using pip:

.. code:: sh
    :number-lines:

    $ pip install ooze


User Guide
------------

1. :ref:`how-injection-works`

2. :ref:`ooze-provide-decorator`

3. :ref:`ooze-provide-static`

4. :ref:`ooze-startup`

5. :ref:`ooze-factory`

6. :ref:`ooze-magic`

7. :ref:`environment-variables`

8. :ref:`configuration-files`

9. :ref:`ooze-pools`

10. :ref:`multi-module`

11. :ref:`ooze-fastapi`

12. :ref:`bottle-plugin`
