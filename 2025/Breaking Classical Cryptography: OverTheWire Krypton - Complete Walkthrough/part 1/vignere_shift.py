#!/usr/bin/python3
# ==============================================================================
# Developed by Cybersecurity Engineer: Abdelrahman Mohamed
# This code is part of the Medium story:
# "Breaking Classical Cryptography: OverTheWire Krypton — Complete Walkthrough (Part 1)"
# https://medium.com/@abdelrhmanmohamed.sec
# https://www.linkedin.com/in/abdelrhman-mohamed-sec
# PURPOSE: Extracts every key_length-th character from a Vigenere ciphertext
#          starting at a given offset (shift). This isolates all characters
#          encrypted by the SAME key byte, turning a Vigenere column into
#          a simple Caesar cipher that can be broken by frequency analysis.
#
#          Example with key_length=3, shift=0: extracts positions 0,3,6,9,...
#          Example with key_length=3, shift=1: extracts positions 1,4,7,10,...
#          Example with key_length=3, shift=2: extracts positions 2,5,8,11,...
#
# Usage:
#   python3 vignere_shift.py <filename> <key_length> [shift]
#   Example: python3 vignere_shift.py found1 3 0   # column 0
#   Example: python3 vignere_shift.py found1 3 1   # column 1
#   Example: python3 vignere_shift.py found1 3 2   # column 2
# ==============================================================================

import sys

if __name__=="__main__":

	key_length = 4
	shift = 0
	out_string = ""

	if len(sys.argv) > 4:
		print("Usage: python3 vignere_shift.py filename key_length [shift]")
		exit(0)
	else:

		try:
			key_length = int(sys.argv[2])
			if len(sys.argv) == 4:
				shift = int(sys.argv[3])
		except:
			print("key_length and [shift] must be an int")
			exit(0)

		try:
			with open(sys.argv[1]) as fh:
				lines = fh.readlines()
		except:
			print("No file named '" + sys.argv[1] + "'")
			exit(0)

		for line in lines:
			line = line.replace(" ", "")
			line = line.replace("\n", "")
			for index in range(shift, len(line)):
				if index % key_length == shift:
					out_string += line[index]

		print(out_string)
