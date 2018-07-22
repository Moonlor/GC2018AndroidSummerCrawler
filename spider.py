import requests
import re
from bs4 import BeautifulSoup
import codecs

#===============================UrlManager===============================

class UrlManager(object):

    def __init__(self):
        self._new_urls = set()
        self._old_urls = set()

    def newUrlSize(self):
        return len(self._new_urls)

    def oldUrlSize(self):
        return len(self._old_urls)

    def hasNewUrl(self):
        return self._new_urls

    def getNewUrl(self):
        new_url = self._new_urls.pop()
        self._old_urls.add(new_url)
        return new_url

    def addNewURl(self, url):
        if url is None:
            return
        if url not in self._new_urls and url not in self._old_urls:
            self._new_urls.add(url)

    def addNewUrls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.addNewURl(url)

#===============================Downloader===============================

class Downloader(object):

    def download(self, url):
        if url is None:
            return None

        user_agent = 'Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11'
        headers = {'User-Agent' : user_agent}
        r = requests.get(url, headers = headers)

        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None

# ===============================HtmlParser===============================


class HtmlParser(object):

    def parser(self,page_url,html_cont):

        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont,'html.parser')
        new_urls = self.getNewUrls(page_url,soup)
        new_data = self.getNewData(page_url,soup)

        return new_urls,new_data


    def getNewUrls(self,page_url,soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r'/item/.*'))
        page_url = "https://baike.baidu.com"

        for link in links:
            new_url = link['href']
            new_full_url = page_url + new_url
            new_urls.add(new_full_url)

        return new_urls

    def getNewData(self,page_url,soup):
        data={}
        data['url']=page_url
        title = soup.find('dd',class_='lemmaWgt-lemmaTitle-title').find('h1')
        data['title']=title.get_text()
        summary = soup.find('div',class_='lemma-summary')
        data['summary']=summary.get_text()
        return data


# ===============================DataOutput===============================

class DataOutput(object):

    def __init__(self):
        self.datas=[]

    def storeData(self,data):
        if data is None:
            return
        self.datas.append(data)

    def outputHtml(self):
        fout=codecs.open('baike.html','w',encoding='utf-8')
        fout.write("<!DOCTYPE html>")
        fout.write('<html lang="en">')
        fout.write('<head><meta charset="UTF-8"></head>')
        fout.write("<body>")
        fout.write('<table border="1">')

        for data in self.datas:
            fout.write("<tr>")
            fout.write("<th>%s</th>"%data['url'])
            fout.write("<th>%s</th>"%data['title'])
            fout.write("<th>%s</th>"%data['summary'])
            fout.write("</tr>")
            self.datas.remove(data)

        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()

# ===============================DataOutput===============================

class Spider(object):

    def __init__(self):
        self.manager = UrlManager()
        self.downloader = Downloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self,root_url):

        self.manager.addNewURl(root_url)

        while(self.manager.hasNewUrl() and self.manager.oldUrlSize()<20):
            try:
                new_url = self.manager.getNewUrl()

                html = self.downloader.download(new_url)

                new_urls,data = self.parser.parser(new_url,html)

                self.manager.addNewUrls(new_urls)

                self.output.storeData(data)
                print("已经抓取%s个链接" % (self.manager.oldUrlSize()))
            except Exception as e:
                print(e)
                print("抓取失败")

        self.output.outputHtml()

# ===============================__main__===============================

if __name__=="__main__":
    spider = Spider()
    url = input("请输入百科词条链接: \n")
    spider.crawl(url)



