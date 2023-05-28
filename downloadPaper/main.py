import glob
from utils4paperreading import *

# 目标路径
cwd_path = r'E:\学习\阅读\面向智能反射面数能系统的波形设计\通信感知一体化'

mymkdirs(os.path.join(cwd_path, '文章备份'))
with open(cwd_path+'\\mypaper.txt', 'r') as f:
    for fline in f.readlines():
        paper_id = fline.split('/')[-1].strip('\n')
        citationCount, papername, publicationDate, firstauthor, conferenceOrJounal = \
            GetPaperInfo('https://ieeexplore.ieee.org/document/'+str(paper_id))
        filename = checkfilename((str(firstauthor)+'++'+str(citationCount)+'+'+str(papername)).replace(' ', '_'))
        DownOneFile('https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber='+str(paper_id)+'&ref=', cwd_path+'\\'+filename+'.pdf')
        for filename in glob.glob(cwd_path+'/*.pdf'):
            shutil.copy(src=os.path.join(cwd_path, filename), dst=os.path.join(cwd_path, '文章备份'))
            path_dir = filename.split('.pdf')[0].split('\\')[-1]
            mymkdirs(os.path.join(cwd_path, path_dir))
            mdinfo = [
                'Date: ' + time.strftime('%Y.%m.%d  %H:%M', time.localtime(time.time())),
                '\n',
                'Author: Joffrey LC',
                '\n',
                '\n-------------------------------------\n'
                '**'+papername+'**.  '+'*'+firstauthor+'*'+' et.al.  **'+str(conferenceOrJounal)+', '+str(publicationDate)+'**  ([pdf](https://ieeexplore.ieee.org/document/'+str(paper_id)+'))'+'  (Citations **'+str(citationCount)+'**)\n'
                '## Quick Overview\n'
            ]
            mypaperspace(os.path.join(cwd_path, path_dir), mdinfo)
# 避免重复下载，删除已下载的pdf url
with open(cwd_path+'\\mypaper.txt', 'w') as f:
    print('already finished')
# To do:
# shutil.move 移动文件名较长的文件时会发生错误，有时间的话尝试自己写一个移动文件的代码
# 没有检测是否成功下载
