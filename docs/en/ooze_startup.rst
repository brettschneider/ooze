===========================
The @ooze.startup decorator
===========================

Overview
--------
Typically you use *ooze.run()* to run your application using the Ooze dependency graph.
*Ooze.run* can determine what to run by two mechanics: an argument given or a callable
that has been decorated with *@ooze.startup*.

Here's how it looks when you use an argument:


.. code:: python

    import ooze

    @ooze.provide
    def get_version():
        with open('version.txt') as infile:
            return infile.read()

    def main(get_version):
        print(f"Version: {get_version()})
        ...

    ooze.run(main)

You can see that the *main* function is passed to *ooze.run* as an argument.  When Ooze
tries to run *main*, it will attempt to satify any dependencies that it has automatically.

If, for some reason, you'd prefer not to pass your starting-point function into the
*ooze.run* function, you can omit it.  You simply have to "tag" your starting point with
the *ooze.start* decorator:

.. code:: python

    import ooze

    @ooze.provide
    def get_version():
        with open('version.txt') as infile:
            return infile.read()

    @ooze.startup
    def main(get_version):
        print(f"Version: {get_version()})
        ...

    ooze.run()

Ooze will look for the **last* function that has been decorated with *@ooze.startup* and
will execute that function as if it has been passed in as an argument.