from eTinex.spiders.eTinexSpider import EtinexspiderSpider
from scrapy import crawler


def main():
    spider = crawler.CrawlerProcess()
    spider.crawl(EtinexspiderSpider)
    spider.start()

    pass


if __name__ == '__main__':
    main()


