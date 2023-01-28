import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import ast
import os


def get_data():
    if os.path.exists('./news_url.txt'):
        news_file = open('./news_url.txt', 'r')
        news_list_str = news_file.read()
        news_list = ast.literal_eval(news_list_str)
        news_file.close()
    else:
        origin_url = 'https://new.qq.com'
        browser = webdriver.Chrome(service=Service('./chromedriver.exe'))
        browser.get(origin_url)
        for i in range(10):
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)
        page_text = browser.page_source
        tree = etree.HTML(page_text)
        web_news_list = tree.xpath("//ul[@class = 'list']//div[@class = 'detail']//h3/a/@href")
        news_list = []
        news_list.extend(web_news_list)
        news_file = open('news_url.txt', 'w')
        news_file.write(str(news_list))
        news_file.close()
        print(len(news_list))
        time.sleep(5)
        browser.quit()

    if not os.path.exists('../data/data_content'):
        os.makedirs('../data/data_content')
    if not os.path.exists('../data/data_url'):
        os.makedirs('../data/data_url')
    page = 1
    for index, url in enumerate(news_list):
        res = requests.get(url)
        page_tree = etree.HTML(res.text)
        try:
            title = page_tree.xpath('//h1/text()')[0]
        except:
            continue
        ret = page_tree.xpath("//div[@class = 'content-article']")[0].xpath(".//p/text()")
        if not ret:
            continue
        print(page)
        for i in range(len(ret)):
            ret[i] = ret[i].strip()
        raw_content = ''.join(ret)
        content = raw_content.strip()
        fnews = open(os.path.join('../data/data_content', str(page) + '.txt'), 'w', encoding='utf-8')
        time.sleep(0.3)
        fnews.write(title + '\n' + content + '\n')
        fnews.close()
        fnewsurl = open(os.path.join('../data/data_url', str(page) + '.txt'), 'w', encoding='utf-8')
        fnewsurl.write(url)
        page += 1
        fnewsurl.close()


if __name__ == '__main__':
    get_data()
