.. _ooze-pools:
================================
Resource sharing with Ooze pools
================================

Overview
--------
Up to this point, Ooze has provided two, high-level options for instantiating objects to
be placed in the dependency graph:

- @ooze.provide / ooze.provide_static
- @ooze.factory

The first option effectively creates singletons.  Each object in the graph is there from
application startup and is continually reused when needed... never being re-instantiated.

The second option (*@ooze.factory*) executes and returns every time it's called upon to
be injected, resulting in a new instance of a dependency each and every time it's used.

These two extremes may not suffice in a long-running multi-threaded environment (think
Flask or Bottle web servers).  Take for example a database connection as a dependency.
Having one database connection over the lifespan of the application can be, at best
a serious performance issue under load and, at worst, a serious security issue.

On the flip side, having the system spin up new database connection for each and every
web request is expensive and can noticeably slow down each and every request.

Pools can solve this problem by allowing you to create a pool of dependencies that
can be reused over and over (aka Database Connection Pools).  Unlike database
connection pools Ooze pools can be used with any Python object.


Usage
-----

A pool has to be instantiated and told how to manage instances of your dependency.  The
pool constructor takes the following arguements:


.. code:: Python
    :number-lines:

    import ooze.pool

    pool = ooze.pool.Pool(create_item, reclaim_item, teardown_item, pool_size)


The arguments have the following meanings:

+---------------+------------+-------------------------------------------------------------------+
| Argument      | Default    | Description                                                       |
+===============+============+===================================================================+
| create_item   | (required) | is a callable that takes no arguments, but returns a new instance |
|               |            | of the dependency that you'd like to pool.  The pool instance     |
|               |            | will call this callable on an as-needed basis when it wants to    |
|               |            | add new instances of your dependency to the pool.                 |
+---------------+------------+-------------------------------------------------------------------+
| reclaim_item  | None       | is a callable that takes a single argument, an instance of your   |
|               |            | dependency, and returns nothing.  Ooze calls this on items when   |
|               |            | they are returned to the pool.  The purpose of this callable is   |
|               |            | to 'reset' the dependency so that it will be ready for the next   |
|               |            | injection.                                                        |
+---------------+------------+-------------------------------------------------------------------+
| teardown_item | None       | is a callable that takes a single arguement, an intance of your   |
|               |            | dependency, and returns nothing.  The purpose of this callable is |
|               |            | to gracefully shut down your dependency (close a db connection    |
|               |            | for example) before your script terminates.                       |
+---------------+------------+-------------------------------------------------------------------+
| pool_size     | 5          | is an integer indicating how large you'd like to pool to be at    |
|               |            | any given time.                                                   |
+---------------+------------+-------------------------------------------------------------------+

The only required argument to the Pool constructor is *create_item*.  That being said, you'd
be wise to at least consider providing a *reclaim_item* so you can verify and reset items
before they get used again, especially if they maintain any kind of internal state.

The pool instance is a Python context manager.  Use with Python **with** statement
on the pools *item()* method to obtain an instance of the dependency item.

An example to illustrate (again you can use Pools with anything, I just happen
to use database connections in my example as they are easy to relate to):


.. code:: Python
    :number-lines:

    def create_item():
        db_con_factory = ooze.resolve('database_factory')
        # Defined elsewhere but returns a fresh, new database connection
        return db_con_factory()

    def reclaim_item(db_con):
        try:
            db_con.commit()
        except:
            pass

    def teardown_item(db_con):
        db_con.close()

    # Register a new Pool in the dependency graph.  It will retain 10 connections
    ooze.provide_static('database_pool', ooze.pool.Pool(
        create_item, reclaim_item, teardown_item, 10
    ))

    @ooze.provide
    class AddressRepository:
        def __init__(self, database_pool):
            self.database_pool = database_pool

        def get_addresses(self):
            with self.database_pool.item() as db_conn:
                return db_conn.cursor().execute('select * from addresses').fetchall()


In the above example, the *database_pool* is injected into the *AddressRepository*
when Ooze starts up.  The *database_pool* will instantiate new database connections as
needed by calling the *create_item* callable.  It will maintain a pool of 10
connections, reusing them as needed.

Then the application stops, the *database_pool* will call the *teardown_item*
callable on each and every item in the pool to gracefully shut down the connections.


Thread safety
-------------
The Ooze dependency injector is thread-ignorant.  This is not an accident, but rather
a purposeful decision to keep Ooze simple, easy to understand and easy to maintain.

The Ooze Pools, however **ARE INDEED** thread aware and thread-safe.  You should feel
confident using Ooze Pools in your web (or any other multi-threaded) environments.