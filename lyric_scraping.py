from selenium import webdriver
import pandas as pd
import time


# 打开网页
def open_url(browser, url):
    browser.get(url)
    browser.implicitly_wait(5)
    # print('已成功打开网址：'+ url)


# 在qq音乐的页面搜索歌曲,返回歌曲链接
def get_songurl(browser, name):
    base_url = 'https://y.qq.com/n/ryqq/search?w='
    song_url = base_url + name
    open_url(browser, song_url)
    url = browser.find_element_by_css_selector('li:nth-child(1) span>a').get_attribute('href')
    print(name[:-2] + ' : ' + url)
    return url, name


# 获取歌词
def get_lyric(browser, url, name):
    open_url(browser, url)
    js = "var q=document.documentElement.scrollTop=700"
    browser.execute_script(js)
    time.sleep(1)

    try:
        browser.find_element_by_css_selector(".mod_lyric .c_tx_highlight").click()  # 要点一下展开才能得到完整的歌词呢
        lyric_split = browser.find_elements_by_css_selector('#lrc_content p>span')

        with open('歌词/'+ name + '.txt', 'w', encoding='utf-8') as f:
            for ly in lyric_split:
                f.write(ly.text+'\n')
        print(name+' 的歌词已存储完毕')

    except:
        print(name + '歌词没存储到')


def main():
    # 准备数据
    df1 = pd.read_excel('qqmusic.xlsx')
    songlist = df1['name'].to_list()

    path = '/Users/suyuesu/Desktop/chromedriver'
    chromeOptions = webdriver.ChromeOptions()
    browser = webdriver.Chrome(path, options=chromeOptions)
    browser.get('https://y.qq.com/')

    temp = input("请登录qq音乐，登陆成功后输入1")
    if temp == '1':
        for name in songlist:
            song_url, song_name = get_songurl(browser, name+'苏醒')  # 加上名字一起搜索，才能准确的出现在第一的位置
            get_lyric(browser, song_url, name)


if __name__ == '__main__':
    main()