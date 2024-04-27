import json
import os
import openai

from flask import Flask, render_template, request
from typing import Union
from dotenv import load_dotenv
from difflib import get_close_matches #try to match best response with given input

app = Flask(__name__)

# Set your OpenAI API key
load_dotenv()
openai.api_key = os.environ.get("CHATGPT_TOKEN")
openai.debug = os.environ.get("DEBUG")

#load data from dataset file
def load_data(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Save data to dataset file
def save_data(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Find best match for user from dataset
def find_best_match(user_question: str, questions: list[str]) -> Union[str, None]:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6) #n=1 returns best answer, n=3 would return best 3. cutoff=0.6 = 60% similar
    return matches[0] if matches else None

# Get answer for question froom knowledge_base.json
def get_answer_for_question(question: str, dataset: dict) -> Union[str, None]:
    for q in dataset["questions"]:
        if q["question"] == question:
            return q["answer"]

# Initialize dataset
knowledge_base = load_data('knowledge_base.json')

# Route to handle user input
@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form['user_input']

        if user_input.lower() == "quit":
            return render_template('index.html', user_input=user_input, bot_response="Bot: Goodbye!")
        
        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            return render_template('index.html', user_input=user_input, bot_response=f'Bot: {answer}')
        else:
            bot_response = "Bot: I don't know the answer. Let me consult ChatGPT. Please wait..."

            # Use ChatGPT to generate a response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )
            new_answer = response['choices'][0]['message']['content']

            bot_response += f"\nBot: ChatGPT suggests: '{new_answer}'"
            # Prompt user for confirmation or providing a correct answer
            confirm = input("You: (type 'yes' to accept or anything else to provide your own answer) ")

            if confirm.lower() == 'yes':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_data('knowledge_base.json', knowledge_base)
                bot_response += "\nBot: Great! I learned a new response."
            else:
                print("Bot: Okay, please provide the correct answer:")
                correct_answer = input("You: ")
                if correct_answer.lower() != 'skip':
                    knowledge_base["questions"].append({"question": user_input, "answer": correct_answer})
                    save_data('knowledge_base.json', knowledge_base)
                    bot_response += "\nBot: Thank you for teaching me!"
            
            return render_template('index.html', user_input=user_input, bot_response=bot_response)
    else:
        return render_template('index.html')
