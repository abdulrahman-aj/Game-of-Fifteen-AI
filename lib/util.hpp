#include <string>
#include <vector>

using T = uint64_t;

void init_consts(int);
char* c_get_solvable(int);
T hash_board(std::vector<int>&);
std::string c_solve_bidirectional(T);