import requests
import os


def get_and_save_image(url, name):
    response = requests.get(url)
    with open(f'./assets/images/article/{name}', 'wb') as file:
        file.write(response.content)


def replace_cdn_image():
    # 遍历 ./content/english 目录下的文件夹
    for root, _, files in os.walk('./content/english'):
        for file in files:
            if file.endswith('.md'):
                is_need_replace = False
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 匹配图片链接
                    for line in content.split('\n'):
                        if 'https://cdn.nlark.com/yuque' in line:
                            print(line)
                            is_need_replace = True
                            if line.startswith('image:'):
                                image_url = line.split('image: ')[1].split('"')[1].split('#')[0]
                            else:
                                image_url = line.split('](')[1].split(')')[0].split('#')[0]
                            name = image_url.split('/')[-1].split('#')[0]
                            get_and_save_image(image_url, name)
                            content = content.replace(image_url, f'/images/article/{name}')
                if is_need_replace:
                    with open(os.path.join(root, file), 'w', encoding='utf-8') as f:
                        f.write(content)

if __name__ == '__main__':
    replace_cdn_image()
