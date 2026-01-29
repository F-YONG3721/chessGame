import os

class Board:
    BOARD_SIZE = 9
    event = None
    board = list()
    attackList = list()
    enPassantDict = dict() #{key: 儲存執行的棋子, value: 儲存可被吃的棋子}
    __kingLocation = dict()

    # 初始化棋盤
    def __init__(self):
        self.board = [[" " for i in range(self.BOARD_SIZE)] for j in range(self.BOARD_SIZE)]

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
        self.event = Event()

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
            return True


        # 檢查是否符合移動規則
        if self.event.checkMoveRule(currentX, currentY, nextX, nextY, self):     
            self.__draw(currentX, currentY, nextX, nextY)
            
            if(type(chessKind) == King):
                self.__kingLocation[chessKind.group] = tuple([nextX, nextY])

            # 將棋子設定成已移動過
            chessKind.setEverMove() 

            # 建立攻擊表
            self.attackList = self.event.buildAttackList(chessKind.group, self)

            return True
        else:
            return False

    # 下棋
    def __draw(self, currentX, currentY, nextX, nextY):  
        chessKind = self.board[currentY][currentX]  # 取得棋子
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
                if(i <= 7 and j > 0):
                    print(f"{self.attackList[i][j]:^5s}", end = "|")
                elif(j == 0 and i != 8):
                    print(f"{str(8-i):^5s}", end = "|")
                elif(i > 7 and j > 0):
                    print(f"{chr(96 + j):^5s}", end = "|")
                else:
                    print(f"{self.attackList[i][j]:^5s}", end = "|")
            
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
        self.__kingLocation["white"] = (5, 7)
        self.__kingLocation["black"] = (5, 0)


class Event:

    def __init__(self):
        pass

    # 檢查是否符合移動規則
    def checkMoveRule(self, currentX, currentY, nextX, nextY, board: Board):

        chessKind = board.board[currentY][currentX] # 取得棋子
        targetLocation = board.board[nextY][nextX] # 取得目標位置的狀態

        #check not over the board
        if nextX  < 1 or nextX > 8 or nextY < 0 or nextY > 7:
            return False

        # check chessKind is a chess
        if type(chessKind) == str:
            return False

        # check group
        if type(targetLocation) != str and targetLocation.group == chessKind.group:
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

        # 檢查小兵是否升變(promotion)
        if type(chessKind) == Pawn and (nextY == 0 or nextY == 7):
            self.checkPromotion(currentX, currentY, nextX, nextY, board)

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
                    return True
        
        # 檢查小兵是否觸發過路兵規則(en passant)
        if type(chessKind) == Pawn and abs(currentY - nextY) == 2 and checkMove:
            if (nextX - 1) >= 1 and type(board.board[nextY][nextX - 1]) == Pawn and board.board[nextY][nextX - 1].group != chessKind.group:
                board.enPassantDict.setdefault(board.board[nextY][nextX - 1], chessKind) # 將可被吃的棋子加入到許可表中
            
            if (nextX + 1) <= 8 and type(board.board[nextY][nextX + 1]) == Pawn and board.board[nextY][nextX + 1].group != chessKind.group:
                board.enPassantDict.setdefault(board.board[nextY][nextX + 1], chessKind)

        # 檢查是否符合規則
        if checkMove or checkEat:
            board.clearEnPassantDict(chessKind.group)             
            return True
        else:
            return False
    
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
            if abs(currentX - pointX) <= 2 and board.attackList[pointY][pointX] == "X":
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
        attackList = [[" " for i in range(board.BOARD_SIZE)] for j in range(board.BOARD_SIZE)]

        for currentY in range(board.BOARD_SIZE - 1):
            for currentX in range(1, board.BOARD_SIZE):
                
                chessKind = board.board[currentY][currentX]

                # 確認chessKind是棋子
                if type(chessKind) == str:
                    continue 
                
                # 避免後來的棋子蓋過原本棋子的攻擊範圍
                if attackList[currentY][currentX] != "X":
                    attackList[currentY][currentX] = chessKind.kind

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

                        # 小兵的特殊狀況
                        if type(chessKind) != Pawn:
                            checkEat = chessKind.checkEat(currentY, currentX, y, x)
                        elif (type(targetLocation) != str and targetLocation.group != group) or type(targetLocation) == str:
                            attackList[y][x] = "X"
                            break
                        else:
                            break
                            
                        # 如果不符合吃子的規則就退出
                        if checkEat == False:
                            break
                        
                        # 如果是可以攻擊的點就畫上"X"
                        if type(targetLocation) == str:
                            attackList[y][x] = "X"

                        elif targetLocation.group != group:
                            attackList[y][x] = "X"
                            break
                        else:
                            break
                        
                        # 往下個點繼續找
                        x += direction[0]
                        y += direction[1]

        return attackList 


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
    __usersystem = "windows"
    __clearprompt = None
    chessBoard = None

    def __init__(self):
        self.chessBoard = Board()
        self.setUserSystem()
        

    def start(self):

        # 簡單的交互
        currentPlayer = "white"
        switchPlayer = {
            "black" : "white",
            "white" : "black"
        }

        os.system(self.__clearprompt) # 清空畫面

        self.chessBoard.print_board()

        while(True):
            try:
                control = input(f"Your move, {currentPlayer}, please input position: ").split(" ")
                
                # 檢查是否符合輸入格式
                if(len(control)!= 2 and control[0] != "q"):
                    raise Exception("Input Error")
                elif(control[0] == "q"):
                    print("gameover")
                    break
                
                os.system(self.__clearprompt)

                if self.chessBoard.moveChess(control[0], control[1], currentPlayer):
                    self.chessBoard.printAttackList()
                    self.chessBoard.print_board()
                    self.chessBoard.printEnpassantDict()
                    currentPlayer = switchPlayer[currentPlayer]
                else:
                    self.chessBoard.print_board()
                    print("Can't Move")

            except Exception as e:
                print(f"Error: {e}")
                control = input("continue?: ")
                if control == "q":
                    break
                else:
                    os.system(self.__clearprompt)
            else:
                pass
                
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
              
if __name__ == "__main__":
    chessGame = ChessGame()
    chessGame.start()