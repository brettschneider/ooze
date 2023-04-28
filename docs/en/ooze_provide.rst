===========================
The @ooze.provide decorator
===========================

Overview
--------
You can use the *@ooze.provide* decorator to add functions and classes to your application's
dependency graph.

.. code-block:: python
    :number-lines:

    @ooze.provide('get_users')
    def lookup_user_list():
        return requests.get('https://myapp.com/api/users').json()

The *name* argment of *@ooze.provide* is optional.  If you don't specify it, Ooze will
assume the name of the function/class to be it's name in the dependency graph.

.. code-block:: python
    :number-lines:

    @ooze.provide
    def lookup_user_list():
        return requests.get('https://myapp.com/api/users').json()

In the above example, Ooze inserts the function into the graph as *lookup_user_list*.

For classes, if the name is omitted from the decorator, Ooze will lowercase the name of
the class when inserting it into the dependency in the graph. In the following example,
the class will be inserted into the dependency graph as
**welcomewagon**, not as *WelcomeWagon*.

.. code-block:: python
    :number-lines:

    @ooze.provide
    class WelcomeWagon:
        def __init__(self):
            ...

As with the function decoration, you are free to specify a name for your class when
inserting it into the graph.  If you specify a name, Ooze will not lower case it.

.. code-block:: python
    :number-lines:

    @ooze.provide('WELCOME_WAGON')
    class WelcomeWagon:
        def __init__(self):
            ...

This class would be inserted into the graph as *WELCOME_WAGON*.


A note about class instantiation
--------------------------------
When decorating a function with *@ooze.provide*, Ooze places the function as-is into
the dependency graph.  However, when *@ooze.provide* decorates a class, it's not
decorating an object instance, but rather a class.  This is a subtle, but important
difference.

When you're using dependencies, you're not expecting a *class* to be injected into
your functions.  You're expecting an object *instance*.  How does Ooze deal with that?

I'm glad you asked!

The first time Ooze is asked to run/resolve any dependencies either via *ooze.run* or
*ooze.resolve*, Ooze will try to instantiate all classes that are registered in the
graph.  If it can't, it will raise an **InjectionError* exception.

However, if it _can_ instantiate instances of registered classes, it will place the
instances into the dependency graph and will use them when injecting dependencies
into functions/methods.

This is important to note because you can't assume that a dependency injected into
your functions are brand-new.  They may have been used by other functions/methods
earlier in your code's execution.  This has serious implications for multi-threaded
applications that you should take into consideration.  If you need a new instance of
a class each time it's used, you should look at the @ooze.factory decorator.
