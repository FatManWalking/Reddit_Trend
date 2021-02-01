# Reddit_Trend
Crawling through specified Subreddits on Reddit.com to analyse Trends via NLP models.

## Usage
if you want to use this for yourself request your own credentials and create a .json file to store your secrets in.
Format:
```json
{
  "secret" : "30-chars",
  "api_id" : "14-chars",
  "username" : "your username",
  "user_agent" : "name of your app",
  "password" : "your reddit password"
}
```
## Run the Application
Start Application by running:
```git
bokeh serve --show main.py
```

## Folders:
#### ```/daten```: 
Used database in pickle format. Note: make sure to use the same enviroment as the creator of the file to ensure consistency and functionality when using pickle.

#### ```/development```
This folder contains files used to further develop and test the application and is not used in the actual application itself.


