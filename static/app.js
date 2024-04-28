function processInput() {
    var inputText = document.getElementById('inputText').value;
    var outputDiv = document.getElementById('output');
    outputDiv.innerHTML = '<p>User: ' + inputText + '</p>';
    // Here you can add logic to process the input text, like sending it to a backend server or performing some computation.
}