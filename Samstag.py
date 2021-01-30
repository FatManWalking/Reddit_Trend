import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
import math
import json
import nltk
import praw
#from nltk.corpus import stopwords
    
class Vektor():
    """A class to build the word vectors and do the analysis on the data

    df (pandas.dataframe): the modifid dataframe for the related topic
    timeframe (datetime): the amount of days the trends are to be searched in
    """
    df = "_"
    timeframe = datetime.today()
    
    @classmethod
    def data_update(cls, df, days):
        """updates the class variables df(pd.dataframe) and timeframe(datetime)
        """
        cls.df = df
        cls.timeframe = datetime.today() - timedelta(days=days)
        
    def __init__(self, df, days=1):
        self.data_update(df, days)
        self.split()
        
    def split(self):
        """splits the data into posts inside and outside the defined timeframe
        creates self.now and self.old (pandas.datframe)
        """
        
        mask_now = (Vektor.df["created"] > Vektor.timeframe)
        self.now = Vektor.df.loc[mask_now]
        self.now.reset_index(inplace=True, drop=True)
        
        mask_old = (Vektor.df["created"] < Vektor.timeframe)
        self.old = Vektor.df.loc[mask_old]
        self.old.reset_index(inplace=True, drop=True)
    
    def tokenizer(self, df):
        """breaks up the titles of the given dataframe up in tokens and gives a series of those tokens

        Args:
            df (pandas.dataframe): the dataframe whose titles are to be tokenized
        Return:
            series (pandas.series): a series of tokens
        """
        series = df['title']
        series = series.str.lower()
        series = series.str.replace('\d+', '')
        series = series.str.replace('\W+', ' ')
        series = series.str.split(' ')

        return series

    def total_tf(self, df):
        """calcs a total term freq over all documents to build a general word vector

        Args:
            df (pd.dataframe): the database to calc the tf on
        Returns:
            tf: A dic of the total_tf over the given document
        """
        tf = dict()
        
        for tokens in df["title"]:
            token_count = dict(Counter(tokens))
            tf.update({key:(tf.get(key,0)+value) for key, value in token_count.items()})
            
        return tf

    def within_tf(self, df):
        """calcs the within term freq over all titles to build word vectors

        Args:
            df (pd.dataframe): the database to calc the tf on
        Returns:
            tf: A dic of the within_tf over the given document
        Note:
            A set of all tokens can be gained via total_tf.keys()
        """
        tf = list()

        for tokens in df['title']:
            dict_ = dict(Counter(tokens))
            tf.append({key:value/len(dict_) for key, value in dict_.items()})

        return tf
    
    def idf(self, df):
        """calculating the idf of a given dataframe

        Args:
            df (pd.dataframe): see above
        """
        # total number of documents
        N = len(df)
        
        # number of documents containing a term
        tD = dict()
        for tokens in df['title']:
            tD.update({token:( tD.get(token, 0)+1) for token in set(tokens)})
        
        # calc idf out of the above calcs
        idf = {key:math.log10(N / value) for key, value in tD.items()}
        return idf
    
    def tf_idf(self, tf, idf):
        """calcultes tf-idf from tf and idf

        Args:
            tf (dict): term-freq
            idf (dict): inverse document-freq

        Returns:
            dict: the calc tf-idf
        """
        return {key:(tf[key]*idf[key]) for key in tf.keys()}
    
    #TODO: Modify
    def context(self, trendwords, filtered_trends):
        """A Generator to give context to the found trendwords
        
        Args:
            trendwords (list): A list of the found words that are trending
            filtered_trends (dict): Dict of the calculted relevance of all words

        Yields:
            context_dic (dict): the words that are in context with the trendword and their rating
            word (string): the word the dict belongs to
        """
        for word in trendwords:
            context_dic = self.title_context(word)
            for key, value in context_dic.items():
                for token, tf in value.items():
                    value[token] = tf * filtered_trends[token]

            yield context_dic, word

    #TODO: Modify
    def title_context(self, word):
        context_dic = {}
        for tokens in self.now['title']:
            if word in tokens:
                tokens = [other_word for other_word in tokens if len(other_word)>2 and other_word != word]
                if word in context_dic:
                    context_dic[word]["counter"] += 1
                    context_dic[word]["tokens"] += tokens
                else: context_dic[word] = {"counter":1, "tokens":tokens}

        for key, value in context_dic.items():
            #context_dic[key]["tokens"] = [word for word in value["tokens"] if (not word in set(stopwords.words('english'))) and (word != key)]
            context_dic[key]["tokens"] = dict(Counter(value["tokens"]))
            context_dic[key] = {word:float(value/context_dic[key]["counter"]) for word, value in context_dic[key]["tokens"].items()}

        return sort_dict(context_dic, reverse=False)

#renamed the old "auswahl" function
def read_database(searchword):
    """Reads the .pkl file of the selected topic and returns a modifid dataframe

    Args:
        searchword (string): the database file that is to be analysed
    Returns:
        df (pandas.dataframe): A modifid dataframe with the wanted data
    """
    # A list of subreddits found to have negativ impact on the analyses and no value
    killTags = ['futbol', 'newsokunomoral', 'newStreamers', 'newsbloopers', 'newsokur', 'NewSkaters', 'newsentences']
    dataframe = pd.read_csv(f"daten/{searchword}.csv", sep=";")
    
    df = dataframe.iloc[[index for index,row in dataframe.iterrows() if row['subreddit'] not in killTags]]
    # converts the unix-timestamp given by the API to datetime
    df['created'] = pd.to_datetime(df.loc[:,('created')], unit='s')
    
    return df

def sort_dict(dic, reverse=True):
    """return the dict sorted by values
    """
    return {k: v for k, v in sorted(dic.items(), key=lambda item: item[1],reverse = reverse)}
    
def Ablauf(searchword):
    """Sequencing through the source code of this file and returning the results to the main

    Args:
        searchword (string): the topic all analysis based around, there has to be a corresponding .pkl with that name
    """
    
    # Datatransformation step 1
    df = read_database(searchword)
    
    # Object Initalisation and datatransformation step 2
    datasource = Vektor(df, 1)
    
    # Variables for better readbility
    df = Vektor.df
    now = datasource.now
    old = datasource.old
    
    # Variables to store our results
    whole = dict()
    trend = dict()
    archiv = dict()
    
    # Iterating of all three datasources
    for data,name in [(df, "all"), (now, "now"), (old, "old")]:
        
        #Use Tokenizer
        data['title'] = datasource.tokenizer(data)
        
        #Use tf calculation
        total_tf = datasource.total_tf(data)
        within_tf = datasource.within_tf(data)
        
        #Use idf calculation
        idf = datasource.idf(data)
        
        # Calc tf-idf
        tf_idf_total = datasource.tf_idf(total_tf, idf)
        tf_idf_within = list()
        for i in within_tf:
            tf_idf_within.append(datasource.tf_idf(i, idf))
        
        #sort_dict(tf_idf_1, reverse=True)
        #TODO: Skipped stopword removal

        data_return = {"total_tf":total_tf, "within_tf":within_tf, "idf":idf ,"tf_idf_total":tf_idf_total, "tf_idf_within":tf_idf_within}
        if name == "all":
            whole = data_return
        elif name == "now":
            trend = data_return
        elif name == "old":
            archiv = data_return
    #print(sort_dict(trend["tf_idf_total"], reverse=False))
    ergebnis = {key:(value*(1/trend["tf_idf_total"][key])*whole["idf"][key]) for key, value in trend["total_tf"].items()}
    ergebnis = sort_dict(ergebnis, reverse=True)
    #print(ergebnis)
    trend_generator = datasource.context(list(ergebnis.keys())[:10], ergebnis)
    
    for i in trend_generator:
        print(i, "\n")
        
        
if __name__ == "__main__":
    
    Ablauf("news")
    
    # 2021-01-30 17:50:55.699930
    # Wombats shit in squares