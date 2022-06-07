import datetime
import requests
import urllib.request
import json
import os.path
from datetime import datetime
from tqdm import tqdm

def photoVk_to_Disk(TOKEN_VK, count_photo=5):
    version_api_vk = 5.131
    url = 'https://api.vk.com/method/'
    method = 'photos.get'
    profile_photo_vk = requests.get(
        f'{url}{method}?user_ids=begemot_korovin&'
        f'photo_sizes=1&extended=1&count={count_photo}&'
        f'album_id=profile&access_token={TOKEN_VK}'
        f'&v={version_api_vk}').json()['response']
    list_files = []
    print("Загрузка файлов из VK на локальный диск:   ")
    for item in tqdm(profile_photo_vk['items']):
        for key, value in item.items():
            if key == 'likes':
                likes = value['count']
            if key == 'sizes':
                height_ = 0
                for photo in value:
                    if photo['height'] > height_:
                        height_ = photo['height']
                        url_photo = photo['url']
                        size_ = photo['type']
        file = str(likes) + '.jpg'
        if os.path.exists(file):
            file = str(likes) + '_' + str(datetime.date(datetime.now())) + '.jpg'
        urllib.request.urlretrieve(url_photo, file)
        dict = {}
        dict['file_name'] = file
        dict['size'] = size_
        list_files.append(dict)
    return list_files

def photoDisk_to_YADisk(token, array):
    list_files_YA = []
    url = 'https://cloud-api.yandex.net:443'
    params = {'path': 'PHOTO_VK'}
    headers = {"Authorization": token}
    requests.put(url + '/v1/disk/resources', headers=headers, params=params)
    print("Загрузка файлов с диска на Яндекс диск и создание лога:   ")

    for item in tqdm(array):
        for key, val in item.items():
            if key == 'file_name':
                file_name = val
            if key == 'size':
                size_ = val

        params = {'path': 'PHOTO_VK/' + file_name, 'overwrite': 'true'}
        headers = {"Authorization": token}
        url_file = requests.get(url + '/v1/disk/resources/upload', headers=headers, params=params).json()['href']
        response = requests.put(url_file, data=open(file_name, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            dict = {}
            dict['file_name'] = file_name
            dict['size'] = size_
            list_files_YA.append(dict)
    with open('info.json', 'w') as f:
        json.dump(list_files_YA, f)
    return True

def drop_files(list_files):
    for item in list_files:
        if (os.path.isfile(item['file_name'])):
            os.remove(item['file_name'])
    print("Загрузка завершена!!!")

if __name__ == '__main__':
    TOKEN_VK = 'a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd'
    TOKEN_YA_DISK = ''

    list_files_download = photoVk_to_Disk(TOKEN_VK)
    photoDisk_to_YADisk(TOKEN_YA_DISK, list_files_download)
    drop_files(list_files_download)
