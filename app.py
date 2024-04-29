from flask import Flask, render_template, request, jsonify
import json
import os
import openai
from dotenv import load_dotenv
from difflib import get_close_matches

app = Flask(__name__)

load_dotenv()
openai.api_key = os.environ.get("CHATGPT_TOKEN")

def load_knowledge_base(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_knowledge_base(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question, questions):
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question, knowledge_base):
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        knowledge_base = load_knowledge_base('knowledge_base.json')
        bot_response = ""

        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            bot_response = get_answer_for_question(best_match, knowledge_base)
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )
            bot_response = response['choices'][0]['message']['content']

            # Save the user input and bot response to knowledge_base.json
            knowledge_base["questions"].append({"question": user_input, "answer": bot_response})
            save_knowledge_base('knowledge_base.json', knowledge_base)

        return jsonify({'user_input': user_input, 'bot_response': bot_response})
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
