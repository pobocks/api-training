import json, time, runtime
from asnake.client import ASnakeClient
from asnake.client.web_client import ASnakeAuthError

# Create a client
client = ASnakeClient()
client.authorize()  # login, using default values

# print instructions
print ("This script will add the container_profiles included in a separate json file to ArchivesSpace.")
input("Press Enter to continue...")

# post container_profiles
print ("The following container profiles have been added to ArchivesSpace:")
jsonfile = open("containerProfiles.json")
jsonfile = json.load(jsonfile)
for container_profile in jsonfile:
    post = client.post("/container_profiles", json=container_profile).json()
    print (post)

print ("You've just completed your first API POST.  Congratulations!")
