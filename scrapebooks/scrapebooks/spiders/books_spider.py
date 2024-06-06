import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BooksSpider(scrapy.Spider):
    name = 'books'
    page = 0
    # start_urls = ['http://www.knjizare-vulkan.rs/domace-knjige/'] 

    def start_requests(self):
        url = 'http://www.knjizare-vulkan.rs/domace-knjige/'
        yield SeleniumRequest(
            url=url,
            wait_time=10,
            callback=self.parse,
        )

    def parse(self, response):
        for book_link in response.css('a.product-link::attr(href)').getall():
            yield SeleniumRequest(
                url=response.urljoin(book_link),
                wait_time=10,
                callback=self.parse_book,
            )
            # yield response.follow(book_link, self.parse_book)

        # next_button = driver.find_element(By.CSS_SELECTOR, 'a.next-page')
        # if next_button:
        #     next_button.click()
        #     WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, 'a.book-link'))
        #     )
        #     sel = Selector(text=driver.page_source)
        #     self.parse(sel)

        next_page = response.css('a.icon-caret-right::attr(href)').get()
        if next_page:
            self.page += 1
            yield SeleniumRequest(
                url=f'http://www.knjizare-vulkan.rs/domace-knjige/{(f"page-{self.page}") if self.page else ""}',
                wait_time=10,
                callback=self.parse,
            )
        #     yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        table = response.css('table.product-attrbite-table')
        yield {
            'naziv': response.css('div.product-details-info > div.heading-wrapper > div.title > h1 span::text').get(),
            'kategorija': response.css('div.category a').xpath('normalize-space(string())').get(),
            'autor': table.css('tr:nth-child(2) td:nth-child(2)').xpath('normalize-space(string())').get(),
            'cena': response.css('div.product-price > span.product-price-value').xpath('normalize-space(string())').get(),
            'izdavac': table.css('tr:nth-child(4) td:nth-child(2)').xpath('normalize-space(string())').get(),
            'godina_izdanja': table.css('tr:nth-child(7) td:nth-child(2)::text').get(),
            'broj_strana': table.css('tr:nth-child(9) td:nth-child(2)::text').get(),
            'tip_poveza': table.css('tr:nth-child(6) td:nth-child(2)').xpath('normalize-space(string())').get(),
            'format': table.css('tr:nth-child(8) td:nth-child(2)::text').get(),
            'opis': response.css('div.description.read-more-text').xpath('normalize-space(string())').get(),
            # izdavač, godina izdanja, broj strana, tip poveza, format, opis
            #'izdavac': response.css('div#tab_product_specification').get()
        }
