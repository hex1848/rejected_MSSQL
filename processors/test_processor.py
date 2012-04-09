""" Unified Log Processing Class """
import logging
import _mssql
import sys
import simplejson
import uuid
import os
from time import strftime


class test_processor:
    
    def process(self, binding, message):
        try:
        	logging.debug('In test_processor: %s' % message.body)
	
		item = simplejson.loads(message.body)
	
		g_session = item["g_session"]
		g_sub_session = "null"

		b_sub = str(item["b_sub"])
		log_event = item["log_event"]
		fk_customer = str(item["fk_customer"])
		fk_mailbox = str(item["fk_mailbox"])
		log_source = str(item["log_source"])
		application = item["application"]
		message = item["message"]
		dt_created = item["dt_created"]
		prefix = str(item["prefix"])
		extension = str(item["extension"])

		#g_session = str(uuid.uuid1())
		#g_sub_session = "null"
		#b_sub = str(0)
		#log_event = "DEBUG"
		#fk_customer = str(0)
		#fk_mailbox = str(0)
		#log_source = str(os.getenv('HOSTNAME'))
		#application = "TEST"
		#message = message.body
		#dt_created = str(strftime("%Y-%m-%d %H:%M:%S"))
		#prefix = str(0)
		#extension = str(0)

		
		sqlcmd = "EXEC mt_Add_LOG '" + g_session + "'"
		sqlcmd += ", " + g_sub_session + ""
		sqlcmd += ", " + b_sub + ""
		sqlcmd += ", '" + log_event + "'"
		sqlcmd += ", " + fk_customer + ""
		sqlcmd += ", " + fk_mailbox + ""
		sqlcmd += ", '" + log_source + "'"
		sqlcmd += ", '" + application + "'"
		sqlcmd += ", '" + message + "'"
		sqlcmd += ", '" + dt_created + "'"
		sqlcmd += ", " + prefix + ""
		sqlcmd += ", " + extension + ""

		server = str(binding['mssqlserver'])
		user = str(binding['mssqluser'])
		password = str(binding['mssqlpassword'])
		database = str(binding['mssqldatabase'])
	
		#print server + " " + user + " " + password + " " + database
		#print sqlcmd

		conn = _mssql.connect(server=server, user=user, password=password, database=database)
		res = conn.execute_scalar(sqlcmd)

	        return True
	except:
		e = sys.exc_info()[1]
		logging.error('Error saving to database: %s' % e)

        return False
