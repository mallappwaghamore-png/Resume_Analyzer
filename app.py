from flask import Flask,render_template,request
import os
from datetime import datetime
from pymongo import MongoClient
import pdfplumber

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
        filepath=os.path.join(app.config["UPLOAD_FOLDER"],file.filename)
        file.save(filepath)
        with pdfplumber.open(filepath) as pdf:
            text=""
            for page in pdf.pages:
                text+=page.extract_text()
            print(text)

        skills=["Python","Java","JavaScript","HTML","CSS","SQL","MongoDB","Flask","Django","React","Git","Docker"]
        found_skills=[]
        for skill in skills:
            if skill.lower() in text.lower():
                found_skills.append(skill)
        score=0
        score=len(found_skills)*10
        if score>100:
            score=100
        upload_time=datetime.now().strftime("%d-%m-%Y %I:%M %p")

        document = {"filename":file.filename, "upload_time":upload_time, "status": "Success"}
        collection.insert_one(document)
        return render_template("result.html",filename=file.filename,upload_time=upload_time,text=text,found_skills=found_skills,score=score)
    return "Only PDF files are allowed!"



if __name__ == "__main__":
    app.run(debug=True)