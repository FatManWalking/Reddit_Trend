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
                    

economics = ["Economics","business","entrepreneur","marketing","BasicIncome","business","smallbusiness","stocks","wallstreetbets","stockmarket"]

all_topics = sport+politik+economics
print(all_topics)




if __name__ == "__main__":
    searchword = str(input("In welchem Bereich suchst du?"))
    crawler = Crawler()
    subred_list = crawler.crawling(searchword)
    
    try:
        posts = pd.read_pickle(f"daten/{searchword}.pkl")
    except:
        posts = pd.DataFrame(columns=['title','id','url', 'score', 'subreddit', 'num_comments', 'body', 'created'])

    for subreddit in subred_list:
        print(subreddit)
        try:
            subred = crawler.subreddit(name=f"{subreddit}", limit=10_000)
            for post in subred:
                
                if post.id not in list(posts["id"]):
                    posts = posts.append({'title':post.title,'id':post.id, 'url':post.url, 'score':post.score, 'subreddit':post.subreddit, 'num_comments':post.num_comments, 'body':post.selftext, 'created':post.created},ignore_index=True)
        except:
            continue
    posts.to_pickle(f"daten/{searchword}.pkl")

    import pandas as pd 
