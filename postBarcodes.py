import json, csv, runtime
from asnake.client import ASnakeClient
# print instructions
print ('This script replaces existing fauxcodes with real barcodes (linked in a separate csv file) in ArchivesSpace.')
input('Press Enter to connect to ArchivesSpace and post those barcodes...')

# This is where we connect to ArchivesSpace.  See authenticate.py
client = ASnakeClient()
client.authorize()

# open csv and generate dict
reader = csv.DictReader(open('barcodes.csv'))

# GET each top_container listed in top_containers and add to records
print ('The following barcodes have been updated in ArchivesSpace:')
for row in reader:
	uri = row['uri']
	container = client.get(uri).json()
	container['barcode'] = row['real']
	post = client.post(uri, json=container).json()
	print(post)
