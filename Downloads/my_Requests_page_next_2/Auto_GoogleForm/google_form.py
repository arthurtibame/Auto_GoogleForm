import requests
from bs4 import BeautifulSoup
import lxml
from urllib3._collections import HTTPHeaderDict
import random


class GoogleForm:
    
    def __init__(self, month, day, input_text):
        self.month = str(month) + '月'
        self.day = str(day)+"日"
        self.ss = requests.Session()
        self.url_get = 'https://docs.google.com/forms/d/e/1FAIpQLSef0JxlDOELXGXYAuUW06Y3-tYIkmj9wMUX5xrwaSFRUb6X7Q/viewform'
        self.url_post = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSef0JxlDOELXGXYAuUW06Y3-tYIkmj9wMUX5xrwaSFRUb6X7Q/formResponse"
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 ',
                    'cookie': "CONSENT=YES+TW.en-GB+202003; HSID=AIdWlXZJlrbVdulWk; SSID=AgEFP5Ehi2hzBnsnY; APISID=d4MuA88grnOCu28i/AsS0HMIg-vaTtt8hm; SAPISID=RKaBtpkLqGKTruOz/Ao2TE0iABsYMBVUlw"
                }
        self.data = HTTPHeaderDict()
        self.data.add('entry.583024700', input_text)
        self.data.add('entry.1000003', self.month)
        self.data.add('entry.2789839', self.day)
        self.name_list=[]

        
    
    def get_question(self):        
        res_get = self.ss.get(self.url_get, headers=self.headers)
        soup = BeautifulSoup(res_get.text, 'lxml')
        
        names = soup.find_all("div", attrs={"class":'docssharedWizToggleLabeledPrimaryText'})
        for name in names[1:]:
            self.name_list.append(name.text)
        print(self.name_list)
        draftResponse = soup.select('input[type="hidden"]')[-3]
        fbzx = soup.select('input[type="hidden"]')[-1]
        self.data.add(draftResponse['name'], draftResponse['value'][:-1]) # 去掉換行符號
        self.data.add(fbzx['name'], fbzx['value']) 
        print(self.data)
        return ['200']

    
    def submit_response(self):
        # random student number 
        student_num = [i for i in range(1,random.randint(1,31))]
        # append to data
        for num in student_num:
            name = self.name_list[num]   
            self.data.add("entry.1000006", name)
        
        res_post = self.ss.post(self.url_post, headers=self.headers,data=self.data)

        return res_post

if __name__ == "__main__":
    
    test = GoogleForm(6,1, "fuck")
    test.get_question()
    print(test.submit_response())

 