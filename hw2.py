import sys 
import math
import json
import struct
from collections import Counter
from sys import argv

max_lookahead = 64
max_search = 1024

inputfileTop = "/Users/thomashague/Documents/modest proposal.txt"


def LZ77_decoding(inputFile, outputFile):

	f = open(inputFile, "rb")
	bytes = f.read(3)

	outFile = open(outputFile, "wb")

	outputString = ""

	while bytes != "":
		(offset_and_length, char) = struct.unpack(">Hc", bytes)
		offset = offset_and_length>>6
		length = offset_and_length - (offset<<6)
		#print(offset,length,char)

		if(offset == 0 and length == 0):
			outputString = outputString + char
		else:
			copy_idx = len(outputString) - max_search
			if copy_idx < 0:
				copy_idx = 0
			for i in range(0, length): 
				outputString = outputString + outputString[i + offset + copy_idx]
			outputString = outputString + char

		bytes = f.read(3)
	outFile.write(outputString)












def LZ77_search(search, lookahead):
	ls = len(search) #length of the search buffer
	llh = len(lookahead)  #length of the lookahead buffer

	if ls == 0:
		 return (0,0, lookahead[0])
	if llh == 0:
		return null 

	best_offset = 0
	best_length = 0 #is this right?

	buf = search+lookahead 
	search_pointer = ls

	for i in range(0,ls): #all of the potential starting positions for search
		offset = 0
		length = 0
		while buf[i+length] == buf[search_pointer+length]: #is "sp" = spearchpointer?
			#found a match
			length = length + 1
			#check for search reaching the end of the look_ahead
			if search_pointer + length == len(buf):  
				length = length - 1 
				break
		if length > best_length:
			best_offset = i
			best_length = length
	return (best_offset, best_length, buf[search_pointer+best_length])






def main():
	#open output file, read input file.
	output = open("/Users/thomashague/Documents/encoded.txt", 'wb')

	f = open(inputfileTop, "rb")
	input = f.read()

	#initialize variables
	search_idx = 0
	look_idx = 0

	#encoding while loop
	while look_idx < len(input):
		#set up search and lookahead buffers
		search = input[search_idx: look_idx]
		look_ahead = input[look_idx:look_idx+max_lookahead]
		#call search
		tupl = LZ77_search(search, look_ahead)
		#print(tupl)
		#pack the tuple
		offset_length = ((tupl[0]<<6) + tupl[1])
		out_bytes = struct.pack(">Hc", offset_length, tupl[2])  #where tupl[2] = character
		#write to output file
		output.write(out_bytes)
		#update the search_idx and look_idx (slide window)
		look_idx = look_idx + tupl[1] + 1
		search_idx = look_idx - max_search #tupl[1] = "length" in tuple result
		#check if search_idx<0, if so, set it to 0
		if(search_idx < 0):
			search_idx = 0

	output.close()



	LZ77_decoding("/Users/thomashague/Documents/encoded.txt", "/Users/thomashague/Documents/decoded.txt")

	decodedFile = open("/Users/thomashague/Documents/decoded.txt", "rb")
	decodedBytes = decodedFile.read()
	if decodedBytes == input:
		print "success"


main()













