import feedparser
from alfred.modules.api.a_base_model import ABaseModel
from alfred.modules.api.a_base_module import ABaseModule
from alfred.modules.api.view_components.a_heading import AHeading
import alfred.modules.api.a_module_globals as amg

from .db import make_session
from .models import Source, create_new_database


# TODO should be called if no databes exists
# create_new_database()


class BaseModel(ABaseModel):
    pass


class Article(BaseModel):
    def __init__(self, title, body):
        super().__init__()
        self.title = title
        self.body = body


class AlfredNews(ABaseModule):
    def callback(self):
        pass

    def construct_view(self):
        h1 = AHeading(1, "News module")
        self.add_component(h1)

        try:
            fetch_articles()
        except:
            pass

        articles = Article.all()
        for article in articles:
            self.add_component(AHeading(2, article.title))
            self.add_component(AHeading(3, article.body))


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
            body = entry.get('summary', '')

            if Article.find_by(title=title) is None:
                article = Article(title, body)
                print(f'Saving article "{title}"')
                article.save()
