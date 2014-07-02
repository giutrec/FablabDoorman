#!/usr/bin/env python

from sys import argv
import sqlite3
from datetime import datetime
import os
source_dir = os.path.dirname(os.path.abspath(__file__))
cardcode = ''.join(argv[1])
db = sqlite3.connect(os.path.join(source_dir, 'logger.db'))
c = db.cursor()
format = "%Y-%m-%d %H:%M"
start_time = "16:00"
stop_time = "18:00"
weekend = False

def arduino():
				global start_time, stop_time, weekend
				start_time = "00:00"
				stop_time = "23:59"
				weekend = True
def direttivo():
				global start_time, stop_time, weekend
				start_time = "00:00"
				stop_time = "23:59"
				weekend = True
def host():
				global start_time, stop_time, weekend
				start_time = "15:30"
				stop_time = "00:00"
				weekend = True
def ordinario():
				global start_time, stop_time, weekend	
				start_time = "16:03"
				stop_time = "22:30"
				weekend = False

#dictionary with all time profiles 
options = {"arduino" : arduino,
           "direttivo" : direttivo,
           "host" : host,
           "ordinario" : ordinario,
}

c.execute('''CREATE TABLE IF NOT EXISTS intothedoor(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, datetime TEXT NOT NULL, cardcode TEXT NOT NULL)''')
c.execute('''CREATE TABLE IF NOT EXISTS allowedusers(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, cardcode TEXT NOT NULL, timeAccessProfile TEXT NOT NULL)''')

def insert_user(dataBase, username=None, cardcode=None, timeAccessProfile=None ):
  c = db.cursor()
  log = open('log.txt', 'w')
  if username and cardcode and timeAccesProfile:
		c.execute("INSERT INTO allowedusers(username, cardcode, timeAccessProfile) VALUES (?,?,?)", (username, cardcode, timeAccessProfile))
		dataBase.commit()
  else:
		log.write('You need to provide a username, cardcode and time Access Profile')
		return
  log.close()

  return

#insert_user(db, 'Utente', '1815453204', 'ordinario')
#insert_user(db, 'presidente', '181545325', 'direttivo')

def log_rfid_read(dataBase, cardcode):
  c = db.cursor()
  date = str(datetime.utcnow().isoformat())
  c.execute("INSERT INTO intothedoor(datetime, cardcode) VALUES (?,?)", (date, cardcode))
  dataBase.commit()
  return

def check_allowed_user(dataBase, cardcode=None):
  c = db.cursor()

  if cardcode:
		cardcode = (cardcode,)
		c.execute("select count (*) from allowedusers where cardcode=?", cardcode)
		result = c.fetchone()[0]
		
		if result > 0: # the cardcode is present in the database
			# now check the time
			c.execute("select timeAccessProfile and username from allowedusers where cardcode=?", cardcode)
			timeAccessProfile = c.fetchone()[0] # string corresponding to the timeAccessProfile
			options[timeAccessProfile]() #search inside the dictionary

			# some time conversions 
			now = datetime.today()
			start_date_string = now.strftime("%Y-%m-%d ") + start_time
			start_date = datetime.strptime(start_date_string, format)

			stop_date_string = now.strftime("%Y-%m-%d ") + stop_time
			stop_date = datetime.strptime(stop_date_string, format)

			weekday = now.isoweekday()
			if 	weekday <= 5: # weekly day
				# check if request is in the time range
				if now >= start_date and now <= stop_date:
					print 'y'
					print 'username'
				else:
					print 'n'
			elif weekend == True:
				print 'y'
			else:
				print 'n'

		else:
			print 'n'

  return
  
log_rfid_read(db, cardcode)
check_allowed_user(db, cardcode)
