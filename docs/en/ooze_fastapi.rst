=========================================
Ooze integration with FastAPI
=========================================

Overview
--------
FastAPI has its own dependency injection system that does not directly integrate with
Ooze.  That being said, Ooze provides a special `@magic_dependable` decorator that can
be used to bridge to FastAPI's dependency injection system.

A typical use of FastAPI's dependency injection system would look like the following:

.. code-block:: python
    :number-lines:

    from fastapi import Depends, FastAPI

    app = FastAPI()

    async def dependable_query(q: Union[str, None]):
        return q

    @app.get('/')
    async def get_root(search: str = Depends(dependable_query)):
        return {"search_query": search}

One would think that they could simply decorate `get_root` with the @ooze.magic
decorator to include Ooze dependencies in the call.  Unfortunately, FastAPI does
its own argument inspection on routed calls to `get_root` fails because
FastAPI wouldn't be able to find the dependencies in its own dependency graph.

.. code-block:: python
    :number-lines:

    from fastapi import Depends, FastAPI
    import ooze

    app = FastAPI()

    async def dependable_query(q: Union[str, None]):
        return q

    @ooze.provide
    def upper_query(value: str) -> str:
        return value.upper()

    @app.get('/')
    @ooze.magic    # !!!!! THIS FAILS - IT JUST WON'T WORK !!!!!
    async def get_root(search: str = Depends(dependable_query), upper_query):
        return {"search_query": upper_query(search)}

To get around this, Ooze provides a `@magic_dependable` decorator that you can
use on a function that accepts Ooze dependencies.

.. code-block:: python
    :number-lines:

    from fastapi import Depends, FastAPI
    import ooze

    app = FastAPI()

    async def dependable_query(q: Union[str, None]):
        return q

    @ooze.provide
    def upper_query(value: str) -> str:
        return value.upper()

    @ooze.magic_dependable
    def upper_factory(upper_query):  # Ooze injects upper_query
        return upper_query

    @app.get('/')
    async def get_root(search: str = Depends(dependable_query), upper_query=Depends(upper_factory):
        return {"search_query": upper_query(search)}

Anything that is function decorated with `@ooze.magic_dependable` can be referenced
from FastAPI's `Depends`.  Once decorated with `@ooze.magic_dependable`, the function
will get all its dependencies injected from Ooze.

FastAPI support both `async def` and `def` function definitions for Dependables.
Ooze will honor both.