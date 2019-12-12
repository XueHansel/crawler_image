# -*- coding: utf-8 -*-

"""根据搜索词下载百度图片"""
import re
import sys
import urllib
import os
import requests

from contextlib import closing
import threading
import json as js


## 多线程的百度图片网络爬虫


headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

#线程数
thread_num = 30
#http请求超时设置
timeout = 30
def download(img_url, img_name, img_class):
    if os.path.isfile(os.path.join(os.path.join(out_dir, img_class), img_name)):
        return    ####如果之前下载过这个文件，就跳过
    with closing(requests.get(img_url, stream=True, headers=headers, timeout=timeout)) as r:
        rc = r.status_code
        if 299 < rc or rc < 200:
            print ('returnCode%s\t%s' % (rc, img_url))
            return
        content_length = int(r.headers.get('content-length', '0'))
        if content_length == 0:
            print ('size0\t%s' % img_url)
            return
        try:

            with open(os.path.join(os.path.join(out_dir, img_class), img_name), 'wb') as f:
                for data in r.iter_content(1024):
                    f.write(data)
            print(img_name)
        except:
            print('savefail\t%s' % img_url)


# def get_img_url_generate():
#     imgs=[]
#     with open(json_path,'r') as f:
#         setting=js.load(f)
#         images=setting["images"]
#         for img in images:
#             imgs=[]
#             img_url=img['url']
#             img_id=img['id']
#             img_class=img['class']
#             imgs.append(img_url)
#             imgs.append(img_id)
#             imgs.append(img_class)
#             try:
#                 if img_url:
#                     yield imgs
#             except:
#                 break
	

lock = threading.Lock()
def loop(imgs, label):
    print ('thread %s is running...' % threading.current_thread().name)

    while True:
        try:
            with lock:
                img_url = next(imgs)
                img_id = img_url.strip().split('/')[-1]
                if  not img_id.endswith('.jpg' or '.png' or '.jpeg'):
                    continue
        except StopIteration:
            break
        try:
            
            download(img_url,img_id,label)
        except:
            print ('exceptfail\t%s' % img_url)
    print ('thread %s is end...' % threading.current_thread().name)


# imgs = get_img_url_generate()







def get_onepage_urls(onepageurl):
    """获取单个翻页的所有图片的urls+当前翻页的下一翻页的url"""

    if not onepageurl:
        print('已到最后一页, 结束')
        return [], ''

    try:
        html = requests.get(onepageurl)
        html.encoding = 'utf-8'
        html = html.text
    except Exception as e:
        print(e)
        pic_urls = []
        nextpage_url = ''
        return pic_urls, nextpage_url

    pic_urls = re.findall('"objURL":"(.*?)",', html, re.S)
    nextpage_urls = re.findall(re.compile(r'<a href="(.*)" class="n">下一页</a>'), html, flags=0)
    nextpage_url = 'http://image.baidu.com' + nextpage_urls[0] if nextpage_urls else ''

    return pic_urls, nextpage_url


# def down_pic(pic_urls, label):
#     """给出图片链接列表, 下载所有图片"""

#     for i, pic_url in enumerate(pic_urls):

#         try:
#             pic = requests.get(pic_url, timeout=15)
#             dirpath1 = os.path.join(dirpath,str(label))
#             os.mkdir(dirpath1)
#             img_name ='fimg_' + str(i) + '.jpg'
#             filename = os.path.join(dirpath1, img_name)

#             with open(filename, 'wb') as f:
#                 f.write(pic.content)
#                 print('成功下载第%s张图片: %s' % (str(i + 1), str(pic_url)))
#             txtName = 'fimg_' + str(i) + '.txt'
#             writeTxt(dirpath1, txtName, img_name, label)
#         except Exception as e:
#             print('下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
#             print(e)
#             continue


# def writeTxt(dirpath, txtName, img_name, label):
#     filename = os.path.join(dirpath, txtName)
#     file = open(filename, 'w')
#     line = img_name + ', ' + str(label)
#     file.write(line)
#     file.close()
#     return True


if __name__ == '__main__':

    
    #下载地址文件夹
    out_dir ='f:/data_et1'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open('f:/code_repository/crawler/name2.txt', encoding='utf-8') as f:
        line_list = [k.strip() for k in f.readlines()]  # 用 strip()移除末尾的空格

    labels = []
    keywords = []
    for line in line_list:
        label = line.split(":")[0]
        labels.append(label)
        keyword = line.split(":")[1].split('/')[-1]
        keywords.append(keyword)

    for img_cla in keywords:  #建立类别文件夹，保存在不同文件夹中
        if not os.path.exists(os.path.join(out_dir,img_cla)):
            os.makedirs(os.path.join(out_dir,img_cla))

    for keyword in keywords:
        url_init_first = r'http://image.baidu.com/search/flip?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1497491098685_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&ctd=1497491098685%5E00_1519X735&word='
        url_init = url_init_first + urllib.parse.quote(keyword, safe='/')
        all_pic_urls = []
        onepage_urls, nextpage_url = get_onepage_urls(url_init)
        all_pic_urls.extend(onepage_urls)

        nextpage_count = 0  # 累计翻页数
        max_page = 20

        while True:
            onepage_urls, nextpage_url = get_onepage_urls(nextpage_url)
            nextpage_count += 1
            #print('第页' % str(nextpage_count))
            if (nextpage_url == '' and onepage_urls == []) or nextpage_count>max_page:
                break
            all_pic_urls.extend(onepage_urls)

        imgs = iter(all_pic_urls)
        for i in range(0, thread_num):
            t = threading.Thread(target=loop, name='LoopThread %s' % i, args=(imgs,keyword,))
            t.start()

        # down_pic(list(set(all_pic_urls)), label)


