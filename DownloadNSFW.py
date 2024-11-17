import os
import json
import requests
import time

def Mkdir(path): # path是指定文件夹路径
    if os.path.isdir(path):
        # print('文件夹已存在')
        pass
    else:
        os.makedirs(path)

def process_json_files():
    totalcount = okcount = errcount = 0 #初始化计数器
    headers = {
        #根据情况调整
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
    }
    # 遍历 data 文件夹中的所有 json 文件，来源：https://github.com/Mabbs/pixiv-index/tree/main/data
    for file in os.listdir(data_folder):
        if file.endswith('.json'):
            file_path = os.path.join(data_folder, file)
            # 打开并读取 json 文件
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    totalcount = totalcount + 1
                    data = json.load(f)
                    url = data['url'] #获得 json 中的url
                    picurl = pixivimgrp + url #拼合图片路径
                    print(f"{[time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())]}[第{totalcount}个 json 文件]获取到图片地址：{picurl}")
                except json.JSONDecodeError as e:
                    print(f"无法解析 {file}: {e}")
            # 读取响应
            response = requests.get(picurl, headers=headers)
            if response.status_code == 200:
                #图片下载正确的情况
                okcount = okcount + 1
                #输出图片
                with open(os.path.join(download_folder, os.path.basename(picurl)), 'wb') as out_file:
                    out_file.write(response.content)
                print(f"{[time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())]}[第{okcount}个成功]图片下载完成。")
                os.rename(file_path, os.path.join(data_downloaded_folder, file)) #移动 json 文件
            else:
                #图片下载异常的情况
                errcount = errcount + 1
                print(f"{[time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())]}[第{errcount}个错误]图片下载失败，状态码：{response.status_code}。")
                os.rename(file_path, os.path.join(data_error_folder, file)) #移动 json 文件

if __name__ == '__main__':
    data_folder = 'data' #存放 json 文件的文件夹
    data_error_folder = 'data_error' #存放异常 json 文件的文件夹
    download_folder = 'download' #存放所下载的图片的文件夹
    data_downloaded_folder = 'data_downloaded' #存放已下载的 json 文件的文件夹
    pixivimgrp = 'https://i.yuki.sh' #此处根据情况填写反代地址
    Mkdir(data_folder)
    Mkdir(data_error_folder)
    Mkdir(download_folder)
    Mkdir(data_downloaded_folder)
    process_json_files()
