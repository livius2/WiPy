import gc
import time
from machine import RTC

def websrv():
	rtc = RTC()
	rtc.ntp_sync("pool.ntp.org")
	
	# minimal Ajax in Control Webserver
	import socket	
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.bind(('', 80))
	soc.listen(0)	# just queue up some requests
	while True:
		conn, addr = soc.accept()
		try:
			print("Got a connection from %s" % str(addr))
			request = conn.recv(1024)
			conn.sendall('HTTP/1.1 200 OK\nConnection: close\nServer: nanoWiPy\nContent-Type: text/html\n\n')
	##		print("Content = %s" % str(request))
			request = str(request)
			print(request)
			ib = request.find('Val=')
			if ib > 0 :
				ie = request.find(' ', ib)
				Val = request[ib+4:ie]
				print("Val =", Val)
				conn.send(Val)
			else:
				with open('/flash/lib/webpage.html', 'r') as html:
					lt = time.localtime()
					vs = html.read().replace('$DATA_GODZINA$', str(lt[0]) + '-' + str(lt[1]) + '-' + str(lt[2]) + ' ' + str(lt[3]) + ':' + str(lt[4]) + ':' + str(lt[5]))
					conn.send(vs)
			conn.sendall('\n')
		finally:
			conn.close()
		print("Connection wth %s closed" % str(addr))
		gc.collect()
