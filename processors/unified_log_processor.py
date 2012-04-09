""" Unified Log Processing Class """
import logging
import _mssql
import sys
import simplejson
import uuid
import os
import time
from time import strftime


class unified_log_processor:
    
	def process(self, thread, message):
		returnVal = False

		try:
			logging.debug('In unified_log_processor: %s' % message.body)
		
			binding = thread.binding
			item = simplejson.loads(message.body)
		
			# INITIALIZE VARIABLES
			try:
				g_session = str(item["g_session"])
			except:
				g_session = "null"

			try:
				g_sub_session = str(item["g_sub_session"])
			except:
				g_sub_session = "null"

			b_sub = str(item["b_sub"])
			log_event = str(item["c_log_event"])
			fk_customer = str(item["fk_customer"])
			fk_mailbox = str(item["fk_mailbox"])
			log_source = str(item["c_log_source"])
			application = str(item["c_application"])
			message = str(item["c_message"])
			message = message.replace("'", "")
			dt_created = str(item["dt_created"])
			prefix = str(item["i_prefix"])
			extension = str(item["i_extension"])

			if len(g_session) == 0 or \
			g_session is None or \
			g_session == "None":
				g_session = "null"

			if len(g_sub_session) == 0 or \
			g_sub_session is None or \
			g_sub_session == "None":
				g_sub_session = "null"

			if len(log_event) == 0 or \
			log_event is None or \
			log_event == "None":
				log_event = "null"

			if b_sub.isdigit() == False:
				b_sub = "0"

			if fk_customer.isdigit() == False:
				fk_customer = "0"

			if fk_mailbox.isdigit() == False:
				fk_mailbox = "0"

			if prefix.isdigit() == False:
				prefix = "0"

			if extension.isdigit() == False:
				extension = "0"

			sqlcmd = "EXEC mt_Add_LOG '" + str(g_session) + "'"
		
			if g_sub_session == "null":
				sqlcmd += ", null"
			else:
				sqlcmd += ",'" + str(g_sub_session) + "'"
		
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

			if g_session == "null":
				# we must have a g_session!
				raise Exception, "Null or Empty gSession : " + sqlcmd

			if log_event == "null":
				#we must have a log event!
				raise Exception, "Null or Empty Log Event : " + sqlcmd

			server = str(binding['mssqlserver'])
			user = str(binding['mssqluser'])
			password = str(binding['mssqlpassword'])
			database = str(binding['mssqldatabase'])
	
			#print server + " " + user + " " + password + " " + database
			#print sqlcmd

			conn = None

			if thread.mssql_conn != None and thread.mssql_conn.connected == True:
				conn = thread.mssql_conn
			
			try:
				if conn == None:
					conn = _mssql.connect(server=server, user=user, password=password, database=database)
					logging.error("Reconnecting to mssql database")
					thread.mssql_conn = conn

				res = conn.execute_scalar(sqlcmd)
				returnVal = True
			except:
				e = sys.exc_info()[1]
				logging.error('Error saving to database: %s' % e)
				logging.error('sqlcmd: ' + sqlcmd)
				time.sleep(5)
				
				if conn != None:
					conn.close()
			#finally: 
				#if conn != None:
				#	conn.close()

		except:		
			e = sys.exc_info()[1]
			logging.error('Error in Unified Log Processor: %s' % e)
			time.sleep(1)
	
		return returnVal
