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
        Crawls through the subreddit
        """
        pass

    def subreddit(self, name="all", limit=10):
        subred = self.reddit.subreddit(name)
        return subred.hot(limit=limit)

    def weighting(self):
        """
        Weights the upvotes and comments against the size of the community
        """
        pass

    def dummy(self):
        """
        just a dummy
        """
        pass

