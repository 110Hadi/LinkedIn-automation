from flask import Flask, request
from openai import OpenAI
# from dotenv import load_dotenv
# import os


client = OpenAI(
    api_key="AIzaSyALSSIVvK-CtY4zpieYvnrGxZC-MRyQry0",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    topics = []
    if request.method == "POST":
        prompt = request.form["prompt"]
        response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)
        answer = response["choices"][0]["message"]["content"]
        topics = answer.split("\n")
        topics = [t.strip("0123456789. ") for t in topics if t.strip()]


if __name__ == "__main__":
    app.run(debug=True)


