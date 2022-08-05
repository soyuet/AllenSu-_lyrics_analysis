import jieba
import os
import re
import pandas as pd
import numpy as np
from collections import Counter
import wordcloud
from PIL import Image

path = '歌词/'
pattern = re.compile("[a-zA-Z\d\s\n\'\)\(\,\’\.\《\》]")
useless_info = ['\n', '\'', '\)', '\(', '\,', '\’', '\.', '\《', '\》', ' ']


# 得到file_list，即歌词的文件，返回文件名列表
def get_file_list():
    file_list = os.listdir(path)
    for filename in file_list:
        if '.txt' not in filename:
            file_list.remove(filename)
    file_list.sort()
    return file_list

# 返回原创歌曲的file_list
def get_original_lyric_list():
    df1 = pd.read_excel('original_table.xlsx')
    song_list = df1[df1['词原创'] == 1]['歌曲名称'].tolist()
    file_list =[]
    for song in song_list:
        file_list.append(song+'.txt')
    return file_list


# 第一个时期的file_list
def get_first_lyric_list():
    df1 = pd.read_excel('original_table.xlsx')
    song_list = df1[df1['发表时间'] < 2014]['歌曲名称'].tolist()
    file_list = []
    for song in song_list:
        file_list.append(song+'.txt')
    return file_list


# 第二个时期的file_list（以2018作为分割）
def get_second_lyric_list():
    df1 = pd.read_excel('original_table.xlsx')
    song_list = df1[(df1['发表时间'] >= 2014) & (df1['发表时间'] < 2018)]['歌曲名称'].tolist()
    file_list = []
    for song in song_list:
        file_list.append(song+'.txt')
    return file_list


# 第三个时期的file_list
def get_third_lyric_list():
    df1 = pd.read_excel('original_table.xlsx')
    song_list = df1[(df1['发表时间'] >= 2018)]['歌曲名称'].tolist()
    file_list = []
    for song in song_list:
        file_list.append(song+'.txt')
    return file_list


# 返回rap的file_list
def get_hiphop_lyric_list():
    df1 = pd.read_excel('original_table.xlsx')
    song_list = df1[df1['说唱'] == 1]['歌曲名称'].tolist()
    file_list =[]
    for song in song_list:
        file_list.append(song+'.txt')
    return file_list


# 分词, 返回所有分词的列表（删去了\n、空格、标点符号等）
def split_word(filename):
    one_song = []
    with open(path + filename, 'r', encoding='utf-8') as f1:
        for line in f1.readlines():
            each_sentence = jieba.cut(line, cut_all=False)
            one_song.extend(each_sentence)
            for character in one_song:
                for each in useless_info:
                    if each in character:
                        one_song.remove(character)
    return one_song


# 返回中文歌词长度和处理后的中文文本
def count_chinese_word():
    all_word = ""
    file_list = get_file_list()
    for filename in file_list:
        with open(path + filename, 'r', encoding='utf8') as f1:
            all_word = all_word + re.sub(pattern, '', f1.read())
    return len(all_word), all_word


# 返回英文歌词长度和处理后的英文文本
def count_english_word():
    all_word = []
    file_list = get_file_list()
    for filename in file_list:
        for word in split_word(filename):
            if re.match('[a-zA-Z]', word):
                all_word.append(word)
    return len(all_word), all_word


# 计算总字数
def count_words():
    number = count_chinese_word()[0] + count_english_word()[0]
    return number


# 计算所选文档的词频
def all_word_frequency(file_list):
    all_words = []
    if len(file_list) > 1:
        for filename in file_list:
            try:
                with open(path + filename, 'r', encoding='utf8') as f1:
                    all_words.extend(split_word(filename))
            except:
                continue
    else:
        with open(path + file_list, 'r', encoding='utf8') as f1:
            all_words.extend(split_word(file_list))
    frequency = Counter(all_words)
    return frequency, all_words


# 删掉stopwords之后的词频
def words_frequency_clean(file_list):
    stop_words = []
    clean_words = []
    with open('stopword_china.txt', 'r', encoding='utf-8') as f1, open('stopword_english.txt', 'r', encoding='utf-8')as f2:
        temp = (f1.readlines())
        temp.extend(f2.readlines())
    for i in temp:
        stop_words.append(i.replace('\n', ''))
    all_word = all_word_frequency(file_list)[1]
    for word in all_word:
        word2 = word.lower()
        if word2 not in stop_words:
            clean_words.append(word)
    frequency = Counter(clean_words)
    return frequency, clean_words


def original_lyric_frequency():
    return words_frequency_clean(get_original_lyric_list())[0]


# 生成词云
def generate_wordcloud(text, up_photo, word_cloud_name):
    img = Image.open(up_photo)
    mask = np.array(img)
    w = wordcloud.WordCloud(width=600, height=400, font_path='SimHei.ttf', font_step=3, mask=mask, background_color='white', collocations=False)
    w.generate(text)
    w.to_file(word_cloud_name+'.png')
    print('已生成词云')


# 所有歌曲的发布频率
def get_publish_frequency():
    df1 = pd.read_excel('original_table.xlsx')
    song_list = []
    time_list =[]
    file_list = get_file_list()
    for i in file_list:
        song = i.replace('.txt', '')
        song_list.append(song)
    for i in song_list:
        year = int(df1[df1['歌曲名称'] == i]['发表时间'].tolist()[0])
        time_list.append(year)
    return dict(Counter(time_list))


# 原创歌曲的发布频率
def get_original_publish_frequency():
    df1 = pd.read_excel('original_table.xlsx')
    song_list = []
    time_list =[]
    file_list = get_original_lyric_list()
    for i in file_list:
        song = i.replace('.txt', '')
        song_list.append(song)
    for i in song_list:
        year = int(df1[df1['歌曲名称'] == i]['发表时间'].tolist()[0])
        time_list.append(year)
    return dict(Counter(time_list))


def inquiry_function():
    temp = int(input("""
    请输入你需要的功能:
    1. 查询歌词的字数
    2. 获取所有歌曲的词频
    3. 获取原创歌曲的词频
    4. 获取初期（2007-2012）的词频
    5. 获取中期（2014-2018）的词频
    6. 获取近期（2018-2022）的词频
    """))
    if temp == 1:
        q2 = int(input("""
        请问你具体要什么字数？
        1. 所有歌词的字数
        2. 中文字数
        3. 英文字数
        """))
        if q2 == 1:
            print(count_words())
        elif q2 == 2:
            print(count_chinese_word()[0])
        elif q2 == 3:
            print(count_english_word()[0])
        else:
            print("输入错误")
    elif temp == 2:
        print(words_frequency_clean())
    elif temp == 3:
        print(original_lyric_frequency())
    elif temp == 4:
        print(words_frequency_clean(get_first_lyric_list()))
    elif temp == 5:
        print(words_frequency_clean(get_second_lyric_list()))
    elif temp == 6:
        print(words_frequency_clean(get_third_lyric_list()))
    else:
        print('输入错误')


def main():
    # file_list = get_third_lyric_list()
    # word_list = words_frequency_clean(file_list)[1]
    # new_text = ' '.join(word_list)
    # generate_wordcloud(new_text, '2022allen.jpg', 'woldcloud2022-2')

    # frequency = words_frequency_clean(file_list)[0]
    # print(frequency)

   inquiry_function()





if __name__ == "__main__":
    main()

