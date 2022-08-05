import os

path = '歌词/'
useful_info = ['男：', '女：', '合：', '苏：', '鲁：', '方：', '苏醒：', '戴娆：', '陆虎：', '张远：', '虎：', '远：', '醒：', '三人']

# 更改内容，将词：曲：等信息替换成""
def alter_content(filename):
    with open(path + filename, 'r', encoding='utf-8') as f1, open(path + '改/' + filename, 'w', encoding='utf-8') as f2:
        for line in f1.readlines():
            if '：' in line:
                for i in useful_info:
                    if i in line:
                        line = line.replace(i, '')
                        f2.write(line)
                    else:
                        need_replace = True
                # 如果这句话里有：，且不是由人名、男、女带来的：，就需要删掉这句话
                if need_replace:
                    line = ""
                    f2.write(line)
            if ' - ' not in line:
                f2.write(line)
    print('歌曲： ' + filename[:-4] + " 完成了")


# 逐个读取文件，然后删掉无关内容。得到新的文件
def main():
    file_list = os.listdir(path)
    file_list.sort()
    for filename in file_list:
        if '.txt' in filename:
            alter_content(filename)
    print('所有歌的歌词都清理好了')


if __name__ == '__main__':
    main()