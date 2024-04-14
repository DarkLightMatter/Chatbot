import re

# Define patterns and corresponding responses
patterns_responses = {
    r'hi|hello|hey': 'Hello! How can I assist you?',
    r'how are you?': "I'm good. Thanks for asking! How was your day today?",
    # Add more patterns and responses as needed
}

def chatbot_response(user_input):
    # Iterate over patterns and find a match
    for pattern, response in patterns_responses.items():
        match = re.match(pattern, user_input.lower())
        if match:
            # If there's a match, return the corresponding response
            return response.format(*match.groups())
    
    # If no match is found, return a default response
    return "I'm sorry, I didn't understand that."

# Main loop for interacting with the chatbot
while True:
    user_input = input("You: ") 
    if user_input.lower() == 'exit':
        print("Chatbot: Goodbye!")
        break
    else:
        bot_response = chatbot_response(user_input)
        print("Chatbot:", bot_response)
