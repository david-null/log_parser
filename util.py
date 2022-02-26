import sys, getopt, re

def main(argv):
	inputFile=""
	numFirst=-1
	numLast=-1
	timestampFlag=False
	ipv4Flag=False
	ipv6Flag=False
	ipv4String=""
	ipv6String=""
	try:
		opts,args=getopt.getopt(argv,"hf:l:tiIm:M:",["help","first=","last=","timestamps","ipv4","ipv6","ipv4m=","ipv6m="])
	except getopt.GetoptError:		
		print("Invalid Input\n")
		print_usage()
		sys.exit(1)
	for opt, arg in opts:
		if opt == "-h":
			print_usage()
			sys.exit()
		elif opt == "-f" or opt == "--first":
			numFirst=int(arg)
		elif opt == "-l" or opt == "--last":
			numLast=int(arg)
		elif opt == "-t" or opt == "--timestamps":
			timestampFlag=True
		elif opt == "-i" or opt == "--ipv4":
			ipv4Flag=True
		elif opt == "-I" or opt == "--ipv6":
			ipv6Flag=True
		elif opt == "-m" or opt == "--ipv4m":
			ipv4String=arg
		elif opt == "-M" or opt == "--ipv6m":
			ipv6String=arg
	print([numFirst,numLast])
	print(str(timestampFlag)+","+str(ipv4Flag)+","+str(ipv6Flag))
	print(ipv4String+","+ipv6String)

def print_usage():
	print("\n\
Usage: ./util.py [OPTION]... [FILE]\n\
\n\
Supported options:\n\
---------------------\n\
	- h, --help Print help\n\
	- f, --first NUM Print first NUM lines\n\
	- l, --last NUM Print last NUM lines\n\
	- t, --timestamps Print lines that contain a timestamp in HH:MM:SS format\n\
	- i, --ipv4 Print lines that contain an IPv4 address\n\
	- I, --ipv6 Print lines that contain an IPv6 address (standard notation)\n\
	- m, --ipv4m Print lines that contain an IPv4 address, matching IPs are highlighted\n\
	- M, --ipv6m Print lines that contain an IPv6 address (standard notation), matching IPs are highlighted\n")

if __name__ == "__main__":
   main(sys.argv[1:])