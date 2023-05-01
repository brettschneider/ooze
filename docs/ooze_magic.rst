.. _ooze-magic:
===========================
The @ooze.magic decorator
===========================

Overview
--------
Ooze has the ability to inject SOME arguments into a function, allowing you to specify
others.  This is done using the **@ooze.magic** decorator. When you decorate a function
with the **@ooze.magic** decorator, can you later call that function with only a portion
of the arguments it expects.  Ooze will see the attempted call and try to inject any
remaining (missing) function arguments that you didn't supply.  Here's a quick example:

A quick example may make it more clear:

.. code:: python
    :number-lines:

    import ooze
    import socket

    ooze.provide_static('version', '1.0.0')

    @ooze.magic
    def app_title(hostname, version):
        print(f"App version {version} running on {hostname}")

    app_title(socket.gethostname())

Running this script will output:

.. code:: sh
    :number-lines:

    $ python script.py
    App version 1.0.0 running on macbook.local
    $

You'll notice the definition of **app_title** takes 2 arguments (hostname and version) but
that the call made on line 13 only specifies 1 (hostname). The **@ooze.magic** decorator
informs Ooze that it is responsible for injecting the remaining arguments into the function
call.  If Ooze is unable to locate a dependency that matches the argument name, it will raise
an **InjectionError** exception.
