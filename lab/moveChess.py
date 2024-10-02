import os

###########################################
#       20241001把棋盤從3x3 --> 5x5        #  
# 提醒: 若要擴大棋盤範圍 Class的char2int要改#
# 增新棋子需要改動的地方：                  #
# 1. class的word2icon                     #
# 2. class的checkMove                     #
# 3. moveChess()                          
#  
# 20241002把棋盤擴到8x8
###########################################

# 測試移動棋子的方法是否正確

# 棋盤
#----------------
# 1 |   |   |   |
#----------------
# 2 |   |   |   |
#----------------
# 3 |   |   |   |
#----------------
#   | a | b | c | 

BOARD_ROW_MAX_LIMIT = 9 # 棋盤垂直的最大範圍 (n + 1)
BOARD_COLUMN_MAX_LIMIT = 9 # 棋盤水平的最大範圍 (n + 1)

chessBoard = [[" " for j in range(BOARD_COLUMN_MAX_LIMIT)] for i in range(BOARD_ROW_MAX_LIMIT)] # 建立棋盤及初始化


# 棋子位置的紀錄
chessLocation = dict()

# 棋子的物件
class Chess:
    global chessBoard
    global chessLocation
    # 將字串轉到對應的數字
    char2int = {
        'a' : 1,
        'b' : 2,
        'c' : 3,
        'd' : 4,
        'e' : 5,
        'f' : 6,
        'g' : 7,
        'h' : 8,
        '1' : 1,
        '2' : 2,
        '3' : 3,
        '4' : 4,
        '5' : 5,
        '6' : 6,
        '7' : 7,
        '8' : 8
    }
    # 將棋子的名稱轉到對應的icon
    word2icon = {
        "WhiteKnight" : '♘',
        "WhiteBishop" : '♗',
        "WhiteQueen" : '♕',
        "BlackKing" : '♚',
        "BlackRook" : '♜',
        "BlackQueen": '♛',
        "BlackPawn" : '♟'
    }
    
    # 初始化
    def __init__(self, kind):
        self.kind = self.word2icon[kind]

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
        moveX = self.char2int[x] 
        moveY = self.char2int[y]

        if self.checkMove(moveX, moveY) == True:
            self.checkEat(x, y) # 檢查吃否吃子 

            chessBoard[self.row][self.column] = ' ' # 把原本在地位置去掉
            self.row = moveY - 1
            self.column = moveX
            self.__setPosition() # 移動到新位置
            return True
        else:
            print("此移動不符合規則")
            print(f"x: {x}, y: {y}\noriginalX: {self.column}, originalY: {self.row + 1}")
            return False
            

    # 檢查移動是否符合規定
    def checkMove(self, x, y):
        originalX = self.column
        originalY = self.row + 1 # 這裡會加一是因為我想把0去掉比較方便計算(0, 1, 2) → (1, 2, 3)
        print(f"-----\ncheck Test\nx: {x}, y: {y}\n-----")#
        if self.kind == '♘':
            # print(f"Knight x: {x}, y: {y}__\noriX: {originalX}, oriY: {originalY}")
            # 把棋盤想像成一個坐標系, 騎士移動的規則符合下列的計算
            if (x == originalX + 1 and y == originalY + 2) and ((x < BOARD_COLUMN_MAX_LIMIT and x >= 0) and (y < BOARD_ROW_MAX_LIMIT and y >= 0)):
                # print("1")
                return True
            
            elif (x == originalX + 1 and y == originalY - 2) and ((x < BOARD_COLUMN_MAX_LIMIT and x >= 0) and (y < BOARD_ROW_MAX_LIMIT and y >= 0)):
                # print("2")
                return True
            
            elif (x == originalX - 1 and y == originalY - 2) and ((x < BOARD_COLUMN_MAX_LIMIT and x >= 0) and (y < BOARD_ROW_MAX_LIMIT and y >= 0)):
                # print("3")
                return True
            
            elif (x == originalX - 1 and y == originalY + 2) and ((x < BOARD_COLUMN_MAX_LIMIT and x >= 0) and (y < BOARD_ROW_MAX_LIMIT and y >= 0)):
                # print("4")
                return True
            
            elif (x == originalX + 2 and y == originalY + 1) and ((x < BOARD_COLUMN_MAX_LIMIT and x >= 0) and (y < BOARD_ROW_MAX_LIMIT and y >= 0)):#
                # print("1")
                return True
            
            elif (x == originalX + 2 and y == originalY - 1) and ((x < BOARD_COLUMN_MAX_LIMIT and x >= 0) and (y < BOARD_ROW_MAX_LIMIT and y >= 0)):
                # print("2")
                return True
            
            elif (x == originalX - 2 and y == originalY - 1) and ((x < BOARD_COLUMN_MAX_LIMIT and x >= 0) and (y < BOARD_ROW_MAX_LIMIT and y >= 0)):
                # print("3")
                return True
            
            elif (x == originalX - 2 and y == originalY + 1) and ((x < BOARD_COLUMN_MAX_LIMIT and x >= 0) and (y < BOARD_ROW_MAX_LIMIT and y >= 0)):
                # print("4")
                return True            
            
            else:
                print(f"move error!| originalX: {originalX}, originalY: {originalY}\n x: {x}, y: {y}")
                return False

        elif self.kind == '♜':
            # 城堡的移動規則: 只要一軸固定不變, 另一軸可以任意移動
            if (y == originalY or x == originalX) and ((x < BOARD_COLUMN_MAX_LIMIT and x >= 0) and (y < BOARD_ROW_MAX_LIMIT and y >= 0)):
                return True
            else:
                print("move error!")
                return False

        elif self.kind == '♗':
            # 主教的移動規則: 和前次座標相減然後(x / y) ** 2 == 1
            if (((originalX - x) / (originalY - y)) ** 2 == 1) and ((x < BOARD_COLUMN_MAX_LIMIT and x >= 0) and (y < BOARD_ROW_MAX_LIMIT and y >= 0)):
                return True

        elif self.kind == '♕' or self.kind == '♛':
            if (((y == originalY or x == originalX)) or (((originalX - x) / (originalY - y)) ** 2 == 1)) and ((x < BOARD_COLUMN_MAX_LIMIT and x >= 0) and (y < BOARD_ROW_MAX_LIMIT and y >= 0)):
                print(f"-----\nQueen 移動檢測: \nx: {x}, y: {y}\noriginalX: {originalX}, originalY: {originalY}\n-----")#
                return True
            else:
                print("move error!")
                return False

        elif self.kind == '♚':
            if (((y == originalY + 1 or y == originalY - 1) and (x == originalX)) or ((x == originalX + 1 or x == originalX -1) and (y == originalY))) or (((originalX - x) ** 2 == 1 and (originalY - y) ** 2 == 1) and (((originalX - x) // (originalY - y)) ** 2 == 1)) and ((x < BOARD_COLUMN_MAX_LIMIT and x >= 0) and (y < BOARD_ROW_MAX_LIMIT and y >= 0)):
                return True
            else:
                print("move error")
                return False

        elif self.kind == '♟':
            if ((y == originalY - 1) and (x == originalX)) and ((x < BOARD_COLUMN_MAX_LIMIT and x >= 0) and (y < BOARD_ROW_MAX_LIMIT and y >= 0)):
                return True
            else:
                print("move error")
                return False

        else:
            print(f"沒有此種{self.kind}棋子")
            return False
        
    def checkEat(self, x, y):
        location = x + y # 合併成輸入格式
        print(f"goto: {location}")
        moveX = self.char2int[x] # 設成物件內的格式
        moveY = self.char2int[y]

        if (chessLocation.get(location) != None):
            chessBoard[moveY - 1][moveX] = ' ' # 移除棋盤上被吃掉的棋
            chessLocation.pop(location) # 移除位置記錄上被吃掉的棋
            return True
        else:
            return False

# 初始化棋盤
def initialBoard():
    global chessBoard

    for i in range(BOARD_ROW_MAX_LIMIT):
        for j in range(BOARD_COLUMN_MAX_LIMIT):
            if i == (BOARD_ROW_MAX_LIMIT - 1) and j != 0:
                chessBoard[i][j] = chr(96 + j)
            elif j == 0 and i != (BOARD_ROW_MAX_LIMIT - 1):
                chessBoard[i][j] = str(i + 1)
            else:
                pass 

# 印出棋盤
def printBoard():
    print("-"*(6*BOARD_COLUMN_MAX_LIMIT))
    print(f"{'test chess move':^48s}")
    for i in range(len(chessBoard)):
        print("-"*(6*BOARD_COLUMN_MAX_LIMIT))
        for j in range(len(chessBoard[i])):
            print(f"{chessBoard[i][j]:^5s}|", end='')
        print()
        
# 輸入位置
def inputlocation():
    locationList = input("請輸入棋子要移動到的位置(ex: a3 b1): ").split(sep=' ')
    check = '' #
    # 檢驗資料輸入格式是否正確
    if len(locationList) != 2: # 串列內是否只有兩個元素
        print("請輸入兩筆資料")
        inputlocation()
        return False # 跳出函式

    for i in locationList:
        if len(i) == 2: # 確認元素一內 只有兩個字元 ex: e1
            pass
        else:
            print(f"第{i}個資料錯誤\n請重新輸入")
            inputlocation()
            return False # 跳出函式
        
        for j in range(len(i)): # 確認元素內符合 a1 這樣的格式 
            check = i[j]
            if j == 0:
                # print(f"typecheck: {type(check)}")
                if check.isalpha() == False:
                    print(f"資料輸入錯誤: 應為字母\n錯誤:{check}\n{check.isalpha()}")
                    inputlocation()
                    return False # 跳出函式               

            if j == 1:
                if check.isdigit() == False:
                    print(f"資料輸入錯誤: 應為數字\n錯誤:{check}\n{check.isdigit()}")
                    inputlocation()
                    return False # 跳出函式 

    # 檢查起始位置是否有放置棋子
    if chessLocation.get(locationList[0]) == None:
        print("此位置無放置任何棋, 請重新輸入")
        inputlocation()
        return False # 跳出函式
    
    print(f"locationList: {locationList}") #

    # 移動和記錄棋子
    if (moveChess(locationList[0], locationList[1]) == True):  # 如果可以移動
        recordMoveLocation(locationList[0], locationList[1]) # 則記錄此移動
    else:
        # print(f"chessLocation.get: {chessLocation.get(locationList[0])}")
        print("此移動無效或違規, 請重新移動")
        inputlocation()
        return False # 跳出函式

    return None

# 記錄移動位置
def recordMoveLocation(initial, final):
    chessTemporary = object()

    # 更改資料
    chessTemporary = chessLocation.get(initial)
    chessLocation.pop(initial) # 1. 先刪除初始位置(initail)
    chessLocation.setdefault(final, chessTemporary) # 2. 寫入 位置(final) : 棋子物件名稱

# 移動
def moveChess(initial, final):
    # 移動棋子
    
    # 1. 把final 分成 x(字串型態英文字母), y(字串型態數字)
    for i in range(len(final)):
        if i == 0:
            x = final[i]
        elif i == 1:
            y = final[i]
        else:
            print("move location error")

    # 錯誤在這: 原本是先改位置在移動棋盤, 但我換成先移動再改棋盤就無效了 (# 已解決)
    # 2. 利用if 判斷式找到final 位置對應的物件 ex: if chessLocation[final] == whiteBishop:
    if chessLocation[initial] == whiteKnight: # 3. 執行該物件的 move ex: whiteBishop.move(x, y) 
        if whiteKnight.move(x, y) == False: # move 會回傳此移動是否錯誤
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
        
    elif chessLocation[initial] == whiteQueen:
        if whiteQueen.move(x, y) == False:
            return False
        else:
            return True

    elif chessLocation[initial] == blackQueen:
        if blackQueen.move(x, y) == False:
            return False
        else:
            return True
    
    elif chessLocation[initial] == blackPawn:
        if blackPawn.move(x, y) == False:
            return False
        else:
            return True

    elif chessLocation[initial] == blackKing:
        if blackKing.move(x, y) == False:
            return False
        else:
            return True

    else:
        print(f"error -- not this chess!")
    
    print(f"目前的移動狀態: {chessLocation}")

# 建立物件
whiteKnight = Chess("WhiteKnight")
whiteBishop = Chess("WhiteBishop")
blackRook = Chess("BlackRook")
whiteQueen = Chess("WhiteQueen")
blackQueen = Chess("BlackQueen")
blackPawn = Chess("BlackPawn")
blackKing = Chess("BlackKing")



# debug用
def checkflow():
    os.system("cls")
    initialBoard()
    

    whiteKnight.setInitPosition('a', '3')
    chessLocation.setdefault("a3", whiteKnight)

    whiteBishop.setInitPosition('b', '3')
    chessLocation.setdefault("b3", whiteBishop)

    blackRook.setInitPosition('a', '1')
    chessLocation.setdefault("a1", blackRook)
    printBoard()

    a = ""

    while a != "exit":

        inputlocation()
        a = input("exit 退出: ")
        os.system("cls")
        printBoard()

#
def main():
    initialBoard() # 初始化棋盤
    
    #將棋子放到棋盤上
    whiteKnight.setInitPosition('a', '3') # 定位
    chessLocation.setdefault("a3", whiteKnight) # 記錄位置

    whiteBishop.setInitPosition('b', '3')
    chessLocation.setdefault("b3", whiteBishop)

    blackRook.setInitPosition('a', '1')
    chessLocation.setdefault("a1", blackRook)

    whiteQueen.setInitPosition('c', '3')
    chessLocation.setdefault("c3", whiteQueen)

    blackQueen.setInitPosition('d', '5')
    chessLocation.setdefault("d5", blackQueen)

    blackPawn.setInitPosition('a', '5')
    chessLocation.setdefault("a5", blackPawn)

    blackKing.setInitPosition('c', '5')
    chessLocation.setdefault("c5", blackKing)

    os.system("cls")
    printBoard()
    # 移動流程測試
    a = ""
    while a != 'exit':
        try: 
            
            inputlocation()
                
        except Exception as e:
            print(f"{'-' * 6}\n*** error: {e}\n{'-' * 6}")
        else:
            pass
        
        finally:
            a = input("輸入[exit]退出, [enter]繼續:")
            os.system("cls")
            printBoard()
            



main()
# checkflow()