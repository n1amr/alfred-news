from alfred.modules.api.a_base_module import ABaseModule
from alfred.modules.api.view_components.a_heading import AHeading
import feedparser
from .models import Source, create_new_database
from .db import make_session
from alfred.modules.api.view_components.a_divider import ADivider
from alfred.modules.api.view_components.a_pagination import APagination
from alfred.modules.api.view_components.a_list import AList
from alfred.modules.api.view_components.a_unordered_list import AUnorderedList
from alfred.modules.api.view_components.a_href import AHref
from alfred.modules.api.view_components.a_icon import AIcon
from alfred.modules.api.view_components.a_script import AScript
from alfred.modules.api.view_components.a_paragraph import AParagraph
from alfred.modules.api.view_components.a_image import AImage
from alfred.modules.api.view_components.a_collapsible import ACollapsible
import os
from .db import ROOT_PATH



create_new_database()


class AlfredNews(ABaseModule):
    def callback(self):
        pass

    def construct_view(self):
        h1 = AHeading(1, "News module")
        h2 = AScript(src= os.getcwd() + "/alfred/resources/js/a_pagination.js")
        h7 = AScript(src= ROOT_PATH + "/resources/a_badges_collapsibles.js")
        h3 = ADivider()


        self.add_component(h1)
        self.add_component(h3)
        self.add_component(h2)


        session = make_session()
        all_sources = session.query(Source).all()
        news_list = []
        #all_sources = {'cnn':{'url':'http://spectrum.ieee.org/rss/blog/automaton/fulltext'}} #Debug
        counter = 0 #Debug
        for source in all_sources:
            feed = feedparser.parse(source.url)
            for entry in feed['entries']:

                ########################## Debug
                if counter == 5:
                    break
                else:
                    counter += 1
                ##########################

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


                html_title = AHeading(6,title) ##Title_header
                html_title.attrs['style'] = "color:black; display: inline-block;"
                html_title.attrs['class'] = "collapsible-header-value"


                kwargs ={"style":"display:block;max-width:350px;max-height:350px;width: auto;height: auto;"}
                html_image = AImage(source=image, **kwargs )
                html_summary = AParagraph(summary)
                html_date = AParagraph(date)
                html_link = AHref(url=url, link="Read")

                html_div = AParagraph() ##News_body
                html_div.add_to_content(html_image)
                html_div.add_to_content(html_summary)
                html_div.add_to_content(html_date)
                html_div.add_to_content(html_link)

                news_list.append({'header':{'value':html_title},'body':{'value':html_div}})

        self.add_component(ACollapsible(collapsible_type={},attributes=news_list))
        self.add_component(h7)
