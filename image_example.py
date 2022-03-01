import requests

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/98.0.4758.102 Safari/537.36"
}
url = "https://m.avito.ru/icons/open-graph-default.svg"
response = requests.get(url, headers=headers)
print()

with open("image1.svg", "wb") as f:
    f.write(response.content)

# stream=True
# with requests.get()


def get_extension(headers):
    if "Content-Type" not in headers:
        raise ValueError(f"There are no Content-Type in headers: {headers}")
    return headers["Content-Type"].split("/")[-1].split("+")[0]


#
#
# url = "https://www.chopochom.com/front/wp-content/uploads/2017/01/zen.jpg"
# r = requests.get(url)
# print(r.headers["Content-Type"])
# # f"file.{get_extension(r.headers)}"
# print()
#
