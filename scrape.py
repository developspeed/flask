from autoscraper import AutoScraper

# Define the URL and wanted list
url = 'https://www.wix.com/blog'
wanted_list = ["MARKETING INSIGHTS", 'How to design a logo from start to finish (complete guide)']

# Create an instance of AutoScraper
scraper = AutoScraper()

# Build the scraper
result = scraper.build(url, wanted_list)

# print(result)
# Get the results and group them
answer = scraper.get_result_similar(url, grouped=True)


print(answer)