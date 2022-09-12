#!/usr/bin/env python
"""
This example script starts a Flask app that reads and updates a sqlite
database.  It demonstrates Ooze's object pool as well as it's
@ooze.magic decorator to seemlessly integrate Ooze with Flask.
"""
import ooze
from flask import Flask
from counter import DatabaseCounter


app = Flask(__name__)

@app.route('/<page>')
@ooze.magic
def get_count(page, db_counter: DatabaseCounter):
    """
    Flask will call get_count(), passing the 'page' argument in... but Flask doesn't
    know or care about the db_counter.  This is where Ooze steps in.  The
    @ooze.magic decorator sees that the db_counter argument has not been provided by
    Flask and handles injecting the db_counter into this function automatically.
    """
    return {'page': page, 'count': db_counter.get_count(page)}


if __name__ == '__main__':
    app.run()
