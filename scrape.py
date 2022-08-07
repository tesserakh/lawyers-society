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
        
        # Names
        full_name = response.css('h2.member-info-title::text').get().strip()
        split_name = full_name.split(' ')
        last_name = split_name[-1]
        del split_name[-1]
        given_name = ' '.join(split_name)
        labels = ['Full Name', 'Fist Name', 'Last Name']
        values = [full_name, given_name, last_name]

        profile_info = response.css('div.cell.small-12.medium-6').css('div.member-info-wrapper')
        special_info = response.css('div.member-special-cases')
        
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


        data = { labels[i]: values[i] for i in range(len(labels)) }
        data.update({ 'Link': response.meta['url'] })

        yield data


if __name__ == '__main__':
    DOWNLOADER_MIDDLEWARES = {

        'FEEDS': {'lawyers.json': {
            'format': 'json',
            'overwrite': True
        }},
        'LOG_LEVEL': 'DEBUG'
        #'HTTPCACHE_ENABLED': True, # developing purpose to reduce the time only
        #'HTTPCACHE_IGNORE_HTTP_CODES': [400, 403, 404, 413, 414, 429, 456, 503, 529, 500], # developing purpose to reduce the time only

    }
    process = CrawlerProcess(DOWNLOADER_MIDDLEWARES)
    process.crawl(LawyersSpider)
    process.start()
