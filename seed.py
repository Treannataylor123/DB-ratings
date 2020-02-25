"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User, Movie, Rating
from datetime import datetime
# from model import Rating
# from model import Movie

from model import connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    # open the file
    for row in open("seed_data/u.user"):
        # parse a line
        row = row.rstrip()
        # parse the line futher by spliting the line by fields/catagory
        user_id, age, gender, occupation, zipcode = row.split("|")

        # created an object
        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""
    # print('Movies')

    Movie.query.delete()

    for row in open("seed_data/u.item"):
        row = row.strip().split('|')
        new_row = row[0:5]

        movie_id, title, released_at, blank_space, imdb_url = new_row

        title = title[0:-7]
        # title = title.split("(")
        # title = title[0]
        # print(title)

        format = "%d-%b-%Y"
        date = datetime.strptime(released_at, format)
        released_at = date

        movie = Movie(movie_id=movie_id, title=title, released_at=released_at,
                      imdb_url=imdb_url)

        db.session.add(movie)

    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""
    # print('Load')

    Rating.query.delete()

    for row in open("seed_data/u.data"):
        user_id, movie_id, score, timestamp = row.rstrip().split()

        rating = Rating(movie_id=movie_id, user_id=user_id,
                        score=score)

        db.session.add(rating)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # # # In case tables haven't been created, create them
    db.drop_all()
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
