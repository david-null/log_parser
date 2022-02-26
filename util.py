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

	#Validate arguments using getopt
	try:
		opts,args=getopt.getopt(argv,"hf:l:tiIm:M:",["help","first=","last=","timestamps","ipv4","ipv6","ipv4m=","ipv6m="])
	except getopt.GetoptError:		
		print("Invalid Input\n")
		print_usage()
		sys.exit(1)
	

	#Validate file presence
	lines=[]
	try:
		inputFile=args[0]
		with open(inputFile) as fp:
			lines = [line.rstrip('\n') for line in fp]
	except IndexError:
		#print("File argument missing, reading from standard input....")
		lines=[line.rstrip('\n') for line in sys.stdin]
	except IOError:
		print("File not found!\n")
		sys.exit(1)
	except Exception as e:
   		print("Unexpected error: "+str(e))

   	#Assign args/flags based on arguments received
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

	#print([numFirst,numLast])
	#print(str(timestampFlag)+","+str(ipv4Flag)+","+str(ipv6Flag))
	#print(ipv4String+","+ipv6String)

	#Set header and footer "bucket" limits, if no options were given
	if numFirst==-1:
		numFirst=len(lines)
	if numLast==-1:
		numLast=len(lines)

	#check no intersection with header and footer limits
	if numFirst+numLast<=len(lines):
		print_no_intersect()

	#break down based on header/footer limits
	lines=lines[len(lines)-numLast:numFirst]

	res_lines=[]

	#if timestampflag is set, check for matches with HH:MM:SS
	if timestampFlag:
		for line in lines:
			if re.search("([01]\d|2[0-3]):([0-5][0-9]):([0-5][0-9])",line):
				res_lines+=line
		lines=res_lines

	#Exit if intersection is empty

	if lines==[]:
		print_no_intersect()




def print_usage():
	print("Usage: python3 util.py [OPTION]... [FILE]\n\
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

def print_no_intersect():
	print("No lines found in log file with current options!")
	sys.exit()

def print_log(lines):
	for line in lines:
		print(line)

if __name__ == "__main__":
   main(sys.argv[1:])