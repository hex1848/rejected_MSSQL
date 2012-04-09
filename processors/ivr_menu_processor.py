""" IVR Menu Processing Class """
import logging
import _mssql
import sys
import simplejson
import uuid
import os
from time import strftime
import time

class ivr_menu_processor:

	def process(self, thread, message):
		returnVal = False

		try:

			logging.debug('In ivr_menu_processor: %s' % message.body)

			binding = thread.binding
			item = simplejson.loads(message.body)

			callUUID = str(item["callUUID"])
			menuID = str(item["menuID"])
			response = str(item["response"])
			fkMailbox = str(item["fkMailbox"])
			order = str(item["order"])
			tries = str(item["tries"])
			ir_count = str(item["ir_count"])
			to_count = str(item["to_count"])
			created = str(item["created"])

			if fkMailbox.isdigit() == False:
				fkMailbox = "null"

			if order.isdigit() == False:
				order = "0"

			if tries.isdigit() == False:
				tries = "0"

			if ir_count.isdigit() == False:
				ir_count = "0"

			if to_count.isdigit() == False:
				to_count = "0"

			sqlcmd = "exec ivr_LogIVRMenu "
			sqlcmd += "'" + str(callUUID) + "'"
			sqlcmd += ", " + fkMailbox + ""
			sqlcmd += ", " + menuID + ""
			sqlcmd += ", " + order + ""
			sqlcmd += ", '" + response + "'"
			sqlcmd += ", " + tries + ""
			sqlcmd += ", " + ir_count + ""
			sqlcmd += ", " + to_count + ""
			sqlcmd += ", '" + created + "'"

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
