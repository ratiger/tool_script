#-*-coding:utf-8-*-
# 删除某目录下所有文件名中含有的特定字段（广告字段）

import os

path = r'E:\somedir'
pattern = '请添加ad888'
cnt = 0

print('开始整理，在目录：',path,'中，修改文件名中含有：',pattern,'的项。')

for root, dirs, files in os.walk(path): # 获取该目录下所有子目录和文件
    for file_name in files:        
        if pattern not in file_name:
            continue
        old_name = os.path.join(root, file_name)
        new_name = old_name.replace(pattern, '')
        os.rename(old_name , new_name)
        cnt = cnt + 1

print('整理完成，总删除',cnt,'项。')