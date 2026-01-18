# coding = utf-8
#!/usr/bin/python
import base64
import os
import sys
from os.path import isfile

import urllib3
from urllib3.exceptions import InsecureRequestWarning

sys.path.append('..')
from base.spider import Spider


import requests
import pprint
import json
import time
import sys
import re

sys.path.append('..')

xurl = "https://cloud.189.cn/web"
Cookie='你自己的C0DEF9E474AAB5EDBC0B37EE6BE8E75F30CA79559020B3ECA421E438A1511975995'
headerx = {
    'accept':'application/json;charset=UTF-8',
    #'accept-encoding': 'gzip, deflate, br',
    #'accept-language': 'zh-CN, zh;q=0.9',
    #'browser-id':'cee80d83f0df62bd8e0587d18cf21c21',
    'cookie': Cookie,
    'referer': 'https://h5.cloud.189.cn/index.html?accessToken=FF4443E32EDF0F637786593BE709B11B',
    #'sec-ch-ua': '"Not-A.Brand";v="24", "Chromium";v="14"',
    #'sec-ch-ua-mobile':'?0',
    #'sec-ch-ua-platform': '"Windows"',
    #'sec-fetch-dest': 'empty',
    #'sec-fetch-mode': 'cors',
    #'sec-fetch-site': 'same-origin',
    #'sign-type': '1',
    'user-agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Mobile Safari/537.36"
    #"user-agent": "okhttp/4.1.0"
    }
headers = {"user-agent": "okhttp/4.1.0"}
class Spider(Spider):

    def __init__(self):
        self.header2 = None

    def init(self, extend):


        pass

    def getName(self):
        return "首页"



    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass
    def fetchJY(self, url, headers=None, retry=2):
        """统一的网络请求接口"""

        urllib3.disable_warnings(InsecureRequestWarning)
        if headers is None:
            headers = headerx
        
        for i in range(retry + 1):
                try:
                    response = requests.get(url, headers=headers,verify=False)

                    return response
                except Exception as e:
                    if i == retry:
                        print(f"请求异常: {url}, 错误: {str(e)}")
                        return None
                    continue

    def homeContent(self, filter):
        # 修改搜索分类的生成方式为 ['名称', 's_分类'] 形式


        result = {"class": [

            {"type_id": "-11", "type_name": "189"},

            {"type_id": "0", "type_name": "同步盘"},
            {"type_id": "124581220331200290", "type_name": "APK"}


        ]
        }

        return result
    def isfile(self, cid):
        return self.categoryContent(cid,1,1)

    downloadUrl = 'null'
    largeUrl = 'http://preview.cloud.189.cn/image/imageAction?param=2B9080F813DD3C8BAC095D2DC7817A24043C43EC9FE1B2AA63978F93398D50A67FDA02D92DC517D101BB64D8C48F50E3A9B85F867CE50A55C486146CFF4DC020305B1784A12EF0D388189F94266F37EE8ED97A401F26BC15F6F930E852A04A9FD1B2ED566BF0063EEC9EDCBF'
    def categoryContent(self, cid, pg, filter, ext):


        url = f'https://cloud.189.cn/api/portal/listFiles.action?noCache=0.4243807427091393&fileId={cid}'
        response = self.fetchJY(url=url, headers=headerx)
        sss=response.json()
        pg=1
        videos = []

        #print(sss)

        try:

            for item in sss["data"]:
                fileType=item["fileType"]
                print(fileType != '')
                fileId = item["fileId"]
                if fileType != '':
                   self.downloadUrl="http:"+item["downloadUrl"]
                   print(self.downloadUrl)
                   self.largeUrl="http:"+item['icon']["largeUrl"]

                video = {
                "vod_id": f'{fileId}#{fileType}#{self.downloadUrl}',
                "vod_name": item["fileName"],
                "vod_pic": self.largeUrl,
                "vod_remarks": "播放量：999",
                 }
                videos.append(video)
            return {
              "list": videos,
              "page": pg,
              "pagecount": 9999,
              "limit": 90,
              "total": 999999,
               }
        except Exception as e:
            video = {
                "vod_id": "323741220374240408",
                "vod_name": '出错了',
                "vod_pic": "http://preview.cloud.189.cn/image/imageAction?param=2B9080F813DD3C8BAC095D2DC7817A24043C43EC9FE1B2AA63978F93398D50A67FDA02D92DC517D101BB64D8C48F50E3A9B85F867CE50A55C486146CFF4DC020305B1784A12EF0D388189F94266F37EE8ED97A401F26BC15F6F930E852A04A9FD1B2ED566BF0063EEC9EDCBF",
                "vod_remarks": "播放量：999",
            }
            videos.append(video)
            return {
              "list": videos,
              "page": pg,
              "pagecount": 9999,
              "limit": 90,
              "total": 999999,
               }

    def format_views(self, num):
        return f"{num / 10000:.1f}万" if num >= 10000 else str(num)

    headers2={'accept': 'application/json;charset=UTF-8',

         'accesstoken': 'FF4443E32EDF0F637786593BE709B11B',
         'origin':'https://h5.cloud.189.cn',
         'referer': 'https://h5.cloud.189.cn/main.html',

         'sec-ch-ua-platform': "Android",
         'sec-fetch-dest': 'empty',
         'sec-fetch-mode': 'cors',
         'sec-fetch-site': 'same-site',
         'sign-type': '1',
         'signature':'4556139985bd5461267d89bd5c3cff9c',
         'cookie': Cookie,
         'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Mobile Safari/537.36',
         'x-request-id': 'ada3c297eab340508',
               }
    def detailContent(self, ids):
        #playerContent(),Z这个是TVBOX点击播放自动调用的方法


        result = {}
        videos = []
        id = ids[0]
        id2=id.split('#')[0]
        id3 = id.split('#')[1]
        id4 = id.split('#')[2]
        print(id3 =='')
        if id3 !='':
            video = {
                "vod_id": id2,
                "vod_name": "title1",
                "vod_actor": "",
                "vod_director":" name1",
                "vod_content": "fans1",
                "vod_remarks": "fans1",
                "vod_year": "",
                "vod_area": "",
                "vod_play_from": "B站",
                "vod_play_url": id4+"_"+id4,
            }
            videos.append(video)
            result["list"] = videos
            return result







        url2 = f'https://cloud.189.cn/api/open/file/listFiles.action?&folderId={id2}'
        response2 = self.fetchJY(url2, headers=headerx)
        res=response2.json()


        # 提取视频URL
        print(res)
        playUrl = ''
        vod = {
            "vod_id": id2,
            "vod_name": id,
            "vod_pic": "data['result']['cover']",
            "type_name": "data['result']['share_sub_title']",
            "vod_actor": "data['result']['actors'].replace('\n', '，')",
            "vod_content": "self.removeHtmlTags(data['result']['evaluate'])"
        }
        try:
            for item in res["fileListAO"]["fileList"]:
                did=item["id"]
                title1=item["name"]
               # did = res["fileListAO"]["fileList"][0]["id"]
                #title1 = res["fileListAO"]["fileList"][0]["name"]
                print("jy==",did)
                #playUrl = playUrl + '[{}]/{}${}_{}#'.format(remark, name, eid, cid)
                playUrl = playUrl + '[{}]/{}${}_{}#'.format(did, title1, did, did)
            vod['vod_name'] = title1
            vod['vod_play_from'] = '189'
            vod['vod_play_url'] = playUrl.strip('#')
            result = {
                'list': [
                    vod
                ]
            }
            return result




        except Exception as e:




            video = {
               "vod_id":  id,
               "vod_name": "title1",
               "vod_actor": "",
               "vod_director": "title1",
               "vod_content": "title1",
               "vod_remarks": "错误了",
               "vod_year": "",
               "vod_area": "",
               "vod_play_from": "189",
               "vod_play_url": "https://download.cloud.189.cn/file/downloadFile.action?dt=51&expired=1766728823671&play=1&sk=ddfeb673-1de5-43af-8e16-f39d59d3704c&ufi=225201224636943009&zyc=180&token=cloud4&sig=Lp%2BgigluAzkG2ZF8pJyI8xDfd8s%3D"}

            videos.append(video)
            result["list"] = videos
            return videos




    def playerContent(self, flag, id, vipFlags):
        pidList = id.split("_")
        aid = pidList[0]
        cid = pidList[1]
        if aid.startswith('http://'):return  {"parse": 0, "url": aid, "header": headerx}

        url3 = f'https://cloud.189.cn/api/portal/getNewVlcVideoPlayUrl.action?noCache=0.7193496316698806&fileId={aid}&type=2'
        response3 = self.fetchJY(url3, headers=self.headers2)
        sd = response3.json()
        print("sd===", sd)
        try:
            ids = sd["normal"]['url']
            return {"parse": 0, "url": ids, "header": headerx}


        except Exception as e:
            return {"parse": 0,"url": id, "header": headerx}



    def searchContentPage(self, key, quick, page):
        # 使用B站官方搜索API
        api_url = "https://api.bilibili.com/x/web-interface/search/type"
        params = {
            "keyword": key,
            "page": page,
            "search_type": "video",
            "pagesize": 20
        }

        try:
            response = self.fetch(api_url, params=params, headers=headerx, verify=False)
            data = response.json()
            
            if data.get("code") != 0:
                return {"list": [], "page": page, "pagecount": 1, "total": 0}
                
            result = data.get("data", {})
            videos = []
            
            for item in result.get("result", []):
                # 清理标题中的HTML标签
                title = item.get("title", "")
                title = re.sub(r'<[^>]+>', '', title)
                
                # 构建视频信息
                video = {
                    "vod_id": item.get("bvid", ""),
                    "vod_name": title,
                    "vod_pic": self.fix_url(item.get("pic", "")),
                    "vod_remarks": self.format_search_remarks(item)
                }
                videos.append(video)
            
            # 计算分页信息
            total = result.get("numResults", 0)
            pagecount = (total + 19) // 20  # 每页20条，计算总页数
            
            return {
                "list": videos,
                "page": int(page),
                "pagecount": pagecount,
                "limit": 20,
                "total": total
            }
            
        except Exception as e:

            return {"list": [], "page": page, "pagecount": 1, "total": 0}

    def format_search_remarks(self, item):
        """格式化搜索结果的备注信息"""
        parts = []
        
        # 时长
        duration = item.get("duration")
        if duration:
            parts.append(f"时长: {duration}")
        
        # 播放量
        play = item.get("play", 0)
        parts.append(f"播放: {self.format_views(play)}")
        
        # UP主
        author = item.get("author")
        if author:
            parts.append(f"UP: {author}")
        
        # 发布时间
        pubdate = item.get("pubdate")
        if pubdate:
            year = time.strftime("%Y", time.localtime(pubdate))
            parts.append(f"{year}年")
        
        return " · ".join(parts)

    def fix_url(self, url):
        """修复URL格式"""
        if url.startswith("//"):
            return "https:" + url
        return url

    def searchContent(self, key, quick, pg="1"):
        return self.searchContentPage(key, quick, pg)

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None




#s=Spider()
#s.homeContent(1)
#print(s.categoryContent("-11","2","",""))
#dd='823403226712919834#mp4#http://m.cloud.189.cn/downloadFile.action?fileStr=4D4D1DAA10DB56E657F42263C18D0186FA966FA8E4228BB120FC00C2E216EFB2F6BD3AA4AE808998907BB6E7C1E1EC10E0F6014CE522E1EF4739616A&downloadType=1'
#print(s.detailContent([dd,1]))
#print(s.playerContent(1,"http://225201224636943009_1",0))

#print(s.detailContent(["BV1LZ2LBQEuZ","1"]))
#sd=s.fetchJY(url="https://jihulab.com/ymz1231/xymz/-/raw/main/ymshaoer",headers=headers).text.encode('utf-8')
#sd=s.fetchJY(url="http://ok321.top/ok",headers=headers).text.encode('utf-8')
#ur='http://ok.zoho.to//z/=HK'

#sd=s.fetchJY(url=ur,headers=headers).text.encode('utf-8')
#sss=sd.__str__()
#print(sd.decode('ASCII'))
#print(sd)
#print(sd.decode('utf-8'))
#dd=sss.split("**")[1]
#print(base64.b64decode(sd).decode('utf-8'))
#print(base64.b64decode(dd).decode('utf-8'))


#print(  s.detailContent(["BV1yc411w71d","1"]))


#print(s.playerContent("1",[url,"1"],"1"))


#response = requests.get(url, headers=headers,verify=False)
#print(s.homeContent(0))
#print(s.categoryContent('0',1,1,1))

#url='https://cloud.189.cn/api/portal/listFiles.action?noCache=0.4243807427091393&fileId=-11'
#response = s.fetchJY(url, headers=headerx)
#print(response.json())
#url2='https://cloud.189.cn/api/open/file/listFiles.action?noCache=0.943665168470273&pageSize=60&pageNum=1&mediaType=0&folderId=323741220374240408&iconOption=5&orderBy=lastOpTime&descending=true'
#response2 = s.fetchJY(url2, headers=headerx)
