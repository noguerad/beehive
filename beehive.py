#!/usr/bin/python

'''
Created by David Noguera contacta@noguerad.es.
This script takes a number of ports and tries to open a conection to them.
I'm reading a database where I store the IPs and have a field for each port, so it's easy to update it's status.
You can run this script on crontab each 2 minutes, this way you can almost have the status of a big net each short time.
You can use, change and distribute this script. And surely you'll make it better :)
'''

import socket, subprocess, sys
import mysql.connector

### The bee class
class Abella(object):

	def __init__(self):
		### We'll store the IPs and ports here for the loop.
		self.ips = []
		### I look if ports 22 and 37777 are responding.
		self.ports = [22, 37777]

		### Read IPs from de database.
		conexio1 = mysql.connector.connect(user='your_user', password='your_password', host='your_server', database='your_ddbb_name')
        cursor = conexio1.cursor()
        ### I have a field in my database to specify old IPs, if CLOSED, i don't add it.
		consultaip = "SELECT num_machine,ip FROM `machines` WHERE `status`<>'CLOSED'"
		cursor.execute(consultaip)
		### Generating the format "num,ip" for each result.
		for (num_machine, ip) in cursor:
			self.ips.append("{},{}".format(num_machine, ip))
		cursor.close()
		conexio1.close()

	def estat(self):
		### Mysql conexion, use your own user, pass, server and database name.
		conexio = mysql.connector.connect(user='your_user', password='your_password', host='your_server', database='your_ddbb_name')
        cursor = conexio.cursor()
        ### We try if the socket opens, and then update the database status for each one.
		for i in self.ports:
			for x in self.ips:
				x = x.split(",")
				for port in range (i, i+1):
					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					### Timeout for waiting for the conection.
					sock.settimeout(2)
					try:
						sock.connect((x[1], port))
						### Updating the status on the database if opened.
						quin = str(port) 
						query = "UPDATE machines SET port"+quin+" = '"+quin+"' WHERE num_machine = '"+x[0]+"'"
	                    cursor.execute(query)
        	            conexio.commit()
					except Exception:
						### Updating the status on the database if closed.
						quin = str(port)
                        query = "UPDATE machines SET port"+quin+" = '0' WHERE num_machine = '"+x[0]+"'"
                        cursor.execute(query)
                        conexio.commit()
					finally:
						# Close the socket.
						sock.close()
		cursor.close()
		### Closing the conection.
        conexio.close()

if __name__ == "__main__":
	Abella().estat()

