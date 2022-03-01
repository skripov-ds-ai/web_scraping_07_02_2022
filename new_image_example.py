import wget

# pip install wget

url = "https://m.avito.ru/icons/open-graph-default.svg"
wget.download(url)


# https://static.onlinetrade.ru/img/items/s/materinskaya_plata_asus_prime_z390_p_lga1151_atx__950311_1.jpg
# https://static.onlinetrade.ru/img/items/m/materinskaya_plata_asus_prime_z390_p_lga1151_atx__950311_1.jpg
# https://static.onlinetrade.ru/img/items/b/materinskaya_plata_asus_prime_z390_p_lga1151_atx__950311_1.jpg
# import requests
# # pip install requests
#
# url = "https://upload.wikimedia.org/wikipedia" \
#       "/commons/thumb/1/17/Yin_yang.svg/240px-Yin_yang.svg.png"
# url = "https://aif-s3.aif.ru/images/021/767" \
#       "/ee422685554002f5e08116b0268fb23b.jpg"
# response = requests.get(url)
#
# print(response)
# with open("file.png", "wb") as f:
#     f.write(response.content)
#     print()
#
# wget.download(url)
