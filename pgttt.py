# Solution code to "The Tic-Tac-Toe Mysteries of Xerloc O'Xolmes"
# https://blog.zarfhome.com/2024/08/tic-tac-toe-mysteries
# Bart Massey 2024

def blank_board():
    return [['.'] * 3 for _ in range(3)]

blank = blank_board()

posns = [
    ['a', 'b', 'c'],
    ['d', 'e', 'f'],
    ['g', 'h', 'i'],
]
locs = {posns[r][c] : (r, c) for r in range(3) for c in range(3)}
def loc(board, m):
    r, c = locs[m]
    return board[r][c]

def print_board(board):
    for row in board:
        print(''.join(row))

players = ['X', 'O']
def piece(player):
    return players[player]

def lines(board):
    lines = []
    for r in range(3):
        lines.append([(posns[r][c], board[r][c]) for c in range(3)])
    for c in range(3):
        lines.append([(posns[r][c], board[r][c]) for r in range(3)])
    lines.append([(posns[rc][rc], board[rc][rc]) for rc in range(3)])
    lines.append([(posns[rc][2 - rc], board[rc][2 - rc]) for rc in range(3)])
    return lines

def won(player, board):
    p = piece(player)
    for line in lines(board):
        np = 0
        for pos, square in line:
            if square == p:
                np += 1
        if np == 3:
            return True
    return False

def wins(player, board):
    wins = []
    p = piece(player)
    for line in lines(board):
        np = 0
        wp = None
        for pos, square in line:
            if square == p:
                np += 1
            elif square == '.':
                wp = pos
        if np == 2 and wp is not None:
            wins.append(wp)
    return wins

def blocks(player, board):
    blocks = []
    p = piece(1 - player)
    for line in lines(board):
        np = 0
        bp = None
        for pos, square in line:
            if square == p:
                np += 1
            elif square == '.':
                bp = pos
        if np == 2 and bp is not None:
            blocks.append(bp)
    return blocks

def free_moves(board):
    return [posns[r][c] for r in range(3) for c in range(3) if board[r][c] == '.']

def moves(player, board):
    r = wins(player, board)
    if r:
        return r
    r = blocks(player, board)
    if r:
        return r
    return free_moves(board)

def compatible_moves(player, board, target):
    p = piece(player)
    ms = moves(player, board)
    return [m for m in ms if loc(target, m) == p]

def ttt(board, target, player=0, played=[]):
    if board == target:
        return [played]
    ms = compatible_moves(player, board, target)
    if not ms:
         return []
    p = piece(player)
    seqs = []
    for m in ms:
        r, c = locs[m]
        board[r][c] = p
        seqs += ttt(board, target, player=1-player, played = played + [m])
        board[r][c] = '.'
    return seqs

def show_game(played):
    player = 0
    board = blank_board()
    for m in played:
        r, c = locs[m]
        board[r][c] = piece(player)
        print_board(board)
        print()
        player = 1 - player

# Problem 1
def p1():
    target = [
        ['O', 'O', 'X'],
        ['.', 'X', '.'],
        ['.', '.', 'X'],
    ]
    seqs = ttt(blank, target)
    m = seqs[0][-1]
    for s in seqs:
        assert s[-1] == m
    print(m)

# Problem 2
# Note that the question could be "What were the last three moves?"
# Answer is e, a, c
def p2():
    target = [
        ['X', 'X', 'O'],
        ['X', 'O', '.'],
        ['O', 'X', 'O'],
    ]
    seqs = ttt(blank, target)
    m = seqs[0][-1]
    for s in seqs:
        assert s[-1] == m
    print(m)

# Problem 3
def p3():
    target = [
        ['.', 'O', 'X'],
        ['.', 'X', 'O'],
        ['.', 'O', '.'],
    ]
    xs = []
    for p in ['a', 'd', 'i']:
        r, c = locs[p]
        target[r][c] = 'X'
        mseqs = ttt(blank, target)
        if mseqs:
            xs.append(p)
        target[r][c] = '.'
    print(xs[0])

# Problem 4
# There are two possible move sequences, so no.
def p4(show_games=False):
    target = [
        ['.', 'O', 'X'],
        ['X', 'X', 'X'],
        ['O', '.', 'O'],
    ]
    board = [
        ['.', '.', '.'],
        ['.', 'X', '.'],
        ['.', '.', '.'],
    ]
    mseqs = ttt(board, target, player=1, played=['e'])
    if show_games:
        for i, s in enumerate(mseqs):
            print(f"game {i + 1}:")
            show_game(s)
    else:
        print(mseqs)

# Problem 5
def p5():
    target_phi = [
        ['X', 'O', 'X'],
        ['O', 'O', '.'],
        ['.', '.', 'X'],
    ]
    if ttt(blank, target_phi):
        print("phi")
    target_theta = [
        ['O', 'X', 'O'],
        ['X', 'X', '.'],
        ['.', '.', 'O'],
    ]
    if ttt(blank, target_theta):
        print("theta")

# Problem 6
def p6():
    target = [
        ['X', 'O', 'O'],
        ['O', 'X', '.'],
        ['X', '.', '.'],
    ]
    for m in ['a', 'e', 'g']:
        board = blank_board()
        r, c = locs[m]
        board[r][c] = 'X'
        seqs = ttt(board, target, player=1, played=[m])
        lasts = {s[-1] for s in seqs}
        if len(lasts) > 1:
            print(m)

p1()
p2()
p3()
p4()
p5()
p6()
