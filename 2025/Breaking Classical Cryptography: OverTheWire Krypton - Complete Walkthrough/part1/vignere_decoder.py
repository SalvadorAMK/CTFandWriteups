#!/usr/bin/python3
# ==============================================================================
# Developed by Cybersecurity Engineer: Abdelrahman Mohamed
# This code is part of the Medium story:
# "Breaking Classical Cryptography: OverTheWire Krypton — Complete Walkthrough (Part 1)"
# https://medium.com/@abdelrhmanmohamed.sec
# https://www.linkedin.com/in/abdelrhman-mohamed-sec
# PURPOSE: Decodes a Vigenere-encrypted ciphertext using a known key.
#          For each character at index i in the ciphertext, subtracts the
#          corresponding key character (key[i % len(key)]) modulo 26.
#          Formula: plaintext[i] = (ciphertext[i] - key[i % keylen]) mod 26
#
# Usage:
#   python3 vignere_decoder.py <filename> <key>
#   Example: python3 vignere_decoder.py krypton4 KEY
# ==============================================================================

import sys

key = ""
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

if __name__=="__main__":

	out_string = ""

	if (len(sys.argv)) != 3:
		print("Usage: python3 vignere_decoder.py filename key")
		exit(0)
	else:

		key = sys.argv[2]

		print("Decoding file '" + sys.argv[1] + "' with key '" + sys.argv[2] + "':\n")

		try:
			with open(sys.argv[1]) as fh:
				lines = fh.readlines()
		except:
			print("No file named '" + sys.argv[1] + "'")
			exit(0)

		for line in lines:
			line = line.replace(" ", "")
			line = line.replace("\n", "")
			for index in range(len(line)):
				c = alphabet[(alphabet.index(line[index]) - alphabet.index(key[index % len(key)])) % 26]
				out_string += c

	print(out_string)
