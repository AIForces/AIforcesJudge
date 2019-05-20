def make_move():
    board = [input().split() for _ in range(n)]
    my_ptr = 'R' if player == 'RED' else 'B'
    my_x = my_y = None
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == my_ptr:
                my_x = i
                my_y = j
    delta = [[0, -1, 'L'], [-1, 0, 'U'], [0, 1, 'R'], [1, 0, 'D']]
    for move in delta:
        nx = my_x + move[0]
        ny = my_y + move[1]
        if nx in range(n) and ny in range(m):
            if board[nx][ny] == '.':
                print(move[2])
                return


if __name__ == '__main__':
    player = input()
    level = int(input())
    n, m = map(int, input().split())
    while True:
        make_move()
