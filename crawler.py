from pathlib import Path
import praw
import json
                    
class Crawler():

    def __init__(self, subreddits = "all"):

        self.credentials()
        self.subreddits = subreddits
    
    def credentials(self):
        """
        loads and returns the credentials to the Reddit API from a secret json file
        creates self.reddit
        """
        path = Path.cwd().joinpath("secrets.json")
        with open(path) as file:
            secrets = json.load(file)

        self.reddit = praw.Reddit(client_id = secrets["api_id"], client_secret = secrets["secret"], 
                    user_agent = secrets["user_agent"], username = secrets["username"], password = secrets["password"])
    
    def crawling(self):
        """
        Crawls through the list of subreddits on r/ListOfSubreddits
        """
        return self.subreddit(name="ListOfSubreddits", limit=1)

    def subreddit(self, name="all", limit=10):
        """
        andere Optionen:
            hot, new, controversial, top, gilded
        """
        subred = self.reddit.subreddit(name)
        return subred.new(limit=limit)

    def weighting(self):
        """
        Weights the upvotes and comments against the size of the community
        """
        pass

    def pandas_tab(self):

        import pandas as pd
        posts = []
        ml_subreddit = self.reddit.subreddit('MachineLearning')
        for post in ml_subreddit.hot(limit=10):
            posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
        posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
        print(posts)

