from alfred.modules.api.a_base_widget import ABaseWidget
from alfred.modules.api.view_components.a_paragraph import AParagraph
from alfred.modules.api.view_components.a_href import AHref
from .alfred_news import AlfredNews
import feedparser


class AlfredNewsWidget(ABaseWidget):
    def callback(self):
        feed = feedparser.parse("http://rss.cnn.com/rss/edition.rss")
        for entry in feed['entries']:
            self.title = entry.get('title', '')
            self.summary = entry.get('summary', '')
            self.date = entry.get('updated', '')
            self.url = entry.get('link', '')
            try:
                self.image = entry.get('media_content', '')[0]['url']  # CNN
            except:
                pass

            break

    def construct_view(self):
        self.title = self.title
        self.content.append(AParagraph(self.summary))
        self.content.append(AParagraph(self.date))
        # self.content.append(AParagraph(AHref(url = self.date, link = 'Read')))
        self.image_url = self.image
        self.title_on_image = False
