import pandas as pd
import datetime
from aiohttp import web
import json

class NewsData():
    def __init__(self,path_to_news_json,path_to_comments_json):
        self.__comments_df = self.__generate_comments_dataframe(path_to_comments_json)
        self.__news_df = self.__generate_news_dataframe(path_to_news_json)

    def get_news_with_comments(self, news_id):
        #поскольку новость может выйти в промежутке между запросами, актуальность новостей по дате проверяется в момент запроса
        #Дата сейчас возвращается в формате "%Y-%m-%d %H-%M%-%S" Если необходимо в качестве разделителя использовать именно "Т", то можно откомментить код
        actual_news = self.__news_df[self.__news_df['date'] < datetime.datetime.now()].copy()
        actual_news['date'] = actual_news['date'].map(lambda x: datetime.datetime.strftime(x, '%Y-%m-%dT%H:%M:%S'))
        if news_id in set(actual_news.id.tolist()):
            comments = self.__comments_df[(self.__comments_df['news_id']==news_id)&(self.__comments_df['date'] < datetime.datetime.now())].copy()            
            actual_news = actual_news[actual_news['id']==news_id]
            result = actual_news.to_dict('records')[0]
            comments['date'] = comments['date'].map(lambda x: datetime.datetime.strftime(x, '%Y-%m-%dT%H:%M:%S'))
            result['comments'] = comments.to_dict('records') 
            result['comments_count'] = len(comments)
            return result
        return {}

    def get_actual_news(self):
        #поскольку новость может выйти в промежутке между запросами, актуальность новостей по дате проверяется в момент запроса
        #Дата сейчас возвращается в формате "%Y-%m-%d %H-%M%-%S" Если необходимо в качестве разделителя использовать именно "Т", то можно откомментить код
        actual_news = self.__news_df[self.__news_df['date'] < datetime.datetime.now()].copy()
        actual_news['date'] = actual_news['date'].map(lambda x: datetime.datetime.strftime(x, '%Y-%m-%dT%H:%M:%S'))
        actual_news['date'] = actual_news['date'].astype('str')
        result = {'news': actual_news.to_dict('records'),
        'news_count':len(actual_news) }
        return result

    def __generate_comments_dataframe(self, path_to_comments_json):
        df = self.__get_dataframe_from_json(path_to_comments_json, 'comments')
        #оставшиеся новости сортируются по дате
        df['date'] = df['date'].astype('datetime64')
        df = df.sort_values(by=['date'], ascending=False)
        return df

    def __generate_news_dataframe(self, path_to_news_json):
        df = self.__get_dataframe_from_json(path_to_news_json, 'news')
        #Из полученных из файла данных необходимо убрать удаленные новости. 
        df = df[df['deleted']=='False']
        #оставшиеся новости сортируются по дате
        df['date'] = df['date'].astype('datetime64')
        df = df.sort_values(by=['date'], ascending=False)
        return df

    def __add_comments_count(self, df):
        #Подсчет количества комментов для каждой новости
        df['comments_count']=None
        news_id = df['id'].tolist()
        for n_id in news_id:
            count_comments = len(self.__comments_df[self.__comments_df['news_id']==n_id &(self.__comments_df['date'] < datetime.datetime.now())])
            df.at[df['id']==n_id, 'comments_count'] = count_comments
        return df

    def __get_dataframe_from_json(self,file_path, key):
        #Метод получает данные из файла и преобразовывает их в датафрейм 
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(data[key])
        return df

class NewsApi():
    def __init__(self, storage):
        self.data = storage
        self.app = web.Application()
        self.app.router.add_get('/', self.get_news)
        self.app.router.add_get('/news/{id}', self.get_news_with_comments)
    
    async def get_news(self, request):
        response_obj = self.data.get_actual_news()
        return web.Response(text=json.dumps(response_obj),status=200)

    async def get_news_with_comments(self, request):
        news_id = int(request.match_info['id'])
        response_obj = self.data.get_news_with_comments(news_id)
        if response_obj: 
            return web.Response(text=json.dumps(response_obj),status=200)
        return web.Response(text='404',status=404)


path_to_news = '/home/gex/git/projects/aiohttp_news/news.json'
path_to_comments = '/home/gex/git/projects/aiohttp_news/comments.json'
storage = NewsData(path_to_news, path_to_comments)
api = NewsApi(storage)
web.run_app(api.app)
