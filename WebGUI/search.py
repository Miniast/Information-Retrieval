import glob
import os
import jieba
import ast
from collections import Counter
import math

words_freq = {}
words_index = {}
global_news = []
stopwords = []


# Information retrieval using VSM
def get_weight(TF, DF):
    global global_news
    return TF * math.log(len(global_news) / DF, 10)


def cos_sim():
    pass


def load():
    fdata = open('../data/global_data.txt', 'r', encoding='utf-8')
    tmp = fdata.readline()
    global words_freq, words_index, global_news, stopwords
    words_freq = eval(tmp)
    tmp = fdata.readline()
    words_index = eval(tmp)
    tmp = fdata.readline()
    global_news = ast.literal_eval(tmp)
    fstopwords = open('../InvertedIndex/cn_stopwords.txt', 'r', encoding='utf-8')
    stopwords = fstopwords.read()
    fstopwords.close()


def search(text):
    if not global_news:
        load()
    raw_words = jieba.lcut_for_search(text)
    words = []
    for word in raw_words:
        if word not in stopwords:
            words.append(word)
    words_dict = dict(Counter(words))
    news_set = set()
    for word in words:
        news_set = news_set | set(words_index[word])
    news_list = list(news_set)
    res_list = []
    for index in news_list:
        col_top = 0.0
        col_bot1 = 0.0
        col_bot2 = 0.0
        for word, value in words_dict.items():
            now_weight = get_weight(value, words_freq[word])
            if word in global_news[index]['words']:
                col_top += now_weight * get_weight(global_news[index]['words'][word], words_freq[word])
            col_bot1 += now_weight * now_weight
        for word, value in global_news[index]['words'].items():
            now_weight = get_weight(value, words_freq[word])
            col_bot2 += now_weight * now_weight
        col_bot1 = math.sqrt(col_bot1)
        col_bot2 = math.sqrt(col_bot2)
        if col_bot1 * col_bot2 == 0:
            break
        correlation = col_top / (col_bot1 * col_bot2)
        res_list.append({
            'correlation': correlation,
            'title': global_news[index]['title'],
            'url': global_news[index]['url']
        })
    res_list = sorted(res_list, key=lambda x: x['correlation'], reverse=True)

    # existed_logs = glob.glob('./log/*.txt')
    # logs_num = len(existed_logs)
    # flog = open(os.path.join('./log', str(logs_num + 1) + '.txt'), 'w', encoding='utf-8')
    # flog.write(str(res_list))
    # flog.close()

    res_list = res_list[0:min(len(res_list), 5)]
    return res_list


if __name__ == '__main__':
    print('Debug mode:\n')
    load()
    search('唐山打人事件')
