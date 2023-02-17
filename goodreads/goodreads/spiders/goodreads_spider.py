import scrapy
from toolz import curry


class ShelvesSpider(scrapy.Spider):
    name = "shelves"
    shelf_names = ["favorite", "reread", "must", "best"]
    shelf_names_re = "|".join(shelf_names)

    start_urls = [
        "https://www.goodreads.com/review/list/40648422"
    ]

    def response_get(self, response, x, is_int=False):
        val = response.xpath(x).get()
        if is_int:
            int(str.strip(val))
        return val

    def convert_rating(self, rating):


    def parse(self, response):
        shelf_urls = response.xpath(
                f"//*[@id='paginatedShelfList']//*[re:test(@title, '{self.shelf_names_re}')]/@href"
            )
        yield from response.follow_all(shelf_urls, self.parse_shelf)

    def parse_shelf(self, response_shelf):
        for book in response_shelf.xpath(
                "//*[@id='booksBody']//*[@class='bookalike review']"
        ):
            yield self.parse_book(book)

    def parse_book(self, response_book):
        # book_xpath = lambda x: response_book.xpath(x).get()
        book_xpath = curry(self.response_get)(response_book)

        yield {
            "title": book_xpath(
                "//*[@class='field title']//@title"
            ),
            "isbn13": book_xpath(
                "//*[@class='field isbn13']//div//text()", is_int=True
            ),
            "author": book_xpath(
                "//*[@class='field author']//a//text()"
            ),
            "date_pub": book_xpath(
                "//*[@class='field date_pub']//div//text()", is_int=True
            )
            "mean_rating": book_xpath(
                "//*[@class='field avg_rating']//div//text()", is_int=True
            ),
            "num_rating": book_xpath(
                "//*[@class='field num_ratings']//div//text()", is_int=True
            ),
            "user_rating": book_xpath(
                , is_int=True
            ),
            "date_read": book_xpath(),
            "date_added": book_xpath(),
            "review_text": self.parse_review(review)
        }





