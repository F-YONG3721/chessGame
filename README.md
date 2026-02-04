# 西洋棋 Chess Game (Python CLI)

## 概述
這是我剛學習完Python時，開始做的Side project。
我的目標是用Python完成一個西洋棋遊戲，至少要有以下基本的功能
* 判斷棋子的移動、吃子及特殊規則是否正確
* 判斷勝利條件
* 下棋的流程

使用終端介面進行遊戲。  

目前有連網的功能，使得不同地區的人可以透過網路下棋。

## 未來規劃
* 用Pygame製作圖形化介面

## 需求
* Python: 3.12(開發與測試的環境)
理論上相容 Python 3.x，其餘版本尚未嘗試

* windows, macOS, linux(須支援終端機介面) 

## 使用方式
### 開啟遊戲
用終端機開啟`start.py`即可開始遊戲。
```bash
$ python3 start.py
```

### 輸入基本資料  
之後會請您輸入以下的資料:
#### OS
* 請輸入您的作業系統
* 這會用在清理終端機介面  

#### Mode
* `online` : 網路連線模式
* `offline` : 單機模式(沒有機器人)

### Online模式下的設定
選用**online**模式後，會請您輸入以下資訊
#### Host
* `server` : 開啟房間，等待別人加入
* `client` : 加入別人房間

#### IP
* 輸入開啟或加入房間的IP

#### Port
* 輸入開啟或加入房間的Port

#### Color
若您Host選擇`server`，在這裡會需要您填入棋子的顏色(`white`, `black`)

### 遊戲開始
遊戲開始後，白方先下才換黑方，交替進行
#### 輸入的格式
終端會顯示棋盤的座標，輸入棋子的座標與目的地的座標，中間空一格，即可將棋子移動。 

範例:
```bash
: e2 e4
```
這樣可以將e兵移動至e4格

#### 中途退出遊戲
| 模式 | 指令 |
|------|------|
| offline | `q` |
| online  | `surrender` |

## 專案結構
```text
.
├── start.py                     # 遊戲進入點
├── chess_game.py                # 遊戲核心邏輯
├── README.md                    # 專案說明
└── docs/
    ├── idea.md                  # 記錄開發過程中的想法
    └── design/                   
        └── chess_game.drawio     # 遊戲進行的流程圖
```