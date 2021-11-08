/* SI 413 Fall 2021
 * Lab 8
 * This file contains the implementations of longer methods in the
 * AST class hierarchy.
 */

#include "ast.hpp"

//Frame ST; // The actual declaration of the global symbol table

// ArithOp constructor
ArithOp::ArithOp(Exp* l, Oper o, Exp* r) {
  op = o;
  left = l;
  right = r;
  ASTchild(left);
  ASTchild(right);
}

// Evaluates an arithmetic operation
Value ArithOp::eval(Frame* f) {
  int l = left->eval(f).num();
  int r = right->eval(f).num();
  switch(op) {
    case ADD: return Value(l + r);
    case SUB: return Value(l - r);
    case MUL: return Value(l * r);
    case DIV:
      if (r != 0) return Value(l / r);
      else if (!error) {
        error = true;
        errout << "ERROR: Divide by zero" << endl;
      }
      break;
    default:
      // should never happen...
      errout << "Internal Error: Illegal arithmetic operator" << endl;
  }
  return Value();
}

// Constructor for CompOp
CompOp::CompOp(Exp* l, Oper o, Exp* r) {
  op = o;
  left = l;
  right = r;
  ASTchild(left);
  ASTchild(right);
}

// Constructor for BoolOp
BoolOp::BoolOp(Exp* l, Oper o, Exp* r) {
  op = o;
  left = l;
  right = r;
  ASTchild(left);
  ASTchild(right);
}
