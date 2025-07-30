from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


app = Flask(__name__)

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

@app.route("/", methods=["GET"])
def Topic_Gen():
    topics = []
    if request.method == "GET":
        data = request.get_json()
        prompt = data.get("prompt", '')
        response = chat.send_message(prompt)
        answer = response.text
#     model="gemini-1.5-flash",
#     messages=[
#         {
#             "role": "user",
#             "content": prompt
#         }
#     ]
# )
#         answer = response["choices"][0]["message"]["content"]
        topics = answer.split("\n")
        topics = [t.strip("0123456789. ") for t in topics if t.strip()]


        #### Save the topics to a JSON file
        ####    -----------file path-------------     --file name--
        path = r"c:\Users\Dell\LinkedIn-automation" + r"\topics.json"
        with open(path, "w") as f:
            json.dump(topics, f, indent=4)

          ####To enhance code search how to use gemini-2.5-flash         
    return jsonify({"Topics": topics})


def Content_Gen():
    if request.method == "POST":
        data = request.get_json()
        topic = data.get("topic", '')
        response = model.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {
                    "role": "user",
                    "content": f"Generate content for the topic: {topic}"
                }
            ]
        )
        content = response["choices"][0]["message"]["content"]
        return jsonify({"content": content})
    return jsonify({"error": "Invalid request method"})



if __name__ == "__main__":
    app.run(debug=True)


