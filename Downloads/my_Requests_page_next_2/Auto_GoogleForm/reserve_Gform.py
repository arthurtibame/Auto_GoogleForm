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
from datetime import date, timedelta


def auto_apply(month, day, applicant):
   ss = requests.Session()
   url = 'https://docs.google.com/forms/d/e/1FAIpQLSef0JxlDOELXGXYAuUW06Y3-tYIkmj9wMUX5xrwaSFRUb6X7Q/viewform'

   headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 ',
               'cookie': "CONSENT=YES+TW.en-GB+202003; HSID=AIdWlXZJlrbVdulWk; SSID=AgEFP5Ehi2hzBnsnY; APISID=d4MuA88grnOCu28i/AsS0HMIg-vaTtt8hm; SAPISID=RKaBtpkLqGKTruOz/Ao2TE0iABsYMBVUlw"
            }
   res_get = ss.get(url, headers=headers)
   soup = BeautifulSoup(res_get.text, 'lxml')  
   
   #soup crawl hidden input ley & value
   draftResponse = soup.select('input[type="hidden"]')[-3]
   fbzx = soup.select('input[type="hidden"]')[-1]

   # students' name (list of names in the class)
   #names = soup.find_all("div", attrs={"class":'docssharedWizToggleLabeledPrimaryText'})

   # dict of data add input
   data = HTTPHeaderDict()

   #google form hidden input
   data.add(draftResponse['name'], draftResponse['value'][:-1]) # 去掉換行符號
   data.add(fbzx['name'], fbzx['value']) 
   data.add('pageHistory', '0') 

   # applicants of applying machine room (網頁出現要填入的資料)
   data.add('entry.583024700', str(applicant)) # applicant
   data.add('entry.1000005', '206') # classroom number

   data.add('entry.1000006', str(applicant))
   data.add('entry.1000006', '吳柏叡')
   data.add('entry.1000006', '李嘉倫')
   data.add('entry.1000006', '林宥辰')
   data.add('entry.1000006', '吳定楠')
   data.add('entry.1000006', '姜莉敏')
   #applying date 
   apply_month = str(month) + '月'
   apply_day = str(day) + '月'
   data.add('entry.1000003', apply_month)
   data.add('entry.2789839', apply_day)

   # post and submit
   url2 = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSef0JxlDOELXGXYAuUW06Y3-tYIkmj9wMUX5xrwaSFRUb6X7Q/formResponse"
   res_post = ss.post(url2, headers=headers, data=data)
   soup = BeautifulSoup(res_post.text, 'lxml')   
   try:
      content = soup.select('div[class="freebirdFormviewerViewResponseConfirmationMessage"]')[0]
      if res_post.status_code==200 and content is not None:
         return content
   except:
      
         return 'Response' + str(res_post.status_code)

def main():
   applicant = str(input("請輸入申請者姓名:  "))
   days = int(input("請輸入要續借天數: "))
   # get today date
   today_date = date.today()

   for i in range(1,days+1):
       #reserve days
      reserve_days = timedelta(days=i)
      reserve_date = today_date + reserve_days
      result = auto_apply(reserve_date.month, reserve_date.day, applicant)
      print(result)
      print()
      print("已成功預約 {} ".format(reserve_date))


if __name__ == "__main__":
   main()    

