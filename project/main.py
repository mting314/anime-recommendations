import re
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from flask import render_template, request, session, Blueprint

from . import db
from .models import Ratings, NewRecs
from .utils import user_id, customid, parse_anime_info

main = Blueprint('main', __name__)



# Home page
@main.route('/')
def index():
    return render_template("base.html")


# loads the user profile
@main.route('/profile', methods=['GET', 'POST'])
def get_profile():
    if request.method == 'GET':
        userid = user_id(session.get('username'))
        username = session.get('username')
        ratings = db.session.query(Ratings).filter(Ratings.userid == userid).all()

        ratings_list = []
        for i in ratings:
            ratings_list.append([i.anime_id, i.rating])

        animes = []
        for i in ratings_list:
            anime = parse_anime_info(i[0])
            anime.update({"rating": i[1]})
            animes.append(anime)

        return render_template('profile.html', recs=animes, username=username)
    else:
        return 'Error in login process...'


# search books page
@main.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        animes = []
        response_string = "https://myanimelist.net/anime.php?cat=anime&q=" + quote(request.form.get("title")) + "&type=0&score=0&status=0&p=0&r=0&sm=0&sd=0&sy=0&em=0&ed=0&ey=0&c%5B%5D=a&c%5B%5D=b&c%5B%5D=c&c%5B%5D=f&gx=0"
        if request.form.get("genre"):
            response_string += "&genre%5B%5D=" + request.form.get("genre")

        page = requests.get(response_string)

        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find("div", {"class": "js-categories-seasonal js-block-list list"})
        if results is None:
            return render_template("searchResults.html", animes=None)
        results = results.find("table").find_all("tr")[1:]
        for result in results:
            image_url = result.find("td").find("img")["data-src"]
            image_url = image_url.replace("r/50x70/", "").replace("r/100x140/", "")

            info_data = result.find_all("td")[1].find("a")
            title = info_data.text

            raw_anime_url = info_data['href']
            matches = re.search("\/anime\/([\d]*?)\/", raw_anime_url)
            # check if this is actually an anime div we found
            if matches:
                # need to replace the tiny search result images with the full ones

                anime_id = matches[1]
                animes.append({
                    "image_url": image_url,
                    "anime_id": anime_id,
                    "title": title
                })

        if not request.form.get("title"):
            return "Please enter a book title below."

        return render_template("searchResults.html", animes=animes)

    else:
        username = session.get('username')
        return render_template("search.html", username=username)


# book details route
@main.route("/bookDetails/<anime_id>")
def bookDetails(anime_id):
    return render_template("bookDetails.html", book=parse_anime_info(anime_id))


# submitting new book ratings
@main.route("/new-rating", methods=['POST'])
def postnew():
    if request.method == 'POST':
        col_id = customid()
        userid = user_id(session.get('username'))
        rating = request.form['rating']
        anime_id = request.form.get('bookid')
        username = session.get('username')

        data = Ratings(col_id, userid, rating, anime_id, username)
        db.session.add(data)
        db.session.commit()
        return render_template('success.html')


# getting book recommendations
@main.route("/recs", methods=['GET'])
def getrecs():
    if request.method == 'GET':
        userid = user_id(session.get('username'))
        recs = db.session.query(NewRecs).filter(NewRecs.userid == userid).all()

        bk = [parse_anime_info(i.anime_id) for i in recs]

        book = dict(work=bk) if len(bk) > 0 else None
        return render_template('recs.html', recs=book)
    else:
        return "No Data"


if __name__ == '__main__':
    main.run()
