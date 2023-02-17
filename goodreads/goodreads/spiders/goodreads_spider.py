import scrapy
from toolz import curry


class ShelvesSpider(scrapy.Spider):
    """

    """
    name = "shelves"
    shelf_names = ["favorite", "reread", "must", "best"]
    shelf_names_re = "|".join(shelf_names)

    start_urls = [
        "https://www.goodreads.com/review/list/40648422"
    ]

    def response_get(self, response, x, is_int=False):
        """

        :param response:
        :param x:
        :param is_int:
        :return:
        """
        val = response.xpath(x).get()
        if is_int:
            int(str.strip(val))
        return val

    def convert_rating(self, rating:str):
        """

        :param rating:
        :return:
        """
        rating_map = {
            "it was amazing": 5,
            "really liked it": 4,
            "liked it": 3,
            "it was OK": 2,
            "didn't like it": 1
        }
        for k, v in rating_map.items():
            if rating == k:
                return v

    def parse(self, response):
        """

        :param response:
        :return:
        """
        shelf_urls = response.xpath(
                f"//*[@id='paginatedShelfList']//*[re:test(@title, '{self.shelf_names_re}')]/@href"
            )
        yield from response.follow_all(shelf_urls, self.parse_shelf)

    def parse_shelf(self, response_shelf):
        """

        :param response_shelf:
        :return:
        """
        for book in response_shelf.xpath(
                "//*[@id='booksBody']//*[@class='bookalike review']"
        ):
            yield self.parse_book(book)

    def get_review(self, reponse_review):
        """

        :param reponse_review:
        :return:
        """
        def parse_review(response):
            # TODO: come back here for extracting text of review
            yield response.xpath("")


        yield scrapy.Request(reponse_review.urljoin(href), parse_review)

    def parse_book(self, response_book):
        """

        :param response_book:
        :return:
        """
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
            "user_rating": convert_rating(book_xpath(
                "//*[@class='field rating']//*[@class=' staticStars notranslate']/@title"
            )),
            "date_read": book_xpath(
                "//*[@class='field date_read']//*[@class='date_read_value']/text()"
            ),
            "date_added": book_xpath(
                "//*[@class='field date_added']//div//@title"
            ),
            "review_text": self.parse_review(response_book.xpath(
                "//*[@class='field actions']//*[text()='view (with text)']/@href"
            ))
        }





