#include <iostream>
#include <random>
#include <time.h>
using namespace std;

mt19937 rnd(time(0));

int get_rnd(int r) {
    return abs(int(rnd())) % r;
}

int level, n, m;
string player;

void make_move() {
    vector<vector<char>> field(n, vector<char>(m));
    int my_x = -1, my_y = -1;
    char my_ptr = player == "RED" ? 'R' : 'B';

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> field[i][j];
            if (field[i][j] == my_ptr) {
                my_x = i;
                my_y = j;
            }
        }
    }

    int xc[] = {0, 1, 0, -1};
    int yc[] = {-1, 0, 1, 0};

    vector<int> possible_moves;
    char lit[] = {'L', 'D', 'R', 'U'};

    for (int move = 0; move < 4; move++) {
        int nx = my_x + xc[move];
        int ny = my_y + yc[move];
        if (nx >= 0 && nx < n && ny >= 0 && ny < m && field[nx][ny] == '.') {
            possible_moves.push_back(move);
        }
    }

    cout << lit[possible_moves[get_rnd(possible_moves.size())]] << endl;
    cout.flush();
}
int main() {
    cin >> player >> level >> n >> m;
    while(true) {
        make_move();
    }
}