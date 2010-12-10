# Error Logging Middleware class for Django 1.1
# by Jannik Altgen
# 11-8-2009

from syslog import *
import time

class Syslog_Output:

	def process_exception(self, request, exception):
		# Compile the string for the exception in the format: "Variable: Value" so as to make it readable
		
		filename='/srv/django/log/%s_error.csv'%(time.strftime('%y-%m-%d-%H-%M-%s'))
		csv = file(filename, 'w')
		
		exception_string = "\n\Request: %s"%(request)
		exception_string += "\n\Exception: %s"%(exception)
		syslog (LOG_DEBUG, exception_string)
		csv.writelines("Exception: %s, this is my output!"%(exception_string))
		csv.close()
		return None

