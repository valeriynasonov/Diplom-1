import requests
import json
import os
from pprint import pprint
user_id = input("Введите id пользователя")
dict = {}
list = [ ]
url = " "
like = " "
count = 0
create_folder = requests.put(
    "https://cloud-api.yandex.net/v1/disk/resources",
    params={
        "path": "/PHOTOYOU",
        "overwrite": "true"
    },
    headers={"Authorization": "AgAAAAAG8IFWAADLW7bs7mIDUEy3hFfBZxI4uIU"})
resp_albums = requests.get(
    "https://api.vk.com/method/photos.getAlbums/",
    params={
        "owner_id":
        user_id,
        "access_token":
        "token",
        "v":
        "5.126"
    }).json()
if "error" in resp_albums:
    print("Ошибка:", resp_albums["error"]["error_msg"])
elif resp_albums["response"]["count"] == 0:
    print("У пользователя нет альбомов с фотографиями")
else:
    for element in resp_albums["response"]["items"]:
        resp_url = requests.get(
            "https://api.vk.com/method/photos.get/",
            params={
                "owner_id":
                user_id,
                "album_id":
                element["id"],
                "extended":
                "1",
                "count": "5",
                "access_token":
                "token",
                "v":
                "5.126"
            }).json()
        if "error" in resp_url:
            print("Ошибка:", resp_url["error"]["error_msg"])
            continue
        else:
            count += resp_url["response"]["count"]
            list_of_height = []
            list_of_width = []
            for element in resp_url["response"]["items"]:
                for position in element["sizes"]:
                    q = { }
                    list_of_height.append(position["height"])
                    list_of_width.append(position["width"])
                    max_height = max(list_of_height)
                    max_width = max(list_of_width)
                    if position["height"] == max_height and position["width"] == max_width:
                        q["size"] = position["type"]
                        url = position["url"]
                for k, v in element["likes"].items():
                    if k == "count":
                        like = str(v) + "like" + ".jpg"
                        q["file_name"] = like
                        list.append(q)
                        dict[url] = like
                        with open("PHOTO_USERS1", "w") as f:
                            json.dump(list, f, ensure_ascii = True, indent = 2)
                        create_file = requests.post(
                        "https://cloud-api.yandex.net/v1/disk/resources/upload",
                        params={"path": "/PHOTOYOU/" + like,
                        "url": k},
                        headers={"Authorization": "token"})
import alive
from alive_progress import alive_bar
import time
with alive_bar(count) as bar:
    for i in range(count):
        bar()
        time.sleep(1)
