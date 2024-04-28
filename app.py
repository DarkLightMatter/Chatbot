from flask import Flask, render_template, request, jsonify

from chatbot import get_answer_for_question

app = Flask(__name__)

#get website
@app.get("/")
def index_get():
    #loading the index.html file to dispaly on screen
    return render_template("index.html")


@app.post('/predict')
def predict():
    text = request.get_json().get("Message")
    # TODO: check if text is valid
    response = get_answer_for_question(text)   #get_response = function from chatbot to get response
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)