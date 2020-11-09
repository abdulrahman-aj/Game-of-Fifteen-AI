#include <Python.h>
#include <string>
#include <sstream>
#include <vector>

#include "util.hpp"

char* c_solve(std::string s) {
  std::stringstream in(s);
  std::vector<int> board;
  int tmp;
  while (in >> tmp) {
    board.push_back(tmp);
  }
  if ((int)board.size() == 9) {
    init_consts(3);
  } else {
    init_consts(4);
  }
  std::string ans = c_solve_bidirectional(hash_board(board));
  char* ret = (char*)malloc(ans.size() + 1);
  strcpy(ret, ans.c_str());
  return ret;
}

static PyObject* get_solvable(PyObject* self, PyObject* args) {
  int n;

  if (!PyArg_ParseTuple(args, "i", &n)) return NULL;

  return Py_BuildValue("s", c_get_solvable(n));
}

static PyObject* solve(PyObject* self, PyObject* args) {
  char *board;

  if (!PyArg_ParseTuple(args, "s", &board)) return NULL;
  
  return Py_BuildValue("s", c_solve(board));
}

static PyMethodDef methods[] = {
  {"get_solvable", get_solvable, METH_VARARGS, "get_solvable(N):\nGenerates a solvable NxN Puzzle."},
  {"solve", solve, METH_VARARGS, "solve(Board as numbers seperated by spaces):\nPre-conditions:\n1. 3x3 or 4x4.\n2. Solvable.\nReturns where to move the Zero tile."},
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef fifteen_module = {
  PyModuleDef_HEAD_INIT,  // Must
  "fifteen_solver",       // Module name
  "15 Puzzle Solver",     // Doc
  -1,                     // Global state
  methods                 // Methods
};

/*
 *  initializer function
 *  Name is strict: PyInit_module_name
 */
PyMODINIT_FUNC PyInit_fifteen_solver() {
  return PyModule_Create(&fifteen_module);
}
