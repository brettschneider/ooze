===========================
The @ooze.factory decorator
===========================

Overview
--------
Sometimes a dependency isn't necessarily available when the application starts up.  Or,
a dependency needs to be calculated given certain runtime realities. Or... you need a new
instance of a dependency each and every time it's called upon.  This is where factories
come in.

When you define a **factory** dependency in Ooze, Ooze doesn't store the function/class
in the dependency graph.  It calls the function and stores the result of that function
in the dependency graph.

A quick example may make it more clear:

.. code-block:: python
    :number-lines:

    import ooze
    import json


    @ooze.factory('config')
    def lookup_config():
        with open('config.json') as infile:
            return json.load(infile)


    @ooze.provide('db')
    class DatabaseManager:
        def __init__(self, config: dict):
            self.config = config

        def get_connection(self):
            pass

In the above example, the DatabaseManager needs a *config* dictionary to be injected into
it so that it knows how to connect to a database.  The DatabaseManager shouldn't have to
CALL *lookup_config* to get the config.  It just cares about getting the config values
injected into it.

Since we've decorated *lookup_config* with the *@ooze.factory* decorator (as opposed to the
*@ooze.provide* decorator), Ooze will run *lookup_config* whenever *config* is injected
as a dependency and inject its return value rather than the function itself.

Execution timing
----------------
It's important to note that the factory will be called each and every time that
the dependency is injected into another item.  This means when you execute one
function that depends on the factory and execute another function the depends on the
same factory... this will result in the factory being called twice.