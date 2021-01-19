from crawler import Crawler
import pandas as pd

sport =   ["sports", "running", "bicycling", "golf", "fishing", "skiing", "sportsarefun", "tennis",
                    "rugbyunion","discgolf","cricket","sailing","nfl","CFB","fantasyfootball",
                    "baseball","mlb","fantasybaseball",
                    "nba","collegebasketball","fantasybball","skateboarding","snowboarding","longboarding",
                    "formula1","MMA","squaredcircle","ufc","boxing","wwe","MMAStreams","hockey","nhl",
                    "olympics","apocalympics2016","soccer","worldcup","Bundesliga"]
        
politik = [ "worldnews", "news", "nottheonion", "UpliftingNews"
            "offbeat", "gamernews", "floridaman", "energy",
            "syriancivilwar", "truecrime"]
                    
if __name__ == "__main__":
    
    crawler = Crawler()
    #subred = crawler.crawling()
    posts = pd.DataFrame(columns=['title', 'score', 'subreddit', 'num_comments', 'body', 'created'])
    for subreddit in politik:
        print(subreddit)
        try:
            subred = crawler.subreddit(name=f"{subreddit}", limit=10_000)
        
            for post in subred:
                posts = posts.append({'title':post.title, 'score':post.score, 'subreddit':post.subreddit, 'num_comments':post.num_comments, 'body':post.selftext, 'created':post.created},ignore_index=True)
        except:
            continue
    posts.to_pickle("daten/Politik.pkl")
    
        
   
    """
        with open("basis.txt", "a") as file:
            file.write(f"\n ### {subreddit} ### \n")
            for i in subred:
                file.write(f"{i.title}\n")
    """
    # crawler.pandas_tab()
"""
    posts = []
    ml_subreddit = self.reddit.subreddit('MachineLearning')
    for post in ml_subreddit.hot(limit=10):
        posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    print(posts)
"""