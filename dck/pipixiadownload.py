import random
import urllib.request, json
import requests


def video_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72 '
    }
    video_num = str(requests.get(url).url).split('/')[-1].split('?')[0]
    URL = 'https://h5.pipix.com/bds/webapi/item/detail/?item_id=' + video_num + '&source=share'
    r1 = requests.get(URL, headers=headers)
    video_name = r1.json()['data']['item']['content'] + ".mp4"
    if video_name == '':
        video_name = int(random.random() * 2 * 1000)
    video_url = r1.json()["data"]["item"]["origin_video_download"]["url_list"][0]["url"]
    return video_url, video_name


def aria2c_download(todownloadurl):
    downloadurl, filename = video_info(todownloadurl)
    jsonreq = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                          'method': 'aria2.addUri',
                          'params': ["token:darkness", [str(downloadurl)], {"out": filename}]}).encode("utf-8")
    c = urllib.request.urlopen('https://sjhlaria2c.herokuapp.com:443/jsonrpc', jsonreq)
    c.read()


if __name__ == '__main__':
    share_url = 'https://h5.pipix.com/s/JRggpTj/'
    aria2c_download(share_url)
    print('下载完成！')
