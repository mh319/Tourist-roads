# In the spirit of linked data, this script was found by me -
# from https://gist.github.com/baskaufs/54207ab81eee4f9aa468137df5967d30 -
# I only changed formatting from N-Triples to Turtle.
# His script was again found from -
# https://github.com/rhasan/sw/blob/master/genames/convert2ntriples.py

import rdflib

# This rewrites the weird xml-ish format of the "all-geonames-rdf.txt" file that can be found here:
#
# This takes the rdf data dump and turns it into turtle format in a text file.
# The script runs for 10hrs+

fo = open("geonames.txt", "wb")
totalStmt = 0
with open("all-geonames-rdf.txt", encoding="utf8") as fileobject:
    count = 0
    for line in fileobject:
        if count/10000 == int(count/10000):
            print(count)

        if count%2 != 0:
            g = rdflib.Graph()
            result = g.parse(data=line,format='xml')
            totalStmt += len(g)
            s = g.serialize(format='turtle')
            fo.write(s)

        count += 1

print ("Total statements: ", totalStmt)
fo.close()