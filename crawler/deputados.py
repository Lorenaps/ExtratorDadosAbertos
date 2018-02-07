import scrapy
import json
import csv

class Deputados(scrapy.Spider):
    name = 'toAPIDadosAbertos'
    pages = 0
    data = []

    def start_requests(self):
        urls = ['https://dadosabertos.camara.leg.br/api/v2/deputados']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers={'accept': 'application/json'})

    def parse(self, response):
        item_json = json.loads(response.body)   #get body of response. Comes as str
        item_list = item_json.get("dados")   #add a new set of datas returned (a new page) in list
        self.data = self.data + item_list
        self.pages += 1

        if item_json.get('links')[1].get('rel') == 'next':
            next_page = item_json.get('links')[1].get('href')
        else:
            next_page = None

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse, headers={'accept': 'application/json'})
        else:
            filename = '../data/deputados.json'
            with open(filename, 'w') as f:
                f.write(json.dumps(self.data))

        self.log("End of crawler \nTotal pages: " +
                 str(self.pages) +
                 "\nTotal items: " +
                 str(len(self.data)) + "\n")