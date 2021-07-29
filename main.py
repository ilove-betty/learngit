'''import requests, os, time
from bs4 import BeautifulSoup


# 1.准备url和请求头
# 2.发送get,获取响应数据,转换为html
# 3.提取本页图片和下一页地址
# 4.保存图片
# 5.循环执行第三步操作
class BianImgSpider:
    def __init__(self, url, base_url='https://cn.bing.com/images/search?q=%e5%9c%b0%e5%b9%b3%e7%ba%bf4&form=HDRSC2&first=1&tsc=ImageBasicHover'):
        self.base_url = base_url
        self.url = url
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
        self.has_next = True  # 判断是否有下一页

    def get_html(self):
        """
        获取url地址的html源码
        :return: html源码
        """
        response = requests.get(self.url, headers=self.headers)
        response.encoding = 'gbk'
        return response.text

    def get_imgs_next_url(self):
        """
        获取图片本页的图片列表和下一页的地址
        :return: 图片列表,下一页url
        """
        print("正在爬取网页:", self.url)
        html = self.get_html()
        # print(html)
        # exit()
        soup = BeautifulSoup(html, 'lxml')
        img_list = soup.select('.slist ul li a img')
        # print(img_list)
        # 提取图片的src,装进列表
        imgs = []
        for i in img_list:
            src = i['src']
            src = self.base_url + src
            # print(src)
            # exit()
            imgs.append(src)
        # 提取下一页
        try:
            # next_url = soup.select('.page > a:nth-child(13)')[0]
            # print(next_url['href'])
            # exit()
            # 找到page
            page = soup.select('.page')[0]
            # print(page, type(page))
            # 下一页是最后一个a
            # print(page.a)
            # print(page.contents)
            # print(page.contents[-1])
            href = page.contents[-1]['href']
            # print(href)
            next_url = self.base_url + href
            # print(next_url)
            return next_url, imgs
        except:
            print("没有下一页了")
            # 告知没有下一页了,方便操作
            self.has_next = False

    def save_img(self, imgs):
        """
        保存列表中的图片
        :param imgs: 图片列表
        :return: True
        """
        try:
            for img in imgs:
                # 提取图片名字
                # print(type(img))
                img_name = img.split('/')[-1]
                # print(img_name)
                # 设置图片保存地址
                save_path = 'imgs'
                if not os.path.exists(save_path):
                    os.mkdir(save_path)
                response = requests.get(img, headers=self.headers)
                # 获取图片流
                with open(save_path + "/" + img_name, 'wb') as f:
                    # 每次读写1M数据
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                # exit()
            print("一个图片列表被保存成功")
            return True
        except:
            print("保存失败")
            return False

    def run(self):
        """
        运行爬虫,保存图片
        :return: 成功返回True,失败返回False
        """
        try:
            while self.has_next:
                next_url, imgs = self.get_imgs_next_url()
                # print(imgs)
                # print(next_url)
                # 保存图片
                self.save_img(imgs)
                # 将url改为下一页的url
                self.url = next_url
                # 文明爬取,每爬取一页,休息一秒钟,防止破坏服务器
                time.sleep(1)
            return True
        except:
            print("保存图片失败")
            return False


if __name__ == '__main__':
    spider = BianImgSpider('https://cn.bing.com/images/search?q=%e5%9c%b0%e5%b9%b3%e7%ba%bf4&form=HDRSC2&first=1&tsc=ImageBasicHover')
    spider.run()'''
# -*- coding: utf-8 -*-
import re
import requests
from urllib import error
from bs4 import BeautifulSoup
import os

num = 0
numPicture = 0
file = ''
List = []


def Find(url, A):
    global List
    print('正在检测图片总数，请稍等.....')
    t = 0
    i = 1
    s = 0
    while t < 1000:
        Url = url + str(t)
        try:
            # 这里搞了下
            Result = A.get(Url, timeout=7, allow_redirects=False)
        except BaseException:
            t = t + 60
            continue
        else:
            result = Result.text
            pic_url = re.findall('"objURL":"(.*?)",', result, re.S)  # 先利用正则表达式找到图片url
            s += len(pic_url)
            if len(pic_url) == 0:
                break
            else:
                List.append(pic_url)
                t = t + 60
    return s


def recommend(url):
    Re = []
    try:
        html = requests.get(url, allow_redirects=False)
    except error.HTTPError as e:
        return
    else:
        html.encoding = 'utf-8'
        bsObj = BeautifulSoup(html.text, 'html.parser')
        div = bsObj.find('div', id='topRS')
        if div is not None:
            listA = div.findAll('a')
            for i in listA:
                if i is not None:
                    Re.append(i.get_text())
        return Re


def dowmloadPicture(html, keyword):
    global num
    # t =0
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)  # 先利用正则表达式找到图片url
    print('找到关键词:' + keyword + '的图片，即将开始下载图片...')
    for each in pic_url:
        print('正在下载第' + str(num + 1) + '张图片，图片地址:' + str(each))
        try:
            if each is not None:
                pic = requests.get(each, timeout=7)
            else:
                continue
        except BaseException:
            print('错误，当前图片无法下载')
            continue
        else:
            string = file + r'\\' + keyword + '_' + str(num) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            return


if __name__ == '__main__':  # 主函数入口
    ##############################
    # 这里加了点
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Upgrade-Insecure-Requests': '1'
    }

    A = requests.Session()
    A.headers = headers
    ###############################
    word = input("请输入搜索关键词(可以是人名，地名等): ")
    # add = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%E5%BC%A0%E5%A4%A9%E7%88%B1&pn=120'
    url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&pn='

    # 这里搞了下
    tot = Find(url, A)
    Recommend = recommend(url)  # 记录相关推荐
    print('经过检测%s类图片共有%d张' % (word, tot))
    numPicture = int(input('请输入想要下载的图片数量 '))
    file = input('请建立一个存储图片的文件夹，输入文件夹名称即可')
    y = os.path.exists(file)
    if y == 1:
        print('该文件已存在，请重新输入')
        file = input('请建立一个存储图片的文件夹，)输入文件夹名称即可')
        os.mkdir(file)
    else:
        os.mkdir(file)
    t = 0
    tmp = url
    while t < numPicture:
        try:
            url = tmp + str(t)
            # 这里搞了下
            result = A.get(url, timeout=10, allow_redirects=False)

        except error.HTTPError as e:
            print('网络错误，请调整网络后重试')
            t = t + 60
        else:
            dowmloadPicture(result.text, word)
            t = t + 60
    print('当前搜索结束，感谢使用')
    print('猜你喜欢')

    for re in Recommend:
        print(re, end='  ')
