import graphex

if __name__ == "__main__":
	print("====")
	print("Test")
	print("====")
	print()
	print("======")
	print("Graph1")
	print("======")
	print("Expecting: ")
	print(str(3.14/2))
	print("Result:")
	graphex.GraphEx("../samples/Graph1.json").execute()

	print()
	print("======")
	print("Graph2")
	print("======")
	print("Expecting: ")
	print(str(3.14/2/2))
	print("Result:")
	graphex.GraphEx("../samples/Graph2.json").execute()

	print()
	print("==================")
	print("DuplicateNameGraph")
	print("==================")
	try:
		graphex.GraphEx("../samples/DuplicateNameGraph.json").execute()
		print("This should never be printed.")
	except Exception:
		print("Malformed graph was detected.")

	print()
	print("Done")
	print()