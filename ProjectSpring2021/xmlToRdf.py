from rdflib import Graph, Literal, Namespace, URIRef, BNode
from rdflib.namespace import RDF, RDFS, XSD
import xml.etree.ElementTree as ET
from rdflib.collection import Collection
from geo import reverse_geo, reverse_geo_address

g = Graph()
ex = Namespace("http://example.org/Tourism/")
gn = Namespace("http://www.geonames.org/ontology#")
wgs84_pos = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")

g.bind("ex", ex)
g.bind("gn", gn)
g.bind("wgs84_pos", wgs84_pos)

tree = ET.parse("turistvegene-data-ut.xml")
root = tree.getroot()

for turistveg in root.findall('turistveg'):
    # Finds the data in the different xml tags
    title = turistveg.find('title').text.title().replace(' ', '') # Capitalizes all words in title and removes spaces
    length = turistveg.find('length').text
    sealevel = turistveg.find('sealevel').text
    total_ferries = turistveg.find('totalferries').text
    lat_start = turistveg.find('latitude-start').text
    lat_end = turistveg.find('latitude-end').text
    long_start = turistveg.find('longitude-start').text
    long_end = turistveg.find('longitude-end').text

    # Gives the geonames geonameID from reverse geocoding the coordinates through geonames API
    # see "geo.py" file
    start = reverse_geo(lat_start + ',' + long_start)
    end = reverse_geo(lat_end + ',' + long_end)
    start_geoID = start[1]
    end_geoID = end[1]

    # Gives address info through Nominatim reverse geocoding.
    address_start_rev = reverse_geo_address(lat_start + ',' + long_start)
    address_end_rev = reverse_geo_address(lat_end + ',' + long_end)
    municipality_start = address_start_rev[0]
    municipality_end = address_end_rev[0]
    postcode_start = address_start_rev[1]
    postcode_end = address_end_rev[1]
    county_start = address_start_rev[2]
    county_end = address_end_rev[2]
    hamlet_start = address_start_rev[3]
    hamlet_end = address_end_rev[3]

    # Adds all turistveger with title, length_km, altitude and total ferries.
    g.add((ex.turistveg, RDF.type, RDFS.Class))
    g.add((URIRef(ex + title), RDF.type, ex.turistveg))
    g.add((URIRef(ex + title), ex.Length_km, Literal(length, datatype=XSD.integer)))
    g.add((ex.Length_km, RDFS.domain, ex.turistveg))
    g.add((URIRef(ex + title), wgs84_pos.alt, Literal(sealevel, datatype=XSD.integer)))
    g.add((URIRef(ex + title), ex.totalFerries, Literal(total_ferries, datatype=XSD.integer)))
    g.add((ex.totalFerries, RDFS.domain, ex.turistveg))

    # Adds the start of the turistveg as it's own class with coordinates and geonamesID that can be used as a reference
    # to the geonames database
    g.add((ex.turistvegStart, RDF.type, RDFS.Class))
    g.add((URIRef(ex + title + 'Start'), RDF.type, ex.turistvegStart))
    g.add((URIRef(ex + title), ex.turistvegStart, URIRef(ex + title + 'Start')))
    g.add((URIRef(ex + title + 'Start'), wgs84_pos.lat, Literal(lat_start, datatype=XSD.float)))
    g.add((URIRef(ex + title + 'Start'), wgs84_pos.long, Literal(long_start, datatype=XSD.float)))
    g.add((URIRef('https://sws.geonames.org/' + str(start_geoID) + '/'), RDF.type, gn.Feature))
    g.add((URIRef(ex + title + 'Start'), ex.geonameID, URIRef('https://sws.geonames.org/'+str(start_geoID)+'/')))

    # Adds address information to the start
    address_start = BNode()
    g.add((URIRef(ex + title + 'Start'), ex.address, address_start))
    g.add((address_start, RDF.type, ex.Address))
    g.add((address_start, ex.municipality, Literal(municipality_start)))
    g.add((address_start, ex.postalCode, Literal(postcode_start)))
    g.add((address_start, ex.county, Literal(county_start)))
    g.add((address_start, ex.hamlet, Literal(hamlet_start)))

    # Adds the end of the turistveg as it's own class with coordinates and geonamesID that can be used as a reference
    # to the geonames database
    g.add((ex.turistvegEnd, RDF.type, RDFS.Class))
    g.add((URIRef(ex + title + 'End'), RDF.type, ex.turistvegEnd))
    g.add((URIRef(ex + title), ex.turistvegEnd, URIRef(ex + title + 'End')))
    g.add((URIRef(ex + title + 'End'), wgs84_pos.lat, Literal(lat_end, datatype=XSD.float)))
    g.add((URIRef(ex + title + 'End'), wgs84_pos.long, Literal(long_end, datatype=XSD.float)))
    g.add((URIRef('https://sws.geonames.org/' + str(end_geoID) + '/'), RDF.type, gn.Feature))
    g.add((URIRef(ex + title + 'End'), ex.geonameID, URIRef('https://sws.geonames.org/' + str(end_geoID) + '/')))

    # Adds address information to the end
    address_end = BNode()
    g.add((URIRef(ex + title + 'End'), ex.address, address_end))
    g.add((address_end, RDF.type, ex.Address))
    g.add((address_end, ex.municipality, Literal(municipality_end)))
    g.add((address_end, ex.postalCode, Literal(postcode_end)))
    g.add((address_end, ex.county, Literal(county_end)))
    g.add((address_end, ex.hamlet, Literal(hamlet_end)))

    # We didn't find descriptions to really be something that is valuable to this project
    # However, it could be added as RDFS.comment
    # description_no = turistveg.find('description_no').text
    # description_en = turistveg.find('description_en').text
    # description_de = turistveg.find('description_de').text
    # g.add((URIRef(ex + title), RDFS.comment, Literal(description_no, lang='no')))
    # g.add((URIRef(ex + title), RDFS.comment, Literal(description_en, lang='en')))
    # g.add((URIRef(ex + title), RDFS.comment, Literal(description_de, lang='de')))


    for t_veg_att in turistveg.find('turistveg-attraksjoner'):
        att_title = t_veg_att.find('title').text.title().replace(' ', '') # Capitalizes all words in title and removes spaces
        lat = t_veg_att.find('latitude').text
        long = t_veg_att.find('longitude').text

        # Gives address info through Nominatim reverse geocoding to "turistvegattraksjoner"
        att_address_rev = reverse_geo_address(lat + ',' + long)
        att_municipality = att_address_rev[0]
        att_postcode = att_address_rev[1]
        att_county = att_address_rev[2]
        att_hamlet = att_address_rev[3]

        # Uses geonames reverse geocoding to get the geonamesID of the nearest toponym given the lat-long coordinates
        att_geoID = reverse_geo(lat + ',' + long)[1]

        # Adds all turistvegattraksjoner with latitude, longitude, geonamesID and what turistveg they are located on
        g.add((ex.turistvegAttraksjon, RDF.type, RDFS.Class))
        g.add((URIRef(ex + att_title), RDF.type, ex.turistvegAttraksjon))
        g.add((URIRef(ex + att_title), ex.locatedOn, URIRef(ex + title)))
        g.add((URIRef(ex + title), ex.attraksjoner, URIRef(ex + title + '-Attraksjoner')))
        Collection(g, URIRef(ex + title + '-Attraksjoner'),
                   [URIRef(ex + att_title)])
        g.add((URIRef(ex + att_title), wgs84_pos.lat, Literal(lat, datatype=XSD.float)))
        g.add((URIRef(ex + att_title), wgs84_pos.long, Literal(long, datatype=XSD.float)))

        g.add((URIRef('https://sws.geonames.org/' + str(att_geoID) + '/'), RDF.type, gn.Feature))
        g.add((URIRef(ex + att_title), ex.geonameID, URIRef('https://sws.geonames.org/' + str(att_geoID) + '/')))

        address_att = BNode()
        g.add((URIRef(ex + att_title), ex.address, address_att))
        g.add((address_att, RDF.type, ex.Address))
        g.add((address_att, ex.municipality, Literal(att_municipality)))
        g.add((address_att, ex.postalCode, Literal(att_postcode)))
        g.add((address_att, ex.county, Literal(att_county)))
        g.add((address_att, ex.hamlet, Literal(att_hamlet)))

        # We didn't find descriptions to really be something that is valuable to this project
        # However, it could be added as RDFS.comment
        # att_description_no = t_veg_att.find('description_no')
        # att_description_en = t_veg_att.find('description_en')
        # att_description_de = t_veg_att.find('description_de')
        # g.add((URIRef(ex + att_title), RDFS.comment, Literal(att_description_no, lang='no)))
        # g.add((URIRef(ex + att_title), RDFS.comment, Literal(att_description_en, lang='en)))
        # g.add((URIRef(ex + att_title), RDFS.comment, Literal(att_description_de, lang='de')))

# Write to text file
g.serialize(destination='graph.txt', format='turtle')

# Print in terminal
#print(g.serialize(format='turtle').decode())