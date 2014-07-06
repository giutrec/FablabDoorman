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
stop_time = "19:00"
weekend = False

def Direttivo():
				global start_time, stop_time, weekend
				start_time = "00:00"
				stop_time = "23:59"
				weekend = True
def Host():
				global start_time, stop_time, weekend
				start_time = "15:00"
				stop_time = "23:59"
				weekend = True
def Ordinario():
				global start_time, stop_time, weekend	
				start_time = "16:15"
				stop_time = "20:00"
				weekend = False

#dictionary with all time profiles 
options = {"direttivo" : Direttivo,
           "host" : Host,
           "ordinario" : Ordinario,
}

c.execute('''CREATE TABLE IF NOT EXISTS intothedoor(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, datetime TEXT NOT NULL, cardcode TEXT NOT NULL)''')
c.execute('''CREATE TABLE IF NOT EXISTS fablaballowedusers(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, cardcode TEXT NOT NULL, timeAccessProfile TEXT NOT NULL)''')
c.execute('''CREATE TABLE IF NOT EXISTS arduinoallowedusers(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, cardcode TEXT NOT NULL)''')

def insert_fabuser(dataBase, username=None, cardcode=None, timeAccessProfile=None):
  c = db.cursor()
  log = open('log.txt', 'w')
  if username and cardcode:
		c.execute("INSERT INTO fablaballowedusers(username, cardcode, timeAccessProfile) VALUES (?,?,?)", (username, cardcode, timeAccessProfile))
		dataBase.commit()
  else:
		log.write('You need to provide a username and a cardcode')
		return
  log.close()

  return

#insert_fabuser(db, 'udirettivo', '1815453204', 'direttivo')
#insert_fabuser(db, 'uhost', '1815453205', 'host')
#insert_fabuser(db, 'uordinario', '1815453206', 'ordinario')

def insert_arduser(dataBase, username=None, cardcode=None):
  c = db.cursor()
  log = open('log.txt', 'w')
  if username and cardcode:
		c.execute("INSERT INTO arduinoallowedusers(username, cardcode) VALUES (?,?)", (username, cardcode))
		dataBase.commit()
  else:
		log.write('You need to provide a username and a cardcode')
		return
  log.close()

  return

#insert_arduser(db, 'arduino', '1815453207',)

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
		c.execute("select count (*) from fablaballowedusers where cardcode=?", cardcode)
		result = c.fetchone()[0]
		
		if result > 0: # the cardcode is present in the database
			# now check the time
			c.execute("select timeAccessProfile from fablaballowedusers where cardcode=?", cardcode)
			timeAccessProfile = c.fetchone()[0] # string corresponding to the timeAccessProfile
			options[timeAccessProfile]() #search inside the dictionary

			# some time conversions 
			now = datetime.today()
			start_date_string = now.strftime("%Y-%m-%d ") + start_time
			start_date = datetime.strptime(start_date_string, format)

			stop_date_string = now.strftime("%Y-%m-%d ") + stop_time
			stop_date = datetime.strptime(stop_date_string, format)

			weekday = now.isoweekday()
			c.execute("select username from fablaballowedusers where cardcode=?", cardcode)
                        name = c.fetchone()[0]
			if 	weekday <= 5: # weekly day
				# check if request is in the time range
				if now >= start_date and now <= stop_date:
					print 'y'
					#print name
				else:
					print 'n'
					#print 'outofhours'
			elif weekend == True:
				print 'y'
				#print name
			else:
				print 'n'
				#print 'nowend'

		else:
			c.execute("select count (*) from arduinoallowedusers where cardcode=?", cardcode)
			result = c.fetchone()[0]
			
			if result > 0:
	                        c.execute("select username from arduinoallowedusers where cardcode=?", cardcode)
				name = c.fetchone()[0]
				print 'y'
				#print name
			else:
				print 'n'

  return

log_rfid_read(db, cardcode)
check_allowed_user(db, cardcode)
