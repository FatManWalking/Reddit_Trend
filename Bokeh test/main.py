from bokeh.plotting import curdoc
from bokeh.layouts import layout
from bokeh.models.widgets import TextInput, Button, DataTable, TableColumn, Paragraph, RadioButtonGroup
from bokeh.models import ColumnDataSource
import numpy as np
import pandas as pd
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, HTMLTemplateFormatter
from bokeh.models import ColumnDataSource, CustomJS


from crawler import Crawler

global main_layout
global anfrage 

main_layout = layout(children=[[[],[],[],[]],[],[]])



def start_categories(attr,old,new):
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
    politics = [ "worldnews", "news", "nottheonion", "UpliftingNews"
            "offbeat", "gamernews", "floridaman", "energy",
            "syriancivilwar", "truecrime"]
    economics = ["Economics","business","entrepreneur","marketing","BasicIncome","business","smallbusiness",
                "stocks","wallstreetbets","stockmarket"]
    news = ["news"]
    all_topics = [sport, politics, economics, news]

    current_words = all_topics[popular_categories.active]
    calculate(current_words)


def startfunc():
    global main_layout
    text = Paragraph(text = anfrage.value)
    main_layout.children[1] = text
    status1 = Paragraph(text = 'Status: Rechne...')
    main_layout.children[0].children[3] = status1
    current_words = anfrage.value
    current_words = current_words.split(', ')
    #print(current_words)
    current_words.append(0)
    calculate(current_words)

def calculate(current_words):
    global main_layout
    status1 = Paragraph(text = 'Status: Rechne...')
    main_layout.children[0].children[3] = status1
    crawler = Crawler()
    subred_list = []
    if current_words[-1] == 0:
        for j in range(len(current_words)-1):
            searchword = current_words[j]
            subred_list_ = crawler.crawling(current_words[j])
            subred_list = subred_list + subred_list_
    else:
        subred_list = current_words
        searchword = current_words[0]
    try:
        posts = pd.read_pickle(f"daten/{searchword}.pkl")
    except:
        posts = pd.DataFrame(columns=['title','id','url', 'score', 'subreddit', 'num_comments', 'body', 'created'])

    for subreddit in subred_list:

        #str_subred = str(subreddit)
        #status1 = Paragraph(text = str_subred)
        #main_layout.children[0].children[3] = status1
        print(subreddit)
        try:
            #print(70)
            subred = crawler.subreddit(name=f"{subreddit}", limit=10_000)
            #print(71)
            for post in subred:
                #print(74)
                if post.id not in list(posts["id"]):
                    #print(76)
                    posts = posts.append({'title':post.title,'id':post.id, 'url':post.url, 'score':post.score, 'subreddit':post.subreddit, 'num_comments':post.num_comments, 'body':post.selftext, 'created':post.created},ignore_index=True)
                    #print(78)
        except:
            continue
    posts.to_pickle(f"daten/{searchword}.pkl")


    status = Paragraph(text = 'Status: Download erfolgreich')
    main_layout.children[0].children[3] = status

    create_table()




def create_table():
    words = ['GUTEN TAG', "HALLO"]
    data = {}
    for word in words:
        data[word] = str('https://news.google.com/search?q='+word+'&hl=en-US&gl=US&ceid=US:en')    
    datas = pd.DataFrame(data.items(), columns=['Word', 'News'])


 
    col1 = TableColumn(field='News', title='News' ,formatter=HTMLTemplateFormatter(template = '<a target="_blank" href="<%= News %>"><%= value %></a>'))
    col2 = TableColumn(field='Word', title='Word')
    Columns = [col2, col1] 
    data_table = DataTable(columns=Columns, source=ColumnDataSource(datas), width = 1200, height = 150)

    #Columns = [TableColumn(field=Ci, title=Ci) for Ci in datas.columns] 
    #data_table = DataTable(columns=Columns, source=ColumnDataSource(datas)) 

    main_layout.children[2] = data_table














popular_categories = RadioButtonGroup(labels=["sport", "politics", "economics", "news"], active = None)
popular_categories.on_change('active', start_categories)

anfrage = TextInput(value = 'Hier Anfrage einfügen')

go_button = Button(label = 'Start der Analyse', button_type = 'success')
go_button.on_click(startfunc)



status = Paragraph(text = 'Status: Warte auf Input')




main_layout.children[0].children[0] = anfrage
main_layout.children[0].children[1] = go_button
main_layout.children[0].children[2]= popular_categories
main_layout.children[0].children[3] = status


curdoc().add_root(main_layout)
curdoc().title = 'Trenderkennung'