#!/usr/bin/env python

from sys import argv
from datetime import datetime
format = "%Y-%m-%d %H:%M"
start_time = "16:00"
stop_time = "20:00"

now = datetime.today()
start_date_string = now.strftime("%Y-%m-%d ") + start_time
start_date = datetime.strptime(start_date_string, format)
stop_date_string = now.strftime("%Y-%m-%d ") + stop_time
stop_date = datetime.strptime(stop_date_string, format)

weekday = now.isoweekday()

if weekday <= 5:
	if now >= start_date and now <= stop_date:
		print 'a'

