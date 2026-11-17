# Authors: Levi Ransom, Roger Major
# Date: 10/29/26
# File: database.py
# Description: Initialize the database

from extensions import db


def initialize_database(app):
    # Flask resolves this relative SQLite path inside the instance folder.
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///strength_training.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Connect the database object to the Flask app.
    db.init_app(app)
