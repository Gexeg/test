import datetime
import json
from random import randint, choice


all_news = []
news_count = 0
for news_id in range(1,100):
    news = {}
    news['id'] = news_id
    news['title'] = 'news_%s'%(news_id)
    news['date'] = str(datetime.datetime(randint(1970,2056),randint(1,12),randint(1,27),randint(1,23),randint(1,59),randint(1,59)).isoformat())
    news['body'] = 'the news'
    d_n = [True, False]
    news['deleted'] = str(choice(d_n))
    all_news.append(news)
    news_count +=1
data = {'news':all_news,
              'new_count':news_count}

with open('/home/gex/git/projects/aiohttp_news/news.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

all_comments = []
comments_count = 0
for comment_id in range(1,1000):
    comment = {}
    comment['id'] = comment_id
    comment['news_id'] = randint(1,news_count)
    comment['title']=f'comment_{comment_id}'
    comment['date'] = str(datetime.datetime(randint(1970,2056),randint(1,12),randint(1,27),randint(1,23),randint(1,59),randint(1,59)).isoformat())
    comment['comment'] = 'Comment'
    all_comments.append(comment)
    comments_count += 1
comment_data = {'comments':all_comments,
                'comments_count':comments_count}

with open('/home/gex/git/projects/aiohttp_news/comments.json', 'w', encoding='utf-8') as f:
    json.dump(comment_data, f, ensure_ascii=False, indent=4)

