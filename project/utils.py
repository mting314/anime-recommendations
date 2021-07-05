import re

import requests
from bs4 import BeautifulSoup

from . import db
from .models import Ratings

# custom functions
def customid():
    idquery = db.session.query(Ratings).order_by(Ratings.col_id.desc()).first()
    last_id = int(idquery.col_id)
    next_id = int(last_id) + 1
    return next_id

def user_id(userid):
    # if this user hasn't made any ratings yet
    if db.session.query(Ratings).filter(Ratings.username == userid).count() == 0:
        # find the highest id number that does exist
        idquery = db.session.query(Ratings).order_by(Ratings.userid.desc()).first()
        last_id = int(idquery.userid)
        next_id = int(last_id) + 1
        # and give an id right after it
        return next_id
    else:
        idquery = db.session.query(Ratings).filter(Ratings.username == userid).first()
        idquery_old = idquery.userid
        return idquery_old

# def search_by_anime_id()

def parse_anime_info(anime_id):
    response_string = 'https://myanimelist.net/anime/' + str(anime_id)
    page = requests.get(response_string)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find("h1", {"class": "title-name h1_bold_none"}).text

    img = soup.find("img", {"alt": title})

    description = soup.find("p", {"itemprop": "description"})

    if soup.find('span', text=re.compile('Premiered:')):
        premiered = soup.find('span', text=re.compile('Premiered:')).next_sibling.next_sibling.text
    elif soup.find('span', text=re.compile('Aired:')):
        premiered = str(soup.find('span', text=re.compile('Aired:')).next_sibling).strip()
    else:
        premiered = None
    genres = soup.find('span', text=re.compile('Genres:')).next_sibling

    genre_list = []

    for tag in genres:
        if type(tag) != str and tag.name == "span":
            genre_list.append(tag.text)

    anime = {
        "anime_id": anime_id,
        "title": title,
        "image_url": img["data-src"],
        "description": description,
        "premiered": premiered,
        "genres_list": ", ".join(genre_list)
    }

    return anime

