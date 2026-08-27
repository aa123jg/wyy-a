import json
import re

import requests

try:
    from base.spider import Spider as BaseSpider
except ImportError:
    class BaseSpider:
        pass


class Spider(BaseSpider):
    HOST = "https://gqc4.top"
    API = HOST + "/api.php/provide/vod"

    # Main categories for home screen
    CATS = {
        "6": "动作片",
        "7": "喜剧片",
        "8": "爱情片",
        "9": "科幻片",
        "10": "惊恐片",
        "11": "剧情片",
        "12": "战争片",
        "13": "大陆剧",
        "14": "TVB",
        "15": "韩剧",
        "16": "美剧",
        "20": "日剧",
        "21": "海外剧",
        "22": "台剧",
        "24": "音乐",
        "25": "伦理片",
        "26": "纪录片",
        "80": "短剧",
    }

    # Filter options for each category
    FILTERS = {
        "1": {"area": ["全部", "内地", "中国香港", "中国台湾", "美国", "韩国", "日本", "法国", "英国", "其他"], "year": ["全部", "2026", "2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018"]},
        "2": {"area": ["全部", "内地", "中国香港", "中国台湾", "美国", "韩国", "日本", "英国", "其他"], "year": ["全部", "2026", "2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018"]},
    }

    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
            "Referer": self.HOST + "/",
        })

    def getName(self):
        return "共青春影院"

    def init(self, extend=""):
        pass

    def isVideoFormat(self, url):
        return bool(url and any(x in url.lower() for x in (".m3u8", ".mp4", ".flv", ".mkv", ".mpd")))

    def manualVideoCheck(self):
        pass

    def destroy(self):
        self.s.close()

    def _api(self, **kw):
        try:
            r = self.s.get(self.API, params=kw, timeout=15)
            r.raise_for_status()
            return r.json()
        except Exception:
            return {}

    def _html(self, path):
        url = self.HOST + path if path.startswith("/") else path
        try:
            r = self.s.get(url, timeout=15)
            r.raise_for_status()
            return r.text
        except Exception:
            return ""

    @staticmethod
    def _fix_pic(pic):
        if not pic:
            return ""
        pic = pic.replace("&amp;", "&")
        if pic.startswith("//"):
            return "https:" + pic
        if not pic.startswith("http"):
            pic = "https://gqc4.top" + pic
        return pic

    def homeContent(self, filter):
        data = self._api(ac="list")
        classes = [{"type_id": str(c["type_id"]), "type_name": c["type_name"]}
                   for c in data.get("class", []) if str(c.get("type_id")) in self.CATS]
        if not classes:
            classes = [{"type_id": k, "type_name": v} for k, v in self.CATS.items()]
        filters = {}
        for tid in self.CATS:
            filters[tid] = [
                {"key": "area", "name": "地区", "value": [{"n": a, "v": a} for a in ["全部", "内地", "中国香港", "中国台湾", "美国", "韩国", "日本", "法国", "英国", "其他"]]},
                {"key": "year", "name": "年份", "value": [{"n": y, "v": y} for y in ["全部", "2026", "2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017"]]},
                {"key": "by", "name": "排序", "value": [{"n": b, "v": b} for b in ["时间", "人气", "评分"]]},
            ]
        hot = self._api(ac="videolist", pg=1)
        items = []
        for v in hot.get("list", [])[:20]:
            items.append({
                "vod_id": str(v.get("vod_id", "")),
                "vod_name": v.get("vod_name", ""),
                "vod_pic": self._fix_pic(v.get("vod_pic", "")),
                "vod_remarks": v.get("vod_remarks", ""),
            })
        return {"class": classes, "list": items, "filters": filters}

    def homeVideoContent(self):
        data = self._api(ac="videolist", pg=1)
        return {"list": [{
            "vod_id": str(v.get("vod_id", "")),
            "vod_name": v.get("vod_name", ""),
            "vod_pic": self._fix_pic(v.get("vod_pic", "")),
            "vod_remarks": v.get("vod_remarks", ""),
        } for v in data.get("list", [])[:20]]}

    def categoryContent(self, tid, pg, filter, extend):
        page = int(pg or 1)
        params = {"ac": "videolist", "t": tid, "pg": page}
        if extend:
            area = extend.get("area") if isinstance(extend, dict) else None
            year = extend.get("year") if isinstance(extend, dict) else None
            by = extend.get("by") if isinstance(extend, dict) else None
            if area and area != "全部":
                params["area"] = area
            if year and year != "全部":
                params["year"] = year
            if by:
                by_map = {"时间": "time", "人气": "hits", "评分": "score"}
                params["by"] = by_map.get(by, "time")
        data = self._api(**params)
        items = []
        for v in data.get("list", []):
            items.append({
                "vod_id": str(v.get("vod_id", "")),
                "vod_name": v.get("vod_name", ""),
                "vod_pic": self._fix_pic(v.get("vod_pic", "")),
                "vod_remarks": v.get("vod_remarks", ""),
            })
        pc = int(data.get("pagecount", 1) or 1)
        limit = len(items) if items else 20
        return {"page": page, "pagecount": pc, "limit": limit, "total": pc * limit, "list": items}

    def detailContent(self, ids):
        vod_id = str(ids[0])
        # 1. Get basic info from API
        data = self._api(ac="videolist", ids=vod_id)
        v = data.get("list", [{}])[0] if data.get("list") else {}

        # 2. Get all play sources from HTML
        html = self._html("/neirong/" + vod_id + ".html")

        # Parse play sources from HTML bofang links
        # Format: /bofang/{vod_id}-{sid}-{nid}.html
        bofang = re.findall(r'href="/bofang/(\d+)-(\d+)-(\d+)\.html"[^>]*>(.*?)</a>', html, re.DOTALL)

        # Group episodes by source ID
        from collections import OrderedDict
        sources = OrderedDict()
        ep_names_by_sid = {}
        for vid, sid, nid, name in bofang:
            name_clean = re.sub(r'<[^>]+>', '', name).strip()
            if not name_clean or name_clean == "立即播放":
                continue
            # First link for each source is the source name + episode count
            # e.g. "YZ线\t\t\t\t\t\t\t46"
            if sid not in sources:
                sources[sid] = []
                # Extract source name from first entry
                parts = name_clean.split('\t')
                src_name = parts[0].strip() if parts else name_clean
                ep_names_by_sid[sid] = src_name
            # Only add if it looks like an episode (not a source name with tabs)
            if '\t' not in name_clean and name_clean:
                sources[sid].append((nid, name_clean))

        # If no episodes found from HTML, fall back to API
        if not sources:
            api_pf = v.get("vod_play_from", "")
            api_pu = v.get("vod_play_url", "")
            if api_pf and api_pu:
                return {"list": [{
                    "vod_id": vod_id,
                    "vod_name": v.get("vod_name", ""),
                    "vod_pic": self._fix_pic(v.get("vod_pic", "")),
                    "vod_year": v.get("vod_year", ""),
                    "vod_area": v.get("vod_area", ""),
                    "vod_actor": v.get("vod_actor", ""),
                    "vod_director": v.get("vod_director", ""),
                    "vod_content": v.get("vod_content", ""),
                    "vod_play_from": api_pf,
                    "vod_play_url": api_pu,
                }]}

        # Build play_from and play_url
        # Fetch m3u8 URLs for each source's first episode to get the URL pattern
        # We store: ep_name$bofang_id (sid-nid) for playerContent to resolve
        play_from_parts = []
        play_url_parts = []
        for sid, eps in sources.items():
            src_name = ep_names_by_sid.get(sid, "线路" + sid)
            play_from_parts.append(src_name)
            ep_strs = []
            for nid, ep_name in eps:
                ep_strs.append(ep_name + "$" + vod_id + "-" + sid + "-" + nid)
            play_url_parts.append("#".join(ep_strs))

        play_from = "$$$".join(play_from_parts)
        play_url = "$$$".join(play_url_parts)

        return {"list": [{
            "vod_id": vod_id,
            "vod_name": v.get("vod_name", ""),
            "vod_pic": self._fix_pic(v.get("vod_pic", "")),
            "vod_year": v.get("vod_year", ""),
            "vod_area": v.get("vod_area", ""),
            "vod_actor": v.get("vod_actor", ""),
            "vod_director": v.get("vod_director", ""),
            "vod_content": v.get("vod_content", ""),
            "vod_play_from": play_from,
            "vod_play_url": play_url,
        }]}

    def searchContent(self, key, quick, pg="1"):
        page = int(pg or 1)
        data = self._api(ac="videolist", wd=key, pg=page)
        items = []
        for v in data.get("list", []):
            items.append({
                "vod_id": str(v.get("vod_id", "")),
                "vod_name": v.get("vod_name", ""),
                "vod_pic": self._fix_pic(v.get("vod_pic", "")),
                "vod_remarks": v.get("vod_remarks", ""),
            })
        pc = int(data.get("pagecount", 1) or 1)
        return {"page": page, "pagecount": pc, "list": items}

    def playerContent(self, flag, id, vipFlags):
        # id format: vod_id-sid-nid (e.g. "84626-3-1")
        parts = id.split("-")
        if len(parts) < 3:
            return {"parse": 1, "url": "", "header": ""}
        vod_id, sid, nid = parts[0], parts[1], parts[2]
        url = ""
        try:
            html = self._html("/bofang/" + vod_id + "-" + sid + "-" + nid + ".html")
            m = re.search(r'"dmId"\s*:\s*"([^"]+)"', html)
            if m:
                url = m.group(1)
            if not url:
                urls = re.findall(r'(https?://[^\s"<>]+\.(?:m3u8|mp4)[^\s"<>]*)', html)
                if urls:
                    url = urls[0]
        except Exception:
            pass
        direct = self.isVideoFormat(url)
        headers = {"User-Agent": self.s.headers["User-Agent"], "Referer": self.HOST + "/"}
        if not direct and url:
            # Non-m3u8 URLs (e.g. v.qq.com, iqiyi.com) need parse=1
            return {"parse": 1, "url": url, "header": json.dumps(headers, ensure_ascii=False)}
        if not url:
            return {"parse": 1, "url": "", "header": ""}
        return {"parse": 0, "url": url, "header": json.dumps(headers, ensure_ascii=False)}
