#include <iostream>
#include <random>
using namespace std;

mt19937 rnd;

int get_rnd(int r) {
    return abs(int(rnd())) % r;
}
void make_move() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> field(n, vector<int>(m));
    int my_x = -1, my_y = -1;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> field[i][j];
            if (field[i][j] == 1) {
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
        if (nx >= 0 && nx < n && ny >= 0 && ny < m && field[nx][ny] == 0) {
            possible_moves.push_back(move);
        }
    }

    cout << lit[possible_moves[get_rnd(possible_moves.size())]] << endl;
    cout.flush();
}
int main() {
    int map;
    cin >> map;

    while(true) {
        make_move();
    }
}