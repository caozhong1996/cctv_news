import requests
from bs4 import BeautifulSoup
res = requests.get('http://sx.sina.com.cn/')
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')

for newslist in soup.select('.news-list.cur'):
    for news in newslist:
        for li in news.select('li'):
            title = li.select('h2')[0].text
            href = li.select('a')[0]['href']
            time = li.select('.fl')[0].text
            print (time, title, href)
