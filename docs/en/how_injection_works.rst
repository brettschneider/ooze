===========================
How Injection Works in Ooze
===========================

Overview
--------
Like many other dependency injectors, Ooze builds up graph of objects that can be used
in the execution of your script.  *Any* Python object can be included in the graph:

- functions
- static builtin values (lists, dicts, strings)
- objects instantiated from classes

Ooze provides a number of mechanisms that can be used to put items into the dependency
graph.  The most common way is to decorate your class or function with the `@ooze.provide`
decorator.

.. code:: python

    import ooze

    @ooze.provide
    def lookup_user_list():
        return requests.get('https://myapp.com/api/users').json()

In the above code-snippet, the `@ooze.provide` decorator adds the `lookup_user_list`
function to the dependency graph.  The `lookup_user_list` function can now be injected
into other functions and/or objects.

Naming dependencies
-------------------
When items are inserted into the dependency graph, they are given a name.  The name can
be explicitly given by the developer or it can be inferred by Ooze.  The ooze decorators
take an optional *name* argument that allows you to give your dependency a name when
inserting it into the graph

.. code:: python

    @ooze.provide('get_users')
    def lookup_user_list():
        return requests.get('https://myapp.com/api/users').json()

In the above example, the item is given the name *get_users* by the developer.  Conversely
the developer could decide to omit the name and Ooze will assume *lookup_user_list* to be
the name of the dependency when it inserts it into the graph.

.. code:: python

    @ooze.provide
    def lookup_user_list():
        return requests.get('https://myapp.com/api/users').json()

For classes, if the name is omitted from the decorator, Ooze will lowercase the name of
the class when naming the dependency in the graph.  This is because ooze does function-
argument injection and by convention, Python uses lower-case argument variable names.
In the following example, the class will be inserted into the dependency graph as
**welcomewagon**, not as *WelcomeWagon*.

.. code:: python

    @ooze.provide
    class WelcomeWagon:
        def __init__(self):
            ...

As with the function decoration, you are free to specify a name for your class when
inserting it into the graph.  If you specify a name, Ooze will not lower case it.

.. code:: python

    @ooze.provide('WELCOME_WAGON')
    class WelcomeWagon:
        def __init__(self):
            ...

This class would be inserted into the graph as *WELCOME_WAGON*.

Dependency resolution
---------------------
Ooze performs argument dependency injection, meaning that it injects dependencies as
function arguments and class constructor arguments.  It does *not* perform attribute
injection.  It will not set attributes on existing objects with dependencies.

When resolving dependencies, it looks at the names of the arguments and searches the
dependency graph for items with the same name.  It then injects the items it finds
into those arguments.

Take for example the following function:

.. code:: python

    @ooze.provide
    def format_version(version):
        return f"Current version: {version}"

If/when Ooze is asked to execute the *format_version* function, it will try to find
an item in the dependency graph named, **version**.  When it finds an item with that
name, it will call *format_version* passing in the item it found as the argument.


Events/startup
--------------
Ooze automatically builds up the dependency graph by examining the decorators as
each Python module is imported.  You do not need to overtly add items to the graph,
Ooze just sees the decorated items and adds them for you.

Just adding items to the graph doesn't run any of your code though.  You'll need
to kick things off yourself when you're ready.  There are a couple options for
that.

First, there is the *ooze.run()* function.  Ooze.run() will try to start running
the application with a starutp function.

.. code:: python

    def main(greeter, request_processor):
        print(greeter.startup_message())
        print(request_processor())

    if __name__ == '__main__':
        ooze.run(main)

In the above example, Ooze will try to run the *main* function.  It will attempt
to find items named *greeter* and *request_processor* in the dependency graph and
it will pass them as arguements to the *main* function.

*Ooze.run* doesn't have to take any arguments at all.  If no arguments are passed
to *ooze.run*, Ooze will look for a function decorated with the *@ooze.startup*
decorator and will run that.

.. code:: python

    @ooze.startup
    def main(greeter, request_processor):
        print(greeter.startup_message())
        print(request_processor())

    if __name__ == '__main__':
        ooze.run()

You aren't **required** to let Ooze run your code.  That's just convenience
functionality that Ooze provides.  You can also just pull items out of the graph
and run them yourself using the *ooze.resolve* function.

.. code:: python

    @ooze.provide('greeter')
    class WelcomeWagon:
        def __init__(self, text_formatter, version):
            self.text_formatter = text_formatter
            self.version = version

        def greet(self):
            ...

    if __name__ == '__main__':
        g = ooze.resolve('greeter')
        print(g.greet())
