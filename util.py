#!/usr/bin/python3

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
	
	#Assign args/flags based on arguments received
	for opt, arg in opts:
		if opt == "-h":
			print_usage()
			sys.exit()
		elif opt == "-f" or opt == "--first":
			try:
				numFirst=int(arg)
			except ValueError:
				print("Invalid value for argument "+opt)
				print_usage()
				sys.exit(1)
		elif opt == "-l" or opt == "--last":
			try:
				numLast=int(arg)
			except ValueError:				
				print("Invalid value for argument "+opt)
				print_usage()
				sys.exit(1)
		elif opt == "-t" or opt == "--timestamps":
			timestampFlag=True
		elif opt == "-i" or opt == "--ipv4":
			ipv4Flag=True
		elif opt == "-I" or opt == "--ipv6":
			ipv6Flag=True
		elif opt == "-m" or opt == "--ipv4m":
			ipv4Flag=True
			ipv4String=arg
		elif opt == "-M" or opt == "--ipv6m":
			ipv6Flag=True
			ipv6String=arg

	#Validate file presence
	lines=[]
	try:
		inputFile=args[0]
		with open(inputFile) as fp:
			lines = [line.rstrip('\n') for line in fp]
	except IndexError:
		#print("File argument missing, reading from standard input....")
		if sys.stdin.isatty():
			print("File argument missing and no input received from stdin, exiting!")
			sys.exit(1)
		lines=[line.rstrip('\n') for line in sys.stdin]
	except IOError:
		print("File not found!")
		print_usage()
		sys.exit(1)
	except Exception as e:
   		print("Unexpected error: "+str(e))

   	

	#Set header and footer "bucket" limits, if no options were given
	if numFirst==-1:
		numFirst=len(lines)
	if numLast==-1:
		numLast=len(lines)

	#check no intersection with header and footer limits
	if numFirst+numLast<=len(lines):
		lines=[]
		check_no_intersect(lines)

	#break down based on header/footer limits
	lines=lines[len(lines)-numLast:numFirst]


	#if timestampflag is set, check for matches with HH:MM:SS
	if timestampFlag:		
		lines=match_regex_lines("([01]\d|2[0-3]):([0-5][0-9]):([0-5][0-9])",lines)

	#Exit if intersection is empty
	check_no_intersect(lines)
 
	#if ipv4Flag is set, check for matches with [0-255].[0-255].[0-255].[0-255]
	if ipv4Flag:
		lines=match_regex_lines("((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.)){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\D+)",lines)
		#Check for wildcard in ip match argument string to highlight
		if ipv4String != "":
			match_expr=""
			for idx,substring in enumerate(ipv4String.split(".")):
				if substring=="*":
					if idx==3: #end token
						match_expr+="(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\D+)"
					else:						
						match_expr+="((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.))"
				else:
					if idx==3:
						match_expr+=substring
					else:
						match_expr+=substring+"."
			#Highlight line if match
			for idx,line in enumerate(lines):
				if re.search(match_expr,line):
					lines[idx]="[IPV4 MATCH]"+lines[idx]


	#if ipv6Flag is set, check for matches with [0000-ffff]:[0000-ffff]:[0000-ffff]:[0000-ffff]:[0000-ffff]:[0000-ffff]:[0000-ffff]:[0000-ffff]
	if ipv6Flag:
		lines=match_regex_lines("((([0-9]|[a-f]|[A-F]){4})(\:)){7}((([0-9]|[a-f]|[A-F]){4}))",lines)
		#Check for wildcard in ip match argument string to highlight
		if ipv6String != "":
			match_expr=""
			for idx,substring in enumerate(ipv6String.split(":")):
				if substring=="*":
					if idx==7: #end token
						match_expr+="(([0-9]|[a-f]|[A-F]){4})"
					else:						
						match_expr+="((([0-9]|[a-f]|[A-F]){4})(\:))"
				else:
					if idx==7:
						match_expr+=substring
					else:
						match_expr+=substring+":"
			#Highlight line if match
			for idx,line in enumerate(lines):
				if re.search(match_expr,line):
					print(lines[idx])
					lines[idx]="[IPV6 MATCH]"+lines[idx]			
					print(lines[idx])

	#Exit if intersection is empty
	check_no_intersect(lines)

	print_log(lines)

def print_usage():
	print("Usage: ./util.py [OPTION]... [FILE]\n\
\n\
Supported options:\n\
---------------------\n\
	-h, --help Print help\n\
	-f, --first NUM Print first NUM lines\n\
	-l, --last NUM Print last NUM lines\n\
	-t, --timestamps Print lines that contain a timestamp in HH:MM:SS format\n\
	-i, --ipv4 Print lines that contain an IPv4 address\n\
	-I, --ipv6 Print lines that contain an IPv6 address (standard notation)\n\
	-m, --ipv4m Print lines that contain an IPv4 address, matching IPs are highlighted, accepts wildcards *\n\
	-M, --ipv6m Print lines that contain an IPv6 address (standard notation), matching IPs are highlighted, accepts wildcards *\n")

def check_no_intersect(lines):
	if lines==[]:
		print("No lines found in log file with current options!")
		sys.exit()

def print_log(lines):
	for line in lines:
		print(line)

def match_regex_lines(expr,lines):
	res_lines=[]
	for line in lines:
		if re.search(expr,line):
			res_lines.append(line)
	return res_lines

if __name__ == "__main__":
   main(sys.argv[1:])