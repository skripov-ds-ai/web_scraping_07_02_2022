from pprint import pprint

import requests

url_1 = "http://www.google.com/"
response_1 = requests.get(url_1)
print(response_1)
pprint(dict(response_1.headers))
print()

url_2 = "https://www.google.com/"
response_2 = requests.get(url_2)
print(response_2)
pprint(dict(response_2.headers))
print()

headers_3 = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
}
url_3 = "https://www.google.com/"
response_3 = requests.get(url_3, headers=headers_3)
print(response_3)
pprint(dict(response_3.headers))
print(f"Status = {response_3.status_code}")
print()
