from bs4 import BeautifulSoup
import datetime
import requests,re, os, urllib.request

class NasaArchiveParser:
    def __init__(self, url, first_url_part, directory, days_ago = 365):
        self.url_for_pars = url
        self.first_url_part = first_url_part
        self.path_to_dir = directory
        self.parse_from_date = datetime.datetime.today() - datetime.timedelta(days=days_ago)

    def get_links_from_archive(self):
        response = requests.get(self.url_for_pars)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            text_with_date_and_urls = str(soup.b).split('<br/>')

            article_urls = {}
            for date_url in text_with_date_and_urls:
                article_date = re.search('.* <a href="', date_url).group()
                article_date = re.sub(r'\W', ' ', article_date)
                date_year = re.search(r'\d{4}', article_date).group()
                date_day = re.search(r'\s\d{1,2}\s', article_date).group()
                date_month = re.search(r'[a-zA-Z]+', article_date).group()
                article_date = date_year + date_month + date_day
                article_date = re.sub(r'\s', '', article_date)
                article_date = datetime.datetime.strptime(article_date, '%Y%B%d')
                if article_date < self.parse_from_date:
                    return article_urls

                artile_full_url = self.first_url_part + re.search('<a href=".*"', date_url).group()[9:-1]
                article_urls[str(article_date)] = artile_full_url

            return article_urls

    def download_stuff(self, date, url):
        title_text_image = self.get_article_materials(url)
        if title_text_image:
            archive_dir = self.path_to_dir + '/nasa_archive'
            if not os.path.isdir(archive_dir):
                os.makedirs(archive_dir)
            article_dir = archive_dir + '/' + str(date)
            if not os.path.isdir(article_dir):
                os.makedirs(article_dir)

            article_fullpath = str(article_dir) +  '/' + str(title_text_image[0]) + '.txt'
            with open(article_fullpath, "w")as file:
                file.write(title_text_image[1])

            image_fullpath = article_dir + '/' + 'Picture of the Day'
            urllib.request.urlretrieve(title_text_image[2], image_fullpath)

    def get_article_materials(self,url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.p.find('a', attrs={'href': re.compile('.*image.*')}):
                image = self.first_url_part + str(soup.p.find('a', attrs={'href': re.compile('.*image.*')})['href'])
            else:
                return None

            title = soup.title.text.split('-')[1][1:-2]

            text = soup.find(text=re.compile('Explanation.*')).parent.parent.text
            garbage_before_article = re.compile('.*Explanation', re.DOTALL)
            text = re.sub(garbage_before_article, 'Explanation', text)
            technical_links = re.compile('Tomorrow.*Authors', re.DOTALL)
            text = re.sub(technical_links, 'Authors', text)
            text = re.sub('\n', ' ', text)

            return [title, text, image]


archive = 'https://apod.nasa.gov/apod/archivepix.html'
main_link_part = 'https://apod.nasa.gov/apod/'
dir = os.path.abspath(os.curdir)

parser = NasaArchiveParser(archive ,main_link_part, dir)
articles = parser.get_links_from_archive()
for date, url in articles.items():
    parser.download_stuff(date, url)