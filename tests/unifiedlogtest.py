#!/usr/bin/env python
# encoding: utf-8
"""
"""

import amqplib.client_0_8 as amqp
import sys
import os
import zlib
import uuid
from time import strftime


def main():
    conn = amqp.Connection( host="10.1.0.64:5672 ", userid="guest",
                            password="guest", virtual_host="/", insist=False )
    chan = conn.channel()

    chan.queue_declare( queue="UnifiedLogQueue", durable=True,
                        exclusive=False, auto_delete=False )

    chan.exchange_declare( exchange="UnifiedLog", type="direct", durable=True,
                           auto_delete=False )
    
    chan.queue_bind( queue="UnifiedLogQueue", exchange="UnifiedLog",
                     routing_key="UnifiedLog.UnifiedLogQueue" )
    
#    for i in xrange(0, 1000):
    for i in xrange(0, 10):

	g_session = str(uuid.uuid1())
        g_sub_session = "null"
        b_sub = str(0)
        log_event = "DEBUG"
        fk_customer = str(0)
        fk_mailbox = str(0)
        log_source = str(os.getenv('HOSTNAME'))
        application = "UnifiedLog"
        dt_created = str(strftime("%Y-%m-%d %H:%M:%S"))
        prefix = str(0)
        extension = str(0)
			
        content = 'TEST - ' + dt_created

	json = '{'
	json += '"g_session" : "' + g_session + '",'
	json += '"g_sub_session" : "' + g_sub_session + '",'
	json += '"b_sub" : ' + b_sub + ','
	json += '"c_log_event" : "' + log_event + '",'
	json += '"fk_customer" : ' + fk_customer + ','
	json += '"fk_mailbox" : ' + fk_mailbox + ','
	json += '"c_log_source" : "server",'
	json += '"c_application" : "' + application + '",'
	json += '"c_message" : "' + content + '",'
	json += '"dt_created" : "' + dt_created + '",'
	json += '"i_prefix" : ' + prefix + ','
	json += '"i_extension" : ' + extension +''
	json += '}'
        
	#print json

        #message = zlib.compress(json, 9)
    	message = json	
    	msg = amqp.Message(message)
    	chan.basic_publish(msg,exchange="UnifiedLog",routing_key="UnifiedLog.UnifiedLogQueue")    

if __name__ == '__main__':
    main()

