#!/usr/bin/env python3

import json
from typing import Union
from difflib import get_close_matches #try to match best response with given input

#load Knowledge base from JSON file
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

#save data to knowledge base
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

#find best match from dictionary
def find_best_match(user_question: str, questions: list[str]) -> Union[str, None]:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6) #n=1 returns best answer, n=3 would return best 3. cutoff=0.6 = 60% similar
    return matches[0] if matches else None

#get answer for question froom knowledge_base.json
def get_answer_for_question(question: str, knowledge_base: dict) -> Union[str, None]:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
        
def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True: 
        user_input: str = input('You: ')

        if user_input.lower() == "quit":
            break
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print("Bot: I don\'t know the answer. Can you teach me?")
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Bot: Thank you, I learned a new response!")


if __name__ == "__main__":
    print("Press 'quit' to exit the chatbot program.")
    chat_bot()