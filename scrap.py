import requests
from bs4 import BeautifulSoup
from pprint import pprint
import datetime
import sys
import json


matchDate=input("Entrez une date (au format jj-mm-aa ou jj/mm/aa) : ")

matchDate = matchDate.replace('-', '/')
mDate = datetime.datetime.strptime(matchDate, "%d/%m/%Y")

if (mDate.date() <= datetime.datetime.today().date()) :
    id = "pjr"
else :
    matchDate = matchDate.replace('2022', '22')
    matchDate = matchDate.replace('/', '')
    id = "j" + matchDate

file= open("main.html", "w")
file.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css">
    <title>Python Parsing</title>
</head>
<body>
<div class="container mt-2">''')

baseURL = 'https://www.footao.tv/'
page = requests.get(baseURL)
soupdata = BeautifulSoup(page.content, "html.parser")
results = soupdata.find(id='pjr')

data = []

for result in results.find_all("div"):
    teams = result.find("a", class_="rc")
    time = result.find("time")
    link = result.find("a", class_="str")
    league = result.find("span", class_="ap")
    image = result.find("img", class_="im")

    imageSrc = ''


    if teams:
        teamsText = teams.text

    if link:
        linkHref = link['href']

    if image:
        imageSrc = image['src']
        imageSrc = imageSrc.replace('//www.footao.tv/', '')

    if time:
        timeText = time.text

    if league:
        leagueText = league.text

    data.append({
        'teams' : teamsText,
        'link' : teamsText,
        'image' : imageSrc,
        'time' : timeText,
        'league' : leagueText,
    }) 

    # print('teams => ', teamsText)
    # print('time => ', timeText)
    # print('link => ', linkHref)
    # print('league => ', leagueText)

    file.write(f'''

        <div class="card mt-2" style="width: 18rem;">
            <div class="card-header">
                {leagueText}
            </div>
            <img src="{baseURL + imageSrc}" class="card-img-top" alt="{leagueText}" style="width:100%; height:100%">
            <div class="card-body">
                <h5 class="card-title">{teamsText}</h5>
                <p class="card-text">{time}</p>
                <a href="{linkHref}" class="btn btn-primary">Regarder</a>
            </div>
        </div>
        '''
    )


file.write(f'''</div>
</body>
</html>''')


json_data = {'db' : data}

with open('json_data.json', 'w') as outfile:
    json.dump(json_data, outfile)



    # sys.exit()