import hmac
import hashlib
import base64
import requests

import time
import pytz
import datetime



"""
字符    -    URL编码值

空格    -    %20 （URL中的空格可以用+号或者编码值表示）
"          -    %22
#         -    %23
%        -    %25
&         -    %26
(          -    %28
)          -    %29
+         -    %2B
,          -    %2C
/          -    %2F
:          -    %3A
;          -    %3B
<         -    %3C
=         -    %3D
>         -    %3E
?         -    %3F
@       -    %40
\          -    %5C
|          -    %7C 
{          -    %7B
}          -    %7D
"""
def utc_to_now():
    time_zone = pytz.timezone('America/Los_Angeles')
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    Timestamp = timestamp.replace(':', '%3A')
    print(Timestamp)
    return Timestamp

def get_signature(Timestamp):
    SECRET_ACCESS_KEY = 'i3OS+YcCmMw8WfyJTW7f3A2Bvv1u8kI+wqahzPS0'
    Message = "GET\nwebservices.amazon.com\n/onca/xml\nAWSAccessKeyId=AKIAJGDUFSRVEGDP7FCA" \
              "&AssociateTag=zhanghong-20&Condition=All&IdType=ASIN&ItemId=B07355585W" \
              "&Operation=ItemLookup&ResponseGroup=Accessories%2CAlternateVersions" \
              "%2CBrowseNodes%2CEditorialReview%2CImages%2CItemAttributes%2CItemIds" \
              "%2CLarge%2CMedium%2COfferFull%2COfferListings%2COffers%2COfferSummary" \
              "%2CPromotionSummary%2CReviews%2CSalesRank%2CSimilarities" \
              "%2CSmall%2CTracks%2CVariations%2CVariationImages%2CVariationMatrix" \
              "%2CVariationOffers%2CVariationSummary&Service=AWSECommerceService" \
              "&Timestamp=" + Timestamp
    message = Message.encode('utf-8')
    secret = SECRET_ACCESS_KEY.encode('utf-8')

    bytes_k = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
    str_k = str(bytes_k, encoding='utf-8')
    signature = str_k.replace('+', '%2B').replace('=', '%3D').replace('/', '%2F')
    return signature





url = "https://webservices.amazon.com/onca/xml?AWSAccessKeyId=AKIAJGDUFSRVEGDP7FCA" \
      "&AssociateTag=zhanghong-20&Condition=All&IdType=ASIN&ItemId=B07355585W" \
      "&Operation=ItemLookup&ResponseGroup=Accessories%2CAlternateVersions" \
      "%2CBrowseNodes%2CEditorialReview%2CImages%2CItemAttributes%2CItemIds" \
      "%2CLarge%2CMedium%2COfferFull%2COfferListings%2COffers%2COfferSummary" \
      "%2CPromotionSummary%2CReviews%2CSalesRank%2CSimilarities" \
      "%2CSmall%2CTracks%2CVariations%2CVariationImages%2CVariationMatrix" \
      "%2CVariationOffers%2CVariationSummary&Service=AWSECommerceService" \
      "&Timestamp=" + Timestamp + "&Signature=" + signature

print(url)
print(signature)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
proxies = {
  "http": "http://16WRMGEL:070128@n10.t.16yun.cn:6442",
  "https": "http://16WRMGEL:070128@n10.t.16yun.cn:6442",
}
cookies = {
        'session-id': '143-4200094-0072708',
        'ubid-main': '130-8789618-2722706',
        'x-wl-uid': '186thS2piGJyfNLTEbyCDyF2GWwe/zlfSugvlGvU1bDab19SLZR2oJcI4xpHbqAobcB39rKH2B4M=',
        's_fid': '2F0E940E9DA7C6B0-14C268263D6B7009',
        'regStatus': 'pre-register',
        's_cc': 'true',
        's_dslv_s': 'Less%20than%201%20day',
        's_vn': '1573176764977%26vn%3D2',
        's_invisit': 'true',
        'session-id-time': '2082758400',
        'session-token': "/rqfMqAA/YYH373lNuSyY5Yi28AEozqTC2bWPmTWln35JWXkSTxacisQ7m5DwaOP8fE/jq4Kj9w3BDihbyodsxi58ZxWxgSwo9PAD4VzRpya/HAw4pRw0Pd0mv+8vdoQq57AeO7aE4V2NSCYYCuywB9kVsPbO2CehGbBrQFIJDo3TrW2mKHti/LdB2Gu9cOXlOcAOfd46GLhGUCDr5R+Hw==",
        # 's_depth': '4',
        's_dslv': '1541655599801',
        's_nr': '1541655599804-Repeat',

    }
params = dict(
        headers=headers,
        # proxies=proxies,
        # cookies=cookies,
        verify=None,
        timeout=180,
    )

response = requests.get(url, params=params)
print(response.text)

import xml.etree.cElementTree as ET
from lxml import etree
e1 = etree.XML(xml_content) #或者 etree.fromstring(xml_content)

# 1.使用lxml库读写XML格式数据,测试速度比xml.dom.minidom解析的要快;
#   1.1 将string转换成python对象
#       e1 = etree.XML(xml_content) 或者 etree.fromstring(xml_content)
#   1.2 读取xml字符串中的指定节点文本与属性
#       a1 = e1.xpath("//SPEC_LIST/text()")  # 节点文本
#       a1 = e1.xpath("//SPEC_LIST/@clone")  # 节点属性
#   1.3 添加子节点
#       obj = e1.xpath("//SPEC_LIST")[0]  # 获取节点
#       spec = etree.SubElement(obj, "SPEC")  # 添加子节点
#   1.4 修改节点属性
#       obj = e1.xpath("//SPEC_LIST")[0]  # 获取节点
#       obj.attrib['cpu'] = "8"  # 设置节点属性,attrib属性是一个字典;
#   1.5 将python对象转换成string
#       content = etree.tounicode(e1)  # unicode
#       content = etree.tostring(e1)  # bytes

import xml.dom.minidom
from xml.dom.minidom import parse, parseString
# 获取xml节点数据
doc = parseString(response.text)   # 将xml数据转为doc对象

asin = doc.getElementsByTagName("ASIN")[0].childNodes[0].data
ParentASIN = doc.getElementsByTagName("ParentASIN")[0].childNodes[0].data
smallImage = doc.getElementsByTagName("SmallImage")[0].getElementsByTagName("URL")[0].childNodes[0].data
mediumImage = doc.getElementsByTagName("MediumImage")[0].getElementsByTagName("URL")[0].childNodes[0].data
LargeImage = doc.getElementsByTagName("LargeImage")[0].getElementsByTagName("URL")[0].childNodes[0].data
ImageSetsList = doc.getElementsByTagName("ImageSets")[0].getElementsByTagName("ImageSet")
ImageSetsdict = {}
n = 1
for set in ImageSetsList:
    Category = set.getAttribute("Category")
    if not Category in ImageSetsdict.keys():
        ImageSetsdict[Category] = [
            dict(SwatchImage=set.getElementsByTagName("SwatchImage")[0].getElementsByTagName("URL")[0].childNodes[0].data),
            dict(SmallImage=set.getElementsByTagName("SmallImage")[0].getElementsByTagName("URL")[0].childNodes[0].data),
            dict(ThumbnailImage=set.getElementsByTagName("ThumbnailImage")[0].getElementsByTagName("URL")[0].childNodes[0].data),
            dict(TinyImage=set.getElementsByTagName("TinyImage")[0].getElementsByTagName("URL")[0].childNodes[0].data),
            dict(MediumImage=set.getElementsByTagName("MediumImage")[0].getElementsByTagName("URL")[0].childNodes[0].data),
            dict(LargeImage=set.getElementsByTagName("LargeImage")[0].getElementsByTagName("URL")[0].childNodes[0].data),
        ]
    else:
        Category = Category + 'x'*n
        ImageSetsdict[Category] = [
            dict(SwatchImage=set.getElementsByTagName("SwatchImage")[0].getElementsByTagName("URL")[0].childNodes[0].data),
            dict(SmallImage=set.getElementsByTagName("SmallImage")[0].getElementsByTagName("URL")[0].childNodes[0].data),
            dict(ThumbnailImage=set.getElementsByTagName("ThumbnailImage")[0].getElementsByTagName("URL")[0].childNodes[0].data),
            dict(TinyImage=set.getElementsByTagName("TinyImage")[0].getElementsByTagName("URL")[0].childNodes[0].data),
            dict(MediumImage=set.getElementsByTagName("MediumImage")[0].getElementsByTagName("URL")[0].childNodes[0].data),
            dict(LargeImage=set.getElementsByTagName("LargeImage")[0].getElementsByTagName("URL")[0].childNodes[0].data),
        ]

Feature_List = []
FeatureList = doc.getElementsByTagName("Feature")
for f in FeatureList:
    text = f.childNodes[0].data
    Feature_List.append(text)





for node in doc.getElementsByTagName("CERT_LIST"):
    for hostnode in node.getElementsByTagName("CERT"):
        ip = hostnode.getAttribute("ip")
        username = hostnode.getAttribute("username")
        password = hostnode.getAttribute("password")
        datacenter = hostnode.getAttribute("datacenter")
        cluster = hostnode.getAttribute("cluster")
# 写入xml数据
impl = xml.dom.minidom.getDOMImplementation()
dom1 = impl.createDocument(None, 'SPEC_LIST', None)
root = dom1.documentElement
root.setAttribute("cpu", cpu)
root.setAttribute("memory", memory)
root.setAttribute("disk", disk)

specifications = dom1.toxml()  # 将doc对象转为xml数据



class TitleTarget(object):
    def __init__(self):
        self.text = []
    def start(self, tag, attrib):
        self.is_title = True if tag == 'Item' else False
    def end(self, tag):
        pass
    def data(self, data):
        if self.is_title:
            self.text.append(data.encode('utf-8'))
    def close(self):
        return self.text

#
# url = "https://webservices.amazon.com/onca/xml?AWSAccessKeyId=AKIAJGDUFSRVEGDP7FCA&AssociateTag=zhanghong-20&Condition=All&IdType=ASIN&ItemId=B07355585W&Operation=ItemLookup&ResponseGroup=Accessories%2CAlternateVersions%2CBrowseNodes%2CEditorialReview%2CImages%2CItemAttributes%2CItemIds%2CLarge%2CMedium%2COfferFull%2COfferListings%2COffers%2COfferSummary%2CPromotionSummary%2CReviews%2CSalesRank%2CSimilarities%2CSmall%2CTracks%2CVariations%2CVariationImages%2CVariationMatrix%2CVariationOffers%2CVariationSummary&Service=AWSECommerceService&Timestamp=2018-11-08T10%3A12%3A37.000Z&Signature=Ny%2BUDbbMDlw%2B1oPvsemfRxowQM5389Wc%2B63c2nmwhGQ%3D"
#
# response = requests.get(url, params=params)
# print(response.text)