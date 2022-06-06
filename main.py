import json
import requests
from pprint import pprint
import urllib.request
from PIL import Image

# Нужно написать программу для резервного копирования фотографий
# с профиля(аватарок) пользователя vk в облачное хранилище Яндекс.Диск.
#
# Для названий фотографий использовать количество лайков, если количество
# лайков одинаково, то добавить дату загрузки.

#Информацию по сохраненным фотографиям сохранить в json-файл.

# Нужно написать программу, которая будет:
#
# 1 Получать фотографии с профиля. Для этого нужно использовать метод photos.get.
# 2 Сохранять фотографии максимального размера(ширина/высота в пикселях) на Я.Диске.
# 3 Для имени фотографий использовать количество лайков.
# 4 Сохранять информацию по фотографиям в json-файл с результатами.

# Входные данные:
# Пользователь вводит:
#
# id пользователя vk;
# токен с Полигона Яндекс.Диска. Важно: Токен публиковать в github не нужно!
# Выходные данные:
# json-файл с информацией по файлу:
#     [{
#     "file_name": "34.jpg",
#     "size": "z"
#     }]
# Измененный Я.диск, куда добавились фотографии.
class YaUploader:

    def __init__(self, token):
        self.token = token

    def upload(self, likes, file_path):
        url = 'https://cloud-api.yandex.net:443'
        params = {'path': 'PHOTO_VK/'+likes+'.jpg', 'overwrite': 'true'}
        headers = {"Authorization": self.token}
        url_file = requests.get(url+'/v1/disk/resources/upload', headers=headers, params=params).json()['href']
        print(url_file)
        urllib.request.urlretrieve(
            file_path,
            likes+'.jpg')
        #img = Image.open("gfg.png")   open(file_path, 'rb')
        response = requests.put(url_file, files={'file':file_path})
        response.raise_for_status()
        if response.status_code == 201:
            return f'Файл загружен на яндекс диск'



def photoVk_to_yaDisk(TOKEN_VK, YANDEX):
    version_api_vk = 5.131
    url = 'https://api.vk.com/method/'
    method = 'photos.get'
    profile_photo_vk = requests.get(
        f'{url}{method}?user_ids=begemot_korovin&'
        f'photo_sizes=1&extended=1&'
        f'album_id=profile&access_token={TOKEN_VK}'
        f'&v={version_api_vk}').json()['response']

    for item in profile_photo_vk['items']:
        for key, value in item.items():
            if key == 'likes':
                likes = value['count']
            if key == 'sizes':
                height = 0
                for photo in value:
                    if photo['height'] > height:
                        height = photo['height']
                        url_photo = photo['url']
        #pprint(f'{likes}    {url_photo}')
        YANDEX.upload(str(likes), url_photo)

    return profile_photo_vk

if __name__ == '__main__':
    TOKEN_VK = 'a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd'
    TOKEN_YA_DISK = 'AQAAAAAvigESAADLW_SDgmkCJUIuq3-AUBI_m-Y'

    yandex = YaUploader(TOKEN_YA_DISK)
    pprint(photoVk_to_yaDisk(TOKEN_VK, yandex))