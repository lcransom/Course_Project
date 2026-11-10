from extensions import db


def initialize_database(app):
    # This uses the same SQLite database file as the original app.
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///strength_training.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Connect the database object to the Flask app.
    db.init_app(app)
