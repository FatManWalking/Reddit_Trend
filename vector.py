import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
import math
import json
import nltk
from nltk.corpus import stopwords


def auswahl(searchword):
    killTags = ['futbol', 'newsokunomoral', 'newStreamers', 'newsbloopers', 'newsokur', 'NewSkaters', 'newsentences']
    unpickled_df = pd.read_pickle(f"daten/{searchword}.pkl")
    #unpickled_df = pd.read_csv("daten/pickled.csv", sep=";")
    #TODO: das hier vor dem pickeln machen
    #df = unpickled_df[unpickled_df.subreddit not in killTags] #Delete Futbol (Italian, Spanish, Pizza, Pasta)
    #df = df_1[df_1.subreddit != 'newsokunomoral'] 
    #df['created'] = pd.to_datetime(df['created'], unit='s') #Convert unix timestamp2Datetime
    
    df = unpickled_df.iloc[[index for index,row in unpickled_df.iterrows() if row['subreddit'] not in killTags]]
    df['created'] = pd.to_datetime(df.loc[:,('created')], unit='s')
    print(df.head(3))
    return df


class Vektor():

    def __init__(self,df):
        self.df = df
        self.df_today, self.df_before = self.split()

    def split(self):
        """
        splits dateframe in posts of the last 24h and before
        returns: 2 Dataframes (today, before)
        """
        today = datetime.today() - timedelta(days=1)  #Immer die letzten 24h nehmen
        mask_today = (self.df['created'] > today)
        df_today = self.df.loc[mask_today]
        #len_today = len(df_today)
        df_today.reset_index(inplace=True,drop=True)

        mask_before = (df['created'] < today) 
        df_before = df.loc[mask_before]
        #print(len(df_before))
        df_before.reset_index(inplace=True,drop=True)

        return df_today, df_before

    def tokenizer(self, df):
        """
        splits the title of all posts in tokens
        return: dataframe series
        """
        series = df['title']
        series = series.str.lower()
        series = series.str.replace('\d+', '')
        series = series.str.replace('\W+', ' ')
        series = series.str.split(' ')

        return series

    def tf(self, df):
        """
        calcs all tf frequencies and builds a general word vector
        return: term frequencies(list of dicts), all tokens(set of keys)
        """
        tf = []
        all_tokens = []

        for tokens in df['title']:
            dict_ = dict(Counter(tokens))
            tf.append({key:value/len(dict_) for key, value in dict_.items()})
            all_tokens.extend(dict_.keys())

        return tf, set(all_tokens), all_tokens

    def idf(self, df, all_tokens):
        """
        inverse document frequence, smoothed and with log10
        return: doc_freq(dict)
        """
        doc_freq = dict()
        for tokens in df['title']:
            for token in list(set(tokens)):
                doc_freq[token] = doc_freq.get(token, 0) + 1

        doc_freq = {key:math.log10(len(df) / value+1) for key, value  in doc_freq.items()}
        
        return doc_freq

    def tf_idf_modify(self):
        pass
    
    def context(self, trendwords, filtered_trends):
        trendwords = ['mcdonough', 'prolific']
        for word in trendwords:
            context_dic = self.title_context(word)
            for key, value in context_dic.items():
                for token, tf in value.items():
                    value[token] = tf * filtered_trends[token]
            yield context_dic, word
                
            
    def title_context(self, word):
        context_dic = {}
        for tokens in self.df_today['title']:
            if word in tokens:
                tokens = [word for word in tokens if len(word)>2]
                #print(f"prolific was here\n{tokens}\n")
                if word in context_dic:
                    context_dic[word]["counter"] += 1
                    context_dic[word]["tokens"] += tokens
                else: context_dic[word] = {"counter":1, "tokens":tokens}
        for key, value in context_dic.items():
            context_dic[key]["tokens"] = [word for word in value["tokens"] if (not word in set(stopwords.words('english'))) and (word != key)]
            context_dic[key]["tokens"] = dict(Counter(value["tokens"]))
            context_dic[key] = {word:float(value/context_dic[key]["counter"]) for word, value in context_dic[key]["tokens"].items()}
        
        return context_dic
        
        
def Ablauf(searchword):
    df = auswahl(searchword)
    test = Vektor(df)

    test.df_before['title'] = test.tokenizer(test.df_before)
    test.df_today['title'] = test.tokenizer(test.df_today)

    counter = 0
    today = {}
    before = {}
    for i in [test.df_before, test.df_today]:

        tf, set_all_tokens, all_tokens = test.tf(i)
        idf = test.idf(i, set_all_tokens)

        oa_tf = dict(Counter(all_tokens))

        final = dict()
        for key in idf.keys():
            final[key] = math.log10((oa_tf[key]/len(i)) * idf[key])

        final = {k: v for k, v in sorted(final.items(), key=lambda item: item[1],reverse = False)}

        if not counter:
            before = final
        else:
            today = final
        counter += 1

    final_final = dict()
    for key in today.keys():
        final_final[key] = today[key] / before.get(key, 100)
    final_final = {k: v for k, v in sorted(final_final.items(), key=lambda item: item[1],reverse = True)}
    #print(final_final)
        
    filtered_trends = {word:value for word,value in final_final.items() if not word in set(stopwords.words('english'))}
    #print(filtered_trends)
    
    """ab hier beginnt Kontextaufruf
    nicht vergessen: davor noch die wörter die nur 1 mal vorkommen löschen/ignorieren
    """
    
    x = test.context(["Hhihi"], filtered_trends)
    top_list = []
    for dic, word in x:
        n_dic = {k: v for k, v in sorted(dic[word].items(), key=lambda item: item[1],reverse = False)}
        n_dic = [word for word,value in n_dic.items() if value < 0]
        top_list.append((word, n_dic))
        
    return top_list
                
            
    
if __name__ == "__main__":
    searchword = str(input("Wonach suchst du?\n-->  "))
    df = auswahl(searchword)
    test = Vektor(df)

    # Hier dann zwischen dem before und now df unterscheiden
    # test.df durch test.df_before und test.df_today ersetzen


    test.df_before['title'] = test.tokenizer(test.df_before)
    test.df_today['title'] = test.tokenizer(test.df_today)

    counter = 0
    today = {}
    before = {}
    for i in [test.df_before, test.df_today]:

        tf, set_all_tokens, all_tokens = test.tf(i)
        idf = test.idf(i, set_all_tokens)
        #print(idf)

        oa_tf = dict(Counter(all_tokens))
        #oa_tf * idf

        final = dict()
        for key in idf.keys():
            final[key] = math.log10((oa_tf[key]/len(i)) * idf[key])

        final = {k: v for k, v in sorted(final.items(), key=lambda item: item[1],reverse = False)}

        if not counter:
            before = final
        else:
            today = final
        counter += 1

    #print(today)


    final_final = dict()
    for key in today.keys():
        final_final[key] = today[key] / before.get(key, 100)
    final_final = {k: v for k, v in sorted(final_final.items(), key=lambda item: item[1],reverse = True)}
    #print(final_final)
        #doc_freq[token] = doc_freq.get(token, 0) + 1
        
    filtered_trends = {word:value for word,value in final_final.items() if not word in set(stopwords.words('english'))}
    #print(filtered_trends)
    
    """ab hier beginnt Kontextaufruf
    nicht vergessen: davor noch die wörter die nur 1 mal vorkommen löschen/ignorieren
    """
    
    x = test.context(["Hhihi"], filtered_trends)
    for dic, word in x:
        n_dic = {k: v for k, v in sorted(dic[word].items(), key=lambda item: item[1],reverse = False)}
        n_dic = [word for word,value in n_dic.items() if value < 0]
        print(word, n_dic)
        
    

