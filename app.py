import datetime
import os
from flask import Flask, render_template, request # type: ignore
from pymongo import MongoClient
from dotenv import load_dotenv 

load_dotenv()

def create_app():
   app = Flask(__name__)
   # client = MongoClient("mongodb+srv://smfssilva:acs985862@microblog-application.lgcjfgc.mongodb.net/")
   client = MongoClient(os.getenv("MONGODB_URI"))
   app.db = client.microblog


   @app.route("/", methods=["GET", "POST"])
   def home():
      if request.method == "POST":
         entry_content = request.form.get("content")
         formatted_date = datetime.datetime.today().strftime("%d/%m/%Y")
         app.db.entries.insert_one(({"content": entry_content, "date": formatted_date}))

      entries_with_date = [
         (
            entry["content"],
            entry["date"], datetime.datetime.strptime(entry["date"], "%d/%m/%Y").strftime("%d %b")
         )
         for entry in app.db.entries.find({})
      ]
      return render_template("home.html", entries=entries_with_date)
   

   if __name__=="__main__":
      app.run(debug=True)

   return app

