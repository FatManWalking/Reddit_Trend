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
bokeh serve --show main.py
in your command line while opened the folder

## Folders:
  - Daten: Got some Pickels of some Subreddits.
  - Development
