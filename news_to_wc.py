from collections import Counter

import jieba
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from imageio import imread
from wordcloud import WordCloud

url = 'http://www.bjnews.com.cn/realtime?page='


def get_news(urls):
    res = requests.get(urls)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    titles = []
    for tag in soup.find_all('li'):
        try:
            titles.append(tag.a.get_text())
        except:
            print('error')
    return titles


def write_title(titles):
    with open('news.txt', 'a', encoding='utf-8') as f:
        for title in titles:
            f.write(title)


if __name__ == '__main__':
    for page in range(1, 26):
        urls = url + str(page)
        print('正在爬第{}页'.format(page))
        titles = get_news(urls)
        write_title(titles)

    text = open('news.txt', 'r', encoding='utf-8').read()
    text_jieba = list(jieba.cut(text))
    c = Counter(text_jieba)  # 计数
    word = c.most_common(800)  # 取前500

    bg_pic = imread('src.jpg')
    wc = WordCloud(
        font_path='SimHei.ttf',  # 指定中文字体
        background_color='white',  # 设置背景颜色
        max_words=1000,  # 设置最大显示的字数
        mask=bg_pic,  # 设置背景图片
        max_font_size=200,  # 设置字体最大值
        random_state=20  # 设置多少种随机状态，即多少种配色
    )
    wc.generate_from_frequencies(dict(word))  # 生成词云

    wc.to_file('result.jpg')

    # show
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
