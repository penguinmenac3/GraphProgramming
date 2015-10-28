import socket
import json


def serverLoop(host = "localhost", port = 25555):
	serversocket = socket.socket()
	serversocket.bind((host, port))
	serversocket.listen(5)
	print("CTRL + BREAK [Pause] to stop script.")

	# Server waiting for tick requests.
	while 1:
	    (clientsocket, address) = serversocket.accept()
	    clientfile = clientsocket.makefile()
	    while 1:
	    	value = ""
	    	try:
	    		value = json.loads(clientfile.readline())
	    	except Exception:
	    		break

	    	result = calculate(value)
	    	msg = json.dumps(result) + "\n"

	    	try:
	    		clientsocket.send(msg.encode("utf-8"))
	    	except Exception:
	    		break


def calculate(value):
	return {"testout":value["testin"] / 2}


if __name__ == "__main__":
	serverLoop()