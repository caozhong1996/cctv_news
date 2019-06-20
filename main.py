import datetime
import json
import requests
from bs4 import BeautifulSoup
import time

def get_nday_list(n):
    before_n_days = []
    for i in range(1, n + 1)[::-1]:
        before_n_days.append(str(
          (datetime.datetime.strptime('20190617','%Y%m%d') - datetime.timedelta(days=i)).strftime('%Y%m%d')
        ))
    return before_n_days
#day_list = get_nday_list(167)
day_list = get_nday_list(1)

titles = []
urls = []
contents = []
#http://tv.cctv.com/lm/xwlb/day/20190617.shtml
for data in day_list:
    time.sleep(5)
    url = 'http://tv.cctv.com/lm/xwlb/day/' + data + '.shtml'
    res = requests.get(url)
    res.encoding='utf-8'
    bs4 = BeautifulSoup(res.text)
    source = bs4.find_all('a', target='_blank')
    for index, url in enumerate(source):
        if index > 0:
            urls.append(url.get('href'))

print('====地址请求完毕，开始请求正文！====') 

for url in urls:
    time.sleep(5)
    res = requests.get(url)
    res.encoding='utf-8'
    bs4 = BeautifulSoup(res.text)
    title = bs4.find('title')
    titles.append(title.getText())
    content = bs4.find('div', class_='cnt_bd')
    contents.append(content.getText())
    
print(contents)
print(titles)

print('====正文请求完毕，开始写入文件！====') 
