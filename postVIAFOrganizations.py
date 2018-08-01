import json, csv, runtime
from asnake.client import ASnakeClient

# print instructions
print('This script takes viafCorporateResults.csv and posts the organizations as corporate_entities to ArchivesSpace.')
input('Press Enter to continue...')

# This is where we connect to ArchivesSpace.
client = ASnakeClient()
client.authorize() # login, using default values

targetFile = 'viafCorporateResults.csv'

csv = csv.DictReader(open(targetFile))

orgList = []
for row in csv:
    orgRecord = {}
    # changed this since ASpace doesn't come with 'viaf' as an option for source out of the box.
    source =  'naf' if row.get('lc') is not None else 'local'
    orgRecord['names'] = [{'primary_name': row['result'], 'sort_name': row['result'], 'source': source, 'authority_id': row['lc']}]

    post = client.post('/agents/corporate_entities', json=orgRecord).json()
    print(post, '\n')

print("Check out your instance of ArchivesSpace to see what's new.")
