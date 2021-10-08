
## To run the program:

- Install or make sure the following packages are installed in your python environment: rdflib, geopy, sparqlwrapper.
- Make sure blazegraph is installed and up and running.
- Upload "geonamesNOR.ttl" and "graph.txt" to a blazegraph namespace. "geonamesNOR.ttl" will most likely need to be uploaded using the file path type in Blazegraph's UPDATE tab due to it's 580mb size.
- Run the "queries.py" file with your blazegraph URL and namespace set. Alternatively, you can simply look through the program and go to the "query_outputs" folder for sample output data from the queries.

## To retrace the entire project:

- Go to https://www.geonames.org/ontology/documentation.html, under the section "Entry Points into the GeoNames Semantic Web" press the hyperlink "RDF dump" and download the file. (This file is LARGE)
- Go to https://www.nasjonaleturistveger.no/no/presse/%C3%85pne+data and press the hyperlink "Tekster fra nettsiden" and download the file.
- Run the "convertToTurtle.py" file, this will run for 10hrs or so, resulting in a text file called "geonames.txt". (Again, LARGE)
- Run the "onlyNorwegianTriples.py" file, this will give you a text file called "geonamesNOR.txt", refactor this into ".ttl" format.
- Run the "xmlToRdf.py" file with the "turistvegene-data-ut.xml" file in the same folder, this will give you a text file called "graph.txt".
- Follow "To run the program" instructions.



