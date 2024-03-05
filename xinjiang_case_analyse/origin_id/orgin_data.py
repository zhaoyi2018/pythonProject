import json

import pandas
import requests
import re


def get_content(url, decode="utf-8"):
    """
    爬虫获取数据
    :param url:
    :param decode:
    :return:
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.content.decode(decode)
    else:
        print("获取数据失败!")


def deal_province_content(origin_content):
    """
    处理省匹配数据
    :param origin_content:
    :return:
    """
    pattern = re.compile('<td><a href="([0-9]*)\\.html">([\u4e00-\u9fa5]+?)<br /></a></td>')
    return re.findall(pattern, origin_content)


def deal_city_content(origin_content):
    """
    处理省匹配数据
    :param origin_content:
    :return:
    """
    pattern = re.compile('<td><a href="([0-9/]+?)\\.html">(\d+?)</a></td><td><a href="[0-9/]*\\.html">(['
                         '\u4e00-\u9fa5]+?)</a></td>')
    return re.findall(pattern, origin_content)


def address_to_all_data(address, decode='utf-8'):
    """
    中文地址获取详细数据
    :param decode:
    :param address:
    :return:
    """
    response = requests.get("https://restapi.amap.com/v3/geocode/geo?key=a9c5aaf4f21bc691dbfe131e6cff0473&address={}".format(address))
    if response.status_code == 200:
        return json.loads(response.content.decode(decode))
    else:
        print("获取数据失败!")


def parse_address_json_to_lng_lat(json_data):
    """
    解析数据得到经纬度
    :param json_data:
    :return:
    """
    if 'geocodes' in json_data:
        geocode = json_data['geocodes'][0]
        if "location" in geocode:
            return geocode["location"].split(",")
    return ["", ""]


res = []
# 获取省级
# url: http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2022/index.html
province_name = '新疆维吾尔自治区'
province_content = get_content(url="http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2022/index.html")
province_matches = deal_province_content(province_content)
for match in province_matches:
    if match[1] == province_name:
        province_id = match[0]

# 获取市级
# url: http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2022/{}.html
city_content = get_content(url="http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2022/{}.html".format(province_id))
city_matches = deal_city_content(city_content)
for match in city_matches:
    # 市级添加
    tmp = [1, match[1][:6], match[2]]
    tmp.extend(parse_address_json_to_lng_lat(address_to_all_data(match[2])))
    res.append(tmp)

    # 县级添加
    county_content = get_content(url="http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2022/{}.html".format(match[0]))
    county_matches = deal_city_content(county_content)
    for under_match in county_matches:
        tmp = [2, under_match[1][:6], under_match[2]]
        tmp.extend(parse_address_json_to_lng_lat(address_to_all_data(match[2] + under_match[2])))
        res.append(tmp)
df = pandas.DataFrame(res, columns=["area_type", "area_code", "area_name", "lng", "lat"])
df.to_csv("./xinjiang.csv")
