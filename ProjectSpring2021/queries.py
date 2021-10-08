from SPARQLWrapper import SPARQLWrapper, JSON

running = True

namespace = "test" # Put the name of your blazegraph namespace here
sparql = SPARQLWrapper("http://192.168.0.120:19999/blazegraph/namespace/"+ namespace + "/sparql") # This may need to be changed depending on your blazegraph URL

# All the following queries are examples, with your imagination there are endless opportunities to query combinations
# of the geonamesNOR dataset and the turistveg dataset.

def query1():
    '''Gets all turistveger and their predicates and objects.'''
    sparql.setQuery("""
        PREFIX ex: <http://example.org/Tourism/>
        PREFIX wgs84_pos: <http://www.w3.org/2003/01/geo/wgs84_pos#>
        PREFIX gn: <http://www.geonames.org/ontology#>
        SELECT *
        WHERE{
          ?s rdf:type ex:turistveg .
          ?s ?p ?o .
        }
        ORDER BY (?s)
    """)

    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print("Subject: " + result['s']['value'])
        print("Predicate: " + result['p']['value'])
        print("Object: " + result['o']['value'])

def query2():
    '''Gets everything in the turistveg dataset with a geonameID and displays the geonames name from the geonames dataset.'''
    sparql.setQuery("""
        PREFIX ex: <http://example.org/Tourism/>
        PREFIX wgs84_pos: <http://www.w3.org/2003/01/geo/wgs84_pos#>
        PREFIX gn: <http://www.geonames.org/ontology#>
        SELECT ?s ?name
        WHERE{
          ?s ex:geonameID ?o .
          ?o gn:name ?name .
        }
        ORDER BY (?s)
    """)

    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print("Subject: " + result['s']['value'])
        print("Name: " + result['name']['value'])

def query3():
    '''Finds all airports located between the coordinates of turistvegenes start and end.'''
    sparql.setQuery("""
        PREFIX ex: <http://example.org/Tourism/>
        PREFIX wgs84_pos: <http://www.w3.org/2003/01/geo/wgs84_pos#>
        PREFIX gn: <http://www.geonames.org/ontology#>
        
        SELECT ?turistveg ?airport
        WHERE{
          ?turistveg ?p ex:turistveg .
          ?turistveg ex:turistvegStart ?start .
          ?turistveg ex:turistvegEnd ?end .
          ?start wgs84_pos:lat ?startLat .
          ?end wgs84_pos:lat ?endLat .
          ?start wgs84_pos:long ?startLong .
          ?end wgs84_pos:long ?endLong .
          ?link gn:featureCode <https://www.geonames.org/ontology#S.AIRP> .
          ?link wgs84_pos:lat ?airportLat .
          ?link wgs84_pos:long ?airportLong .
          ?link gn:name ?airport .
          FILTER((xsd:float(?airportLat) <= xsd:float(?startLat) && xsd:float(?airportLat) >= xsd:float(?endLat)) || (xsd:float(?airportLat) >= xsd:float(?startLat) && xsd:float(?airportLat) <= xsd:float(?endLat)))
          FILTER((xsd:float(?airportLong) <= xsd:float(?startLong) && xsd:float(?airportLong) >= xsd:float(?endLong)) || (xsd:float(?airportLong) >= xsd:float(?startLong) && xsd:float(?airportLong) <= xsd:float(?endLong)))
        }
        ORDER BY ?turistveg
        """)

    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print("Turistveg: " + result['turistveg']['value'])
        print("Airport: " + result['airport']['value'])

def query4():
    '''Finds any toponym from geonames located between the coordinates of Varanger turistvegs start and end
    and gives their featureCode.'''
    sparql.setQuery("""
                PREFIX ex: <http://example.org/Tourism/>
                PREFIX wgs84_pos: <http://www.w3.org/2003/01/geo/wgs84_pos#>
                PREFIX gn: <http://www.geonames.org/ontology#>
                     
                SELECT ?toponymName ?featureCode
                WHERE{
                  ex:Varanger ex:turistvegStart ?start .
                  ex:Varanger ex:turistvegEnd ?end .
                  ?start wgs84_pos:lat ?startLat .
                  ?end wgs84_pos:lat ?endLat .
                  ?start wgs84_pos:long ?startLong .
                  ?end wgs84_pos:long ?endLong .
                  ?toponym gn:featureCode ?featureCode .
                  ?toponym wgs84_pos:lat ?toponymLat .
                  ?toponym wgs84_pos:long ?toponymLong .
                  ?toponym gn:name ?toponymName .
                  FILTER((xsd:float(?toponymLat) <= xsd:float(?startLat) && xsd:float(?toponymLat) >= xsd:float(?endLat)) || (xsd:float(?toponymLat) >= xsd:float(?startLat) && xsd:float(?toponymLat) <= xsd:float(?endLat)))
                  FILTER((xsd:float(?toponymLong) <= xsd:float(?startLong) && xsd:float(?toponymLong) >= xsd:float(?endLong)) || (xsd:float(?toponymLong) >= xsd:float(?startLong) && xsd:float(?toponymLong) <= xsd:float(?endLong)))
                  }
                  LIMIT 1000
            """)

    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print("Toponym name: " + result['toponymName']['value'])
        print("Feature code: " + result['featureCode']['value'])


def query5():
    '''Get turistveger and their attraksjoner, and the geonames name for the turistattraksjoners nearest coordinate match.
    I also included the attraksjon coordinates and the geonames coordinates for closest toponym to see how closely they match.'''
    sparql.setQuery("""
        PREFIX ex: <http://example.org/Tourism/>
        PREFIX wgs84_pos: <http://www.w3.org/2003/01/geo/wgs84_pos#>
        PREFIX gn: <http://www.geonames.org/ontology#>
        
        SELECT ?turistveg ?attraksjon ?toponymName ?attlat ?toponymlat ?attlong ?toponymlong
        WHERE{
          ?turistveg ?p ex:turistveg .
          ?attraksjon ex:locatedOn ?turistveg .
          ?attraksjon wgs84_pos:lat ?attlat .
          ?attraksjon wgs84_pos:long ?attlong .
          ?attraksjon ex:geonameID ?id .
          ?id wgs84_pos:lat ?toponymlat .
          ?id wgs84_pos:long ?toponymlong .
          ?id gn:name ?toponymName
          }
    """)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print("Turistveg: " + result['turistveg']['value'])
        print("Attraksjon: " + result['attraksjon']['value'])
        print("Toponym name: " + result['toponymName']['value'])
        print("Attraksjon latitude: " + result['attlat']['value'])
        print("Toponym latitude: " + result['toponymlat']['value'])
        print("Attraksjon longitude: " + result['attlong']['value'])
        print("Toponym longitude: " + result['toponymlong']['value'])

def query6():
    '''Get all hotels within 0.1 latitude/longitude degrees of the turistvegattraksjoner.'''
    sparql.setQuery("""
        PREFIX ex: <http://example.org/Tourism/>
        PREFIX wgs84_pos: <http://www.w3.org/2003/01/geo/wgs84_pos#>
        PREFIX gn: <http://www.geonames.org/ontology#>
                            
        SELECT ?attraksjon ?link ?name
        WHERE{
          ?attraksjon rdf:type ex:turistvegAttraksjon .
          ?attraksjon wgs84_pos:lat ?lat .
          ?attraksjon wgs84_pos:long ?long .
          ?link gn:featureCode <https://www.geonames.org/ontology#S.HTL> .
          ?link wgs84_pos:lat ?hLat .
          ?link wgs84_pos:long ?hLong .
          ?link gn:name ?name .
          FILTER(abs(xsd:float(?hLat) - xsd:float(?lat)) <= 0.1 && abs(xsd:float(?hLong) - xsd:float(?long)) <= 0.1)
        }
        ORDER BY ?attraksjon
        """)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print("Attraksjon: " + result['attraksjon']['value'])
        print("Hotel Geonames link: " + result['link']['value'])
        print("Hotel name: " + result['name']['value'])

def query7():
    '''Get all mountains from the geonames dataset that are within 0.3 degree latitude/longitude of a turistvegStart.'''
    sparql.setQuery("""
        PREFIX ex: <http://example.org/Tourism/>
        PREFIX wgs84_pos: <http://www.w3.org/2003/01/geo/wgs84_pos#>
        PREFIX gn: <http://www.geonames.org/ontology#>
        
        SELECT ?start ?mtName ?link 
        WHERE{
          ?link gn:featureCode <https://www.geonames.org/ontology#T.MT> .
          ?link gn:name ?mtName .
          ?link wgs84_pos:lat ?mLat .
          ?link wgs84_pos:long ?mLong .
          ?turistveg ex:turistvegStart ?start .
          ?start wgs84_pos:lat ?lat .
          ?start wgs84_pos:long ?long .
          FILTER(abs(xsd:float(?mLat) - xsd:float(?lat)) < 0.3 && abs(xsd:float(?mLong) - xsd:float(?long)) < 0.3)
          }
          ORDER BY ?start
    """)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print("Turistveg start: " + result['start']['value'])
        print("Mountain: " + result['mtName']['value'])
        print("Geonames link: " + result['link']['value'])

while running:
    print('''
    Write 0 to close the program.
    
    Choose a query by writing a number from 1-7.
    
    1. Gets all turistveger and their predicates and objects.
    2. Gets everything in the turistveg dataset with a geonameID and displays the geonames name from the geonames dataset.
    3. Finds all airports located between the coordinates of turistvegenes start and end.
    4. Finds any toponym from geonames located between the coordinates of Varanger turistvegs start and end and gives their featureCode.
    5. Get turistveger and their attraksjoner, and the geonames name for the turistattraksjoners nearest coordinate match. I also included the attraksjon coordinates and the geonames coordinates for closest toponym to see how closely they match.
    6. Get all hotels within 0.1 latitude/longitude degrees of the turistvegattraksjoner.
    7. Get all mountains from the geonames dataset that are within 0.3 degree latitude/longitude of a turistvegStart.''')

    query = input()

    if query == '1':
        query1()
    if query == '2':
        query2()
    if query == '3':
        query3()
    if query == '4':
        query4()
    if query == '5':
        query5()
    if query == '6':
        query6()
    if query == '7':
        query7()
    if query == '0':
        running = False