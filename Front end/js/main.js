function sendFormData() {

    //Get the first name and the last name stored
    const firstname = document.getElementById("fname").value;
    const lastname = document.getElementById("lname").value;

    if (firstname == "" || lastname == "") {
        alert("Please do not leave first of last name blank");
        return;
    }

    let dict = {};
    dict["fname"] = firstname;
    dict["lname"] = lastname;
    dict["type"] = "name";

    sendData(dict);
}

function sendData(dict) {
    const data = JSON.stringify(dict);

    //Create a socket
    socket = new WebSocket("ws:192.168.1.215:8080");

    // Listen for messages
    socket.addEventListener('message', function (event) {
        console.log('Message from server ', event.data);
    });

    socket.onopen = function (event) {
        socket.send(data);
    };

    socket.addEventListener('message', function (event) {
        //Write the result to the html page
        elem = document.getElementById("result")
        elem.innerHTML = `<h1>${event.data}</h1>`;
        socket.close();
    });

}
