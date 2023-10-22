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

        # Get the values of environment variables
        user_downloads = os.environ.get('UserDownloads')
        output_file_name = os.environ.get('OutputFileName')

        if user_downloads and output_file_name:
            # Calculate the absolute path to the output file
            current_dir = os.path.dirname(__file__)
            output_path = os.path.abspath(os.path.join(current_dir, '..', '..', '..', user_downloads, f'{output_file_name}.html'))

            # Ensure the directory exists, creating it if not
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Save the data to the HTML file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(data)
        else:
            self.logger.error("Environment variables not set or are empty.")
