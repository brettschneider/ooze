========================
OS Environment Variables
========================

Overview
--------
As a convenience feature, when resolving dependencies, Ooze will check to see if
the dependency being injected appears as an OS environment variable.  It checks
the OS environment last after all other places (functions, classes, static values).
This is meant to save you time writing code that pulls info out of the environment.

Often in containerization environment (think Docker, Kubernetes, AWS, etc) sensitive
configuration information is made available to you application via *secrets* in the
form of environment variables.  Ooze makes it possible to directly inject those
secrets (assuming your function argument names match the OS variable names) into
your code.

A quick example:

.. code:: sh

    $ export DATABASE_HOST="locahost"
    $ export DATABASE_USERNAME="admin-tool"
    $ export DATABASE_PASSWORD="itza-sooper-secret"

Then the Python code looks like this:

.. code:: python

    @ooze.provide('db_manger')
    class DatabaseManager:
        def __init__(self, database_host, database_username, database_password):
            self.db = connect(database_host, database_username, database_password)

Ooze will attempt to find your OS variable with the exact case you specify in your
function arguments.  If it can't find it, it will also try upper-case and lower-case
before giving up.

