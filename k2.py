#coding:utf-8
import requests
import re
import time
import os
import urllib.request


def executer(source_result,j):
    # 查找合集中各图片的网址的后半部分
    time.sleep(1)
    source_url_list = re.findall('<a class="thumb" href=(.*?)>',source_result,re.S)
    print("已分析出原网页图片代码")
    print("第",j,"页")
    #f.write("第",j,"页","\n")
    # 循环直到把本页所有图片爬完
    i = 0
    print("共",len(source_url_list),"张")
    while i < len(source_url_list):
        time.sleep(1)
        # 转换成目标图片的网址
        url_aim = "https://konachan.com%s" %str(source_url_list[i].strip('"'))
        # 同时在txt中进行记录
        #f.write(url_aim)
        #f.write("\n")
        time.sleep(1)
        # 进一步获取目标图片的大图地址
        result = requests.get(url_aim).text
        time.sleep(1)
        url_name = re.findall('<li><a class="original-file-unchanged" href="https://konachan.com/image/(.*?)" id="png">',result,re.S)
        if len(url_name) == 0:
            url_name = re.findall('<li><a class="original-file-changed" href="https://konachan.com/image/(.*?)" id="highres">',result,re.S)
            if len(url_name) == 0:
                url_name = re.findall('<li><a class="original-file-unchanged" href="https://konachan.com/image/(.*?)" id="highres">',result,re.S)
        url = "https://konachan.com/image/%s"%str("".join(url_name).strip("'"))
        time.sleep(1)
        path = 'F:/%s'%str(get_message)
        image_name =os.path.basename(url).replace("%20"," ").replace("%28","(").replace("%29",")")
        filepath = path +'/'+image_name
        print("正在下载第",i+1,"张")
        downloadFile(image_name, url,filepath,i)
        print("第",i+1,"张完成")
        #f.write("完成\n")
        i+=1
        time.sleep(1)
        #f.close()
    judge(source_result,j)


def downloadFile(image_name, url,filepath,i):
    headers = {'Proxy-Connection':'keep-alive'}
    r = requests.get(url, stream=True, headers=headers)
    length = float(r.headers['content-length'])
    f = open(filepath, 'wb')
    count = 0
    count_tmp = 0
    time1 = time.time()
    for chunk in r.iter_content(chunk_size = 512):
        if chunk:
            f.write(chunk)
            count += len(chunk)
            if time.time() - time1 > 2:
                p = count / length * 100
                speed = (count - count_tmp) / 1024 / 1024 / 2
                count_tmp = count
                print("第",i+1,"张" + ': ' + formatFloat(p) + '%' + ' Speed: ' + formatFloat(speed) + 'M/S')
                time1 = time.time()
    f.close()

    
def formatFloat(num):
    return '{:.2f}'.format(num)

def judge(source_result,j):
    time.sleep(3)
    source_url_next_tag = re.findall('<a class="next_page" rel="next" href=(.*?)>Next ',source_result,re.S)
    if len(source_url_next_tag) != 0:
        j += 1
        #f =open ("looker.txt",'a')
        #f.write("第",j,"页","\n")
        source_url_next = "https://konachan.com%s" %str("".join(source_url_next_tag).strip('"'))
        print("正在进入下一页")
        time.sleep(2)
        source_result=requests.get(source_url_next).text
        print("已找到原网页代码")
        executer(source_result,j)
    else:
        print("结束")



if __name__== "__main__":
    j = 1
    # 进入作者的图片合集
    get_message = input("请输入作者:\n")
    artist = get_message.replace("(","%28").replace(")","%29")
    num = input("请输入页数：\n")
    #f =open ("looker.txt",'a')
    #f.write(artist)
    #f.write("\n")
    source_url = "https://konachan.com/post?page=%d&tags=%s".replace("%d",num).replace("%s",artist)
    print(source_url)
    source_result = requests.get(source_url).text
    print("已找到原网页代码")
    # 新建该作者文件夹
    #path = 'F:/%s'%str(get_message)
    #os.mkdir (path) 
    executer(source_result,j)
    
