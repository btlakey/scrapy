
import scrapy


class ShelvesSpider(scrapy.Spider):
    name = "shelves"
    shelf_names = ["favorite", "reread", "must", "best"]
    shelf_names_re = "|".join(shelf_names)

    start_urls = [
        "https://www.goodreads.com/review/list/40648422"
    ]

    def parse(self, response):
        shelf_urls = response.xpath(
                f"//*[@id='paginatedShelfList']//*[re:test(@title, '{self.shelf_names_re}')]/@href"
            )
        yield from response.follow_all(shelf_urls, self.parse_shelves)

    def parse_shelves(self, response):
        print(response.xpath("//*[@id='booksBody']").get())
