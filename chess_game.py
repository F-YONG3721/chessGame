import os
import copy

class Board:
    BOARD_SIZE = 9
    event = None
    log = None
    board: list = None
    attackList: list = None
    enPassantDict: dict = None  #{key: 儲存執行的棋子, value: 儲存可被吃的棋子}
    kingLocation: dict = None 

    # 初始化棋盤
    def __init__(self, log):
        # 初始化所有資料
        self.board = [[" " for i in range(self.BOARD_SIZE)] for j in range(self.BOARD_SIZE)]
        self.log = log
        self.enPassantDict = dict()
        self.kingLocation = {"white": (), "black": ()}

        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                # 設定棋盤座標
                if j == 0 and i != self.BOARD_SIZE - 1:
                    self.board[i][j] =  str((self.BOARD_SIZE - 1) - i)
                elif i == self.BOARD_SIZE - 1 and j != 0:
                    self.board[i][j] = chr(96 + j)
        
        # 設定棋子
        self.__setChess()

        # 設定國王的位置
        self.__initKingLocation()

        # 設定Event
        self.event = Event(self.log)

        # 建立攻擊範圍表
        self.attackList = self.event.buildAttackList("white", self)
        
    # 印出棋盤 
    def print_board(self):
        print("-"*(6*self.BOARD_SIZE))
        print(f"{'ChessGeme':^54s}")
        for i in range(self.BOARD_SIZE):
            print("-"*(6*self.BOARD_SIZE))
            for j in range(self.BOARD_SIZE):
                if(type(self.board[i][j]) == str):
                    print(f"{self.board[i][j]:^5s}", end="|")
                else:
                    print(f"{self.board[i][j].kind:^5s}", end="|")
    
            print()

    # 移動棋子
    def moveChess(self, currentPosition, nextPosition, playerGroup):
        # 轉換座標
        currentX = self.__standardPosition(currentPosition[0])
        currentY = self.__standardPosition(currentPosition[1])

        nextX = self.__standardPosition(nextPosition[0])
        nextY = self.__standardPosition(nextPosition[1])

        chessKind = self.board[currentY][currentX]  # 取得棋子類型

        # 檢查玩家移動的是自己的棋子 
        if type(chessKind) != str and chessKind.group != playerGroup:
            self.log.setCurrentEvent("ERROR group is not same")
            return False
        
        # 檢查是否符合易位的規則
        if type(chessKind) == King and abs(currentX - nextX) == 2 and self.event.checkCastling(currentX, currentY, nextX, nextY, self):
            # 找出城堡的位置
            x = (nextX - currentX)//abs(nextX - currentX) 
            y = currentY - nextY

            rookCurrentX = currentX 
            rookCurrentY = currentY

            while 1 <= rookCurrentX <= 8 and 0 <= rookCurrentY <= 7:

                if type(self.board[rookCurrentY][rookCurrentX]) == Rook:
                    break
                else:
                    rookCurrentX += x
                    rookCurrentY += y 
            
            # 易位
            self.__draw(currentX, currentY, nextX, nextY)
            self.__draw(rookCurrentX, rookCurrentY, nextX - x, nextY)

            # 將棋子設定成已移動過
            chessKind.setEverMove()
            self.board[nextY][nextX - x].setEverMove() # 城堡的位置
            
            # 建立攻擊表
            self.attackList = self.event.buildAttackList(chessKind.group, self)
            self.clearEnPassantDict(chessKind.group)

            # 更新日誌
            message: str = "o-o" if abs(currentX-rookCurrentX) == 3 else "o-o-o"
            self.log.writeChessManual(message)

            return True


        # 檢查是否符合移動規則
        if self.event.checkMoveRule(currentX, currentY, nextX, nextY, self):     
            # 檢查小兵是否升變(promotion) 
            if type(chessKind) == Pawn:
                self.event.checkPromotion(currentX, currentY, nextX, nextY, self)

            self.__draw(currentX, currentY, nextX, nextY)
            
            # 將棋子設定成已移動過
            chessKind.setEverMove() 

            # 建立攻擊表
            self.attackList = self.event.buildAttackList(chessKind.group, self)

            message: str = (chessKind.kind + currentPosition + nextPosition)
            self.log.writeChessManual(message)
            return True
        else:
            return False

    # 下棋
    def __draw(self, currentX, currentY, nextX, nextY):  
        chessKind = self.board[currentY][currentX]  # 取得棋子

        if(type(chessKind) == King):
            self.kingLocation[chessKind.group] = tuple([nextX, nextY])

        self.board[currentY][currentX] = " "        # 清空原本位置
        self.board[nextY][nextX] = chessKind        # 移動到新位置

    # 將字元轉成正確的數字格式
    def __standardPosition(self, position):
        if(position.isalpha()):
            position = ord(position) - ord('a') + 1
        elif(position.isdigit()):
            position = 9 - int(position)-1

        return position
    
    # 設定棋子到初始位置上
    def __setChess(self):
        for i in range(self.BOARD_SIZE):
            if(i != 0):
                self.board[1][i] = Pawn("♟", "black")
                self.board[6][i] = Pawn("♙", "white")

            if(i == 1 or i == 8):
                self.board[0][i] = Rook("♜", "black")
                self.board[7][i] = Rook("♖", "white")
            
            if(i == 2 or i == 7):
                self.board[0][i] = Knight("♞", "black")
                self.board[7][i] = Knight("♘", "white")

            if(i == 3 or i == 6):
                self.board[0][i] = Bishop("♝", "black")
                self.board[7][i] = Bishop("♗", "white")

            if(i == 5):
                self.board[0][i] = King("♚", "black")
                self.board[7][i] = King("♔", "white")

            if(i == 4):
                self.board[0][i] = Queen("♛", "black")
                self.board[7][i] = Queen("♕", "white")
    
    # 印出攻擊範圍表
    def printAttackList(self):
        for i in range(self.BOARD_SIZE):
            print("-"*6*self.BOARD_SIZE)
            for j in range(self.BOARD_SIZE):
                info: dict = self.attackList[i][j]
                if(i <= 7 and j > 0):
                    num = len(info["attacker"])
                    print(f"{(str(num) if num > 0 else info["symbol"]):^5s}", end = "|")
                elif(j == 0 and i != 8):
                    print(f"{str(8-i):^5s}", end = "|")
                elif(i > 7 and j > 0):
                    print(f"{chr(96 + j):^5s}", end = "|")
                else:
                    print(f"{info["symbol"]:^5s}", end = "|")
            
            print()
        
        print("-"*54)

    # 印出移動表
    def printMoveList(self):
        moveList = self.event.buildMoveList("white", self)
        for i in range(self.BOARD_SIZE):
            print("-"*6*self.BOARD_SIZE)
            for j in range(self.BOARD_SIZE):
                info: dict = moveList[i][j]
                if(i <= 7 and j > 0):
                    num = len(info["mover"])
                    print(f"{(str(num) if num > 0 else info["symbol"]):^5s}", end = "|")
                elif(j == 0 and i != 8):
                    print(f"{str(8-i):^5s}", end = "|")
                elif(i > 7 and j > 0):
                    print(f"{chr(96 + j):^5s}", end = "|")
                else:
                    print(f"{info["symbol"]:^5s}", end = "|")
            
            print()

    # 清除過路兵許可表
    def clearEnPassantDict(self, group):
        # 先複製一份過路兵許可表, 避免在迴圈中刪除元素造成錯誤
        nowEnPassantDict = self.enPassantDict.copy()
        for chessKind in nowEnPassantDict.keys():
            if chessKind.group == group:
                self.enPassantDict.pop(chessKind)

    # 印出過路兵許可表
    def printEnpassantDict(self):
        if len(self.enPassantDict) != 0:
            print(f"en passant: \n\t", end = "")
            for chessKind in self.enPassantDict.items():
                print(f"[ capture: {chessKind[0].group}{chessKind[0].kind} ,  be captured: {chessKind[1].group}{chessKind[1].kind} ]", end=" ,  ")
            print()

    # 設定國王位置
    def __initKingLocation(self):
        self.kingLocation["white"] = (5, 7)
        self.kingLocation["black"] = (5, 0)

    # 假裝移動成功，回傳board的副本
    def nextStatus(self, currentX, currentY, nextX, nextY):
        tempBoard = copy.deepcopy(self)
        tempBoard.__draw(currentX, currentY, nextX, nextY)
        return tempBoard


class Event:
    log = None

    switchGroup: dict = {
        "white": "black",
        "black": "white"
    }

    def __init__(self, log):
        self.log = log
        

    # 檢查是否符合移動規則
    def checkMoveRule(self, currentX, currentY, nextX, nextY, board: Board):

        chessKind = board.board[currentY][currentX] # 取得棋子
        targetLocation = board.board[nextY][nextX] # 取得目標位置的狀態

        #check not over the board
        if nextX  < 1 or nextX > 8 or nextY < 0 or nextY > 7:
            self.log.setCurrentEvent("ERROR out of range")
            return False

        # check chessKind is a chess
        if type(chessKind) == str:
            self.log.setCurrentEvent("ERROR not chess")
            return False

        # check group
        if type(targetLocation) != str and targetLocation.group == chessKind.group:
            self.log.setCurrentEvent("ERROR group is same")
            return False

        # check move, eat
        checkBlock = self.checkBlock(currentX, currentY, nextX, nextY, board)
        checkMove = chessKind.checkMove(currentX, currentY, nextX, nextY) and type(targetLocation) == str
        checkEat = chessKind.checkEat(currentX, currentY, nextX, nextY) and type(targetLocation) != str
            
        

        # 把小兵吃子與移動的規則區隔開來 
        if type(chessKind) == Pawn:
            checkMove = checkMove and type(targetLocation) == str

        # 騎士不受中間有其他棋子擋住的限制 
        if type(chessKind) != Knight:
            checkEat = checkEat and checkBlock
            checkMove = checkMove and checkBlock

        # 檢查小兵是否吃過路兵(en passant)
        if type(chessKind) == Pawn and (chessKind.checkEat(currentX, currentY, nextX, nextY) and type(targetLocation) == str):
            # 確認吃過路兵的方向是正確的(旁邊的小兵會被吃掉)
            opponentPawnX = None
            opponentPawnY = None

            # 記錄過路兵的位置
            if (chessKind.group == "white") and type(board.board[nextY + 1][nextX]) == Pawn:
                opponentPawnX = nextX
                opponentPawnY = nextY + 1
            elif (chessKind.group == "black") and type(board.board[nextY - 1][nextX]) == Pawn:
                opponentPawnX = nextX
                opponentPawnY = nextY - 1
            
            # 小兵是否可執行過路兵規則
            if(chessKind in board.enPassantDict.keys()) and opponentPawnX != None and opponentPawnY != None:
                if(board.enPassantDict.get(chessKind) == board.board[opponentPawnY][opponentPawnX]):
                    board.board[opponentPawnY][opponentPawnX] = " " # 將被吃的小兵移除
                    board.clearEnPassantDict(chessKind.group)
                    self.log.setCurrentEvent("En passant")
                    return True
        
        # 檢查小兵是否觸發過路兵規則(en passant)
        if type(chessKind) == Pawn and abs(currentY - nextY) == 2 and checkMove:
            if (nextX - 1) >= 1 and type(board.board[nextY][nextX - 1]) == Pawn and board.board[nextY][nextX - 1].group != chessKind.group:
                board.enPassantDict.setdefault(board.board[nextY][nextX - 1], chessKind) # 將可被吃的棋子加入到許可表中
            
            if (nextX + 1) <= 8 and type(board.board[nextY][nextX + 1]) == Pawn and board.board[nextY][nextX + 1].group != chessKind.group:
                board.enPassantDict.setdefault(board.board[nextY][nextX + 1], chessKind)

        # 檢查是否符合規則
        if not (checkMove or checkEat):
            self.log.setCurrentEvent("ERROR Against the rules")
            return False
        
        # 檢查國王是否受到攻擊
        tempBoard: Board = board.nextStatus(currentX, currentY, nextX, nextY)
        kingLocation = tempBoard.kingLocation[chessKind.group]
        attackList = self.buildAttackList(self.switchGroup[chessKind.group], tempBoard)
        kingAttack: bool = attackList[kingLocation[1]][kingLocation[0]]["symbol"] == "X"

        if(kingAttack):
            self.log.setCurrentEvent("ERROR the king is check")
            return False

        board.clearEnPassantDict(chessKind.group)             
        return True
    
    # 檢查是否有其他棋子擋住
    def checkBlock(self, currentX, currentY, nextX, nextY, board: Board):
        # 找出尋找的方向
        x = 0 if currentX == nextX else (nextX - currentX) // abs(nextX - currentX)
        y = 0 if currentY == nextY else (nextY - currentY) // abs(nextY - currentY)

        # 檢查是否有其他棋子擋住
        while(currentX != nextX or currentY != nextY):
            currentX += x
            currentY += y

            # 如果檢查到要移動到的格子就跳出
            if (currentX == nextX and currentY == nextY):
                break
            
            # 如過超出邊界就跳出
            if currentX < 1 or currentX > 8 or currentY < 0 or currentY > 7:
                break

            # 如果有遇到棋子則回傳False
            if type(board.board[currentY][currentX]) != str:
                return False
        
        
        return True
    
    # 檢查是否升變
    def checkPromotion(self, currentX, currentY, nextX, nextY, board: Board):
        if not (nextY == 0 or nextY == 7):
            return
        kind = str(input("小兵即將生變，請選擇生變後的棋子\n Queen(Q), Bishop(B), Knight(N), Rook(R): "))
        chessKind = board.board[currentY][currentX]
        if kind == "Q":
            board.board[currentY][currentX] = (Queen("♕", "white") if (chessKind.group == "white") else Queen("♛", "black"))
        elif kind == "B":
            board.board[currentY][currentX] = (Bishop("♗", "white") if (chessKind.group == "white") else Bishop("♝", "black"))
        elif kind == "N":
            board.board[currentY][currentX] = (Knight("♘", "white") if (chessKind.group == "white") else Knight("♞", "black"))
        elif kind == "R":
            board.board[currentY][currentX] = (Rook("♖", "white") if (chessKind.group == "white") else Rook("♜", "black"))
        else:
            print("輸入錯誤請重新輸入")
            self.checkPromotion(currentX, currentY, nextX, nextY, board)

    # 檢查王車易位
    def checkCastling(self, currentX, currentY, nextX, nextY, board: Board):

        chessKind = board.board[currentY][currentX] # 記錄國王位置
        rookLocation = None # 記錄城堡的位置
         
        noAttack = True # 記錄移動路徑是否受到攻擊
        noChess = True # 記錄中間是否有其他棋子

        # 記錄移動的方向
        x = (nextX - currentX)//abs(nextX - currentX) 
        y = currentY - nextY

        pointX = currentX # 記錄目前的位置
        pointY = currentY # 記錄目前的位置

        # y軸不能移動
        if y != 0:
            return False

        # 檢查各項條件
        while 1 <= pointX <= 8 and 0 <= pointY <= 7:
            currentLocation = board.board[pointY][pointX]

            # 找到城堡
            if type(currentLocation) == Rook:
                rookLocation = board.board[pointY][pointX]
                break # 找到城堡就退出
            
            # 確認中間沒有其他棋子
            if type(currentLocation) != str and type(currentLocation) != Rook and type(currentLocation) != King:
                print(f"中間有其他棋子")
                noChess = False

            # 確認國王的移動範圍未受到攻擊
            if abs(currentX - pointX) <= 2 and board.attackList[pointY][pointX]["symbol"] == "X":
                board.printAttackList()
                print(f"受到攻擊")
                noAttack = False

            pointX += x

            # 超出範圍
            if (1 <= pointX <= 8 and 0 <= pointY <= 7) == False:
                print(f"超出範圍")
                if(rookLocation == None):
                    print(f"找不到城堡")
                    return False
                
                break
            

        # 確認城堡與國王未移動過
        everMoveRook = rookLocation.getEverMove()
        everMoveKing = chessKind.getEverMove()

        # 確認是否符合易位的規則
        if not(everMoveRook or everMoveKing) and noChess and noAttack and rookLocation != None:
            # 將國王與城堡設定成已被移動過
            rookLocation.setEverMove()
            chessKind.setEverMove()
            return True
        else:
            return False
    
    # 建立攻擊範圍表
    def buildAttackList(self, group, board: Board):
        attackList = [[{"symbol":" ", "attacker":[]} for i in range(board.BOARD_SIZE)] for j in range(board.BOARD_SIZE)]
        
        for currentY in range(board.BOARD_SIZE - 1):
            for currentX in range(1, board.BOARD_SIZE):
                
                chessKind = board.board[currentY][currentX]

                # 確認chessKind是棋子
                if type(chessKind) == str:
                    continue 

                # 避免後來的棋子蓋過原本棋子的攻擊範圍
                if attackList[currentY][currentX]["symbol"] != "X":
                    attackList[currentY][currentX]["symbol"] = chessKind.kind

                # 確認是同一方的棋子
                if chessKind.group != group:
                    continue

                # 讀取棋子攻擊的方向
                for direction in chessKind.checkAttack():
                    
                    # 可以攻擊的點
                    x = currentX + direction[0]
                    y = currentY + direction[1]
                    
                    # 在棋盤內尋找可以攻擊的點
                    while 1 <= x <= 8 and 0 <= y <= 7:
                        targetLocation = board.board[y][x] # 棋盤上的位置

                        checkEat = chessKind.checkEat(currentX, currentY, x, y) 

                        # 如果不符合吃子的規則就退出
                        if checkEat == False:
                            break
                        
                        # 如果是可以攻擊的點就畫上"X"
                        if type(targetLocation) == str:
                            attackList[y][x]["symbol"] = "X"
                            attackList[y][x]["attacker"].append(tuple([currentX, currentY]))
                        elif targetLocation.group != group:
                            attackList[y][x]["symbol"] = "X"
                            attackList[y][x]["attacker"].append(tuple([currentX, currentY]))
                            break
                        else:
                            break
                        
                        # 往下個點繼續找
                        x += direction[0]
                        y += direction[1]
        
        return attackList 

    # 建立移動範圍表
    def buildMoveList(self, group, board: Board):
        moveList = [[{"symbol":" ", "mover":[]} for i in range(board.BOARD_SIZE)] for j in range(board.BOARD_SIZE)]
        
        for currentY in range(board.BOARD_SIZE - 1):
            for currentX in range(1, board.BOARD_SIZE):
                
                chessKind = board.board[currentY][currentX]

                # 確認chessKind是棋子
                if type(chessKind) == str:
                    continue 

                # 避免後來的棋子蓋過原本棋子的攻擊範圍
                if moveList[currentY][currentX]["symbol"] != "X":
                    moveList[currentY][currentX]["symbol"] = chessKind.kind

                # 確認是同一方的棋子
                if chessKind.group != group:
                    continue

                other: list = []
                if type(chessKind) == Pawn:
                    other = [(0, -1) if (group == "white") else (0, 1)] 

                # 讀取棋子攻擊的方向
                for direction in (chessKind.checkAttack() + other):
                    # 可以攻擊的點
                    x = currentX + direction[0]
                    y = currentY + direction[1]
                    
                    # 在棋盤內尋找可以攻擊的點
                    while 1 <= x <= 8 and 0 <= y <= 7:
                        targetLocation = board.board[y][x] # 棋盤上的位置
                        patternData: dict = moveList[y][x]
                        
                        checkMove = chessKind.checkMove(currentX, currentY, x, y) 
                        checkEat = chessKind.checkEat(currentX, currentY, x, y)

                        if(not checkMove and type(chessKind) == Pawn):
                            checkEat = chessKind.checkEat(currentX, currentY, x, y)
                            
                        # 如果不符合吃子的規則就退出
                        if not (checkMove or checkEat):
                            break
                        
                        # 如果是可以攻擊的點就畫上"X"
                        if type(targetLocation) == str:
                            patternData["symbol"] = "X"
                            patternData["mover"].append(tuple([currentX, currentY]))
                        elif targetLocation.group != group and checkEat:
                            patternData["symbol"] = "X"
                            patternData["mover"].append(tuple([currentX, currentY]))
                            break
                        else:
                            break
                        
                        # 往下個點繼續找
                        x += direction[0]
                        y += direction[1]
        
        return moveList 

    # 檢查國王是否可以解除攻擊狀態
    def isKingInCheck(self, group, board: Board):        
        tempBoard: Board = copy.deepcopy(board)
        attackList = self.buildAttackList(self.switchGroup[group], tempBoard)
        
        kingLocation = tempBoard.kingLocation[group]
        kingX: int = kingLocation[0]
        kingY: int = kingLocation[1]
        king: Chess = tempBoard.board[kingY][kingX]

        if(attackList[kingY][kingX]["symbol"] != "X"):
            return True

        # step1 檢查國王是否可以透過移動自己解除攻擊狀態
        for direction in king.checkAttack():
            x: int = direction[0]
            y: int = direction[1]
            if (kingX+x < 1 or kingX+x > 8) or (kingY+y < 0 or kingY+y > 7):
                continue
            if(self.checkMoveRule(kingX, kingY, kingX+x, kingY+y, tempBoard)):
                return True
        
        # step2 檢查是否可以透過移動其他棋子解除國王受攻擊的狀態
        moveList = self.buildMoveList(group, tempBoard)

        # ... 對所有的攻擊者都檢查是否自己有棋子透過移動可解除...
        for attacker in attackList[kingY][kingX]["attacker"]:
            attackerX: int = attacker[0]
            attackerY: int = attacker[1]
            # 確認攻擊者的方位
            x: int = 0 if kingX == attackerX else (attackerX-kingX) // abs(attackerX-kingX) 
            y: int = 0 if kingY == attackerY else (attackerY-kingY) // abs(attackerY-kingY) 

            currentX = kingX+x
            currentY = kingY+y

            # 讀取路線上和自己同群的棋子並且確認它可不可以到這個點 
            while 1 <= currentX <= 8 and 0 <= currentY <= 7:
                # 遍歷路線上的己方棋子
                for friendlyPiece in moveList[currentY][currentX]["mover"]:
                    friendlyPieceX = friendlyPiece[0]
                    friendlyPieceY = friendlyPiece[1]

                    if(self.checkMoveRule(friendlyPieceX, friendlyPieceY, currentX, currentY, tempBoard)):
                        return True
                
                # 當遍歷到攻擊者時就退出
                if(currentX == attackerX and currentY == attackerY):
                    break

                currentX += x
                currentY += y
        # 確認國王到攻擊者的位置
        # 對每個位置找有沒有自己的棋子可以到
        return False


class Log:
    __chessManual: list  # 記錄棋子的移動
    __eventLog: list     # 記錄發生的事件(ex: 棋子移動, 移動錯誤, ...)
    __step: int          # 記錄現在是第幾回合
    currentEvent: str  # 記錄現在所發生的事件
    
    def __init__(self):
        self.__chessManual = []
        self.__eventLog = []
        self.__step = 1
        self.currentEvent = "Initial"
        self.addEvent("Initial")
    
    def getChessManual(self):
        return copy.deepcopy(self.__chessManual)
    
    def getEventLog(self):
        return copy.deepcopy(self.__eventLog)

    def getCurrentEvent(self):
        return self.currentEvent
    
    def getStep(self):
        return copy.deepcopy(self.__step)
    
    def writeChessManual(self, message: str):
        self.setCurrentEvent("Move chess, "+message)
        if self.__step != len(self.__chessManual):
            self.__chessManual.append([message])
        else:
            self.__chessManual[self.__step-1].append(message)
            self.__step += 1
        
    def addEvent(self, message: str):
        self.__eventLog.append(str(self.__step) + ": " + message)

    def setCurrentEvent(self, message: str):
        self.addEvent(message)
        self.currentEvent = message


class Chess:
    __evenMove = False
    def __init__(self, kind, group): 
        self.kind = kind
        self.group = group
    
    def setEverMove(self):
        self.__evenMove = True
    
    def getEverMove(self):
        return self.__evenMove


class King(Chess):
    def checkMove(self, x1, y1, x2, y2):
        if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
            return True
        else:
            return False
    
    def checkEat(self, x1, y1, x2, y2):
        return self.checkMove(x1, y1, x2, y2)

    def checkAttack(self):
        return [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    

class Queen(Chess):
    def checkMove(self, x1, y1, x2, y2):
        if abs(x1 - x2) == abs(y1 - y2) or x1 == x2 or y1 == y2:
            return True
        else:
            return False
    
    def checkEat(self, x1, y1, x2, y2):
        return self.checkMove(x1, y1, x2, y2)
    
    def checkAttack(self):
        return [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


class Bishop(Chess):
    def checkMove(self, x1, y1, x2, y2):
        if abs(x1 - x2) == abs(y1 - y2):
            return True
        else:
            return False
    
    def checkEat(self, x1, y1, x2, y2):
        return self.checkMove(x1, y1, x2, y2)

    def checkAttack(self):
        return [(1, 1), (1, -1), (-1, -1), (-1, 1)]


class Knight(Chess):
    def checkMove(self, x1, y1, x2, y2):
        if abs(x1 - x2) == 1 and abs(y1 - y2) == 2:
            return True
        elif abs(x1 - x2) == 2 and abs(y1 - y2) == 1:
            return True
        else:
            return False
    
    def checkEat(self, x1, y1, x2, y2):
        return self.checkMove(x1, y1, x2, y2)
    
    def checkAttack(self):
        return [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]


class Rook(Chess):
    def checkMove(self, x1, y1, x2, y2):
        if x1 == x2 or y1 == y2:
            return True
        else:
            return False
    
    def checkEat(self, x1, y1, x2, y2):
        return self.checkMove(x1, y1, x2, y2)
    
    def checkAttack(self):
        return [(0, 1), (0, -1), (-1, 0), (1, 0)]


class Pawn(Chess):
    def checkMove(self, x1, y1, x2, y2):
        x = x2 - x1
        y = y2 - y1

        if not(self.getEverMove()):
            if((y <= 2 and self.group == "black") or (y >= -2 and self.group == "white")) and x == 0:
                return True
            else:
                return False
        else:
            if((y == 1 and self.group == "black") or (y == -1 and self.group == "white")) and x == 0:
                return True
            else:
                return False
            
    def checkEat(self, x1, y1, x2, y2):
        x = x2 - x1
        y = y2 - y1

        if((y == 1 and self.group == "black") or (y == -1 and self.group == "white")) and (abs(x) == 1):
            return True
        else:
            return False
    
    def checkAttack(self):
        if self.group == "white":
            return [(-1, -1), (1, -1)]
        elif self.group == "black":
            return [(-1, 1), (1, 1)]
    
    def setFistMove(self):
        self.__firstMove = False
    
    def getFirstMove(self):
        return self.__firstMove


class ChessGame:
    def __init__(self):
        self.log = Log()
        self.currentPlayer = "white"
        self.chessBoard = Board(self.log)
        self.__usersystem = "windows"
        self.__clearprompt = "cls"
        self.setUserSystem()
        self.switchPlayer = {
            "white" : "black",
            "black" : "white"
        }
        
    def start(self):
        while(True):
            os.system(self.__clearprompt) # 清空畫面
            self.printChessBoard() #
            print(f"Event: {self.log.getCurrentEvent()}")

            if(not self.checkGameContinue()):
                break
            
            # 可以從這裡決定哪個玩家輸入
            control = input(f"Your move, {self.currentPlayer}, please input position: ").split(" ")
                
            try:
                # 檢查是否符合輸入格式
                if(not self.checkFormat(control)):
                    if(not self.checkGameContinue(control)):
                        break
                    raise Exception("Input Error")
            except Exception as e:
                print(f"Error: {e}")
                control = input("continue?: ")
                if control == "q":
                    self.printFinalInfo()
                    break
            else:
                if self.chessBoard.moveChess(control[0], control[1], self.currentPlayer):
                    self.currentPlayer = self.switchPlayer[self.currentPlayer]

    def setUserSystem(self):
        while True:
            try:
                self.__usersystem = str(input("input your OS(windows/linux/mac): "))
                if(self.__usersystem not in ["windows", "linux", "mac"]):
                    raise Exception("Input Error")
                else:
                    if self.__usersystem == "windows":
                        self.__clearprompt = "cls"
                    
                    if self.__usersystem in ["linux", "mac"]:
                        self.__clearprompt = "clear"
                    break
            except Exception as e:
                print(f"error: {e}")
    
    def printChessBoard(self):
        # self.chessBoard.printMoveList()
        # self.chessBoard.printAttackList()
        self.chessBoard.print_board()
        self.chessBoard.printEnpassantDict()
        # print(f"is black king in check: {self.chessBoard.event.isKingInCheck("black", copy.deepcopy(self.chessBoard))}")
        
    def printLog(self):
        print("棋譜")
        chessManual = self.log.getChessManual()
        
        t: int = 1
        for i in chessManual:
            print(f"{t}: ", end = "")
            for j in i:
                print(j, end = ' ')
            print()
            t += 1
        print()
        print("事件列表")
        for i in self.log.getEventLog():
            print(i)
        print()

    def checkFormat(self, control):
        if(len(control) != 2):
            return False
        
        if len(control[0]) != 2 or len(control[0]) != 2:
            return False
                
        if(control[0][0] not in "abcedfgh" or control[1][0] not in "abcdefgh"):
            return False

        if(control[0][1] not in "12345678" or control[1][1] not in "12345678"):
            return False


        return True

    def checkGameContinue(self, control = ["00","00"]):
        if(len(control) == 1 and control[0] == 'q'):
            self.printFinalInfo()
            return False

        if not self.chessBoard.event.isKingInCheck(self.currentPlayer, self.chessBoard):
            self.printFinalInfo()
            return False

        return True

    def printFinalInfo(self):
        print()
        print("Gameover")
        print(f"{self.switchPlayer[self.currentPlayer]} WIN")
        print(f"{self.currentPlayer} LOSS")
        print()
        self.printLog()

if __name__ == "__main__":
    chessGame = ChessGame()
    chessGame.start()