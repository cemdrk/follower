from py2neo import Graph, Node, Relationship
from urllib.request import urlopen
import ssl
import json


URL = 'https://api.github.com/users/cemdrk'

g = Graph(host='127.0.0.1')

# context for https connection
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def get_json(url):
    global CTX
    html = urlopen(url, context=CTX).read()
    return json.loads(html.decode('utf-8'))


def add_node(name):
    global g
    n = Node('Person', name=name)
    g.create(n)
    return n


def add_follower(node):
    rel = Relationship(main_node, "followed by", node)
    g.create(rel)


json_data = get_json(URL)
print(json_data)

name = json_data['login']
main_node = add_node(name)

f_url = get_json(json_data['followers_url'])

for f in f_url:
    n = add_node(f['login'])
    add_follower(n)
