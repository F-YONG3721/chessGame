# 測試移動棋子的方法是否正確

# 棋盤
chessBoard = [
    [],       # 1
    [],       # 2
    [],       # 3
    []
]    # a  b  c


class Chess:
    global chessBoard

    # 將字串轉到對應的數字
    char2int = {
        'a' : 1,
        'b' : 2,
        'c' : 3,
        '1' : 1,
        '2' : 2,
        '3' : 3
    }
    # 將棋子的名稱轉到對應的icon
    word2icon = {
        "WhiteKnight" : '♘',
        "BlackRook" : '♜',
        "WhiteBishop" : '♗'
    }
    
    # 初始化
    def __init__(self, kind, x, y):
        self.kind = self.word2icon[kind]
        self.row = self.char2int[y] - 1 # 這裡-1 的目的是要對應到串列的範圍
        self.column = self.char2int[x]
        # print(f"test: row: {self.row}, column: {self.column}")
        self.__setPosition()

    # 設定棋子位置
    def __setPosition(self):
        chessBoard[self.row][self.column] = self.kind

    # 移動棋子
    def move(self, x, y):
        x = self.char2int[x] 
        y = self.char2int[y]

        if self.__checkMove(x, y) == True:
            chessBoard[self.row][self.column] = ' ' # 把原本在地位置去掉
            self.row = y - 1
            self.column = x
            self.__setPosition() # 移動到新位置
        else:
            print("此移動不符合規則")

    # 檢查移動是否符合規定
    def __checkMove(self, x, y):
        originalX = self.column
        originalY = self.row + 1 # 這裡會加一是因為我想把0去掉比較方便計算(0, 1, 2) → (1, 2, 3)

        if self.kind == '♘':
            # print(f"Knight x: {x}, y: {y}__\noriX: {originalX}, oriY: {originalY}")
            # 把棋盤想像成一個坐標系, 騎士移動的規則符合下列的計算
            if (x == originalX + 1 and y == originalY + 2) and ((x < 4 and x >= 0) and (y < 4 and y >= 0)):
                print("1")
                return True
            
            elif (x == originalX + 1 and y == originalY - 2) and ((x < 4 and x >= 0) and (y < 4 and y >= 0)):
                print("2")
                return True
            
            elif (x == originalX - 1 and y == originalY - 2) and ((x < 4 and x >= 0) and (y < 4 and y >= 0)):
                print("3")
                return True
            
            elif (x == originalX - 1 and y == originalY + 2) and ((x < 4 and x >= 0) and (y < 4 and y >= 0)):
                print("4")
                return True
            
            elif (x == originalX + 2 and y == originalY + 1) and ((x < 4 and x >= 0) and (y < 4 and y >= 0)):#
                print("1")
                return True
            
            elif (x == originalX + 2 and y == originalY - 1) and ((x < 4 and x >= 0) and (y < 4 and y >= 0)):
                print("2")
                return True
            
            elif (x == originalX - 2 and y == originalY - 1) and ((x < 4 and x >= 0) and (y < 4 and y >= 0)):
                print("3")
                return True
            
            elif (x == originalX - 2 and y == originalY + 1) and ((x < 4 and x >= 0) and (y < 4 and y >= 0)):
                print("4")
                return True            
            
            else:
                print("move error!")
                return False

        elif self.kind == '♜':
            # 城堡的移動規則: 只要一軸固定不變, 另一軸可以任意移動
            if (y == originalY or x == originalX) and ((x < 4 and x >= 0) and (y < 4 and y >= 0)):
                return True
            else:
                print("move error!")
                return False

        elif self.kind == '♗':
            # 主教的移動規則: 和前次座標相減然後(x / y) ** 2 == 1
            if (((originalX - x) // (originalY - y)) ** 2 == 1) and ((x < 4 and x >= 0) and (y < 4 and y >= 0)):
                return True

        else:
            print(f"沒有此種{self.kind}棋子")
            return False



# 初始化棋盤
def initialBoard():
    global chessBoard

    for i in range(4):
        for j in range(4):
            if i == 3 and j != 0:
                chessBoard[i].append(chr(96 + j))
            elif j == 0 and i != 3:
                chessBoard[i].append(str(i + 1))
            else:
                chessBoard[i].append(" ")

# 印出棋盤
def printBoard():
    print("-"*24)
    print(f"{'test chess move':^24s}")
    for i in range(len(chessBoard)):
        print("-"*24)
        for j in range(len(chessBoard[i])):
            print(f"{chessBoard[i][j]:^5s}|", end='')
        print()
        
# 輸入位置
def inputlocation():
    pass






def main():
    initialBoard() # 初始化棋盤
    
    printBoard() # 印出棋盤
    
    #將棋子放到棋盤上
    whiteKnight = Chess("WhiteKnight", 'a', '3')
    whiteBishop = Chess("WhiteBishop", 'b', '3')
    blackRook = Chess("BlackRook", 'a', '1')

    printBoard() # 印出棋盤

    # 移動測試
    whiteKnight.move('b', '1')
    printBoard()
    whiteKnight.move('c', '2')
    printBoard()
    whiteKnight.move('c', '3')
    printBoard()
    whiteKnight.move('a', '2')
    printBoard()
    whiteKnight.move('c', '1')
    printBoard()


main()