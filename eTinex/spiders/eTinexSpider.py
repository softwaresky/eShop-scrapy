# -*- coding: utf-8 -*-
import scrapy

from ..items import EtinexItem


class EtinexspiderSpider(scrapy.Spider):
    name = 'eTinexSpider'
    # allowed_domains = ['https://www.e-tinex.mk/']
    # 'https://www.e-tinex.mk//'
    start_urls = ['https://www.e-tinex.mk/']

    def parse(self, response):
        # div => tree_menu otvoreno_meni
        # for link in response.css('div.tree_menu otvoreno_meni a::attr(href)'):
        #     print (link)

        # for href in response.css("ul.mtree transit").extract():
        #     print (href)

        for sel_href in response.xpath("//ul[@class='mtree transit']//a"):

            if isinstance(sel_href, scrapy.Selector):

                if "href" in sel_href.css("a").attrib:
                    category = sel_href.css("a::text").get()
                    href = sel_href.css("a").attrib["href"]
                    absolute_url = self.start_urls[0] + href

                    yield scrapy.Request(absolute_url, callback=self.parse_category)


    def parse_category(self, response):
        # a -> proizvod_link

        for href_str_ in response.xpath("//a[@class='proizvod_link']/@href").extract():
            absolute_url = self.start_urls[0] + href_str_
            yield scrapy.Request(absolute_url, callback=self.parse_product)

    def url_join(self, urls, response):
        joined_urls = []
        for url in urls:
            joined_urls.append(response.urljoin(url))

        return joined_urls

    def parse_product(self, response):

        # div -> container_proizvo
        # div -> line_pateka
        # div -> naslov_produkt, brend_produkt, cena_akcija_proizvod
        # a -> slika_proizvod_otvoren

        lst_category_path = []
        for sel_a_ in response.xpath("//div[@class='line_pateka']/a"):
            if sel_a_.css("a::attr(href)").get():
                category = sel_a_.css("a::text").get()
                category = str(category).strip().replace("\n", "").replace("\r", "")
                lst_category_path.append(category)

        category_path = "->".join(lst_category_path)
        # print (category_path)

        naslov_produkt = response.xpath("//div[contains(@class, 'naslov_produkt')]/text()").get()
        if naslov_produkt:
            naslov_produkt = str(naslov_produkt).strip()

        brend_produkt = response.xpath("//div[contains(@class, 'brend_produkt')]/text()").get()
        if brend_produkt:
            brend_produkt = str(brend_produkt).strip()

        # print (brend_produkt)

        for sel_div_ in response.xpath("//div[contains(@class, 'container_proizvo')]"):
            img = sel_div_.css("img::attr(src)").get()

            relative_img_urls = sel_div_.css("img::attr(src)").extract()

            cena = sel_div_.css("div.obicna_cena::text").get()
            if cena:
                cena = str(cena).lower().replace(".", "").replace("ден", "").replace(" ", "")

                if cena:
                    cena = float(cena)
                else:
                    cena = 0.0

            opis_title = sel_div_.css("div.opis_title::text").get()
            if opis_title:
                opis_title = str(opis_title).strip()

            opis = sel_div_.css("div.opis_proizvod::text").get()
            if opis:
                opis = str(opis).strip().replace("\r", "").replace("\n", "")

            product_type_str = ""
            input_div = sel_div_.xpath('//div[@class="number-input"]/input')
            if input_div:
                product_type_str = input_div[0].attrib["data-mera"].strip()

            yield EtinexItem(
                title=naslov_produkt,
                brand=brend_produkt,
                category_path=category_path,
                description_title=opis_title,
                description=opis,
                product_type=product_type_str,
                price=cena,
                image_urls=self.url_join(relative_img_urls, response)

            )