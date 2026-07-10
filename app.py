from flask import Flask,render_template,request
import os
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)
client=MongoClient("mongodb://localhost:27017/")
db=client["resume_analyzer"]
collection=db["uploads"]

UPLOAD_FOLDER="uploads"
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER

def allowed_file(filename):
    return filename.endswith(".pdf")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload",methods=["POST"])
def upload():
    file=request.files["resume"]

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config["UPLOAD_FOLDER"],file.filename))
        upload_time=datetime.now().strftime("%d-%m-%Y %I:%M %p")

        document = {"filename":file.filename, "upload_time":upload_time, "status": "Success"}

        collection.insert_one(document)

        return render_template("result.html",filename=file.filename,upload_time=upload_time)
    return "Only PDF files are allowed!"



if __name__ == "__main__":
    app.run(debug=True)