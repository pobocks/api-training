import json, csv, os, runtime
from time import sleep
from asnake.client import ASnakeClient

# This is where we connect to ArchivesSpace.
client = ASnakeClient()
client.authorize() # login, using default values

# User supplied filename
do_csv = input('Enter csv filename: ')
base_file_name = os.path.basename(do_csv)

# Open csv, create new csv
csv_dict = csv.DictReader(open(do_csv, 'r', encoding='utf-8'))
f=csv.writer(open(base_file_name + '.just_posted.csv', 'w'))
f.writerow(['title', 'digital_object_id', 'digital_object_uri', 'archival_object_uri'])

# Note: if this script is re-run to create new digital objects or updated to include additional rows
# (e.g. after changing the do object IDs, or if you attempt to add another row that references a preceding archival object)
# then only the most-recently created digital objects will be linked
# and the previously-created digital objects will be orphaned records.

# Parse csv and update ArchivesSpace.
for row in csv_dict:
    file_uri = row['fileuri']
    title = row['title']
    digital_object_id = row['objectid']
    ref_ID = row['refID']
    # Construct new digital object from csv
    doRecord = {'title': title, 'digital_object_id': digital_object_id, 'publish': False}
    doRecord['file_versions'] = [{'file_uri': file_uri, 'publish': False, 'file_format_name': 'jpeg'}]

    doPost = client.post('/repositories/2/digital_objects', json=doRecord).json()
    print(doPost)
    # Store uri of newly posted digital objects because we'll need it
    uri = doPost['uri']
    # Find AOs based on refIDs supplied in csv
    AOQuery = json.dumps({
        "query": {
            "jsonmodel_type":"boolean_query",
            "op":"AND",
            "subqueries":[
                {
                    "jsonmodel_type":"field_query",
                    "field":"primary_type",
                    "value":"archival_object",
                    "literal":True
                },
                {
                    "jsonmodel_type":"field_query",
                    "field":"ref_id",
                    "value": ref_ID, "literal":True
                },
                {
                    "jsonmodel_type":"field_query",
                    "field":"types",
                    "value":"pui",
                    "literal":True
                }
            ]
        }
    })

    # it can take some time for the posted DOs to be indexed, so...
    showed_up_yet = None
    while not showed_up_yet:
        aoSearch = list(client.get_paged('search', params={"filter": AOQuery}))
        if any(aoSearch):
            showed_up_yet = True
        else:
            print("DOs not present in search yet, waiting a second for the indexer to catch up")
            sleep(1)
    linked_ao_uri = aoSearch[0]['uri']
    # Get and store archival objects from above search
    aoRecord = client.get(linked_ao_uri).json()
    # Find existing instances and create new ones from new digital objects
    exising_instance = aoRecord['instances'][0]
    new_instance = {"instance_type": "digital_object", "digital_object": {"ref": uri}}

    # Merge old and new instances
    instances_new = []
    instances_new.append(exising_instance)
    instances_new.append(new_instance)
    aoRecord['instances'] = instances_new
    # Post updated archival objects
    aoPost = client.post(linked_ao_uri, json=aoRecord).json()
    print(aoPost)
    # Save select information to new csv file
    f.writerow([title, digital_object_id, uri, linked_ao_uri])

# Feedback to user
print ('New .csv saved to working directory.  Go have a look!')
