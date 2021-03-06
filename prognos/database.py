#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
   database.py

   Copyright 2014 Ozkar L. Garcell <ozkar.garcell@gmail.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""

import sys
import time
import sqlite3 as lite
from os import makedirs
from os.path import expanduser, join, exists

from PyQt4 import QtGui

class PrognosDB(object):

    def __init__(self):
        if not exists(join(expanduser("~"), '.prognos')):
            makedirs(join(expanduser("~"), '.prognos'))
        self.database_path = join(expanduser("~"), '.prognos/prognos.db')

    def create_connection(self):
        try:
            self.connection = lite.connect(self.database_path)
            self.connection.text_factory = str
            self.cur = self.connection.cursor()
        except lite.Error, e:
            print "Error %s:" % e.args[0]

    def create_table(self):
        self.cur.executescript("""
            PRAGMA encoding="UTF-8";
            CREATE TABLE IF NOT EXISTS prognos(id INTEGER PRIMARY KEY AUTOINCREMENT, year INT, month INT, day INT, location TEXT,day_temp INT, night_temp INT, weather_status TEXT, date_created DATETIME DEFAULT current_timestamp, UNIQUE(year, month, day, location));
            CREATE INDEX IF NOT EXISTS idx_date ON prognos(year, month, day);
            """)
        self.connection.commit()

    def check_values(self, year, month, day):
        cmd = ("SELECT 1 FROM prognos WHERE year='{y}' AND month='{m}' AND day='{d}' LIMIT 1;").format(y=year, m=month, d=day)
        return self.cur.execute(cmd)

    def insert_query(self, params):
        self.cur.executemany("INSERT INTO prognos(year, month, day, location, day_temp, night_temp, weather_status) VALUES(?, ?, ?, ?, ?, ?, ?)", params)
        self.connection.commit()

    def select_location(self, params):
        t_day = int(time.strftime("%d")) - 1
        cmd = ("SELECT * FROM 'main'.'prognos' WHERE location = '{p}' AND day > '{d}';").format(p=params, d=t_day)
        data = self.cur.execute(cmd)
        return data.fetchall()

    def select_query(self, month, day, location):
        cmd = ("SELECT * FROM 'main'.'prognos' WHERE month = '{m}' AND day = '{d}' AND location= '{l}';").format(m=month, d=day, l=location)
        data = self.cur.execute(cmd)
        return data.fetchall()

    def close_connection(self):
        if self.connection:
            self.connection.close()
