import urllib.request
import json
import requests

data = {
    'a': 123,
    'b': 456
}
headers = {'Content-Type': 'application/json'}
r = requests.post("http://localhost:5000/receive_data_from_uav", json=json.dumps(data))
print(r.status_code)