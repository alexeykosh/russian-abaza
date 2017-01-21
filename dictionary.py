import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def get_urls():
    urls = []
    alph = ['А','Б', 'В', 'Г', 'Гв', 'Гъ', 'Гъв', 'Гъь', 'Гь', 'ГI', 'ГIв', 'Д', 'Дж', 'Джв', 'Джь', 'Дз', 'Е', 'Ё', 'Ж',
            'Жв', 'Жь', 'З', 'И', 'Й', 'К', 'Кв', 'Къ', 'Къв', 'Къь', 'Кь', 'КI', 'КIв', 'КIь', 'Л', 'Ль', 'М', 'Н',
            'О', 'П', 'ПI', 'Р', 'С',  'Т',  'Тл', 'Тш', 'ТI', 'У',  'Ф', 'Х', 'Хв', 'Хъ', 'Хъв', 'Хь', 'ХI', 'ХIв',
            'Ц', 'ЦI', 'Ч', 'Чв', 'ЧI', 'ЧIв' ,'Ш', 'Шв', 'ШI', 'Щ', 'Ъ', 'Э', 'Ю', 'Я']
    for item in alph:
        url = "http://www.abazinka.ru/ru/letter/%s?" % item
        urls.append(url)
    return urls


def extract_words(urls):
    russian_words = []
    russian_words2 = []
    for url in urls:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                                 '/39.0.2171.95 Safari/537.36'}
        soup_url = requests.get(url, headers=headers)
        soup = BeautifulSoup(soup_url.text, 'lxml')
        for russian_word in soup.select('.st_rw'):
            russian_words.append(russian_word.text)
    for word in russian_words:
        word = re.sub(',|;', ',', word)
        word = word.split(',')
        russian_words2.append(word)

    flattened = [val for sublist in russian_words2 for val in sublist]
    clean_list = list(filter(None, flattened))
    return clean_list


def making_urls(urls2):
    ok_values = []
    urls_list = []
    keys = []
    values = []
    for word in urls2:
        if word.isalpha():
            keys.append(word)
            word = word.replace(' ', '')
            url = 'http://abazinka.ru/translation?dictionary=all&direction=ru2ab&word=%s' %word
            urls_list.append(url)
        else:
            pass
    for url in urls_list:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                                 '/39.0.2171.95 Safari/537.36'}
        soup_url = requests.get(url, headers=headers)
        soup = BeautifulSoup(soup_url.text, 'lxml')
        for value in soup.select('.result'):
            values.append(value.text)
    for element in values:
        element = re.sub('([1-9][1-9]?(.|\)))', '\n \\1', element)
        element = re.sub('.+ .\. .\.', '', element)
        ok_values.append(element)
    d = {"normalized": keys, "meaning": ok_values}
    s = pd.DataFrame(d, columns=["normalized", "meaning"])
    file = open('russian_abaza.csv', 'w')
    s = s.drop_duplicates()
    s.to_csv(file, encoding='Windows-1251')
    file.close()
    print(len(keys), len(ok_values))
    print(s)


def main():
    urls = get_urls()
    urls2 = extract_words(urls)
    making_urls(urls2)

if __name__ == '__main__':
    main()