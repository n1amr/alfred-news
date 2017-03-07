#!/bin/bash

rm alfred_news/news.sqlite -f && python . && sqlite3 alfred_news/news.sqlite <<<" select s.*,c.* from category c, source s where s.category_id = c.id; "
