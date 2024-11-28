import os
import sys
import json
import requests
import time
import urllib.request
import zipfile
import shutil
from pathlib import Path

def Mkdir(path): # path是指定文件夹路径
    if os.path.isdir(path):
        # print('文件夹已存在')
        pass
    else:
        os.makedirs(path)

def update_pixiv_index():
    # 定义API URL和文件路径
    api_url = "https://api.github.com/repos/Mabbs/pixiv-index/git/refs/heads/main"
    current_sha_file = os.path.join(current_directory, 'pixiv-index-sha')
    zip_file = os.path.join(current_directory, 'main.zip')
    extract_dir = os.path.join(current_directory, 'main')
    newdata_dir = os.path.join(extract_dir, 'pixiv-index-main', 'data')
 
    # 发起GET请求获取最新的SHA
    try:
        response = requests.get(api_url,headers=headers)
        response.raise_for_status()
        data = response.json()
        latest_sha = data['object']['sha']
    except requests.RequestException as e:
        print(f"获取最新SHA时出现异常: {e}")
        return
 
    # 读取当前SHA
    try:
        with open(current_sha_file, 'r') as file:
            current_sha = file.read().strip()
    except FileNotFoundError:
        current_sha = None
 
    # 判断是否需要更新
    if latest_sha and (current_sha is None or current_sha != latest_sha):
        print(f"SHA不匹配。当前SHA: {current_sha}, 最新SHA: {latest_sha}. 下载新的主分支源码压缩包。")
 
        # 下载ZIP文件
        file_url = 'https://github.com/Mabbs/pixiv-index/archive/refs/heads/main.zip'
        full_url = proxy_url + file_url
        # 使用 requests.get 下载文件
        try:
            response = requests.get(full_url, stream=True)
            response.raise_for_status()  # 检查请求是否成功
            with open(zip_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"文件已成功下载到 {zip_file}")
        except requests.exceptions.RequestException as e:
            print(f"下载文件时发生错误: {e}")
            return
 
        # 解压ZIP文件
        if not os.path.exists(extract_dir):
            os.makedirs(extract_dir)
            
        try:
            print(f"开始解压新的主分支源码压缩包...")
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
        except zipfile.BadZipFile:
            print("解压ZIP文件时出错。")
            return
 
        # 更新数据文件
        try:
            shutil.rmtree(os.path.join(current_directory, data_folder))
            shutil.rmtree(os.path.join(current_directory, data_downloaded_folder))
            shutil.rmtree(os.path.join(current_directory, data_error_folder))
            Mkdir(data_downloaded_folder)
            Mkdir(data_error_folder)
            shutil.copytree(newdata_dir, os.path.join(current_directory, data_folder))
            print(f"成功更新数据文件。")
            shutil.rmtree(extract_dir)
        except OSError as e:
            print(f"错误: {e.filename} - {e.strerror}")
        
        # 更新SHA文件
        try:
            with open(current_sha_file, 'w') as file:
                file.write(latest_sha)
        except IOError as e:
            print(f"写SHA文件时出错: {e}")
            return
 
        # 清理下载的ZIP文件
        try:
            os.remove(zip_file)
        except OSError as e:
            print(f"移除ZIP文件时出错: {e}")
 
        print("下载与解压主分支源码压缩包完成。")
    else:
        print("SHA匹配，不需要更新。")

def process_json_files():
    totalcount = okcount = errcount = 0 #初始化计数器
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
    proxy_url = 'https://ghproxy.cc/'
    executable_path = Path(sys.argv[0]).resolve()
    current_directory = executable_path.parent
    headers = {
        #根据情况调整
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
    }
    Mkdir(data_folder)
    Mkdir(data_error_folder)
    Mkdir(download_folder)
    Mkdir(data_downloaded_folder)
    update_pixiv_index()
    process_json_files()
