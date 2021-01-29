from bokeh.plotting import curdoc
from bokeh.layouts import layout
from bokeh.models.widgets import TextInput, Button, DataTable, TableColumn, Paragraph, RadioButtonGroup
from bokeh.models import ColumnDataSource
import numpy as np
import pandas as pd
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, HTMLTemplateFormatter
from bokeh.models import ColumnDataSource, CustomJS

from vector import Ablauf
from crawler import Crawler

global main_layout
global anfrage 

#Define Layout for Bokeh
main_layout = layout(children=[[[],[],[],[]],
                                [],
                                []])



def start_categories(attr,old,new):
    """
    Function that starts the trendanalysis based on the pre-defined RadioButtons
    for the categories sport, politics, economics, news

    Calls calculate with predefined subreddits
    """
    global main_layout
    text = Paragraph(text = str(popular_categories.active))
    main_layout.children[1] = text
    status2 = Paragraph(text = 'Status: Rechne...')
    main_layout.children[0].children[3] = status2
    
    sport =   ["sports", "running", "bicycling", "golf", "fishing", "skiing", "sportsarefun", "tennis",
                    "rugbyunion","discgolf","cricket","sailing","nfl","CFB","fantasyfootball",
                    "baseball","mlb","fantasybaseball",
                    "nba","collegebasketball","fantasybball","skateboarding","snowboarding","longboarding",
                    "formula1","MMA","squaredcircle","ufc","boxing","wwe","MMAStreams","hockey","nhl",
                    "olympics","apocalympics2016","soccer","worldcup","Bundesliga"]
    politics = ['Politics','worldpolitics','anarchism','socialism','conservative','politicalhumor','Libertarian',
                'neutralpolitics','politicaldiscussion','ukpolitics','geopolitics','communism','completeanarchy',
                'politicalcompassmemes']
    economics = ["Economics","business","entrepreneur","marketing","BasicIncome","business","smallbusiness",
                "stocks","wallstreetbets","stockmarket"]
    news = [ "worldnews", "news", "nottheonion", "UpliftingNews"
            "offbeat", "gamernews", "floridaman", "energy",
            "syriancivilwar", "truecrime"]
    all_topics = [sport, politics, economics, news]

    current_words = all_topics[popular_categories.active]
    calculate(current_words)

def startfunc():
    """
    Function that starts the trendanalysis based on user input by text field
    splits the input at seperator (,) if more than one Searchword was used

    Calls calculate with Searchwords
    """
    global main_layout
    text = Paragraph(text = anfrage.value)
    main_layout.children[1] = text
    status1 = Paragraph(text = 'Status: Rechne...')
    main_layout.children[0].children[3] = status1
    current_words = anfrage.value
    current_words = current_words.split(', ')
    current_words.append(0)
    calculate(current_words)

def calculate(current_words):
    """
    Function started by start_categories or startfunc
    Manages the download of all posts
    """
    global main_layout
    status1 = Paragraph(text = 'Status: Rechne...')
    main_layout.children[0].children[3] = status1
    crawler = Crawler()
    subred_list = []

    #If function called by User Input:
    #get all subreddits related to the searchwords
    if current_words[-1] == 0:
        for j in range(len(current_words)-1):
            searchword = current_words[j]
            subred_list_ = crawler.crawling(current_words[j])
            subred_list = subred_list + subred_list_
    else:
        #If function called by RadioButtonGroup:
        #Use the predifined Subreddits as searchwords
        subred_list = current_words
        searchword = current_words[0]
    try:
        #If there is already data from an earlier pickel, use it to have more data and make the trendrecognition more valid
        posts = pd.read_pickle(f"daten/{searchword}.pkl") 
    except:
        #If there is no data found of the topic, create new df
        posts = pd.DataFrame(columns=['title','id','url', 'score', 'subreddit', 'num_comments', 'body', 'created'])

    #Download all subredits and save them or append them to a already existing database if post is not seen before
    #if post is already seen before, stop downloading the old data again
    for subreddit in subred_list:
        print('Now Downloading:',subreddit)
        try:
            subred = crawler.subreddit(name=f"{subreddit}", limit=10_000)
            for post in subred:
                if post.id not in list(posts["id"]):
                    posts = posts.append({'title':post.title,'id':post.id, 'url':post.url, 'score':post.score, 'subreddit':post.subreddit, 'num_comments':post.num_comments, 'body':post.selftext, 'created':post.created},ignore_index=True)
                else:    
                    break
        except:
            continue
    posts.to_pickle(f"daten/{searchword}.pkl")


    status = Paragraph(text = 'Status: Download erfolgreich')
    main_layout.children[0].children[3] = status

    #Start the Function to get all topwords with the current trends
    topwords = Ablauf(searchword)

    #Start function to create table for Bokeh GUI
    create_table(topwords)

def create_table(words):
    """
    Takes output from Ablauf-function (=trendwords) and creates table on GUI
    """
    data = {}
    _list = []

    #Create Link for Google News and unzips related words
    for word in words:
        data[word[0]] = str('https://news.google.com/search?q='+word[0]+'&hl=en-US&gl=US&ceid=US:en')
        _list.append([word[1]])

    #Create Dataframe with all information, the GUI should show
    datas = pd.DataFrame(data.items(), columns=['Word', 'News'])
    datas['Related Words'] = _list

    #Create Table
    col1 = TableColumn(field='News', title='News' ,formatter=HTMLTemplateFormatter(template = '<a target="_blank" href="<%= News %>"><%= value %></a>'))
    col2 = TableColumn(field='Word', title='Word')
    col3 = TableColumn(field='Related Words', title='Related Words')
    Columns = [col2, col3, col1] 
    data_table = DataTable(columns=Columns, source=ColumnDataSource(datas))

    main_layout.children[2] = data_table



#RadiobuttonGroup with predifined subreddist
popular_categories = RadioButtonGroup(labels=["sport", "politics", "economics", "news"], active = None)
popular_categories.on_change('active', start_categories)

#Field for User input
anfrage = TextInput(value = 'Hier Anfrage einfügen')

#Go-Button
go_button = Button(label = 'Start der Analyse', button_type = 'success')
go_button.on_click(startfunc)

status = Paragraph(text = 'Status: Warte auf Input')

#Define Layout, where which buttons should be
main_layout.children[0].children[0] = anfrage
main_layout.children[0].children[1] = go_button
main_layout.children[0].children[2]= popular_categories
main_layout.children[0].children[3] = status


curdoc().add_root(main_layout)
curdoc().title = 'Trenderkennung'