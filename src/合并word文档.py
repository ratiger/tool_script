#-*-coding:utf-8-*-
# 把一个目录下的多个word文档合并成一个word文档
# 需要 win32com

import os
import win32com.client as win32

def isValidPath(path): # 判断路径及目录是否有效
    if not os.path.exists(path):
        print('路径不存在：',path)
        return False
    if not os.path.isdir(path):
        print('不是存在的目录：',path)
        return False
    return True

def isProperFile(file_name, suffix='.docx'): # 筛选合并的word文档
    if not file_name.lower().endswith(suffix): # 通过判断是否以docx结尾来判断是否是word文档   
        return False
    if '$' in file_name: # 正在打开的文档
        return False
    # 可以做一些与具体业务相关的判断
    # ...省略
    return True
 
def get_dir_name(path): # 获取path的最后一段作为文件名
    dir_name = os.path.basename(path)
    # 根据实际业务需求，再做一些调整
    # ...省略
    return dir_name

def create_new_doc_file_path(dir_name, path, suffix='.docx'):
    new_doc_name = dir_name
    while os.path.isfile( os.path.join(path, new_doc_name + suffix) ): # 如果文件名已存在，则添加新尾巴
        new_doc_name = new_doc_name + '_new'
    new_doc_file_path = os.path.join(path, new_doc_name + suffix)
    return new_doc_file_path

def merge_words(docs_path, output_path, word):
    if not isValidPath(docs_path):
        print('invalid docs path:', docs_path)
        return
    if not isValidPath(output_path):
        print('invalid output path', output_path)
        return
    
    dir_name = get_dir_name(docs_path) # 目录名
    new_doc_file_path = create_new_doc_file_path(dir_name, output_path) # 用目录名作为文件名
    print('生成文件名：',new_doc_file_path)

    new_doc = word.Documents.Add() # 新建空白的word文档

    print('开始整理，目录：',docs_path)

    # 将word文档添加到新文档中。    
    for root, dirs, files in os.walk(docs_path): # 获取该目录下所有子目录和文件
        for i,f in enumerate(files):
            if isProperFile(f):
                doc_name = os.path.join(root,f)
                # print('处理文件:',doc_name) # 如何保证顺序？ 目前默认顺序是没有乱的，保险起见打印一下，乱了自己也知道。
                new_doc.Application.Selection.InsertFile(doc_name) # 拼接文档     
                if i < len(files):
                    new_doc.Application.Selection.InsertBreak() # 每份文档后留空白 

    
    new_doc.SaveAs(new_doc_file_path) # 保存文件并关闭
    new_doc.Close()   
    print('整理完成，输出文档:',new_doc_file_path)
    print()


# 输入
docs_path = r'E:\somedir'
output_path = r'E:\another_dir'

# 执行
word = win32.gencache.EnsureDispatch('Word.Application') # 打开word软件
word.Visible = False # 非可视化运行
merge_words(docs_path, output_path, word)
word.Quit()