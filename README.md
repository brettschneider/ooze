# OOZE - Brain-dead simple dependency injection #

Ooze is an attempt to do depdency injection in Python in the simplest
way possible.  It embraces Python decorators to leverage what classes,
functions, and even static values are included in the dependency
injection graph.  You can get started in three easy steps:

* decorate your functions, classes and/or variable items
* assign a startup function
* call ooze's `run()` function

That's it!  Here's a quick example:

    import ooze

    @ooze.provide               # Inject as 'upper_case' since a name wasn't specified
    def upper_case(string):
        return string.upper()


    ooze.provide('address')({   # Inject a static dictionary, naming it 'address'
        "name": "Steve",
        "gender": "male"
    })


    @ooze.provide('greeter')    # Inject as 'greeter'
    class WelcomeWagon:
        def __init__(self, upper_case, address):
            self.address = address
            self.upper = upper_case

        def greet(self):
            return self.upper(f"Hello {self.address['name']}")


    @ooze.startup               # Define where ooze should start running your program
    def main(greeter):
        print(greeter.greet())


    if __name__ == '__main__':
        ooze.run()


## Installing Ooze ##

Installing Ooze is as simple as using pip:

    $ pip install ooze


## Usage Notes ##

The notes below go into more detail about the individual compoenents of the ooze package.

### @ooze.provide ###

The `ooze.provide` decorator is used to add functions, classes and other static items to the
DI graph.  Every item added to the graph needs to have a name.  The `Ooze.provide` decorator
can take the name as an argument.  In the example below the name provided to Ooze is
`file_loader`.

    @ooze.provide('file_loader')   # name given as 'file_loader'
    def load_files(http_client):
        pass

If the item being added to the graph is a class or function, the name provided is optional.
In this case, if a name is not given to `ooze.provide`, it will default to using the class or
function's name.  This time, in the example below, Ooze will determine the name to be
`load_files`.

    @ooze.provide                  # no name given, Ooze assumes 'load_files'
    def load_files(http_client):
        pass

Ooze uses argument names to determine what dependencies are needed to fulfill a request.
In both of the above examples, Ooze will look for an item in the dependency graph named,
`http_client` to inject into the `load_files` function when executing it.  If it can't
find an item named `http_client` it will throw a `InjectionError` exception.

If the item being decorated with `ooze.provide` is a function or a static item (string,
dict, etc.) it is directly added to the ooze dependency graph.

If, however, the item being decorated with `ooze.provie` is a __class__, Ooze will try
to instantiate the class and will add the resulting object instance to the dependency
grap.  Ooze will attempt to inject any needed dependencies into the class
constructor (`__init__`) when instantiating the class.

    @ooze.provide           # no name given, ooze assumes 'databaseclient'
    class DatabaseClient:
        def __init__(connection_string):
            self.connection_string = connection_string

In the above example, Ooze will try to find a `connection_string` in the graph and
will provide it when instantiating the `DatabaseClient`.  It will place the newly
instantiated `DatabaseClient` instance into the dependency graph.

_Note:_ When adding a class to the graph, you can still name it yourself, but if you
don't, Ooze will lower-case the name of you class when adding it.  This is because,
by convention, argument names to functions are always lower-case.  Since the name
name of item in the depdency graph will be used as function/method arguments, this
is reasonable.

_Additional node:_  Ooze is aggressive and will instantiate all class instances at
application startup, not when they are first used.

Adding static items to the dependency graph is easy, however, you are required to
name your items explicitly:

    ooze.provide('version')('1.2.0')
    ooze.provide('config')({
        'env': 'dev',
        'url': 'http://contacts.dev.api.org/'
    })

In the above example, two static items are being added to the dependency graph:

* A string: '1.2.0' is added, named as 'version'
* A  dictionary with keys: 'env' and 'url' added, named as 'config'

Note that the acutal value must be enclosed within parentheses and the lack of
the '@' symbol.  This is because we are directly calling the decorator code to
add the item rather than using Python's decorator syntax.

You can add any static item to the DI graph that you want.  You just have to name it
yourself.

### @ooze.startup ###

While using the `@ooze.provide` decorator is how you add items to the dependency
graph, it doesn't specify when/how to use them.  Ooze doesn't do anything with DI
graph until told to do so.  That's where the `ooze.run()` function comes in.  When
you call `ooze.run()` that sets Ooze into motion.  Ooze will look for a starting point
and then will run it.  The starting point has to be a function, often called `main` or
`startup`.

Ooze can be told where the starting point is in one of 2 ways.  It can be told directly
by an argument passed to the `ooze.run()` function:

    def main(http_client):
        pass

    if __name__ == '__main__':
        result = ooze.run(main)         # Tell it directly
        print(f"Result: {result}")

Or if no startup function is passed to the `ooze.run()` function, it will look for
a function decorated with `@ooze.startup`:

    @ooze.startup
    def main(http_client):
        pass

    if __name__ == '__main__':
        result = ooze.run()             # Infer startup from the @ooze.startup decorator
        print(f"Result: {result}")

In both cases, `ooze.run()` will return the results of calling the startup function
so you can use them in any further processing.

The `ooze.run()` function will try to resolve any dependencies that the startup function
has using what it finds in the dependency graph.

### Other modules and packages ###

Ooze decorators can be used across modules and packages in the event you want/need to
write a non-trvial Python application.  There is only one stipulation:  Any modules or
packages that you want to participate with Ooze must be imported into the Python process.

For example, you may have module `file_reader.py` that has the following code:

    import ooze

    @ooze.provide
    class FileReader(datafile):

        def read(self):
            with open(datafile) as infile:
                return infile.read()

You may also have a module named `main.py` that has the following code:

    import ooze
    import file_reader          # You gotta import this or Ooze won't see it.

    ooze.provide('datafile')('/tmp/stuff.txt')

    def main_func(filereader):
        print(filereader.read())

    if __name__ == '__main__':
        ooze.run(main_func)

When you run `main.py`, `main_func` will have the `FileReader` injected into it as
you'd expect, but only if the `import file_reader` line is present.  If you were to
fail to import the `file_reader` module, Ooze wouldn't have an opportunity to
add the `FileReader` instance to the dependency graph.