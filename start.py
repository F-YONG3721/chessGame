import chess_game
import socket
import json
import os

IP: str
PORT: int
COLOR: str
MODE: str
USEROS: str
CLEARPROMPT: str

switchPlayer: dict = {
    "white" : "black",
    "black" : "white"
}

def setInfo():
    global USEROS, CLEARPROMPT
    
    while True:
        USEROS = str(input("Please input your os(windows, macOS, linux): "))
        if(USEROS not in ["windows", "macOS", "linux"]):
            print("Try again")
            continue
        else:
            break
    
    CLEARPROMPT = "cls" if USEROS == "windows" else "clear"

def setMode():
    global MODE
    MODE = str(input("Please input mode(online, offline):"))

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

def checkGameContinue(board: chess_game.GameCore, draw, currentPlayer) -> bool:
    if(len(draw) == 1 and draw[0] == "surrender"):
        return False
    
    return board.checkGameContinue(currentPlayer)

def setIP():
    global IP
    IP = str(input("Please input IP: "))

def setPort():
    global PORT
    PORT = int(input("Please input PORT: "))

def buildServer() -> socket.socket:
    global IP, PORT
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        setIP()
        setPort()
        try:
            s.bind((IP, PORT))
        except Exception as e:
            print(f"Exception: {e}")
        else:
            break

    s.listen(5)
    return s

def buildClient():
    global IP, PORT
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        setIP()
        setPort()
        try:
            s.connect((IP, PORT))
        except Exception as e:
            print(f"Exception: {e}")
        else:
            break
    return s

def runServer():
    global COLOR
    server = buildServer()
    print("等待連接")
    (conn, client_addr) = server.accept()
    print("連接成功")
    print(f"Clinet IP and Port: {client_addr}")
    
    chessBoard = chess_game.GameCore()
    currentEvent = chessBoard.getLog().getCurrentEvent()
    currentPlayer = "white"
    run = True
    draw = ""

    conn.send(sendData("init", switchPlayer[COLOR], chessBoard.getBoard(), currentEvent))
    
    while run:
        currentEvent = chessBoard.getLog().getCurrentEvent()
        os.system(CLEARPROMPT)
        printBoard(chessBoard.getBoard(), COLOR)
        print(f"Event: {currentEvent}")

        if(not checkGameContinue(chessBoard, draw, currentPlayer)):
            run = False
            conn.send(sendData("gameover", currentPlayer, chessBoard.getBoard(), currentEvent))
            input("Gameover")
            break

        if(currentPlayer == COLOR):
            conn.send(sendData("wait", COLOR, chessBoard.getBoard(), currentEvent))
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
            conn.send(sendData("move", currentPlayer, chessBoard.getBoard(), currentEvent))
            message = conn.recv(2048)
            
            if(len(message) == 0):
                print("end")
                break
            
            message = json.loads(message.decode("utf-8"))
            if(message["command"] == "move"):
                isDrawCorrect = checkFormat(message["move"])
                if(not isDrawCorrect):
                    draw = message["move"]
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
    print(f"Event: {message["info"]}")
    
    run = True
    while run:
        message = client.recv(2048)
        os.system(CLEARPROMPT)
        if(len(message) == 0):
            print("end")
            run = False
            break
        message = json.loads(message.decode("utf-8"))
        printBoard(message["board"], COLOR)
        print(f"Event: {message["info"]}")

        if(message["command"] == "wait"):
            continue
        
        if(message["command"] == "move"):
            draw = input(f"Your turn, {message["color"]}, please input your move: ").split(" ")
            client.send(sendData("move", COLOR, board="", info = "", move=draw))
        elif(message["command"] == "gameover"):
            input("Gameover")
            break
    client.close()

def runOffline():
    chessGame = chess_game.ChessGame()
    chessGame.start()

if __name__ == "__main__":
    setInfo()
    setMode()

    if(MODE == "offline"):
        runOffline()
    elif(MODE == "online"):
        host = setHost()
        if(host == "server"):
            setColor()
            runServer()
        elif(host == "client"):
            runClinet()
        else:
            print("Host not exist.")
            print("Please restart.")
    

    