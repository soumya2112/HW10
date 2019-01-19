from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    news = mongo.db.news.find_one()
    weather = mongo.db.weather.find_one()
    image = mongo.db.image.find_one()
    facts = mongo.db.table.find_one()
    hemisphere = mongo.db.hemisphere.find_one()
    return render_template("index.html", news=news, weather=weather, facts=facts, image=image, hemisphere=hemisphere)

# Route that will trigger the scrape function
@app.route("/scrape")
def scraper():

    news = mongo.db.news
    news_data = scrape_mars.scrape_news()
    news.update({}, news_data, upsert=True)

    image = mongo.db.image
    image_data = scrape_mars.scrape_image()
    image.update({}, image_data, upsert=True)

    weather = mongo.db.weather
    weather_data = scrape_mars.scrape_weather()
    weather.update({}, weather_data, upsert=True)

    table = mongo.db.table
    table_data = scrape_mars.scrape_facts()
    table.update({}, table_data, upsert=True)

   
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
