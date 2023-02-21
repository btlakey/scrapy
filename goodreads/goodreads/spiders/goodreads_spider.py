import scrapy
from toolz import curry
import logging
import locale

logger = logging.getLogger('shelves_logger')
logger.STDOUT = True
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # this handles commas in string numbers


class ShelvesSpider(scrapy.Spider):
    """

    """
    name = "shelves"
    shelf_names = ["favorite", "reread", "must", "best"]
    shelf_names_re = "|".join(shelf_names)

    start_urls = [
        "https://www.goodreads.com/review/list/40648422"
    ]

    def response_get(self, response, xpath_query, **kwargs):
        """

        :param response:
        :param x:
        :return:
        """
        # the . prevents the xpath query from going all the way back to the root node
        val = response.xpath("." + xpath_query).get().strip()
        for type_check, convert in zip(["is_int", "is_float"], [int, float]):
            if kwargs.get(type_check, False):
                val = convert(locale.atoi(val))  # remove any commas that might be there
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

    def get_review(self, response):
        """

        """
        review_url = response.xpath(
            "//*[@class='field actions']//*[text()='view (with text)']/@href"
        )
        yield response.follow(review_url, self.parse_review)

    def parse_review(self, response_review):
        """

        :param reponse_review:
        :return:
        """
        yield self.response_get(
            response_review,
            "//*[@itemprop='reviewBody']//text()"
        )

    def parse_book(self, response_book):
        """

        :param response_book:
        :return:
        """
        # book_xpath = lambda x: response_book.xpath(x).get()
        book_xpath = curry(self.response_get)(response_book)

        return {
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
                "//*[@class='field date_pub']//div//text()"
            ),
            "mean_rating": book_xpath(
                "//*[@class='field avg_rating']//div//text()", is_float=True
            ),
            "num_rating": book_xpath(
                "//*[@class='field num_ratings']//div//text()", is_int=True
            ),
            # "user_rating": self.convert_rating(book_xpath(
            #     "//*[@class='field rating']//*[@class=' staticStars notranslate']/@title"
            # )),
            # "date_read": book_xpath(
            #     "//*[@class='field date_read']//*[@class='date_read_value']/text()"
            # ),
            # "date_added": book_xpath(
            #     "//*[@class='field date_added']//div//@title"
            # ),
            # "review_text": self.get_review(response_book)
        }





