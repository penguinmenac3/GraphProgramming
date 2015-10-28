import graphex
import time
from threading import Thread
import external.server as server

if __name__ == "__main__":
	print("====")
	print("Test")
	print("====")
	print(" ")
	print("Starting server.")
	Thread(target=server.serverLoop).start()
	time.sleep(0.2)

	print(" ")
	print("======================")
	print("Graph1WithNetwork.json")
	print("======================")
	print("Expecting: ")
	print(str(3.14/2))
	print("Result:")
	graphex.GraphEx("../samples/Graph1WithNetwork.json").execute()

	print(" ")
	print("Done")
	print(" ")