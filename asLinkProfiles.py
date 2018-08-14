import json, requests, runtime
from asnake.client import ASnakeClient

# function to find key in nested dictionaries: see http://stackoverflow.com/questions/9807634/find-all-occurences-of-a-key-in-nested-python-dictionaries-and-lists
# and now we're getting fancy!
def gen_dict_extract(key, var):
    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

# This is where we connect to ArchivesSpace.
client = ASnakeClient()
client.authorize() # login, using default values

# provide instructions
print ('This script is used to link all top_containers in a single collection (identified by the ArchivesSpace resource ID number) to a single container_profile (identified by the ArchivesSpace container_profile ID number).')
input('Press Enter to continue...')

# have user enter resource id
resource_id = input('Enter resource ID (in this case, you should enter 1): ')

# search for top_containers linked to entered resource id
endpoint = '/repositories/2/top_containers/search'
advanced_query = json.dumps({
    "filter_term": {
        "field": "collection_uri_u_sstr",
        "value": "/repositories/2/resources/" + resource_id,
        "jsonmodel_type":"field_query"}
})
# Can't use get_paged because this endpoint returns raw Solr
results = client.get(endpoint, params={'aq': advanced_query}).json()["response"]["docs"]

# populate top_containers with the ids of each top_container in search results
top_containers = []
for value in gen_dict_extract('id', results):
    top_containers.append(value)

# GET each top_container listed in top_containers and add to records
records = []
for top_container in top_containers:
    output = client.get(top_container).json()
    records.append(output)

# have user enter container profile id
profile_id = input('Enter container profile ID (I am going to enter 9. You can select another value, as long that ID is in your instance of ArchivesSpace.): ')

# Add container profile to records and post
print ('The following records have been updated in ArchivesSpace:')
for record in records:
    record['container_profile'] = {'ref': '/container_profiles/' + profile_id}
    jsonLine = record
    uri = record['uri']
    post = client.post(uri, json=jsonLine).json()
    print(post)
