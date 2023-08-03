import json

with open('config/login_required','r') as f:
    login_required_urls = set(f.read().split())

with open('config/admin','r') as f:
    admin_urls = f.read().split()

with open('config/admigreja','r') as f:
    admigreja_urls = f.read().split()

with open('config/redirect_allow','r') as f:
    allow_red = set(f.read().split())

with open('datafiles/periodos.json','r',encoding = 'utf-8') as f:
    periodos = json.load(f)

private = {}
for url in admin_urls:
    if url in private:
        private[url].add('3')
    else:
        private[url] = set('3')
for url in admigreja_urls:
    if url in private:
        private[url].add('2')
    else:
        private[url] = set('2')

special_case = {'/novasenha','/static/style.css'}