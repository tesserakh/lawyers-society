import scrapy
from scrapy.crawler import CrawlerProcess

class LawyersSpider(scrapy.Spider):
    name = 'lawyers'
    allowed_domains = ['lso.ca']

    links = 'links.txt'
    with open(links, 'r') as f:
        start_urls = f.readlines()
    for i in range(len(start_urls)):
        start_urls[i] = start_urls[i].strip().lower()

    def start_requests(self):
        for url in self.start_urls:
            meta = {'url': url}
            yield scrapy.Request(url = url, callback = self.parse, meta = meta)
    
    def parse(self, response):
        profile_info = response.css('div.cell.small-12.medium-6').css('div.member-info-wrapper')
        special_info = response.css('div.member-special-cases')
        
        labels = ['Link']
        values = [response.meta['url']]
        
        # Left side content
        for info in profile_info:
            label = info.css('div.member-info-label::text').get().strip()

            # Parsing the data items
            if label == 'Business Address':
                value = info.css('div.member-info-value').css('span::text').getall()
                value = ', '.join(value)
            else:
                value = info.css('div.member-info-value').css('span::text').get()
                if value == None:
                    value = info.css('div.member-info-value::text').get()
                    value = value.strip()
                    
            # Formatting and transforming
            if label == 'Class of Licence':
                value = value.split(' ')[0]
            
            labels.append(label)
            values.append(value)

        # Right side content
        for case in special_info:
            label = case.css('div.member-info-label::text').get().strip()
            if len(case.css('div.member-info-value').css('span::text')) == 2:
                value = case.css('div.member-info-value').css('span::text').getall()
                value = value[1]
            else:
                value = case.css('div.member-info-value').css('span::text').get()
                if value == None:
                    value = case.css('p.member-info-value::text').get()
            value = value.strip()

            labels.append(label)
            values.append(value)


        yield { labels[i]: values[i] for i in range(len(labels)) }

process = CrawlerProcess(settings = {
    'FEED_URI': 'lawyers.json',
    'FEED_FORMAT': 'json',
    'DOWNLOAD_DELAY': 0.25
})

process.crawl(LawyersSpider)
process.start()