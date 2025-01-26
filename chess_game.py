import os

class Board:
    BOARD_SIZE = 9
    board = list()

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
        
    # 印出棋盤 
    def print_board(self):
        print("-"*(6*self.BOARD_SIZE))
        print(f"{"CHESS GAME":^54s}")
        for i in range(self.BOARD_SIZE):
            print("-"*(6*self.BOARD_SIZE))
            for j in range(self.BOARD_SIZE):
                if(type(self.board[i][j]) == str):
                    print(f"{self.board[i][j]:^5s}", end="|")
                else:
                    print(f"{self.board[i][j].kind:^5s}", end="|")
    
            print()

    # 下棋
    def draw(self, currentPosition, nextPosition):
        # 轉換座標
        currentX = self.__standardPosition(currentPosition[0])
        currentY = self.__standardPosition(currentPosition[1])

        nextX = self.__standardPosition(nextPosition[0])
        nextY = self.__standardPosition(nextPosition[1])

        # 取得棋子類型
        chessKind = self.board[currentY][currentX]

        # check move and draw
        if self.__checkMoveRule(currentX, currentY, nextX, nextY):
            self.board[currentY][currentX] = " " # 清空原本位置
            self.board[nextY][nextX] = chessKind # 移動到新位置
            return True
        else:
            return False

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

    # 檢查是否符合移動規則
    def __checkMoveRule(self, currentX, currentY, nextX, nextY):

        chessKind = self.board[currentY][currentX] # 取得棋子
        targetLocation = self.board[nextY][nextX] # 取得目標位置的狀態

        #check not over the board
        if nextX  < 1 or nextX > 8 or nextY < 0 or nextY > 7:
            return False

        # check chessKind is a chess
        if type(chessKind) == str:
            return False

        # check group
        if type(targetLocation) != str and targetLocation.group == chessKind.group:
            return False

        # check move and eat
        checkBlock = self.__checkBlock(currentX, currentY, nextX, nextY)
        checkMove = chessKind.checkMove(currentX, currentY, nextX, nextY) and type(targetLocation) == str
        checkEat = chessKind.checkEat(currentX, currentY, nextX, nextY) and type(targetLocation) != str
        
        # 把小兵吃子與移動的規則區隔開來 
        if type(chessKind) == Pawn:
            checkMove = checkMove and type(targetLocation) == str
        
        # 騎士不受中間有其他棋子擋住的限制 
        if type(chessKind) != Knight:
            checkEat = checkEat and checkBlock
            checkMove = checkMove and checkBlock


        if checkMove or checkEat: 
            return True
        else:
            return False
    
    # 檢查是否有其他棋子擋住
    def __checkBlock(self, currentX, currentY, nextX, nextY):
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
            
            # 如果有遇到棋子則回傳False
            if type(self.board[currentY][currentX]) != str:
                return False
        
        
        return True

class Chess:
    def __init__(self, kind, group):
        self.kind = kind
        self.group = group

class King(Chess):
    def checkMove(self, x1, y1, x2, y2):
        if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
            return True
        else:
            return False
    
    def checkEat(self, x1, y1, x2, y2):
        return self.checkMove(x1, y1, x2, y2)
    
class Queen(Chess):
    def checkMove(self, x1, y1, x2, y2):
        if abs(x1 - x2) == abs(y1 - y2) or x1 == x2 or y1 == y2:
            return True
        else:
            return False
    
    def checkEat(self, x1, y1, x2, y2):
        return self.checkMove(x1, y1, x2, y2)

class Bishop(Chess):
    def checkMove(self, x1, y1, x2, y2):
        if abs(x1 - x2) == abs(y1 - y2):
            return True
        else:
            return False
    
    def checkEat(self, x1, y1, x2, y2):
        return self.checkMove(x1, y1, x2, y2)

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

class Rook(Chess):
    def checkMove(self, x1, y1, x2, y2):
        if x1 == x2 or y1 == y2:
            return True
        else:
            return False
    
    def checkEat(self, x1, y1, x2, y2):
        return self.checkMove(x1, y1, x2, y2)

class Pawn(Chess):
    firstMove = True

    def checkMove(self, x1, y1, x2, y2):
        x = x2 - x1
        y = y2 - y1

        if self.firstMove:
            if((y <= 2 and self.group == "black") or (y >= -2 and self.group == "white")) and x == 0:
                self.firstMove = False
                return True
            else:
                return False
        else:
            if(y == 1 and self.group == "black") or (y == -1 and self.group == "white") and x == 0:
                return True
            else:
                return False
            
    def checkEat(self, x1, y1, x2, y2):
        x = x2 - x1
        y = y2 - y1

        if((y == 1 and self.group == "black") or (y == -1 and self.group == "white")) and (x == 1 or x == -1):
            self.firstMove = False
            return True
        else:
            return False

class ChessGame:
    def __init__(self):
        self.chessBoard = Board()

    def start(self):
        while(True):
            try:
                self.chessBoard.print_board()
                control = input("please input position: ").split(" ")
                if(len(control)!= 2 and control[0] != "q"):
                    raise Exception("Input Error")
                print(control)
            except Exception as e:
                print(f"Error: {e}")
                control = input("continue?: ")
                if control == "q":
                    break
            else:
                if(control[0] == "q"):
                    break
                else:
                    os.system("clear")
                    if self.chessBoard.draw(control[0], control[1]) == False:
                        print("Can't Move")

if __name__ == "__main__":
    chessGame = ChessGame()
    chessGame.start()