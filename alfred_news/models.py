from alfred.modules.api.a_base_model import ABaseModel


class Article(ABaseModel):
    def __init__(self, title, summary, date, url, image):
        super().__init__()
        self.title = title
        self.summary = summary
        self.date = date
        self.url = url
        self.image = image


class Source(ABaseModel):
    def __init__(self, name, url, category_id):
        super().__init__()
        self.name = name
        self.url = url
        self.category_id = category_id


class Category(ABaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def sources(self):
        lst = []
        for source in Source.all():
            if str(source.category_id) == str(self.id):
                lst.append(source)
        return lst
