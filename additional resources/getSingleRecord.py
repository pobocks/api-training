import json
from asnake.client import ASnakeClient

client = ASnakeClient()
client.authorize()

endpoint = '/repositories/3/resources/569'

with open('ASRecord.json', 'w') as f:
    output = client.get(endpoint).json()
    json.dump(output, f)
