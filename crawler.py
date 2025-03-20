import requests
import re
from bs4 import BeautifulSoup

# 读取 document.txt 中的网址
def read_urls(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()
    # 示例文本
    #text = '[三十而立，风华正茂—工高班23级开班仪式暨30周年庆](https://mp.weixin.qq.com/s?__biz=MzA4NDQ1NDM5NA==&mid=2649526243&idx=1&sn=24817f4e9af3daccfc58685dd778345f)'

    # 正则表达式
    pattern = r'\[.*?\]\((https?://[^\s]+)\)'
    # 使用正则表达式提取 URL
    urls = []
    for line in lines:
        # 查找匹配的 URL
        matches = re.findall(pattern, line.strip())
        if matches:
            urls.append(matches[0])
    return urls


# 提取网页内容并保存到文件
def extract_and_save_content(urls, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        for url in urls:
            try:
                response = requests.get(url, timeout=10)  # 设置超时时间
                if response.status_code == 200:
                    print(f"成功获取网页内容：{url}")
                    soup = BeautifulSoup(response.text, "html.parser")
                    # 提取所有段落
                    paragraphs = soup.find_all("p")
                    text_content = "\n\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                    if text_content:
                        file.write(f"URL: {url}\n")
                        file.write(text_content + "\n\n")
                        print(f"地址为 '{url}' 的内容已写入文件。")
                    else:
                        print(f"地址为 '{url}' 的网页没有提取到有效内容。")
                else:
                    print(f"获取网页内容失败，状态码：{response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"请求网页内容时出错：{e}")
urls = read_urls("document.txt")
print(len(urls))
 # 提取网页内容并保存到文件
#extract_and_save_content(urls, "knowledge_base.txt")

import requests
from bs4 import BeautifulSoup


contents = []
def extract_and_save_content1(urls):
    for url in urls:
        # 设置请求头，模拟浏览器访问
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # 发送请求
        response = requests.get(url, headers=headers)

        # 检查请求是否成功
        if response.status_code == 200:
            # 解析网页内容
            soup = BeautifulSoup(response.text, "html.parser")

            # 提取文章标题
            title = soup.find("h2", class_="rich_media_title").get_text(strip=True) if soup.find("h2", class_="rich_media_title") else "未找到标题"

            # 提取文章正文内容
            content = soup.find("div", class_="rich_media_content").get_text(strip=True) if soup.find("div", class_="rich_media_content") else "未找到正文内容"
            contents.append(content)
        else:
            print("请求失败，状态码:", response.status_code)

extract_and_save_content1(urls)

with open("knowledge_base.txt", "w") as f:
    for content in contents:
        f.write(content + "\n")