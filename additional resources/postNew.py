import json
import time
from asnake.client import ASnakeClient

startTime = time.time()

client = ASnakeClient()
client.authorize()

records = json.load(open('all_AOs.json'))
for record in records:
    post = client.post('/repositories/3/archival_objects', json=record).json()
    print(post)

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
