import scrapy
from urllib.parse import urljoin

class ReviewsSpider(scrapy.Spider):
    """

    """
    name = "reviews"
    start_urls = [
        "https://www.goodreads.com/review/list/40648422-samuraikitty?shelf=best-of-the-best"
    ]

    def parse(self, response):
        for book in response.xpath(
            "//*[@id='booksBody']//*[@class='bookalike review']"
        ):
            yield self.parse_review(book)

    def parse_review(self, response_book):
        review_url = response_book.xpath(
            ".//*[@class='field actions']//*[text()='view (with text)']/@href"
        ).get()
        review_url = urljoin("https://www.goodreads.com/", review_url)
        return {
            "review_text": self.get_review()
        }