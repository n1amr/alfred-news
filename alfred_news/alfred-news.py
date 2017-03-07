from alfred.modules.api.a_base_module import ABaseModule
from alfred.modules.api.a_heading import AHeading
from .news import News


class AlfredNews(ABaseModule):
    def callback(self):
        pass

    def construct_view(self):
        h1 = AHeading(1, "News module")
        news = News('hello world')
        h2 = AHeading(2, news.title)

        self.add_component(h1)
        self.add_component(h2)

