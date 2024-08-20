#
# Very simple script to fetch records from the IDL Solr endpoint https://metadata.idl.ucsf.edu
# Download endpoint is https://download.industrydocuments.ucsf.edu
#
#

from timeit import default_timer as timer

from urllib.request import urlopen
import json
import urllib.parse

# SAMPLE COLLECTION CODES
# code name
# mck McKinsey
# pm Philip Morris
# pfas PFAS Collection

#Get a records for a specific collection see above
query ="collectioncode:mck"

# Get records with update date after a certain date (2022-12-01T00:00:00Z)
#query ='ddmudate:[2022-12-01T00:00:00Z TO *] AND industry:opioids'

query = urllib.parse.quote(query)

done = False
count = 0
curserMark = "*"
rows = "1000" #Max rows per page
fieldList = "fl=id,artifact&" # Example of limiting fields to be returned. If you only need the metadata for artifacts(files) for example
#fieldList = ""
start = timer()

while not done:

    res = urlopen('https://metadata.idl.ucsf.edu/solr/ltdl3/select?q='+query+'&wt=json&rows='+rows+'&sort=id+asc&'+fieldList+'cursorMark='+curserMark).read()
    response = json.loads(res)
    nextCurserMark = response['nextCursorMark']

    if (count > 0 and count % 10000 == 0 ):

        print( "Count: %s" % count)
        end = timer()
        print (end-start)
        start = timer()

    if (count == 0):

        print(response['response']['numFound'])

    #print( curserMark,nextCurserMark,len(response['response']['docs']) )
    count = count +  len(response['response']['docs'])

    # DO STUFF WITH THE RECRODS
    for document in response['response']['docs']:

        #Metadata such as ID
        documentId = document['id']
        print ("RecordId: %s" %documentId)
        #print (documentId)
        # Store the artifact metadata or use it directly to download:
        print ("Available artifacts (files): %s" %document.get('artifact','[]'))
        print ("Base URL for the files: https://download.industrydocuments.ucsf.edu/%s/%s/%s/%s/%s" %(documentId[0],documentId[1],documentId[2],documentId[3],documentId))
        # Use other metadata fields:
        #print ("Title: %s" %document.get('ti', "No Title"))

    if (curserMark==nextCurserMark):

        done = True

    curserMark = nextCurserMark



