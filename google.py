"""
1. entry.583024700 : "隨便打名字"
2. entry.1000003 : "6月"
3. entry.2789839 : "1日"
4. entry.1000005 : "206"
# 加入學生名單    
5  entry.1000006_sentinel
   entry.1000006 : 毛彥森 邱耀毅 謝昀燊
6  fvv : 1
7. draftResponse : [null, null, "這邊數字要先抓"]
8. pageHistory : 0 (都是0)
9. fbzx : 每次都要抓
"""
import requests
from bs4 import BeautifulSoup
import lxml
from urllib3._collections import HTTPHeaderDict
from datetime import date

ss = requests.Session()
url = 'https://docs.google.com/forms/d/e/1FAIpQLSef0JxlDOELXGXYAuUW06Y3-tYIkmj9wMUX5xrwaSFRUb6X7Q/viewform'



headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 ',
            'cookie': "CONSENT=YES+TW.en-GB+202003; HSID=AIdWlXZJlrbVdulWk; SSID=AgEFP5Ehi2hzBnsnY; APISID=d4MuA88grnOCu28i/AsS0HMIg-vaTtt8hm; SAPISID=RKaBtpkLqGKTruOz/Ao2TE0iABsYMBVUlw"
         }
res_get = ss.get(url, headers=headers)
soup = BeautifulSoup(res_get.text, 'lxml')


data = HTTPHeaderDict()
data.add('entry.583024700', '林書立')
data.add('entry.1000005', '206')
data.add('pageHistory', '0')
data.add('entry.1000006', '林書立')
data.add('entry.1000006', '吳柏叡')
data.add('entry.1000006', '吳定楠')
data.add('entry.1000006', '李嘉倫')
data.add('entry.1000006', '林宥辰')
data.add('entry.1000006', '張邑丞')


draftResponse = soup.select('input[type="hidden"]')[-3]
fbzx = soup.select('input[type="hidden"]')[-1]

data.add(draftResponse['name'], draftResponse['value'][:-1]) # 去掉換行符號
data.add(fbzx['name'], fbzx['value']) 

today_month = str(date.today().month) + "月"
today_day = str(date.today().day) + "日"

data.add('entry.1000003', today_month)
data.add('entry.2789839', today_day)

print(data)
url2 = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSef0JxlDOELXGXYAuUW06Y3-tYIkmj9wMUX5xrwaSFRUb6X7Q/formResponse"
url_post = ss.post(url2, headers=headers, data=data)
soup = BeautifulSoup(url_post.text, 'lxml')
content = soup.select('div[class="freebirdFormviewerViewResponseConfirmationMessage"]')[0]
print(content.text)
print(url_post)



