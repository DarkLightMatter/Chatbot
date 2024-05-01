var userInputForm = document.getElementById('user-input-form');

userInputForm.addEventListener('submit', function(event) {
    event.preventDefault();
    var inputText = document.getElementById('inputText').value;
    var outputDiv = document.getElementById('output');

    fetch('/', {
        method: 'POST',
        body: new URLSearchParams({
            'user_input': inputText
        }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.json())
    .then(data => {            
        outputDiv.innerHTML += '<p>User: ' + data.user_input + '</p>';
        outputDiv.innerHTML += '<p>Bot: ' + data.bot_response + '</p>';
    });
});
