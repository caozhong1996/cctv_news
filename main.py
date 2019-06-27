import datetime
import json
import requests
from bs4 import BeautifulSoup
import time
import xlwt

SLEEP_TIME = 0.5 # 爬取每个新闻网页的间隔时间，单位为秒
END_TIME = '20190617' # 爬取新闻的截至时间
REQUESTS_DAYS = 167 # 爬取截至时间之前多少天的新闻

urls = []
dates = []
titles = []
contents = []

def get_nday_list(n):
    before_n_days = []
    for i in range(1, n + 1)[::-1]:
        before_n_days.append(str(
          (datetime.datetime.strptime(END_TIME,'%Y%m%d') - datetime.timedelta(days=i)).strftime('%Y%m%d')
        ))
    return before_n_days
day_list = get_nday_list(REQUESTS_DAYS)

def clear_sentence(sentence):
    sentence = sentence.replace('[视频]', '')
    sentence = sentence.replace('_CCTV节目官网-CCTV-1_央视网(cctv.com)', '')
    sentence = sentence.replace('央视网消息（新闻联播）：', '')
    return sentence

#设置表格样式
def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

STYLE = set_style('Times New Roman',400,True)

print('====正在爬取新闻地址！====')

for date in day_list:
    time.sleep(1)
    url = 'http://tv.cctv.com/lm/xwlb/day/' + date + '.shtml'
    res = requests.get(url)
    res.encoding='utf-8'
    bs4 = BeautifulSoup(res.text)
    source = bs4.find_all('a', target='_blank')
    for index, url in enumerate(source):
        if index > 0:
            urls.append(url.get('href'))
            dates.append(date)

print('====地址请求完毕，开始请求正文！====') 

for index, url in enumerate(urls):
    time.sleep(SLEEP_TIME)
    res = requests.get(url)
    res.encoding='utf-8'
    bs4 = BeautifulSoup(res.text)
    title = bs4.find('title').getText()
    titles.append(clear_sentence(title))
    content = bs4.find('div', class_='cnt_bd').getText()
    contents.append(clear_sentence(content))
    print('====共'+ str(len(urls)) +'条,已爬取第' + str(index + 1) + '条！====') 

print('====正文请求完毕，开始写入文件！====') 

#写Excel
def write_excel():
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('新闻',cell_overwrite_ok=True)
    row0 = ["time","title","content"]
    #写第一行
    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i],STYLE)
    for i in range(0,len(titles)):
        sheet1.write(i + 1, 0, dates[i], STYLE)
        sheet1.write(i + 1, 1, titles[i], STYLE)
        sheet1.write(i + 1, 2, contents[i], STYLE)

    f.save('test.xls')

if __name__ == '__main__':
    write_excel()
    print('====完成！====') 
