
import requests
import json
import time
import random
import datetime
import re

global null, false, true
null = ''
false = 0
true = 1

class SpiderWork(object):

    def printTitle(self):
        print("航空公司\t|" + "航班号\t|" + "出发日期\t\t|" + "出发时间\t\t|" + "出发城市\t|" +
              "出发机场\t|" + "到达日期\t\t|" + "到达时间\t\t|" + "到达城市\t|" + "到达机场\t|" +
              "是否经停\t|" + "经停城市\t|" + "经停到达日期\t|" + "经停到达时间\t|" + "经停出发日期\t|" +
              "经停出发时间\t|" + "准点率\t|" + "经济舱价格\t|" + "公务舱价格\t|" + "头等舱价格\t"

              )

    def printData(self, r):

        self.printTitle()

        for i in r["fltitem"]:
            flight_id = i["mutilstn"][0]["basinfo"]["flgno"]
            airline = i["mutilstn"][0]["basinfo"]["airsname"]
            model = i["mutilstn"][0]["craftinfo"]["cname"] + i["mutilstn"][0]["craftinfo"]["craft"]
            dept_date, dept_time = i["mutilstn"][0]["dateinfo"]["ddate"].split(' ')
            dept_city = i["mutilstn"][0]["dportinfo"]["cityname"]
            dept_airport = i["mutilstn"][0]["dportinfo"]["aportsname"] + i["mutilstn"][0]["dportinfo"]["bsname"]
            arv_date, arv_time = i["mutilstn"][0]["dateinfo"]["adate"].split(' ')
            arv_city = i["mutilstn"][0]["aportinfo"]["cityname"]
            arv_airport = i["mutilstn"][0]["aportinfo"]["aportsname"] + i["mutilstn"][0]["aportinfo"]["bsname"]
            isstop = i["mutilstn"][0]["isstop"]

            try:
                if isstop == 1:
                    tran_city = i["mutilstn"][0]["fsitem"][0]["city"]
                    tran_arvdate, tran_arvtime = i["mutilstn"][0]["fsitem"][0]["arrtime"].split(' ')
                    tran_depdate, tran_deptime = i["mutilstn"][0]["fsitem"][0]["deptime"].split(' ')
                else:
                    tran_city = "----"
                    tran_arvdate, tran_arvtime = "0001-01-01", "--------"
                    tran_depdate, tran_deptime = "0001-01-01", "--------"
            except:
                tran_city = "----"
                tran_arvdate, tran_arvtime = "0001-01-01", "------"
                tran_depdate, tran_deptime = "0001-01-01", "------"

            try:
                flight_id = i["mutilstn"][0]["basinfo"]["flgno"] + '|' + i["mutilstn"][1]["basinfo"]["flgno"]
                airline = i["mutilstn"][0]["basinfo"]["airsname"] + '|' + i["mutilstn"][1]["basinfo"]["airsname"]
                model = i["mutilstn"][0]["craftinfo"]["cname"] + i["mutilstn"][0]["craftinfo"]["craft"] + '|' + \
                        i["mutilstn"][1]["craftinfo"]["cname"] + i["mutilstn"][1]["craftinfo"]["craft"]
                tran_city = arv_city
                arv_city = i["mutilstn"][1]["dportinfo"]["cityname"]
                arv_airport = i["mutilstn"][1]["aportinfo"]["aportsname"] + i["mutilstn"][1]["aportinfo"]["bsname"]
                tran_arvdate, tran_arvtime = arv_date, arv_time
                tran_depdate, tran_deptime = i["mutilstn"][1]["dateinfo"]["ddate"].split(' ')
                arv_date, arv_time = i["mutilstn"][1]["dateinfo"]["adate"].split(' ')
                isstop = 1
            except:
                pass

            ontime_Rate = 0
            try:
                for j in i["mutilstn"][0]["comlist"]:
                    if j["type"] == 2:
                        ontime_Rate = j["stip"]
            except:
                pass

            price_1, price_2, price_3 = 99999, 99999, 99999
            try:
              price_1 = i["policyinfo"][0]['priceinfo'][0]['price']
              price_2 = i["policyinfo"][0]['priceinfo'][1]['price']
              price_3 = i["policyinfo"][0]['priceinfo'][2]['price']
            except:
                pass


            print( airline + "\t\t|" + str(flight_id) + "\t|" + dept_date + "\t|" + dept_time + "\t|" + dept_city + "\t|" +
                   dept_airport + "\t|" + arv_date + "\t|" +  arv_time + "\t|" + arv_city + "\t|" + arv_airport + "\t|" +
                   str(isstop) + "\t\t|" + tran_city + "\t|" + tran_arvdate + "\t|" + tran_arvtime +"\t|" + tran_depdate + "\t|" +
                   tran_deptime + "\t|" + str(ontime_Rate) + "\t\t|" +  str(price_1) + "\t\t|" + str(price_2) + "\t\t|" + str(price_3) + "\t\t")

    def crawler(self, dcity, acity, dtime, client_id):

        payload = json.dumps({"preprdid": "","trptpe": 1,"flag": 8,"searchitem": [{"dccode": "%s" % dcity, "accode": "%s" % acity, "dtime": "%s" % dtime}],"version": [{"Key": "170710_fld_dsmid", "Value": "O"}],"subchannel":null,"tid":"{680429c3-617a-434c-93c0-9f9bed847fd8}", "head": {"cid": "%s" % client_id, "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888","syscode": "09", "auth": 'null',"extension": [{"name": "protocal", "value": "https"}]},"contentType": "json"})
        # payload = json.dumps({"preprdid":"","trptpe":1,"flag":8,"searchitem":[{"dccode":"BJS","accode":"SHA","dtime":"2018-11-27"}],"version":[{"Key":"170710_fld_dsmid","Value":"O"}],"subchannel":null,"tid":"{680429c3-617a-434c-93c0-9f9bed847fd8}","head":{"cid":"09031091111093401287","ctok":"","cver":"1.0","lang":"01","sid":"8888","syscode":"09","auth":null,"extension":[{"name":"protocal","value":"https"}]},"contentType":"json"})
        print("正在使用cid : " + client_id)

        header = {'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E304 baiduboxapp/0_11.0.1.8_enohpi_8022_2421/1.3.01_2C2%258enohPi/1099a/40044AA73C7F521FD9D4D47BC8570DFBAA9EC4310ORSBMFSBPO/1"}
        tmp = requests.post('https://m.ctrip.com/restapi/soa2/14022/flightListSearch?_fxpcqlniredt=' + client_id, data=payload, headers=header)
        r = eval(tmp.content.decode('utf-8'))
        print(r)

        try:
            self.printData(r)
            print('成功爬取' + ' ' + dcity + ' ' + acity + ' ' + dtime)
        except (Exception) as e:
            print(e)
            print('发生错误:' + ' ' + dcity + ' ' + acity + ' ' + dtime)
            time.sleep(random.random() * 10 )

    def crawl(self):

        print("爬虫进程开始运行")
        while (True):
            url = 'https://m.ctrip.com/restapi/soa2/10290/createclientid?systemcode=09&createtype=3&head%5Bcid%5D=&head%5Bctok%5D=&head%5Bcver%5D=1.0&head%5Blang%5D=01&head%5Bsid%5D=8888&head%5Bsyscode%5D=09&head%5Bauth%5D=null&head%5Bextension%5D%5B0%5D%5Bname%5D=protocal&head%5Bextension%5D%5B0%5D%5Bvalue%5D=https&contentType=json'
            result = requests.get(url)
            r = eval(result.content.decode('utf-8'))
            client_id = r['ClientID']
            print("获取的 ClientID = " + r['ClientID'])

            date_list = []
            for i in range(10):
                date_list.append((datetime.date.today() + datetime.timedelta(days=i + 1)).strftime("%Y-%m-%d"))

            d_city = input("出发城市编码\n")
            a_city = input("到达城市编码\n")

            for i in range(len(date_list)):
                print('爬虫节点正在解析: 旅行日期 %s | 出发城市 %s | 到达城市 %s' % (date_list[i], d_city, a_city))
                self.crawler(d_city, a_city, date_list[i], client_id)
                time.sleep(random.random() + 4)

if __name__=="__main__":
    spider = SpiderWork()
    spider.crawl()