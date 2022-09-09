===========================
The @ooze.magic decorator
===========================

Overview
--------
Ooze has the ability to only inject what you need injected into a function call.  This is
done with the **@ooze.magic** decortaor.  When you decorate a function with the
**@ooze.magic** decorator, can you later call that function with only a portion of the
arguments it expects.  Ooze will see the attempted all and try to inject any remaining
function arguments that you didn't supply.  Here's a quick example:

A quick example may make it more clear:

.. code:: python

    import ooze
    import socket

    ooze.provide_static('version', '1.0.0')

    @ooze.magic
    def app_title(hostname, version):
        print(f"App version {version} running on {hostname}")

    if __name__ == '__main__':
        app_title(socket.gethostname())

Running this script will output:

.. code:: sh

    $ python script.py
    App version 1.0.0 running on macbook.local
    $

You'll notice the definition of **app_title** takes 2 arguments (hostname and version) but
that the call made later in the script only specifies 1 (hostname). The
**@ooze.magic** decorator informs Ooze that it is responsible for injecting the remaining
arguments into the function call.  If Ooze is unable to locate a dependency that matches
the argument name, it will raise an **InjectionError** exception.
