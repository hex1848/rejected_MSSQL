""" IVR Call Processing Class """
import logging
import _mssql
import sys
import simplejson
import uuid
import os
from time import strftime
import time

class ivr_call_processor:

	def process(self, thread, message):
		returnVal = False
		
		try:
			logging.debug('In ivr_call_processor: %s' % message.body)
			
			binding = thread.binding
			item = simplejson.loads(message.body)

			callUUID = str(item["callUUID"])
			fkMailbox = str(item["fkMailbox"])
			ani = str(item["ani"])
			dialedNumber = str(item["dialedNumber"])
			logSource = str(item["logSource"])
			answerTime = str(item["answerTime"])
			hangupTime = str(item["hangupTime"])

			if fkMailbox.isdigit() == False:
				fkMailbox = "null"

			sqlcmd = "exec ivr_LogIVRCall "
			sqlcmd += "@guid='" + str(callUUID) + "'"
			sqlcmd += ", @pk_mailbox=" + fkMailbox + ""
			if ani != 'None':
				sqlcmd += ", @c_ani='" + ani + "'"
			else:
				sqlcmd += ", @c_ani=null"
			if dialedNumber != 'None':
				sqlcmd += ", @c_dialed_number='" + dialedNumber + "'"
			else:
				sqlcmd += ", @c_dialed_number=null"
			if logSource != 'None':
				sqlcmd += ", @c_log_source='" + logSource + "'"
			if answerTime != 'None':
				sqlcmd += ", @dt_begin_time='" + answerTime + "'"
			if hangupTime != 'None':
				sqlcmd += ", @dt_end_time='" + hangupTime + "'"

			server = str(binding['mssqlserver'])
			user = str(binding['mssqluser'])
			password = str(binding['mssqlpassword'])
			database = str(binding['mssqldatabase'])

			#print server + " " + user + " " + password + " " + database
			logging.debug('%s', sqlcmd)

			conn = None

			if thread.mssql_conn != None and thread.mssql_conn.connected == True:
				conn = thread.mssql_conn
			
			try:
				if conn == None:
					conn = _mssql.connect(server=server, user=user, password=password, database=database)
					logging.warning("Reconnecting to mssql database")
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
			logging.error('Error in IvrCall Processor: %s' % e)
			time.sleep(5)


		return returnVal
