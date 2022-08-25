=========================================
Second Bonus Feature!  Ooze Bottle Plugin
=========================================

Overview
--------
Included in this package is a `Bottle.py <https://bottlepy.org/>`_ plugin that allows
Ooze to seamlessly integrate with Bottle route functions. Simply `.install()` the
plugin and Ooze dependencies will automatically be injected into your bottle functions:

.. code:: python

    import ooze
    from bottle import Bottle

    @ooze.provide
    def add_numbers(x, y):
        return x + y

    app = Bottle()
    app.install(ooze.OozeBottlePlugin())

    @app.get('/add/<x>/<y>')
    def web_add(x, y, add_numbers):
        return {
            'sum': add_numbers(x, y)
        }
