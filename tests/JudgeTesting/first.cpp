#include <iostream>
using namespace std;

int main() {
	int x, y;
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++) {
			int a;
			cin >> a;
			if (a == 0) {
				x = i;
				y = j;
			}
		}
	}
	cout << x << ' ' << y << '\n';
}