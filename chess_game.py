import os

#棋盤
chessBoard = [
    [],                   # 8
    [],                   # 7
    [],                   # 6
    [],                   # 5
    [],                   # 4
    [],                   # 3
    [],                   # 2
    [],                   # 1
    []  # a b c d e f g h            
]

# 定義棋子的類別 種類包括: king queen rook bishop knight pawn 
class Chess:
    global chessBoard

    # 各種西洋棋圖形的utf8編碼
    word2icon = {
        "blackKing": '♚',
        "blackQueen": '♛',
        "blackRook": '♜',
        "blackBishop": '♝',
        "blackKnight": '♞',
        "blackPawn": '♟',
        "whiteKing": '♔',
        "whiteQueen": '♕',
        "whiteRook": '♖',
        "whiteBishop": '♗',
        "whiteKnight": '♘',
        "whitePawn": '♙',
    }

    # 座標轉數字
    char2int = {
        'a': 1,
        'b': 2,
        'c': 3,
        'd': 4,
        'e': 5,
        'f': 6,
        'g': 7,
        'h': 8,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
    }

    def __init__(self, kind, x, y):
        self.kind = self.word2icon[kind]
        self.column = self.char2int[x]
        # print(f"self.column: {x}")
        self.row = self.__modifyRow(self.char2int[y])
        # print(f"self.row: {self.row}")
        chessBoard[self.row][self.column] = self.kind    
    
    @staticmethod
    def __modifyRow(row):
        return (8 - row)

    def __checkMove(self, move2Colum, move2Row):
        # 檢查移動到的位置上有無障礙
        if self.kind == '♚' or self.kind == '♔':
            print("棋子是國王")

        elif self.kind == '♛' or self.kind == '♕':
            print("棋子是皇后")
            pass

        elif self.kind == '♜' or self.kind == '♖':
            print("棋子是城堡")
            pass

        elif self.kind == '♝' or self.kind == '♗':
            print("棋子是主教")
            pass

        elif self.kind == '♞' or self.kind == '♘':
            print("棋子是騎士")
            pass

        elif self.kind == '♟' or self.kind == '♙':
            print("棋子是小兵")
            pass

        else:
            print("棋子錯誤")

        return True

    def move_to(self):
        x, y = input("請輸入移動位置(x,y): ").split(sep=',') # 有可能發生錯誤
        self.moveTo_row = self.__modifyRow(self.char2int[str(y)])
        self.moveTo_column = self.char2int[str(x)]

        print(f"棋子移動到: ({self.moveTo_column}, {self.moveTo_row})")
        
        if self.__checkMove(self.moveTo_column, self.moveTo_row) == True:
            print(f"self.row: {self.row}, self.column: {self.column}")
            chessBoard[self.row][self.column] = ' '
            self.row = self.moveTo_row
            self.column = self.moveTo_column
            chessBoard[self.row][self.column] = self.kind
            return True
            
        else:
            print(f"移動位置錯誤, 請重新移動")
            return False
 

# 初始化棋盤
def initialBoard(board):
    # row 為 數字 1 ~ 8
    for i in range(len(board)):
        if i != 8:
            board[i].append(str(8 - i))
        else:
            board[i].append(' ')

    # colum 為英文 a ~ h
    for i in range(len(board)):
        if i != 0:
            board[len(board) - 1].append(chr(96+i))
        else:
            pass

    # 其他空格填入 ' '
    for i in range(9):
        for j in range(9):
            if i != 8 and j != 0:
                board[i].append(' ')
            else:
                pass

# 列印棋盤
def printBoard(board):
    print(f"{'-'*45}")
    print(f"{'chess_game':^45s}")
    for i in board:
        print(f"{'-'*45}")
        for j in i:
            print(f"{j:^4s}|",sep='', end='')
        print()
        
# 移動棋子
def move(player):
    location = ''
    if player == "white":
         # 棋子種類, x 座標, y 座標

        locationList = []
        location = input("請輸入移動位置(ex:Ke2, Nf3, Pe4, Nxf3, Pxd5): ")
        # 輸入原則: [棋子種類1~2個字元][棋子原始位置]
        for i in location:
            locationList.append(i)

        print(locationList)

        for i in range(len(locationList)):
            print(f"i: {i}")
            if locationList[i] in "KQBNP":
                match locationList[i]:
                    case 'K':
                        print(f"i is K")
                        WK.move_to()
                    case 'Q':
                        print(f"i is Q")
                    case 'B':
                        print(f"i is B")
                    case 'N':
                        print(f"i is R")
                    case 'P':
                        print(f"i is P")
                    case _:
                        pass

    elif player == "black":
        pass

    else:
        print("玩家錯誤(white or black)")



def main():
    while True:
        printBoard(chessBoard)
        # # global return2position
        # WK.move_to()
        # os.system("cls")
        move("white")
        move("black")

initialBoard(chessBoard)
# 把棋子擺上棋盤
# 白方
WK = Chess("whiteKing", 'e', '1')
WQ = Chess("whiteQueen", 'd', '1')
WBR = Chess("whiteBishop", 'c', '1')
WBL = Chess("whiteBishop", 'f', '1')
WNR = Chess("whiteKnight", 'b', '1')
WNL = Chess("whiteKnight", 'g', '1')
WRR = Chess("whiteRook", 'a', '1')
WRL = Chess("whiteRook", 'h', '1')
WPA = Chess("whitePawn", 'a', '2')
WPB = Chess("whitePawn", 'b', '2')
WPC = Chess("whitePawn", 'c', '2')
WPD = Chess("whitePawn", 'd', '2')
WPE = Chess("whitePawn", 'e', '2')
WPF = Chess("whitePawn", 'f', '2')
WPG = Chess("whitePawn", 'g', '2')
WPH = Chess("whitePawn", 'h', '2')

# 黑方
BK = Chess("blackKing", 'e', '8')
BQ = Chess("blackQueen", 'd', '8')
BBR = Chess("blackBishop", 'c', '8')
BBL = Chess("blackBishop", 'f', '8')
BNR = Chess("blackKnight", 'b', '8')
BNL = Chess("blackKnight", 'g', '8')
BRR = Chess("blackRook", 'a', '8')
BRL = Chess("blackRook", 'h', '8')
BPA = Chess("blackPawn", 'a', '7')
BPB = Chess("blackPawn", 'b', '7')
BPC = Chess("blackPawn", 'c', '7')
BPD = Chess("blackPawn", 'd', '7')
BPE = Chess("blackPawn", 'e', '7')
BPF = Chess("blackPawn", 'f', '7')
BPG = Chess("blackPawn", 'g', '7')
BPH = Chess("blackPawn", 'h', '7')

main()
        