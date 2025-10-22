from icrawler.builtin import GoogleImageCrawler

google_crawler = GoogleImageCrawler(storage={'root_dir': './ambulancias/dataset'})
google_crawler.crawl(keyword='ambulancia', max_num=5)
