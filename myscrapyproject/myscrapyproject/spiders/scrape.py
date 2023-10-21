import os
import scrapy


class QuotesSpider(scrapy.Spider):
    # Name of the spider
    name = 'scrape'

    def __init__(self, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.start_urls = [os.environ.get('SCRAPE_URL')]
    def parse(self, response):
        # Extract data from the webpage
        data = response.text

        # Save the data to an HTML file
        output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'output.html'))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(data)
