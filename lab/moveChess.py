# 測試儀動棋子的方法是否正確

chessBoard = [
    [],       # 1
    [],       # 2
    [],       # 3
    []
]    # a  b  c

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


def printBoard():
    print("-"*24)
    print(f"{'test chess move':^24s}")
    for i in range(len(chessBoard)):
        print("-"*24)
        for j in range(len(chessBoard[i])):
            print(f"{chessBoard[i][j]:^5s}|", end='')
        print()
        
        
    
def main():
    initialBoard()
    # print(chessBoard)
    printBoard()

main()