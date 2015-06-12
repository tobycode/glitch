#!/usr/bin/env python
'''
glitch_ui.py:
Randomly corrupts bytes within a file to create glitch art/corruptions.
Just run the script and use the interface.
Alternatively, you can automate the process using the following command line arguments:
glitch.py [input] [amount] [output]
Original glitch logic by Paul Sajna (https://github.com/sajattack)
Interface and optimisations written by tobycode (https://github.com/tobycode)

Use with caution. Do not overwrite files. Written against Python3.
'''

import sys, os, random, time
header_length = {'jpg': 9, 'png': 8, 'bmp': 54, 'gif': 14, 'tiff': 8}

# function for writing a dot for each 100k written
def dot(byte_count):
    if byte_count % 100000 == 0:
        print(".", end="")

# function for corrupting bytes, original by sajattack, modified by tobycode
def glitch(path, amount, output, file_extension):
    if os.path.isdir(path):
        print("The path you specified is a directory, not a file.\nIf you wish to batch corrupt the contents of a folder, you can write a script to do so.\nInformation on doing so is contained in this script's comments.")
        return
    try:
        with open(path, 'rb') as fin:
            with open(output, 'wb') as fout:
                ext = path.split(".")[::-1]
                try:
                    for byte in range(header_length[file_extension[0]]):
                        binf = fin.read(1)
                        bout = binf
                        fout.write(bout)
                except KeyError:
                    print("Can't determine the header length for this file.\nThis may render the output unreadable.")
                    tmp = input("Continue anyway? (Y/n)")
                    if tmp.lower() == "y":
                        pass
                    else:
                        print("Stopping.")
                        return
                if os.path.getsize(path) > 5000000:
                    print("This file might take a while to write.\nDon't close the script - it is still writing your file.")
                bytes_written = 0
                print("Writing bytes", end="")
                time.sleep(0.5)
                while True:
                    binf = fin.read(1)
                    if not binf:
                        break
                    if (random.random() < amount/100):
                        bout = os.urandom(1)
                    else:
                        bout = binf
                    fout.write(bout)
                    bytes_written += 1
                    dot(bytes_written)
                fout.flush()
                fout.close()
    except FileNotFoundError:
        print("Your input file does not exist.")

def main():
    path = "null"
    amount = 0.1
    output = "null"
    file_extension = "null"
    if __name__ == "__main__":
        if len(sys.argv) >= 2:
            path = sys.argv[1]
            file_extension = path.split(".")[::-1]
        if len(sys.argv) >= 3:
            try:
                amount = float(sys.argv[2])
            except ValueError:
                print("[Glitch] Bad value entered for amount, assuming 0.1 (default)")
                amount = 0.1
        if len(sys.argv) >= 4:
            output = sys.argv[3]
        if len(sys.argv) >= 5:
            print("[Glitch] Too many arguments entered. Ignoring " + str(len(sys.argv)) - 4 + " arguments.")
        print("*** glitch.py by sajattack | modified by tobycode ***")
        while path == "null":
            path = input("Enter the path to your input file:\n>>>")
        while True:
            if amount == 0.1:
                try:
                    tmp = input("Enter the percentage of bits to corrupt (or enter/return for 0.1%):\n>>>")
                    if not tmp:
                        break
                    amount = float(tmp)
                    break
                except ValueError:
                    print("You didn't enter a number.")
                    amount = 0.1
            else:
                break
        file_extension = path.split(".")[::-1]
        while output == "null":
            tmp = input("Enter the path to your output file, or nothing to generate one:\n>>>")
            if not tmp:
                output = ""
                for i in path.split(".")[:-1]:
                    output += i
                output += "-glitched.%s" % file_extension[0]
            else:
                output = tmp
        print("Okay, glitching...\nInput:\n\t" + path + "\nGoing to corrupt " + str(amount) + "% of " + str(os.path.getsize(path)) + " bytes.\nOutput:\n\t" + output)
        glitch(path, amount, output, file_extension)
    else:
        print("[Glitch] This function cannot be invoked from within another module.")
        sys.exit(1)
main()