package main

import (
    "log"
    "net/http"
    "time"

    "github.com/gorilla/websocket"
    zmq "github.com/pebbe/zmq4"
)

const (
    writeWait = 10 * time.Second
    pongWait = 60 * time.Second
    pingPeriod = (pongWait * 9) / 10
    maxMessageSize = 512
    publisherSource = "tcp://localhost:5000"
)

var upgrader = websocket.Upgrader{}

type subscription struct {
    subscribe string
}

type Client struct {
    conn *websocket.Conn
}

func (client *Client) readPump() {
    defer func() {
        log.Printf("read pump closing")
        client.conn.Close()
    }()

    client.conn.SetReadLimit(maxMessageSize)
    client.conn.SetReadDeadline(time.Now().Add(pongWait))
    client.conn.SetPongHandler(func(string) error {
        client.conn.SetReadDeadline(time.Now().Add(pongWait))
        return nil
    })
    for {
        _, message, error := client.conn.ReadMessage()
        if error != nil {
            if websocket.IsUnexpectedCloseError(error,
                                                websocket.CloseGoingAway,
                                                websocket.CloseAbnormalClosure) {
                log.Printf("error: %v", error)
            }
            log.Printf("Breaking from reader")
            break
        }
        log.Printf("received %v", message)
    }
}

func (client *Client) writePump() {
    subscriber, _ := zmq.NewSocket(zmq.SUB)
    defer subscriber.Close()
    subscriber.Connect(publisherSource)
    subscriber.SetSubscribe("")
    for {
        message, error := subscriber.RecvMessage(0)
        if error != nil {
            log.Fatalf("Trouble reading from zeromq %v", error)
        }
        log.Printf("Received %v", message)
        data := []byte(message[1])
        error = client.conn.WriteMessage(websocket.TextMessage, data)
        if error != nil {
            log.Printf("%v\n", error)
            break
        }
    }
}

func serve(writer http.ResponseWriter, request *http.Request) {
    _client, error := upgrader.Upgrade(writer, request, nil)
    if error != nil {
        log.Print("upgrade: ", error)
        return
    }

    client := Client{_client}
    go client.readPump()
    go client.writePump()
}

func main() {
    http.HandleFunc("/ws", serve)
    http.Handle("/", http.FileServer(http.Dir("./static")))
    log.Fatal(http.ListenAndServe(":8000", nil))
}
