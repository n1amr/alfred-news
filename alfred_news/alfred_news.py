from alfred.modules.api.a_base_module import ABaseModule
from alfred.modules.api.a_heading import AHeading
import feedparser
from .models import Source, create_new_database
from .db import make_session

create_new_database()


class AlfredNews(ABaseModule):
    def callback(self):
        pass

    def construct_view(self):
        h1 = AHeading(1, "News module")
        h2 = AHeading(2, "hello world")

        self.add_component(h1)
        self.add_component(h2)

        session = make_session()
        all_sources = session.query(Source).all()
        for source in all_sources:
            print(f'getting feeds from {source.url}')
            feed = feedparser.parse(source.url)
            for entry in feed['entries']:
                title = entry.get('title', '')
                summary = entry.get('summary', '')
                print(title)
                print(summary)
                self.add_component(AHeading(2, title))
                self.add_component(AHeading(3, summary))
