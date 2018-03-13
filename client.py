import socket, threading, time
from subprocess import check_output
from sys import platform

key = 8194

shutdown = False
join = False

def getMyHost():
	ip = check_output(['hostname', '--all-ip-addresses'])

	ip = ip.decode('utf-8')

	count = 0
	for i in ip:
		if (i == ' '):
			ip = ip[:count]
		count += 1

	return ip

def receving (name, sock):
	while not shutdown:
		try:
			while True:
				data, addr = sock.recvfrom(1024)
				#print(data.decode("utf-8"))

				# Begin
				decrypt = ""; k = False
				for i in data.decode("utf-8"):
					if i == ":":
						k = True
						decrypt += i
					elif k == False or i == " ":
						decrypt += i
					else:
						decrypt += chr(ord(i)^key)
				print(decrypt)
				# End

				time.sleep(0.2)
		except:
			pass
# print(socket.gethostname())
# host = socket.gethostbyname(socket.gethostname())
if (platform == 'win32'):
	host = socket.gethostbyname(socket.gethostname())
elif (platform == 'linux'):
	host = getMyHost()

print('host = ' + host)
port = 0

# server = ("127.0.1.1", 9090)
# server = ("5.137.18.178", 8080)
# server = ('192.168.1.7', 8080)
# server = ('5.137.18.178', 8080)
server = ("18.222.90.10", 50001)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
# s.bind(("192.168.1.7", port))
s.setblocking(0)

alias = input("Name: ")

rT = threading.Thread(target = receving, args = ("RecvThread",s))
rT.start()

while shutdown == False:
	if join == False:
		s.sendto(("[" + alias + "] => join chat ").encode("utf-8"),server)
		join = True
	else:
		try:
			message = input('-> ')

			# Begin
			crypt = ""
			for i in message:
				crypt += chr(ord(i)^key)
			message = crypt
			# End

			if message != "":
				s.sendto(("["+alias + "] :: "+message).encode("utf-8"),server)
			
			time.sleep(0.2)
		except:
			s.sendto(("["+alias + "] <= left chat ").encode("utf-8"),server)
			shutdown = True

rT.join()
s.close()
