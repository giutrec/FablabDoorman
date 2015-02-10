#!/usr/bin/env python

import sqlite3
from datetime import datetime
import time
import sys
import os

class Profile(object):
    def __init__(self, start_time="16:00", stop_time="19:00", weekend=False):
        self.start_time = start_time
        self.stop_time = stop_time
        self.weekend = weekend

class Direttivo(Profile):
    def __init__(self):
        super(self, Direttivo).__init__(start_time="00:00", stop_time="23:59", weekend=True)

class Host(Profile):
    def __init__(self):
        super(self, Host).__init__(start_time="15:00", stop_time="23:59", weekend=True)

class Ordinario(Profile):
    def __init__(self):
        super(self, Ordinario).__init__(start_time="16:15", stop_time="20:00", weekend=False)

TIME_PROFILES = {
    "direttivo": Direttivo,
    "host":  Host,
    "ordinario": Ordinario,
}

class Doorman(object):
    def __init__(self, db_name=None):
        if not db_name:
            db_name = "logger.db"
        source_dir = os.path.dirname(os.path.abspath(__file__))
        self.db = sqlite3.connect(os.path.join(source_dir, db_name))

    def create_db(self):
        c = self.db.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS intothedoor(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, datetime TEXT NOT NULL, cardcode TEXT NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS fablaballowedusers(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, cardcode TEXT NOT NULL, timeAccessProfile TEXT NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS arduinoallowedusers(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, cardcode TEXT NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS visitorsallowedusers(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, cardcode TEXT NOT NULL, start_time TEXT NOT NULL, end_time TEXT NOT NULL, expiredate TEXT NOT NULL, startdate TEXT NOT NULL )''')

    def insert_fablab_user(self, username, cardcode, profile=None):
        """
        doorman = Doorman()
        doorman.create_db()
        doorman.insert_fablab_user(db, 'udirettivo', '1815453204', 'direttivo')
        doorman.insert_fablab_user(db, 'uhost', '1815453205', 'host')
        doorman.insert_fablab_user(db, 'uordinario', '1815453206', 'ordinario')
        """
        c = self.db.cursor()
        c.execute("INSERT INTO fablaballowedusers(username, cardcode, timeAccessProfile) VALUES (?,?,?)", (username, cardcode, profile))
        self.db.commit()

    def insert_arduino_user(self, username, cardcode):
        """
        doorman = Doorman()
        doorman.create_db()
        doorman.insert_arduino_user(db, 'arduino', '1815453207',)
        """
        c = self.db.cursor()
        c.execute("INSERT INTO arduinoallowedusers(username, cardcode) VALUES (?,?)", (username, cardcode))
        self.db.commit()

    def insert_visitor_user(self, username, cardcode, start_time=None, end_time=None, expire_date=None, start_date=None):
        """
        doorman = Doorman()
        doorman.create_db()
        doorman.insert_visitor_user(db, 'visitor', '1815453208', '8', '23', '1404774000','1404720000')
        """
        c = self.db.cursor()
        c.execute("INSERT INTO visitorsallowedusers(username, cardcode, start_time, end_time, expiredate, startdate) VALUES (?,?,?,?,?,?)", (username, cardcode, start_time, end_time, expiredate, startdate))
        self.db.commit()

    def log_rfid_read(self, cardcode):
        date = str(datetime.utcnow().isoformat())
        c = self.db.cursor()
        c.execute("INSERT INTO intothedoor(datetime, cardcode) VALUES (?,?)", (date, cardcode))
        self.db.commit()

    def check_user(self, cardcode):
        self.log_rfid_read(cardcode)

        c = self.db.cursor()
        c.execute("select count (*) from arduinoallowedusers where cardcode=?", (cardcode,))
        result = c.fetchone()[0]

        if result > 0:
            c.execute("select username from arduinoallowedusers where cardcode=?", (cardcode,))
            name = c.fetchone()[0]
            print 'y'
            #print name
        else:
            c.execute("select count (*) from visitorsallowedusers where cardcode=?", (cardcode,))
            result = c.fetchone()[0]

            if result > 0:
                c.execute("select * from visitorsallowedusers where cardcode=?", (cardcode,))
                nowtime = int(time.time())
                queryres = c.fetchone()
                if int(queryres[6]) < nowtime < int(queryres[5]):
                    now = datetime.today()
                    nowh = now.strftime('%H')
                    if int(queryres[3]) <= int(nowh) <= int(queryres[4]):
                        print 'y'
                    else:
                        print 'n'	
                else:
                    print 'n' 
            else:
                c.execute("select count (*) from fablaballowedusers where cardcode=?", (cardcode,))
                result = c.fetchone()[0]

                if result > 0: # the cardcode is present in the database
                    # now check the time
                    c.execute("select timeAccessProfile from fablaballowedusers where cardcode=?", (cardcode,))
                    timeAccessProfile = c.fetchone()[0] # string corresponding to the timeAccessProfile
                    klass = TIME_PROFILES.get(timeAccessProfile)
                    # default profile
                    if not profile:
                        klass = Profile
                    profile = klass()

                    # some time conversions 
                    now = datetime.today()
                    start_date_string = now.strftime("%Y-%m-%d ") + profile.start_time
                    start_date = datetime.strptime(start_date_string, "%Y-%m-%d %H:%M")

                    stop_date_string = now.strftime("%Y-%m-%d ") + profile.stop_time
                    stop_date = datetime.strptime(stop_date_string, "%Y-%m-%d %H:%M")

                    weekday = now.isoweekday()
                    c.execute("select username from fablaballowedusers where cardcode=?", (cardcode,))
                    name = c.fetchone()[0]
                    if 1 < weekday <= 5 : # weekly day
                        # check if request is in the time range
                        if now >= start_date and now <= stop_date:
                            print 'y'
                            #print weekday
                            #print name

                        else:
                            print 'n'
                            #print 'outofhours'
                    elif profile.weekend == True:
                        print 'y'
                        #print name
                    else:
                        print 'n'
                        #print 'nowend'

if __name__ == '__main__':
    doorman = Doorman()
    doorman.create_db()

    if len(sys.argv) != 2:
        sys.exit(1)
    cardcode = ''.join(sys.argv[1])
    doorman.check_user(cardcode)
