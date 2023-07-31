import json

with open('protected/database_info.json','r') as f:
    cred = json.load(f)

with open('protected/key','r') as f:
    key = f.read()

with open('protected/mail','r') as f:
    email,passw = f.read().split()