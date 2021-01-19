from crawler import Crawler

if __name__ == "__main__":
    
    crawler = Crawler()
    crawler.crawling()
    subred = crawler.subreddit()
    print(type(subred))
    print(next(subred))
    print(dir(subred))

    for i in subred:
        print(i.title, i.url)
    print("all done")