#-*-coding:utf-8-*-
# 统计某文件夹下的音视频文件的总时长 只考虑了很少的异常情况
# 需要安装 cv2和mutagen

import cv2
import os
from mutagen.mp3 import MP3

def get_video_duration(file_name): # 获取视频时长
    cap = cv2.VideoCapture(file_name)
    if cap.isOpened():
        rate = cap.get(5) # 获取帧率
        frame_num = cap.get(7) # 获取帧数
        duration = frame_num/rate
        return duration
    return -1

def get_audio_duration(file_name: str): # 获取音频时长
    if not file_name.endswith('.mp3'):
        return 0
    audio = MP3(file_name)
    return audio.info.length

def beautify_duration(duration): # 美化输出时间
    duration = int(duration) # 把浮点数变为整数
    seconds = duration % 60
    duration = duration // 60
    minutes = duration % 60
    duration = duration // 60
    hours = duration
    res = "{:0>2d}:{:0>2d}".format(minutes,seconds)
    if hours != 0:
        res = "{:0>2d}:{:0>2d}:{:0>2d}".format(hours,minutes,seconds)
    return res

def get_all_files(dir): # 获取所有文件
    if not os.path.isdir(dir):
        print("不是有效路径:",dir)
        return False
    for root, dirs, files in os.walk(dir):
        return True, root, dirs, files

def isAudioOrVideo(file_name):
    file_type = file_name.split('.')[-1]
    support_types = set(['mp4','mp3'])
    return file_type in support_types

def get_total_time(dir, is_video=True): # 目前尚未能识别非音视频类型文件
    ok, root, _, files = get_all_files(dir)
    if not ok:
        return 
    totoal_duration = 0
    for name in files:
        if not isAudioOrVideo(name):
            continue
        full_name = os.path.join(root,name)
        duration = get_video_duration(full_name) if is_video else get_audio_duration(full_name)
        duration = int(duration)
        totoal_duration += duration
    return totoal_duration

def getAllSubDirs(root): # 获取一个目录下的所有子文件夹
    ok, root, dirs, _ = get_all_files(root)
    if not ok:
        return 
    res = [os.path.join(root,name) for name in dirs]
    return res

root = r"D:\somedir"
dirs = getAllSubDirs(root)
res = [(dir,beautify_duration(get_total_time(dir))) for dir in dirs]
for dir, duration in res:
    print(dir,'总时长：', duration)


