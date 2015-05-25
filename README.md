#glitch.py
Randomly changes binary file data in order to create glitch art.
##Usage
```./glitch [infile] [percent] [outfile]```
        
		If the script is run with no arguments, you will be prompted for this information.
		infile: the file you wish to corrupt.
		percent: the overall percentage of bits you wish to corrupt
		outfile: the corrupted output file

Play around with different values for percent, 0.1 seems to work okay for most image formats, 0.01 worked okay for avi video.