import requests
import random
import json


def video_info(url):
    api_url = "https://v1.alapi.cn/api/video/url"

    payload = {
        "url": url
    }
    headers = {'Content-Type': "application/x-www-form-urlencoded"}

    response = requests.request("POST", api_url, data=payload, headers=headers)

    # print(response.text)
    response = json.loads(response.text)
    video_data = response["data"]
    print(video_data)

    video_name = video_data["title"]
    if video_name == '':
        video_name = int(random.random() * 2 * 1000)
    video_name = str(video_name) + ".mp4"
    video_url = video_data["video_url"]
    print(video_name)
    print(video_url)
    return video_url, video_name


video_info("https://h5.pipix.com/s/JPhTBNL/")
