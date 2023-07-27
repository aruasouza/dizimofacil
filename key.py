import json

with open('config/database_info.json','r') as f:
    cred = json.load(f)

with open('config/key','r') as f:
    key = f.read()

with open('config/mail','r') as f:
    email,passw = f.read().split()