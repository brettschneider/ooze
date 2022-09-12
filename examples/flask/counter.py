#!/usr/bin/env python
"""This is a counter class that interacts with SQLite."""
import ooze.pool
import sqlite3


ooze.provide_static('db_pool', ooze.pool.Pool(
    lambda: sqlite3.connect('counter_data.db', check_same_thread=False),
    lambda db: db.commit(),
    lambda db: db.close()
))


@ooze.provide('db_counter')
class DatabaseCounter:

    def __init__(self, db_pool):
        self.db_pool = db_pool
        self.initialize_database()

    def initialize_database(self):
        with self.db_pool.item() as db:
            db.execute("create table if not exists page_count (page, num_hits)")

    def get_count(self, page):
        with self.db_pool.item() as db:
            cursor = db.cursor()
            rs = cursor.execute("select num_hits from page_count where page=?", (page,))
            count_record = rs.fetchone()
            if not count_record:
                db.execute("insert into page_count values (? ,0)", (page,))
                return 0
            else:
                count = int(count_record[0]) + 1
                db.execute(f"update page_count set num_hits={count} where page=?", (page,))
                return count

