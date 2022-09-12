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
    The @ooze.magic decorator handles injecting the db_counter into this function
    automatically.
    """
    return {'page': page, 'count': db_counter.get_count(page)}


if __name__ == '__main__':
    app.run()
