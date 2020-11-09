#include <algorithm>
#include <cstring>
#include <ctime>
#include <map>
#include <queue>
#include <string>
#include <vector>

using namespace std;
using T = uint64_t;

class Node {
 public:
  T state, parent;
  char action;
  int cost, h;
  
  Node(T a, T b, char c, int d, int e)
      : state(a), parent(b), action(c), cost(d), h(e) {}
  
  bool operator<(const Node& rhs) const {
  	return cost + h > rhs.cost + rhs.h;
  }  
};

const char* dir = "LRUD";
const int dr[] = { 0,  0, -1, +1};
const int dc[] = {-1, +1,  0,  0};
int LENGTH;
int SIZE;
int BITS;
int ONES; // (1 << BITS) - 1
T GOAL;

T hash_board(vector<int>& a) {
  T ret = 0;
  for (int i = 0; i < SIZE; ++i) {
    ret |= (T)i << (a[i] * BITS);  	
  }
  return ret;
}

void init_consts(int n) {
  LENGTH = n;
  SIZE = n * n;
  BITS = 0;
  while ((1 << BITS) < SIZE) {
    ++BITS;
  }
  ONES = (1 << BITS) - 1;
  vector<int> goal_board(SIZE);
  for (int i = 0; i < SIZE; ++i) {
    goal_board[i] = i + 1;
  }
  goal_board[SIZE - 1] = 0;
  GOAL = hash_board(goal_board);
}

bool solvable(vector<int>& p) {
  int inv = 0;
  for (int i = 0; i < SIZE; ++i) {
    for (int j = i + 1; j < SIZE; ++j) {
      if (p[i] && p[j] && p[i] > p[j])
        ++inv;
    }
  }
  if (LENGTH % 2 == 1) {
    return inv % 2 == 0;
  } else {
    int row = LENGTH - ((find(p.begin(), p.end(), 0) - p.begin()) / LENGTH);
    return row % 2 != inv % 2;
  }
}

char* c_get_solvable(int n) {
  init_consts(n);
  vector<int> board(SIZE);
  for (int i = 0; i < SIZE; ++i) {
    board[i] = i;  	
  }
  srand(time(NULL));
  for (int i = 0; i < 10; ++i) {
    random_shuffle(board.begin(), board.end());
  }
  while (!solvable(board)) {
    random_shuffle(board.begin(), board.end());  	
  }
  string board_string;
  for (int i = 0; i < SIZE; ++i) {
    board_string.append(to_string(board[i]));
    if (i + 1 != SIZE) {
      board_string.append(" ");
    }
  }
  char* ret = (char*)malloc(board_string.size() + 1);
  strcpy(ret, board_string.c_str());
  return ret;
}

// Sum of Manhattan Distances
int heuristic(T a, T b) {
  int ret = 0;
  a >>= BITS;
  b >>= BITS;
  for (int i = 0; i < SIZE - 1; ++i, a >>= BITS, b >>= BITS) {
    int pos1 = a & ONES;
    int pos2 = b & ONES;
    ret += abs(pos1 / LENGTH - pos2 / LENGTH);
    ret += abs(pos1 % LENGTH - pos2 % LENGTH);
  }
  return ret;
}

vector<pair<T, int>> actions(T state) {
  vector<pair<T, int>> ret;
  int pos = state & ONES; // Position of empty tile
  int row = pos / LENGTH;
  int col = pos % LENGTH;
  for (int direction = 0; direction < 4; ++direction) {
    int new_row = row + dr[direction];
    int new_col = col + dc[direction];
    if (new_row >= 0 && new_row < LENGTH && new_col >= 0 && new_col < LENGTH) {
      int new_pos = new_row * LENGTH + new_col;
      int swap_pos = -1;
      for (int i = 0; i < SIZE; ++i) {
        if ((int)((state >> (i * BITS)) & ONES) == new_pos) {
          swap_pos = i;
          break;
        }
      }
      T new_state = state;
      new_state &= ~ONES;
      new_state &= ~((T)ONES << (swap_pos * BITS));
      new_state |= new_pos;
      new_state |= (T)pos << (swap_pos * BITS);
      ret.emplace_back(new_state, direction);
    }
  }
  return ret;
}

/*
 * Bidirectional A star.
 * Pre-condition: Board is solvable.
 */
string c_solve_bidirectional(T source) {
  priority_queue<Node> q[2];
  map<T, pair<T, char>> last[2]; // pair<parent_mask, action>
  T goal[2] = {GOAL, source};
  // $ for no action
  q[0].emplace(source, 0, '$', 0, heuristic(source, GOAL));
  q[1].emplace(GOAL  , 0, '$', 0, heuristic(source, GOAL));
  vector<T> candidates;
  bool done = false;
  while (!done) {
    done = true;
    for (int i = 0; i < 2; ++i) {
      if (!q[i].empty()) {
        done = false;
        auto top = q[i].top();
        q[i].pop();
        if (last[i].count(top.state)) continue;
        last[i][top.state] = {top.parent, top.action};
        candidates.push_back(top.state);
        for (auto& action : actions(top.state)) {
          if (!last[i].count(action.first)) {
            q[i].emplace(
              action.first,
              top.state,
              action.second,
              top.cost + 1,
              heuristic(action.first, goal[i])
            );
          }
        }
      }
    }
    for (auto& candidate : candidates) {
      if (last[0].count(candidate) && last[1].count(candidate)) {
        // Build answer
        string ret;
        T cur = candidate;
        while (true) {
          auto prev = last[0][cur];
          if (prev.second == '$')
            break;
          
          ret.push_back(dir[(int)prev.second]);
          cur = prev.first;
        }
        reverse(ret.begin(), ret.end());
        cur = candidate;
        while (true) {
          auto prev = last[1][cur];
          if (prev.second == '$')
            break;
          
          ret.push_back(dir[prev.second ^ 1]);
          cur = prev.first;
        }
        return ret;
      }
    }
    candidates.clear();
  }
}
