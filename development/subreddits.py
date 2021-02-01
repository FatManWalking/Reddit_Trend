from crawler import Crawler

test = Crawler()
for i in test.reddit.subreddits.search_by_name("apple"):
    print(i)