import os
# 測試移動棋子的方法是否正確

# 棋盤
chessBoard = [
    [],       # 1
    [],       # 2
    [],       # 3
    []
]    # a  b  c

# 棋子位置的紀錄
chessLocation = {}

# 棋子德物件
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
    def __init__(self, kind):
        self.kind = self.word2icon[kind]
        # self.row = self.char2int[y] - 1 # 這裡-1 的目的是要對應到串列的範圍
        # self.column = self.char2int[x]
        # print(f"test: row: {self.row}, column: {self.column}")
        # self.__setPosition()

    # 設定棋子位置
    def __setPosition(self):
        chessBoard[self.row][self.column] = self.kind

    # 初始化位置
    def setInitPosition(self, x, y):
        # 設定row, column
        self.row = self.char2int[y] - 1 # 這裡-1 的目的是要對應到串列的範圍
        self.column = self.char2int[x]
        self.__setPosition()

    # 移動棋子
    def move(self, x, y):
        x = self.char2int[x] 
        y = self.char2int[y]

        if self.checkMove(x, y) == True:
            chessBoard[self.row][self.column] = ' ' # 把原本在地位置去掉
            self.row = y - 1
            self.column = x
            self.__setPosition() # 移動到新位置
            return True
        else:
            print("此移動不符合規則")
            return False
            

    # 檢查移動是否符合規定
    def checkMove(self, x, y):
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
    locationList = input("請輸入棋子要移動到的位置(ex: a3 b1)").split(sep=' ')
    check = '' #
    # 檢驗資料輸入格式是否正確
    if len(locationList) != 2:
        print("請輸入兩筆資料")
        inputlocation()

    for i in locationList:
        if len(i) == 2:
            pass
        else:
            print(f"第{i}個資料錯誤\n請重新輸入")
            inputlocation()
        
        for j in range(len(i)):
            check = i[j]
            if j == 0:
                print(f"typecheck: {type(check)}")
                if check.isalpha() == False:
                    print(f"資料輸入錯誤: 應為字母\n錯誤:{check}\n{check.isalpha()}")
                    inputlocation()                    

            if j == 1:
                if check.isdigit() == False:
                    print(f"資料輸入錯誤: 應為數字\n錯誤:{check}\n{check.isdigit()}")
                    inputlocation()


    print(f"locationList: {locationList}")
    # 移動和記錄棋子
    if moveChess(locationList[0], locationList[1]) == True:
        recordMoveLocation(locationList[0], locationList[1])
    else:
        print("此移動無效或違規, 請重新移動")
        inputlocation()

# 記錄移動位置
def recordMoveLocation(initial, final):
    chessTemporary = object()
    x = int()
    y = int()
    # 檢查 chessLocation 是否存在
    if chessLocation.get(initial) != "None":
        # 更改資料
        chessTemporary = chessLocation.get(initial)
        chessLocation.pop(initial) # 1. 先刪除初始位置(initail)
        chessLocation.setdefault(final, chessTemporary) # 2. 寫入 位置(final) : 棋子物件名稱

        

# 移動
def moveChess(initial, final):
    # 移動棋子
    if (chessLocation[initial] != 'None'):
        # 1. 把final 分成 x(字串型態英文字母), y(字串型態數字)
        for i in range(len(final)):
            if i == 0:
                x = final[i]
            elif i == 1:
                y = final[i]
            else:
                print("move location error")

        # 錯誤在這: 原本是先改位置在移動棋盤, 但我換成先移動再改棋盤就無效了
        # 2. 利用if 判斷式找到final 位置對應的物件 ex: if chessLocation[final] == whiteBishop:
        if chessLocation[initial] == whiteKnight: # 3. 執行該物件的 move ex: whiteBishop.move(x, y) 
            if whiteKnight.move(x, y) == False:
                return False
            else:
                return True

        elif chessLocation[initial] == whiteBishop:
            if whiteBishop.move(x, y) == False:
                return False
            else:
                return True

        elif chessLocation[initial] == blackRook:
            if blackRook.move(x, y) == False:
                return False
            else:
                return True

        else:
            print(f"error -- not this chess!")

        print(f"目前的移動狀態: {chessLocation}")

# 記錄

whiteKnight = Chess("WhiteKnight")
whiteBishop = Chess("WhiteBishop")
blackRook = Chess("BlackRook")




def main():
    initialBoard() # 初始化棋盤
    
    printBoard() # 印出棋盤
    
    #將棋子放到棋盤上
    whiteKnight.setInitPosition('a', '3')
    chessLocation.setdefault("a3", whiteKnight)

    whiteBishop.setInitPosition('b', '3')
    chessLocation.setdefault("b3", whiteBishop)

    blackRook.setInitPosition('a', '1')
    chessLocation.setdefault("a1", blackRook)

    printBoard() # 印出棋盤

    # if (chessLocation["a3"] == whiteKnight):
    #     print("成功!!!")
    
    # 移動流程測試
    a = ""
    while a != 'exit':
        try: 
                inputlocation()
                
        except Exception as e:
            print(e)
            print("error!!!")
        else:
            pass
        
        finally:
            os.system("cls")
            printBoard()
            a = input("輸入任意字符退出, [enter]繼續:")



main()