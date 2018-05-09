from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)



@app.route("/")
def index():
    marsScrape_Data = mongo.db.marsScrape_DB.find_one()
    return render_template("index.html", marsData=marsScrape_Data)


@app.route("/scrape")
def scrape():
    marsScrape_DB = mongo.db.marsScrape_DB
    #marsScrape_DB = db.marsScrape_DB
    mars_data = scrape_mars.scrape()
    print(mars_data)
    marsScrape_DB.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

