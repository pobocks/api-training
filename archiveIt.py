import requests, json, runtime
from asnake.client import ASnakeClient
# provide instructions
print('This script is used to generate new digital objects within an ArchivesSpace collection for websites crawled in an Archive-It collection.  Please note: This is a "proof of concept" script, NOT completed work.  Do not use in production scenarios.')
input('Press Enter to continue...')

# This is where we connect to ArchivesSpace.
client = ASnakeClient()
client.authorize() # login, using default values

# archiveit_coll = raw_input('Enter the Archive-It collection number: ')
archiveit_coll = '3181'

# search AS for archival_object's with level "Web archive"

warchives = list(client.get_paged(  # get_paged returns an iterator, so wrap in list since we use it multiple times
    'search',                              # the query URL
    params={
        "filter": json.dumps(              # use json.dumps to serialize the query JSON into a string - remember that query is passed as a GET param in the URL
            {"query":
             {"jsonmodel_type": "boolean_query",
              "op":"AND",
              "subqueries":[
                  {"jsonmodel_type":"field_query",
                   "field":"primary_type",
                   "value":"archival_object",
                   "literal":true},
                  {"jsonmodel_type":"field_query",
                   "field":"level",
                   "value":"Web archive",
                   "literal":true},
                  {"jsonmodel_type":"field_query",
                   "field":"types",
                   "value":"pui",
                   "literal":true}
              ]
             }
            } # end query
        ) # end json.dumps
    } # end params
)) # end list and client.get_paged

print('Found ' + str(len(warchives)) + ' archival objects with the instance type "Web archive."')

# grab needed fields out of ao
for ao in warchives:
    url = ao['title']
    uri = ao['uri']

    # search AI and get json of crawls for url listed in AS ao's title field
    request = 'http://wayback.archive-it.org/' + archiveit_coll + '/timemap/json/' + url
    AIoutput = requests.get(request).json()
    print('Found ' + str(len(AIoutput)-1) + ' Archive-It crawls of ' + url + '.')

    # take AI json lists and convert to python dicts
    keys = AIoutput[0]
    crawlList = []
    for AIlist in AIoutput[1:]:
        crawl = {}
        for j in range (0, len(AIlist)):
            crawl[keys[j]] = AIlist[j]
        crawlList.append(crawl)

    # construct digital object json from Archive-It output and post to AS
    print('The following digital objects have been created in ArchivesSpace:')
    newInstances = []
    for crawl in crawlList:
        doid = 'https://wayback.archive-it.org' + '/' + archiveit_coll + '/' + crawl['timestamp'] + '/' + crawl['original']
        filter_query=json.dumps({
            "query":{
                "jsonmodel_type":"boolean_query",
                "op":"AND",
                "subqueries":[
                    {
                        "jsonmodel_type":"field_query",
                        "field":"primary_type",
                        "value":"digital_object",
                        "literal":True},
                    {
                        "jsonmodel_type":"field_query",
                        "field":"digital_object_id",
                        "value": str(doid),
                        "literal":True
                    }
                ]
            }
        })

        existingdoID = list(client.get_paged(search, params={"filter": filter_query}))
        doPost = {}
        if len(existingdoID) != 0:
            print('Digital object already exists.')
        else:
            doPost['digital_object_id'] = doid
            doPost['title'] = 'Web crawl of ' + crawl['original']
            doPost['dates'] = [{'expression': crawl['timestamp'], 'date_type': 'single', 'label': 'creation'}]
            doPost['file_versions'] = [{'file_uri': crawl['filename'], 'checksum': crawl['digest'], 'checksum_method': 'sha-1'}]
        if doPost != {}:
            post = requests.post('/repositories/2/digital_objects', json=doPost).json()
            print(post)
            doItem = {}
            doItem['digital_object'] = {'ref': post['uri']}
            doItem['instance_type'] = 'digital_object'
            newInstances.append(doItem)
    aoGet = client.get(uri).json()
    existingInstances = aoGet['instances']
    existingInstances = existingInstances + newInstances
    aoGet['instances'] = existingInstances
    aoUpdate = client.post(uri, json=aoGet).json()
    print('The following archival objects have been updated in ArchivesSpace:')
    print(aoUpdate)

# TO DO LATER
# Parse dates for ArchivesSpace record, push to AOs above
# Add phystech stating "Archived website" to ASpace resource record
# Add "Web sites" subject tracing to ASpace resource record
# Deal with the fact that this should be able to be run for multiple AI collections (at present limited to one declared in script)
# Improve logic for determining whether something is a duplicate
