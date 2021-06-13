#-*-coding:utf-8-*-
# 把一个目录下的多个word文档合并成一个word文档
# 需要安装moviepy： pip install moviepy

import os
import moviepy.video.io.ffmpeg_tools as fftool
from moviepy.tools import cvsecs

def add_suffix(file_name, suffix): # 文件名拼接后缀
    index = file_name.rfind('.') # 最后一个点号
    res = file_name[:index] + '_' + suffix + file_name[index:]
    return res

# 输入
file_name = r"./泰坦尼克号.mkv"
output_arr = [
    ('04:20','05:07', '片头'),
    ('05:07','07:47', '船头经典拥抱'),
    ('07:45','10:46', 'jack给rose画画'),
]

if not os.path.isfile(file_name): # 校验
    print("不合法的输入", file_name)

for startStr, endStr, suffix in output_arr:
    start = cvsecs(startStr)
    end = cvsecs(endStr)
    
    if start < 0 or start >= end: # 校验
        print("不合法的时间",startStr, endStr)
        continue

    full_output_name = add_suffix(file_name, suffix)
    print('处理文件：', file_name, '时间：', startStr, '-', endStr)
    fftool.ffmpeg_extract_subclip(file_name,start,end,full_output_name) # 剪辑并输出
    print('处理功成功，输出：',full_output_name)


