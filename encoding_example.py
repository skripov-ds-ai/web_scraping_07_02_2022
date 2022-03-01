# Python3.6
# from urllib import request
# Python3.8
from urllib import parse

import requests

search = "материнская плата asus"
# search = request.quote_plus(search.encode("cp1251"))
search = parse.quote_plus(search.encode("cp1251"))
# https://www.onlinetrade.ru/sitesearch.html?query=
# %EC%E0%F2%E5%F0%E8%ED%F1%EA%E0%FF+%EF%EB%E0%F2%E0+asus
# %EC%E0%F2%E5%F0%E8%ED%F1%EA%E0%FF+%EF%EB%E0%F2%E0+asus


print(search)
url = f"https://www.onlinetrade.ru/sitesearch.html?query={search}"
print(url)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}
response = requests.get(url, headers=headers)

print(response)
