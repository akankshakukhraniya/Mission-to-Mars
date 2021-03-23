from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# Route to render index.html template using data from Mongo
@app.route('/')
def index():
    
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)


@app.route('/scrape')
def scrape_all():

    mars = mongo.db.mars
    data = scrape()
    mars.update(
        {},
        data,
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
