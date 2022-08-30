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

    @ooze.provide                       # Inject as 'upper_case' since a name wasn't specified
    def upper_case(string):
        return string.upper()


    ooze.provide_static('address', {    # Inject a static dictionary, naming it 'address'
        "name": "Steve",
        "gender": "male"
    })


    @ooze.provide('greeter')            # Inject as 'greeter'
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

Ooze has **many** features beyond what is demonstrated in the above example
including:

* factories
* automatic environment variable injection
* automatic configuration file parsing and settings injection
* seamless integration with [bottlepy](https://bottlepy.org/)
* injectable object pools (i.e. Database connection pools)
 
Be sure to check out the [documentation](https://github.com/brettschneider/ooze/blob/main/docs/en/index.rst) for more
information.
