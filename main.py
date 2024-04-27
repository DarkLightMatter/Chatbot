import os
import json
import openai
from dotenv import load_dotenv
from difflib import get_close_matches

# Set your OpenAI API key
load_dotenv()
openai.api_key = os.environ.get("CHATGPT_TOKEN")

# Load knowledge base from JSON file
def load_knowledge_base(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Save knowledge base to JSON file
def save_knowledge_base(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Find best match from list of questions
def find_best_match(user_question, questions):
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Get answer for a given question from knowledge base
def get_answer_for_question(question, knowledge_base):
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def chat_bot():
    knowledge_base = load_knowledge_base('knowledge_base.json')

    while True:
        user_input = input('You: ')

        if user_input.lower() == "quit":
            break

        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print("Bot: I don't know the answer. Let me consult ChatGPT. Please wait...")

            # Use ChatGPT to generate a response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )
            new_answer = response['choices'][0]['message']['content']

            print(f"Bot: ChatGPT suggests: '{new_answer}'")
            confirm = input("You: (type 'yes' to accept or anything else to provide your own answer) ")

            if confirm.lower() == 'yes':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Bot: Great! I learned a new response.")
            else:
                print("Bot: Okay, please provide the correct answer:")
                correct_answer = input("You: ")
                if correct_answer.lower() != 'skip':
                    knowledge_base["questions"].append({"question": user_input, "answer": correct_answer})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    print("Bot: Thank you for teaching me!")

if __name__ == "__main__":
    print("Press 'quit' to exit the chatbot program.")
    chat_bot()
