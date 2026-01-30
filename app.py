from flask import Flask, render_template, redirect, request, url_for
app = Flask(__name__)

#8×8の盤面
board_size = 8

#白=1,黒=2,で初期盤面
def init_board():
    board = [[0]*board_size for _ in range(board_size)]
    board[3][3] = 1
    board[4][4] = 1
    board[3][4] = 2
    board[4][3] = 2
    return board

board = init_board()

#方向ベクトル
dir = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1)
    ]

#最初は黒(2)スタート
s_player = 2

@app.route("/")
def game_start():
    return render_template("game_start.html")

@app.route("/game_playing")
def index():
    valid_moves = get_valid_moves(s_player)
    return render_template("index.html", board=board,s_player=s_player, valid_moves=valid_moves)

def get_flip_stone(r, c, player):
    if board[r][c] != 0:
        return []

    if player == 2:
        opponent = 1
    else:
        opponent = 2
    stones_flip = []

    for dy, dx in dir:
        y = dy + r
        x = dx + c
        stones = []

        while 0<=y<board_size and 0<=x<board_size and board[y][x] == opponent:
            stones.append((y, x))
            y += dy
            x += dx
        
        if 0<=y<board_size and 0<=x<board_size and board[y][x] == player:
            stones_flip.extend(stones)

    return stones_flip

def get_valid_moves(player):
    moves = []

    for r in range(board_size):
        for c in range(board_size):
            stones = get_flip_stone(r, c, player)
            if len(stones) > 0:
                moves.append((r, c))

    return moves

def flip_stone(stones, player):
    for y, x in stones:
        board[y][x] = player

def switch():
    global s_player
    if s_player == 1:
        s_player = 2
    else:
        s_player = 1

@app.route("/place", methods=["POST"])
def place():
    global s_player
    r = int(request.form["row"])
    c = int(request.form["col"])

    stones = get_flip_stone(r, c, s_player)

    if len(stones) > 0:
        board[r][c] = s_player
        flip_stone(stones, s_player)
        switch()

        if not has_valid_move(s_player):
            switch()

            if not has_valid_move(s_player):
                return redirect(url_for("game_over"))

    return redirect(url_for("index"))

def has_valid_move(player):
    for r in range(board_size):
        for c in range(board_size):
            stones = get_flip_stone(r, c, player)
            if len(stones) > 0:
                return True
    return False

@app.route("/game_over")
def game_over():
    black = sum(row.count(2) for row in board)
    white = sum(row.count(1) for row in board)

    return render_template("game_over.html", black=black, white=white, board=board)

@app.route("/reset")
def reset():
    global board, s_player
    board = init_board()
    s_player = 2
    return redirect(url_for("game_start"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)