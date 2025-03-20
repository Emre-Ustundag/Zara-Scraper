import sys
import os
sys.path.append('.')
from DB_Connect import connectdb, pull_Product,pull_Product_Flex,update_Product,close_Connection
import requests
import json
import time
import random
from server_mail import start

class Gather:
    def __init__(self,link,size):
        self.link = link
        self.size = size

class product(Gather):
    def __init__(self,link,size):
        super().__init__(link,size)
        self.name = ""
        self.avalible = []   
        self.discount = False
        self.newprice = 0
        self.oldprice = 0

class scraper():
    def __init__(self,link):
        print("Scraper is starting")
        self.link = link
        self.requestCount = 0
        self.session = requests.Session()
   
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                "Accept-Encoding": "gzip, deflate",
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            "Cache-Control": "max-age=0",
            'TE': 'Trailers',
            "Referer": "https://www.zara.com"

        })

    def request(self):
        response = self.session.get(self.link,timeout=10)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            
            data = response.text
            
            data = data[data.find('"productMetaData":')+18:data.find('"parentId":')-1] 
            data = json.loads(data)
            return data
           
        else:
            print(f"Sayfa alınamadı, durum kodu: {response.status_code}")
            
            print("response.cookies.get_dict(): ",response.cookies.get_dict())
            self.reset_Cookies(response.cookies.get_dict())
        self.requestCount += 1
        print("requestCount: ", self.requestCount)
        
    def reset_Cookies(self,cookies):
        self.session.cookies.update(cookies)
        self.request()
    
            
global_requestCount = 0
loopCount = 0


while True:
    connectdb()
    products = pull_Product("Product","*")
    loopCount += 1


    if len(products) != 0:
        for i in products:

            sizes = pull_Product_Flex("Size","*","Product_ID",i[0])
                            
            scrap = scraper(i[2]+"ajax=true"+"&bm-verify=AAQAAAAK_____8iGGD43KMEc7kOEVbp-th_ZbdZlQ3kb78qxacGBU7Lwfy_6_V1eUf-KYU3n8PLjIwGuUJlrbrYNXvPCSHGKtVN5sibWOyiaSsS_o4tFh_n6Ka5XmarZaAjTsELi4YepuIvWB8uebzpBSkkawYiGUq2tR8ds4bcMcjgYhBUooIWVzWG9g8aIvi1pF-et56w2YDs-9SmbjgU-LDLjMtzdTIXfK4CtgL0scdr4NcT-AAQ1AUghFzGhh7YriMWIsCetpsxGgiT-bB6stDNexJS4Tz8qhHFfPlXivOW5NgXU4Bc0FTKGAVeq1fy_VMAvdTIjNRt4e3EXv2ldaZ6IXJWXCuHaB_Wn3VqQA3l8wQ")   #lınk
            try:
                data = scrap.request()
                global_requestCount += 1
            except requests.exceptions.ReadTimeout:
                print("Script yeniden başlatılıyor.")
                time.sleep(random.randint(0,2))
                os.execv(sys.executable, ['python'] + sys.argv)

            for t in data:
                print("##_For Loop_##")
                for k,z in enumerate(sizes):
                    print("z[2]: "+z[2]+ " t[sizeName]: "+t["sizeName"])
                    if t["sizeName"] == z[2] and t["availability"] == "in_stock" and k<len(sizes):
                        print("In stock")
                        sizes[k][3] = True
                        
                    elif t["sizeName"] == z[2] and t["availability"] == "low_on_stock" and k<len(sizes):
                        print("Low on stock")
                        sizes[k][3] = True
                        
                    elif t["sizeName"] == z[2] and t["availability"] == "coming_soon" and k<len(sizes):
                        print("Coming soon")
                        sizes[k][3] = False
                    else:
                        print("Error")
                        
            print("sizes: ",sizes)
            
            if sizes != []:
                update_Product(data[0]["name"],data[0]["price"],sizes)
            print("Sleep: 1")
            time.sleep(1)
    else:
        print("Database'de ürün bulunmamaktadır.")
        
    
    start()
    close_Connection()
    print("---------------------------")
    print("Sleep: 3-5")
    print("loopCount: ",loopCount)
    print("global_requestCount: ",global_requestCount)
    print("---------------------------")

    time.sleep(random.randint(3,5))
    
    