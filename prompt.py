from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai
import random

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


app = Flask(__name__)

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

@app.route("/topics", methods=["GET"])
def Topic_Gen():

    try:
        topics = []
        if request.method == "GET":
            data = request.get_json()
            prompt = data.get("prompt", '')
            response = chat.send_message(prompt)
            answer = response.text

            #### Splitting the answer into topics
            topics = answer.split("\n")
            topics = [t.strip("0123456789. ") for t in topics if t.strip()]

            #### Removing Ai prompts from the topics
            # for topic in topics:
            #     if topic[0:2] != "* ":
            #         topics.remove(topic)


            #### Save the topics to a JSON file
            ####    -----------file path-------------     --file name--
            path = r"c:\Users\Dell\LinkedIn-automation" + r"\topics.json"
            with open(path, "w") as f:
                json.dump(topics, f, indent=4)

            ####To enhance code search how to use gemini-2.5-flash         
        return jsonify({"Topics": topics})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/content", methods=["GET"])
def Content_Gen():

    try:
        content: dict = {}
        # topics = []
        if request.method == 'GET':

            ####reading the topic file and storing its contents in a list
            path = r"c:\Users\Dell\LinkedIn-automation" + r"\topics.json" 
            with open(path, "r") as f:
                file_content = f.read()
                topics = json.loads(file_content)


            ####randomly select a topic from the list
            index = random.randint(0, len(topics) - 1)
            topic = topics[index]
            topics.pop(index)

            ####generate the chosen topic's content and store it in the dictionary
            prompt = f"Generate a LinkedIn post-worthy content about {topic}"
            response = chat.send_message(prompt)
            answer = response.text
            content[topic] = answer

            ####save the content to a JSON file
            path = r"c:\Users\Dell\LinkedIn-automation" + r"\content.json"
            with open(path, "w") as f:
                json.dump(content, f, indent=4)

            ####save the updated topics list back to the file
            path = r"c:\Users\Dell\LinkedIn-automation" + r"\topics.json"
            with open(path, "w") as f:
                json.dump(topics, f, indent=4)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"Content": content})



if __name__ == "__main__":
    app.run(debug=True)


