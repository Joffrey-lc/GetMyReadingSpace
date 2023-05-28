# -*- coding: utf-8 -*-
"""
 @Time    : 2022/3/13 13:32
 @Author  : LC
 @File    : utils4paperreading.py
 @Software: PyCharm
"""
import os
import shutil
import time
import requests

proxies = {'https': 'http://127.0.0.1:7890'}


def checkfilename(filename: str):
    incorrect = [':', '?', '|', '<', '>', '"', '*', '/']
    for f in incorrect:
        filename = filename.replace(f, '_')
    return filename


def mymkdirs(path_dir):
    if os.path.exists(path_dir) is False:
        os.makedirs(path_dir)
        print(path_dir+'已创建')


def mypaperspace(path_paper, mdinfo):
    shutil.move(src=path_paper + '.pdf', dst=os.path.join(path_paper, 'paper.pdf'))
    with open(path_paper + '\\notes.md', 'a', encoding='utf-8') as f:
        for ll in mdinfo:
            f.write(ll)


def GetPaperInfo(srcUrl):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate'}
    with requests.get(srcUrl, stream=True, headers=headers, proxies=proxies) as r:  # timeout=80,stream=True
        start_n = r.text.find('xplGlobal.document.metadata=')
        end_n = r.text[start_n:].find('\n')+start_n
        Info = r.text[start_n:end_n]
        citationCount = Info.split('"citationCountPaper":')[1].split(',')[0]
        papername = Info.split('"formulaStrippedArticleTitle":"')[1].split('"')[0]
        publicationDate = Info.split('"publicationDate":"')[1].split('"')[0]
        firstauthor = Info.split('"authors":[{"name":"')[1].split('"')[0]
        conferenceOrJounal = Info.split('"publicationTitle":"')[1].split('"')[0]
        return citationCount, papername, publicationDate, firstauthor, conferenceOrJounal


def DownOneFile(srcUrl, localFile):
    startTime = time.time()
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36','Accept-Encoding': 'gzip, deflate'}
    with requests.get(srcUrl, stream=True, headers=headers, proxies=proxies) as r:  # timeout=80,stream=True
    # with requests.get(srcUrl, stream=True, headers=headers, proxies=proxies) as r:  # timeout=80,stream=True

        downSize = 0
        with open(localFile, 'wb') as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
                downSize += len(chunk)
                line = '\r%d KB/s - %.2f MB， 共 %.2f MB'
                line = line % (downSize / 1024 / (time.time() - startTime), downSize / 1024 / 1024, 0 / 1024 / 1024)
                print(line,end='')
        timeCost = time.time() - startTime
        line = ' 共耗时: %.2f s, 平均速度: %.2f KB/s'
        line = line % (timeCost, downSize / 1024 / timeCost)
        print(line)
        return downSize