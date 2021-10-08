# This script just takes advantage of how the "geonames.txt"
# file is layed out and finds every resource that has the norwegian country code
# in it and writes it to a new text file, leaving us with only the norwegian toponyms
# from the database in turtle format

# In my experience, after this script is done, the file format of "geonamesNOR.txt" had to be changed to ".ttl" format
# before uploading to blazegraph

toponyms = 0
fo = open("geonamesNOR.txt", "w")
# errors are set to ignore as there are quite a few letters in foreign languages that
# sometimes messed with the formatting
with open("geonames.txt", errors='ignore') as fileobject:
    count = 0
    resource = ''
    # Essentially every time it finds '\n' (new line) twice it sets it as a -
    # resource and writes it if it has the norwegian countrycode in it.
    for line in fileobject:
        resource += line
        if line == '\n':
            count += 1
            if count % 2 == 0:
                if 'gn:countryCode "NO"' in resource:
                    fo.write(resource)
                    resource = ''
                    toponyms += 1
                else:
                    resource = ''

print(toponyms)
fo.close()