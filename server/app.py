from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to Superheroes"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
