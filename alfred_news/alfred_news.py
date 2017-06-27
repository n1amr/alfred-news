import feedparser
from alfred.modules.api.a_base_model import ABaseModel
from alfred.modules.api.a_base_module import ABaseModule
from alfred.modules.api.view_components.a_heading import AHeading
import alfred.modules.api.a_module_globals as amg

from .db import make_session
from .models import Source, create_new_database

from alfred.modules.api.view_components.a_divider import ADivider
from alfred.modules.api.view_components.a_pagination import APagination
from alfred.modules.api.view_components.a_list import AList
from alfred.modules.api.view_components.a_unordered_list import AUnorderedList
from alfred.modules.api.view_components.a_href import AHref
from alfred.modules.api.view_components.a_icon import AIcon
from alfred.modules.api.view_components.a_script import AScript
from alfred.modules.api.view_components.a_paragraph import AParagraph
from alfred.modules.api.view_components.a_image import AImage
from alfred.modules.api.view_components.a_badges_collapsibles import ABadgesCollapsibles
import os
from .db import ROOT_PATH

# TODO should be called if no databes exists
# create_new_database()


class BaseModel(ABaseModel):
    pass


class Article(BaseModel):
    def __init__(self, title, summary, date, url, image):
        super().__init__()
        self.title = title
        self.summary = summary
        self.date = date
        self.url = url
        self.image = image



class AlfredNews(ABaseModule):
    def callback(self):
        pass

    def construct_view(self):
        import dataset
        BaseModel.database = dataset.connect(
            'sqlite:///{path}'.format(path=amg.module_db_path))
        h1 = AHeading(1, "News module")
        badges_js = AScript(src= ROOT_PATH + "/resources/a_badges_collapsibles.js")
        jquery_source = AScript(src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js")
        line_divider = ADivider()

        self.add_component(h1)
        self.add_component(line_divider)
        self.add_component(jquery_source)

        try:
            fetch_articles()
        except:
            pass

        articles = Article.all()
        news_list = []
        for article in articles:
            html_title = AHeading(6,article.title) ##Title_header
            html_title.attrs['style'] = "color:black; display: inline-block;"
            html_title.attrs['class'] = "collapsible-header-value"


            html_image = AImage(html_attributes={"src":article.image, "style":"display:block;max-width:350px;max-height:350px;width: auto;height: auto;"})
            html_summary = AParagraph(article.summary)
            html_date = AParagraph(article.date)
            html_link = AHref(url=url, link="Read")

            html_div = AParagraph() ##News_body
            html_div.add_to_content(html_image)
            html_div.add_to_content(html_summary)
            html_div.add_to_content(html_date)
            html_div.add_to_content(html_link)

            news_list.append({'header':{'value':html_title},'body':{'value':html_div}})

        self.add_component(ABadgesCollapsibles(news_list))
        self.add_component(badges_js)


def fetch_articles():
    session = make_session()
    all_sources = session.query(Source).all()
    for source in all_sources:
        print(f'Getting feeds from {source.url}')
        feed = feedparser.parse(source.url)
        if 'bozo_exception' in feed:
            print(f'ERROR: Exception while fetching from {source.url}')
            continue

        for entry in feed['entries']:
            title = entry.get('title', '')
            summary = entry.get('summary', '')
            date = entry.get('updated','')
            url = entry.get('link','')
            try:
                image = entry.get('media_content','')[0]['url'] #cnn
            except:
                try:
                    image = entry.get('media_thumbnail','')[0]['url'] #bbc
                except:
                    image = ""

            if Article.find_by(title=title) is None:
                article = Article(title, summary, date, url, image)
                print(f'Saving article "{title}"')
                article.save()
