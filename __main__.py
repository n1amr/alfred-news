from alfred_news.db import make_session
import feedparser
from alfred_news.models import Source, create_new_database

create_new_database()
session = make_session()
all_sources = session.query(Source).all()
for source in all_sources:
    print(f'getting feeds from {source.url}')
    feed = feedparser.parse(source.url)
    for entry in feed['entries']:
        print(entry.get('title', ''))
        print(entry.get('summary', ''))
