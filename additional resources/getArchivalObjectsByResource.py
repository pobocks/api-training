import json
from asnake.client import ASnakeClient
import time

startTime = time.time()

def findKey(d, key):
    if key in d:
        yield d[key]
    for k in d:
        if isinstance(d[k], list):
            for i in d[k]:
                for j in findKey(i, key):
                    yield j

repository = input('Enter Repository ID: ')
resourceID= input('Enter resource ID: ')

client = ASnakeClient()
client.authorize()

endpoint = '/repositories/' + repository + '/resources/' + resourceID + '/tree'

output = client.get(endpoint).json()

archivalObjects = []
for value in findKey(output, 'record_uri'):
    if 'archival_objects' in value:
        archivalObjects.append(value)

records = []
for archivalObject in archivalObjects:
    output = client.get(archivalObject).json()
    records.append(output)

f=open('archivalObjects.json', 'w')
json.dump(records, f)
f.close()

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
