#!/usr/bin/env python
# glitch.py:
# Randomly corrupts bytes within a file to create glitch art.
# Just run the script and use the interface.
# If you want, you can automate the process with the following command line arguments:
# glitch.py [input] [amount] [output]
# Original code written by Paul Sajna (https://github.com/sajattack : https://github.com/sajattack/glitch/)
# Interface and optimisations by Toby Jones (https://github.com/tobyjonesdev)
# Use with caution. Written against Python3.

import sys, os, random
header_length = {'jpg': 9, 'png': 8, 'bmp': 54, 'gif': 14, 'tiff': 8}

# function for corrupting bytes. written by sajattack
def glitch(path, amount, output, file_extension):
	try:
		# create a few temp file objects for our input and output
		with open(path, 'rb') as fin:
			with open(output, 'wb') as fout:
				# get file extension from path
				ext = path.split(".")[::-1]
				try:
					for byte in range(header_length[file_extension[0]]):
						bin = fin.read(1)
						bout = bin
						fout.write(bout)
				except KeyError:
					print("Cannot determine the header length for this file.\nTherefore, corrupting it may render it unusable.")
					tmp = input("Continue anyway? (Y/n)")
					if tmp.lower() == "y":
						pass
					else:
						print("Stopping.")
						return
				bytes_written = 0
				print("Writing bytes", end="")
				while True:
					bin = fin.read(1)
					if not bin:
						break
					if (random.random() < amount/100):
						bout = os.urandom(1)
					else:
						bout = bin
					fout.write(bout)
					bytes_written += 1
					if bytes_written % 1000 == 0:
						print(".", end="")
				fout.flush()
				fout.close()
	except FileNotFoundError:
		print("Sorry, your input file couldn't be found.")

def invokeUserInterface():
	path = "null"
	amount = 0.1
	output = "null"
	file_extension = ""
	if __name__ == "__main__":
		if len(sys.argv) == 2:
			path = sys.argv[1]
			file_extension = path.split(".")[::-1]
		elif len(sys.argv) == 3:
			path = sys.argv[1]
			file_extension = path.split(".")[::-1]
			try:
				amount = float(sys.argv[2])
			except ValueError:
				print("[Glitch] Bad value entered for amount. Assuming default.")
				amount = 0.1
		elif len(sys.argv) == 4:
			path = sys.argv[1]
			file_extension = path.split(".")[::-1]
			try:
				amount = float(sys.argv[2])
			except ValueError:
				print("[Glitch] Bad value entered for amount. Assuming default.")
				amount = 0.1
			output = sys.argv[3]
		elif len(sys.argv) > 4:
			print("[Glitch] Too many arguments entered. Accepting the first three.")
			path = sys.argv[1]
			file_extension = path.split(".")[::-1]
			try:
				amount = float(sys.argv[2])
			except ValueError:
				print("[Glitch] Bad value entered for amount. Assuming default.")
				amount = 0.1
			output = sys.argv[3]
		print("glitch.py by sajattack, modified by tobycode\n")
		while path == "null":
			path = input("Enter the path to your input file:\n>>> ")
		
		while True:
			if amount == 0.1:
				try:
					tmp = input("Enter the percentage of bits to corrupt, or hit enter for 0.1%:\n>>> ")
					if not tmp:
						break
					float(tmp)
					break
				except ValueError:
					pass
			else:
				break
		
		file_extension = path.split(".")[::-1]
		while output == "null":
			tmp = input("Enter the path to your output file, or nothing to generate one:\n>>> ")
			if not tmp:
				output = ""
				for i in path.split(".")[:-1]:
					output += i
				output += "-glitched."
				output += str(file_extension[0])
			else:
				output = tmp
		print("Okay, glitching...")
		print("Input:\n\t" + path)
		print("Going to corrupt " + str(amount) + "% of bits.")
		print("Output:\n\t" + output)
		glitch(path, amount, output, file_extension)
	else:

		print("[Glitch] This function cannot be invoked from within another module. Sorry.")
		sys.exit(1)
invokeUserInterface()