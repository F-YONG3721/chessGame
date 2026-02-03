import chess_game
import socket
import json
import os

IP: str
PORT: int
COLOR: str

switchPlayer: dict = {
    "white" : "black",
    "black" : "white"
}

def setInfo():
    pass

def setMode():
    pass

def setHost():
    return str(input("Please input your host: "))

def setColor():
    global COLOR
    COLOR = str(input("Please input your color: "))

def sendData(command: str = "", color: str = "", board: list = [], info: str = "", move: list = []) -> bytes:
    data: dict = {
        "command" : command,
        "color" : color,
        "board" : board,
        "info" : info,
        "move" : move
    }
    return json.dumps(data).encode("utf-8")

def checkFormat(draw: list) -> bool:
    
    if(len(draw) != 2):
        return False
    
    if len(draw[0]) != 2 or len(draw[0]) != 2:
        return False
            
    if(draw[0][0] not in "abcedfgh" or draw[1][0] not in "abcdefgh"):
        return False

    if(draw[0][1] not in "12345678" or draw[1][1] not in "12345678"):
        return False


    return True

def printBoard(board: list, color: str):
    if(color == "white"):
        for i in board:
            print("-"*(6*len(i)))
            for j in i:
                    print(f"{j:^5s}", end="|")
            print()
    else:
        for i in range(len(board)-2, -1, -1):
            print("-"*(6*len(board)))
            print(f"{board[i][0]:^5s}", end="|")
            for j in range(len(board[i])-1, 0, -1):
                print(f"{board[i][j]:^5s}", end="|")
            print()
        print("-"*(6*len(board)))

        print(f"{" ":^5s}", end="|")
        for i in range(len(board)-1, 0, -1):
            print(f"{board[len(board)-1][i]:^5s}", end="|")
        print()

def setIP():
    global IP
    IP = str(input("Please input IP: "))

def setPort():
    global PORT
    PORT = int(input("Please input PORT: "))

def buildServer() -> socket.socket:
    global IP, PORT
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    s.listen(5)
    return s

def buildClient():
    global IP, PORT
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    return s

def runServer():
    global COLOR
    server = buildServer()
    print("等待連接")
    (conn, client_addr) = server.accept()
    print("連接成功")
    print(f"Clinet IP and Port: {client_addr}")
    
    chessBoard = chess_game.GameCore()
    currentPlayer = "white"
    run = True
    conn.send(sendData("init", switchPlayer[COLOR], chessBoard.getBoard()))
    
    while run:
        os.system("clear")
        printBoard(chessBoard.getBoard(), COLOR)
        if(not chessBoard.checkGameContinue(currentPlayer)):
            run = False
            conn.send(sendData("gameover", currentPlayer, chessBoard.getBoard()))
            input("Gameover")
            break

        if(currentPlayer == COLOR):
            conn.send(sendData("wait", COLOR, chessBoard.getBoard()))
            draw: list = input("Your turn, please input your move: ").split(" ")
            isDrawCorrect: bool = checkFormat(draw)

            if(not isDrawCorrect):
                continue

            if(chessBoard.inputMove(draw[0], draw[1], currentPlayer)):
                print("success")
                currentPlayer = switchPlayer[currentPlayer]
            else:
                print("continue")
                continue
        else:
            conn.send(sendData("move", currentPlayer, chessBoard.getBoard()))
            message = conn.recv(2048)
            if(len(message) == 0):
                print("end")
                break
            
            message = json.loads(message.decode("utf-8"))

            if(message["command"] == "surrender"):
                run = False
                conn.send(sendData("gameover", currentPlayer, chessBoard.getBoard()))
                input("Gameover")
                break

            elif(message["command"] == "move"):
                isDrawCorrect = checkFormat(message["move"])
                if(not isDrawCorrect):
                    continue

                if(chessBoard.inputMove(message["move"][0], message["move"][1], currentPlayer)):
                    currentPlayer = switchPlayer[currentPlayer]
                else:
                    continue
    server.close()

def runClinet():
    global COLOR
    board: list
    client = buildClient()
    message = client.recv(2048)
    if(len(message) == 0):
        print("END")
        return
    message = json.loads(message.decode("utf-8"))

    if(message["command"] == "init"):
        globals()["COLOR"] = message["color"]
        globals()["board"] = message["board"]
    
    printBoard(message["board"], COLOR)
    
    run = True
    while run:
        message = client.recv(2048)
        os.system("clear")
        if(len(message) == 0):
            print("end")
            run = False
            break
        message = json.loads(message.decode("utf-8"))
        printBoard(message["board"], COLOR)

        if(message["command"] == "wait"):
            continue
        
        if(message["command"] == "move"):
            
            draw = input(f"Your turn, {message["color"]}, please input your move: ").split(" ")
            client.send(sendData("move", COLOR, board="", info = "", move=draw))
        elif(message["command"] == "gameover"):
            globals()["board"] = message["board"]
            input("Gameover")
            break
    client.close()

if __name__ == "__main__":
    mode = setMode()
    host = setHost()
    setIP()
    setPort()

    if(host == "server"):
        setColor()
        runServer()
    elif(host == "client"):
        runClinet()
    

    