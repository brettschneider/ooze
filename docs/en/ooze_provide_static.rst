================================
The ooze.provide_static function
================================

Overview
--------
The Ooze dependency injector isn't limited to only injecting functions and classes.  It can
inject any valid Python value.  The *ooze.provide_static* function makes it easy:

.. code:: python

    import ooze

    ooze.provide_static('application_version', '1.0.0')
    ooze.provide_static('config', { 'env': 'prod', 'url': 'https://github.com/' })

The first argument is the name that you want the item to known as in the dependency graph.
The second argument is the value.  Later in your application, you can have these values
injected into your functions simply by naming your arguments:

.. code:: python

    @ooze.provide
    def get_app_status(version, config):
        return f"App version: {version}, environment: {config['env']}"


