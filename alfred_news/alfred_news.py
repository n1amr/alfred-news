import json
import os

import feedparser

from alfred import Logger
from alfred.modules.api.a_base_module import ABaseModule
from alfred.modules.api.view_components.a_collapsible import ACollapsible
from alfred.modules.api.view_components.a_divider import ADivider
from alfred.modules.api.view_components.a_heading import AHeading
from alfred.modules.api.view_components.a_href import AHref
from alfred.modules.api.view_components.a_image import AImage
from alfred.modules.api.view_components.a_paragraph import AParagraph
from alfred.modules.api.view_components.a_script import AScript
from .models import Article, Category, Source

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


class AlfredNews(ABaseModule):
    def callback(self):
        pass

    def initialize(self):
        settings_dict = self.settings.settings_dict
        if settings_dict.get('initialized_db', False):
            return

        initialize_db()

        settings_dict['initialized_db'] = True
        self.settings.commit()

    def construct_view(self):
        self.initialize()

        badges_js = AScript(
            src=ROOT_PATH + '/resources/a_badges_collapsibles.js')
        jquery_source = AScript(
            src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js")

        self.add_component(jquery_source)

        try:
            fetch_articles()
        except:
            pass

        articles = Article.all()
        news_list = []
        for article in articles:
            html_title = AHeading(6, article.title)  # Title_header
            html_title.attrs['style'] = "color:black; display: inline-block;"
            html_title.attrs['class'] = "collapsible-header-value"

            kwargs = {
                "style": "display:block;max-width:350px;max-height:350px;width: auto;height: auto;"}
            html_image = AImage(source=article.image, **kwargs)
            html_summary = AParagraph(article.summary)
            html_date = AParagraph(article.date)
            html_link = AHref(url=article.url, link="Read")

            html_div = AParagraph()  # News_body
            html_div.add_to_content(html_image)
            html_div.add_to_content(html_summary)
            html_div.add_to_content(html_date)
            html_div.add_to_content(html_link)

            news_list.append({'header': {'value': html_title},
                              'body': {'value': html_div}})

        self.add_component(ACollapsible(attributes=news_list))
        self.add_component(badges_js)


def initialize_db():
    Logger().info('Creating new database')
    with open(os.path.join(ROOT_PATH, 'resources', 'sample_data.json'),
              'r') as f:
        sample_data = json.loads(f.read())

    for category, sources in sample_data.items():
        category_obj = Category(name=category)
        category_obj.save()
        for source_name, source_url in sources:
            source_obj = Source(source_name, source_url,
                                category_obj.id)
            source_obj.save()


def fetch_articles():
    Logger().info('fetch_articles()')
    for source in Source.all():
        Logger().info('Getting feeds from {url}'.format(url=source.url))
        feed = feedparser.parse(source.url)

        if 'bozo_exception' in feed:
            Logger().err(
                'bozo_exception while fetching from {url}'.format(
                    url=source.url))

        for entry in feed['entries']:
            title = entry.get('title', '')
            summary = entry.get('summary', '')
            date = entry.get('updated', '')
            url = entry.get('link', '')
            image = ''
            if 'media_content' in entry and len(entry['media_content']) > 0:
                image = entry['media_content'][0]['url']
            elif 'media_thumbnail' in entry and len(
                    entry['media_thumbnail']) > 0:
                image = entry['media_thumbnail'][0]['url']

            if not Article.find_by(title=title):
                article = Article(title, summary, date, url, image)
                Logger().info('Saving article "{title}"'.format(title=title))
                article.save()
