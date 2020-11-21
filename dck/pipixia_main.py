# -*- coding:utf-8 -*-
from flask import Flask, request
import random
import urllib.request, json
import requests

from sqlalchemy import Column, String, create_engine, Integer, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

Db_username = os.getenv("Db_username")
Db_password = os.getenv("Db_password")
Db_host = os.getenv("Db_host")
Db_port = os.getenv("Db_port")
Db_table = os.getenv("Db_table")
PORT = os.getenv("PORT")


# V1
# def video_info(url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                       'Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72 '
#     }
#     video_num = str(requests.get(url).url).split('/')[-1].split('?')[0]
#     URL = 'https://h5.pipix.com/bds/webapi/item/detail/?item_id=' + video_num + '&source=share'
#     r1 = requests.get(URL, headers=headers)
#     video_name = r1.json()['data']['item']['content']
#
#     if video_name == '':
#         video_name = int(random.random() * 2 * 1000)
#     video_name = str(video_name) + ".mp4"
#     video_url = r1.json()["data"]["item"]["origin_video_download"]["url_list"][0]["url"]
#     return video_url, video_name

# V2 版本  第三方api解析
def video_info(url):
    api_url = "https://v1.alapi.cn/api/video/url"
    payload = {
        "url": url
    }
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    response = requests.request("POST", api_url, data=payload, headers=headers)
    response = json.loads(response.text)
    video_data = response["data"]
    video_name = video_data["title"]
    if video_name == '':
        video_name = int(random.random() * 2 * 1000)
    video_name = str(video_name) + ".mp4"
    video_url = video_data["video_url"]
    return video_url, video_name


def aria2c_download(downloadurl, filename):
    jsonreq = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                          'method': 'aria2.addUri',
                          'params': ["token:darkness", [str(downloadurl)], {"out": filename}]}).encode("utf-8")
    c = urllib.request.urlopen('https://odaria2c.herokuapp.com:443/jsonrpc', jsonreq)
    c.read()


Base = declarative_base()


class Pipixia(Base):
    __tablename__ = 'pipixiadownloadurl'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    url = Column(String(200))
    name = Column(String(200), nullable=True)


db_settings = "mysql+pymysql://" + Db_username + ":" + Db_password + "@" + Db_host + ":" + Db_port + "/" + Db_table

engine = create_engine(db_settings)
DBSession = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def db_check_exist(shorturl, name):
    """
    1.检查url是否存在
        存在：直接pass
        不存在：
            检查name是否存在
                存在：name前面+1
                不存在：name不变
    """
    session = DBSession()
    try:
        dbppx = session.query(exists().where(Pipixia.url == shorturl)).scalar()
        if dbppx:
            print("exist")
            return False
        else:
            # 检查重名
            try:
                dbppx1 = session.query(exists().where(Pipixia.name == name)).scalar()
                if dbppx1:
                    name = "1" + name
            except Exception as e:
                print(e)
                return False
            ppx = Pipixia(url=shorturl, name=name)
            session = DBSession()
            session.add(ppx)
            session.commit()
            return name
    except Exception as e:
        print("wrong")
        print(e)
        return False
    finally:
        print("close db session")
        session.close()


app = Flask(__name__)


@app.route('/ppxd', methods=['POST'])
def ppxd():
    downloadurl = request.form['downloadurl']
    long_url, video_name = video_info(downloadurl)
    name = db_check_exist(shorturl=downloadurl, name=video_name)
    if name:
        aria2c_download(downloadurl=long_url, filename=name)
    return '200'


@app.route('/', methods=['GET'])
def index():
    return '200'


if __name__ == "__main__":
    app.run("0.0.0.0", PORT)
