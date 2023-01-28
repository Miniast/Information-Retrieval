import glob
import os.path

import jieba
from collections import Counter

words_freq = {}
words_index = {}
global_news = []


def word_segmention():
    fstopwords = open('./cn_stopwords.txt', 'r', encoding='utf-8')
    stopwords = fstopwords.read()
    fstopwords.close()
    news_set = glob.glob('../data/data_content/*.txt')
    for index in range(len(news_set)):
        fnews = open(os.path.join('../data/data_content', str(index + 1) + '.txt'), 'r', encoding='utf-8')
        news = fnews.read()
        fnews.close()
        pre_news_words = jieba.lcut_for_search(news)
        news_words = []
        for words in pre_news_words:
            if words not in stopwords:
                news_words.append(words)
        words_dict = dict(Counter(news_words))
        for word, value in words_dict.items():
            if word in words_freq:
                words_freq[word] += 1
                words_index[word].append(index)
            else:
                words_freq[word] = 1
                words_index[word] = [index]
        fnewsurl = open(os.path.join('../data/data_url', str(index + 1) + '.txt'), 'r', encoding='utf-8')
        now_url = fnewsurl.read()
        fnewsurl.close()
        global_news.append({
            'title': news[0:news.find('\n')],
            'url': now_url,
            'words': words_dict
        })
    fdata = open("../data/global_data.txt", 'w', encoding='utf-8')
    fdata.write(str(words_freq) + '\n' + str(words_index) + '\n' + str(global_news) + '\n')


if __name__ == '__main__':
    print('debug mode:')
    word_segmention()
