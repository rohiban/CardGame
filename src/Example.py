from sys import argv
from os.path import exists

script, fromfile, tofile = argv

inputfile = open(fromfile)
data = inputfile.read()

print "The input file is %d bytes long" % len(data)

print "Does the output file exist? %r " %exists(tofile)
outputfile = open(tofile, "w")
outputfile.write(data)

print "Done ..."
outputfile.close()
inputfile.close()
