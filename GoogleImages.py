from urllib.request import urlopen
from grab import Grab

import itertools
import uuid
import time
import os


class GoogleImages:
    quantity = 1
    path = ""
    keywords = ""
    search_query = "https://images.search.yahoo.com/search/images?p="

    def __init__(self, keywords, quantity=1, path='source_images'):
        self.keywords = keywords
        self.quantity = quantity
        self.search_query += keywords
        self.path = path

    def SearchImages(self):
        g = Grab()
        g.setup(connect_timeout=50, timeout=50)
        g.go(self.search_query)
        img_link_list = g.xpath_list('//li/a/img')
        top = itertools.islice(img_link_list, int(self.quantity))

        try:
            for x in top:
                img_url = str(x.get('data-src'))
                img_url = img_url.replace('.240.', '.full.')
                img_url = img_url.replace('s3.', 'static.')
                img = urlopen(img_url).read()
                img_name = str(uuid.uuid1()) + self.keywords + ".jpg"
                if os.path.isfile(img_name): os.remove(img_name)
                print(img_name)
                self.path += img_name
                with open(self.path, 'wb') as f:
                    f.write(img)
                    f.close()
        except Exception as error:
            print("Download error: " + error)
