let socket = new WebSocket("ws://" + location.host + "/ws");

socket.onopen = function (e) {
    console.log("websocket opened");
    document.getElementById("conn_status").innerHTML = "connected";
    socket.send(JSON.stringify({"subscribe": ""}))
};

socket.onmessage = function (event) {
    var ul = document.getElementById("content");
    var li = document.createElement("li");
    li.appendChild(document.createTextNode(event.data));
    ul.appendChild(li);
}

socket.onclose = function (event) {
    document.getElementById("conn_status").innerHTML = "closed";
    if (event.wasClean) {
        console.log("connection closed");
    } else {
        console.log("connection died");
    }
}

socket.onerror = function (event) {
    document.getElementById("conn_status").innerHTML = "error";
    console.log("error: " + event.message)
}