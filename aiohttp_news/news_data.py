import json
import pandas as pd

class NewsData():
    def __init__(self,path_to_news_json,path_to_comments_json):
        
        self.comment_df = self.__get_data_from_json(path_to_comments_json, 'comments')

        #После загрузки новости нужно еще немного доработать: убрать удаленные новости, выставить формат даты, отсортировать по дате и добавить 
        #количество комментариев. Хоть это и увеличивает первоначальное время запуска, зато позволяет быстрее обрабатывать данные для запросов
        self.news_df = self.__get_data_from_json(path_to_news_json, 'news')
        self.news_df = self.news_df.loc[self.news_df['deleted']=='False']
        self.news_df['date'] = self.news_df['date'].astype('datetime64')
        self.news_df = self.news_df.sort_values(by=['date'], ascending=False)
        self.news_df = self.__add_comments_coun()

    def __get_data_from_json(self,file_path, key):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(data[key])
        return df

    def __add_comments_coun(self):
        self.news_df['comments_count']=None
        news_id = self.news_df['id'].tolist()
        for n_id in news_id:
            count_comments = len(self.comment_df[self.comment_df['news_id']==n_id])
            self.news_df.at[self.news_df['id']==n_id, 'comments_count'] = count_comments
        return self.news_df


