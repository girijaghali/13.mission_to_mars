from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

import os
#cwd = os.getcwd()
#app = Flask(__name__, template_folder=cwd)

app = Flask(__name__)

conn = 'mongodb+srv://gghali:m001-mongodb-basics@cluster0-6epwg.mongodb.net/test'
client = pymongo.MongoClient(conn) 
mars_db=client.marsScrape_DB
collection = mars_db.marsData


@app.route("/")
def index():
    marsScrape_Data = mars_db.marsData.find_one()
    return render_template("index.html", marsData=marsScrape_Data)


@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    marsD = mars_db.marsData
    marsD.update(
        {},
        mars_data,
        upsert=True
    )


    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

# code to connect without Atlas

