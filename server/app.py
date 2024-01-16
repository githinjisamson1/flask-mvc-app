from flask import Flask
from flask_migrate import Migrate
from models import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_DATABASE_URI"] = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def home():
    return "Welcome to Superheroes API"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
