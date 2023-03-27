===================
Configuration files
===================

Overview
--------
Another convenience feature that Ooze provides in resolving dependencies pertains
to reading configuration files.  Ooze can automatically read configuration files
and inject configuration values into your classes and functions as dependencies.

Ooze will look for the following files in the root of your Python script named:

- application_settings.json
- application_settings.yaml
- application_settings.yml

If it finds any of those files, it will parse them and the root keys in the
resulting dictionary will be made available for injection into your classes
and functions.

A quick example... suppose you have the following `application_settings.yaml`
in the same directory as your Python script:

.. code-block:: yaml
    :number-lines:

    urls:
        customers: http://api.bigcompany.com/marketing/customers
        vendor_1: https://otherco.com/public/api/orders

Then the Python code looks like this:

.. code-block:: python
    :number-lines:

    @ooze.provide('web_client')
    class HttpClient:
        def __init__(self, urls):
            self.url = urls

        def get_customers(self):
            return requests.get(self.urls['customers'])

        def delete_order(self, order_id):
            url = f"{self.urls['vendor_1']}/{order_id}"
            try:
                requests.delete(url)
                return True
            except:
                return False

As you can see, Ooze will find the `application_settings.yaml` file, read it,
parse it and then inject the `urls` configuration into the HttpClient instance.
This all happens automatically.


Supported configuration formats
-------------------------------
Ooze will read JSON and YAML files and parse them automatically.  All other file
formats will result in a `ConfigurationError` exception being raised.


Specifying configuration file manually
--------------------------------------
In addition to looking for configuration settings files in the
`application_settings.(json | yaml | yml)` files, you can manually specify a configuration
file for Ooze to read.  Simply set the `APPLICATION_SETTINGS` environment variable to a
valid file path and Ooze will use that file as the application_settings file.

.. code-block:: sh
    :number-lines:

    $ export APPLICATION_SETTINGS=/opt/myapp/config.yml
    $ python myapp.py

In the above example, Ooze will first try to read the `/opt/myapp/config.yml` file in
search of configuration settings.  If it cannot file that file, it will then attempt to
locate the `application_settings.(json | yaml | yml )` files.

Manually specified configuration files still need to be either JSON or YAML formatted
files.