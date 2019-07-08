import datetime
import sys
sys.path.append('/home/gex/git/projects/aiohttp_news')
import main_v2
import os
import json

class DataChecker():
    #Проверка файлов с новостями и комментариям и пути до них на корректность
    def is_exist(self, path):
        assert os.path.exists(path), 'File does not exist'

    def is_correct_news(self, path):
        #должны присутствовать все поля и поле date должно быть корректного формата
        with open(path, 'r', encoding='utf-8') as f:
            data = dict(json.load(f))
        checked_fields = set()
        checked_fields.update(['id','title','date','body','deleted'])
        for news in data['news']:
            assert set(news.keys()) == checked_fields, 'not all fields in %s'%(news)
            try:
                datetime.datetime.fromisoformat(news['date'])
            except ValueError:
                raise ValueError('date in %s not correct'%(news))

    def is_correct_comments(self, path):
        #должны присутствовать все поля и поле date должно быть корректного формата
        with open(path, 'r', encoding='utf-8') as f:
            data = dict(json.load(f))
        checked_fields = set()
        checked_fields.update(['id','news_id','date','title','comment'])
        for comment in data['comments']:
            assert set(comment.keys()) == checked_fields, '%s not all fields'%(comment)
            try:
                datetime.datetime.fromisoformat(comment['date'])
            except ValueError:
                raise ValueError('date in %s not correct'%(comment))

class PandasChecker():
    def __init__(self,path_to_news, path_to_comments):
        #Проверка формирования кэша из которого берутся данные для запросов
        self.storage = main_v2.NewsData(path_to_news, path_to_comments)

    def is_correct_dataframe_forming_news(self):
        actual_news = self.storage.get_actual_news()
        #Количество новостей должно совпадать с заранее известным для тестовых данных и с написанным в формируемом файле
        assert len(actual_news['news'])==7, 'Количество новостей %s Не совпадает с ожидаемым (7) '%(actual_news['news'])
        assert len(actual_news['news'])==int(actual_news['news_count']), 'Количество новостей %s не совпадает с news_count '%(actual_news['news'])
        #Даты должны идти по возрастанию
        dates = []
        for news in actual_news['news']:
            date =  datetime.datetime.fromisoformat(news['date'])
            dates.append(date)
        start = 0
        end = 1
        started = True
        while end <= len(dates)-1:
            #на данный момент дата должна уже наступить
            if started:
                assert dates[start] <= datetime.datetime.today(), 'Новость с неправильной датой'
                started = False
            assert dates[start] >= dates[end], 'Новости неправильно сортированы %s'%(dates)
            assert dates[end] <= datetime.datetime.today(), 'Новость с неправильной датой'
            start += 1
            end += 1

    def is_correct_dataframe_forming_comments(self):
        news_comment = self.storage.get_news_with_comments(1)
        #Количество комментариев должно совпадать с заранее известным для тестовых данных и с написанным в формируемом файле
        assert len(news_comment['comments'])==4, 'Количество комментариев %s Не совпадает с ожидаемым (4) '%(news_comment['comments'])
        assert len(news_comment['comments'])==int(news_comment['comments_count']), 'Количество комментариев %s не совпадает с comments_count '%(news_comment['comments'])
        #Даты должны идти по возрастанию 
        dates = []
        for news in news_comment['comments']:
            date =  datetime.datetime.fromisoformat(news['date'])
            date =  datetime.datetime.fromisoformat(news['date'])
        start = 0
        end = 1
        started = True
        while end <= len(dates)-1:
            #на данный момент дата должна уже наступить
            if started:
                assert dates[start] <= datetime.datetime.today(), 'Коммент с неправильной датой'
                started = False
            assert dates[start] >= dates[end], 'Комменты неправильно сортированы'
            assert dates[end] <= datetime.datetime.today(), 'Коммент с неправильной датой'
            start += 1
            end += 1



#Проверка текущих данных на корректность
path_to_news = '/home/gex/git/projects/aiohttp_news/news.json'
path_to_comments = '/home/gex/git/projects/aiohttp_news/comments.json'
try:
    data_checker = DataChecker()
    data_checker.is_exist(path_to_news)
    data_checker.is_exist(path_to_comments)
    data_checker.is_correct_news(path_to_news)
    data_checker.is_correct_comments(path_to_comments)
except AssertionError as exc:
    print(exc)   
except ValueError as exc:
    print(exc)   
#Проверка обработки данных пандасом, проводится на тестовых данных
path_to_test_news = '/home/gex/git/projects/aiohttp_news/test_news.json'
path_to_test_comments = '/home/gex/git/projects/aiohttp_news/test_comments.json'

try:
    test_storage = PandasChecker(path_to_test_news, path_to_test_comments)
    test_storage.is_correct_dataframe_forming_news()
    test_storage.is_correct_dataframe_forming_comments()
except AssertionError as exc:
    print(exc)   
