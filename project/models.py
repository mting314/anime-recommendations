from . import db

# Building user model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
    password_hash = db.Column(db.String(200))

    def __init__(self, username, password, password_hash):
        self.username = username
        self.password = password
        self.password_hash = password_hash


# Building ratings model
class Ratings(db.Model):
    __tablename__ = 'ratings'
    col_id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    anime_id = db.Column(db.Integer)
    username = db.Column(db.String(200))

    def __init__(self, col_id, userid, rating, anime_id, username):
        self.col_id = col_id
        self.userid = userid
        self.rating = rating
        self.anime_id = anime_id
        self.username = username


# Building the new recommendations model
class NewRecs(db.Model):
    __tablename__ = 'new_recs'
    index = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    anime_id = db.Column(db.Integer)
    prediction = db.Column(db.Float)

    def __init__(self, userid, anime_id, prediction):
        self.userid = userid
        self.anime_id = anime_id
        self.prediction = prediction