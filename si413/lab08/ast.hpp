/* SI 413 Fall 2021
 * This is a C++ header file for the AST class hierarchy.
 * Lab 8
 * YOUR NAME HERE
 */

#ifndef AST_HPP
#define AST_HPP

#include <cstdlib>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
using namespace std;

#include "colorout.hpp"
#include "value.hpp"
#include "frame.hpp"

// This global variable is the actual global symbol table object.
// It is actually declared in the ast.cpp file, so we put keyword "extern"
// here.
//extern Frame ST;

// Declare the output streams to use everywhere
extern colorout resout;
extern colorout errout;

// Global variable to indicate if an error has occurred.
extern bool error;

// Global variable to indicate there is a human typing at a keyboard
extern bool showPrompt;

// This enum type gives codes to the different kinds of operators.
// Basically, each oper below such as DIV becomes an integer constant.
enum Oper {
  ADD, SUB,
  MUL, DIV,
  LT, GT, LE, GE,
  EQ, NE,
  AND, OR, NOT
};

// These are forward declarations for the classes defined below.
// They show the class hierarchy.
class AST;
  class Stmt;
    class NullStmt;
    class Block;
    class IfStmt;
    class WhileStmt;
    class NewStmt;
    class Asn;
    class Write;
  class Exp;
    class Id;
    class Num;
    class BoolExp;
    class ArithOp;
    class CompOp;
    class BoolOp;
    class NegOp;
    class NotOp;
    class Read;
    class Lambda;
    class Funcall;

/* The AST class is the super-class for abstract syntax trees.
 * Every type of AST (or AST node) has its own subclass.
 */
class AST {
  private:
  protected:
    // These two protected fields determine the structure of the AST.
    vector<AST*> children;

    // Inserts a new AST node as a child of this one.
    void ASTchild(AST* child) { children.push_back(child); }

  public:
    /* Makes a new "empty" AST node. */
    AST() { }

    /* Deallocates memory for this AST note and its children. */
    virtual ~AST() {
      for (AST* child : children) delete child;
      children.clear();
    }
};

/* Every AST node that is not a Stmt is an Exp.
 * These represent actual computations that return something
 * (in particular, a Value object).
 */
class Exp :public AST {
  public:
    /* This is the method that must be overridden by all subclasses.
     * It should perform the computation specified by this node, and
     * return the resulting value that gets computed. */
    virtual Value eval(Frame* f) = 0;
};

/* An identifier, i.e. variable or function name. */
class Id :public Exp {
  private:
    string val;

  public:
    // Constructor from a C-style string
    Id(const char* v) {
      val = v;
    }

    // Returns a reference to the stored string value.
    string& getVal() { return val; }

    // Note the Frame class is responsible for error checking.
    Value eval(Frame* f) override { return f->lookup(val); }
};

/* A literal number in the program. */
class Num :public Exp {
  private:
    int val;

  public:
    Num(int v) {
      val = v;
    }

    // To evaluate, just return the number!
    Value eval(Frame* f) override { return Value(val); }
};

/* A literal boolean value like "true" or "false" */
class BoolExp :public Exp {
  private:
    bool val;

  public:
    BoolExp(bool v) {
      val = v;
    }

    // To evaluate, just return the bool
    Value eval(Frame* f) override { return Value(val); }
};

/* A binary opration for arithmetic, like + or *. */
class ArithOp :public Exp {
  private:
    Oper op;
    Exp* left;
    Exp* right;

  public:
    ArithOp(Exp* l, Oper o, Exp* r);

    Value eval(Frame* f) override; // this is implemented in ast.cpp
};

/* A binary operation for comparison, like < or !=. */
class CompOp :public Exp {
  private:
    Oper op;
    Exp* left;
    Exp* right;

  public:
    CompOp(Exp* l, Oper o, Exp* r);

    Value eval(Frame* f) override {
      int l = left->eval(f).num();
      int r = right->eval(f).num();
      if (l < r)      return Value(op == LT || op == LE || op == NE);
      else if (l > r) return Value(op == GT || op == GE || op == NE);
      else            return Value(op == LE || op == GE || op == EQ);
    }
};

/* A binary operation for boolean logic, like "and". */
class BoolOp :public Exp {
  private:
    Oper op;
    Exp* left;
    Exp* right;

  public:
    BoolOp(Exp* l, Oper o, Exp* r);

    Value eval(Frame* f) override {
      bool first = left->eval(f).tf();
      // short-circuit check
      if ((first && op == OR) || (!first && op == AND)) {
        return Value(first);
      }
      else {
        // can't short-circuit, so return the result of the second part.
        return right->eval(f);
      }
    }
};

/* This class represents a unary negation operation. */
class NegOp :public Exp {
  private:
    Exp* right;

  public:
    NegOp(Exp* r) {
      right = r;
      ASTchild(right);
    }

    Value eval(Frame* f) override {
      return Value(- right->eval(f).num());
    }
};

/* This class represents a unary "not" operation. */
class NotOp :public Exp {
  private:
    Exp* right;

  public:
    NotOp(Exp* r) {
      right = r;
      ASTchild(right);
    }

    Value eval(Frame* f) override {
      return Value(! right->eval(f).tf());
    }
};

/* A read expression. */
class Read :public Exp {
  public:
    Read() { }

    Value eval(Frame* f) override {
      if (showPrompt) cerr << "read> ";
      int v;
      cin >> v;
      return Value(v);
    }
};

/* A Stmt is anything that can be evaluated at the top level such
 * as I/O, assignments, and control structures.
 * The last child of any statement is the next statement in sequence.
 */
class Stmt :public AST {
  private:
    // Pointer to the next statement in sequence, default null.
    Stmt* next = nullptr;

  public:
    // Default constructor. Note that the setNext method must be
    // called by the parser at some point after construction.
    Stmt () { }

    // Getter and setter for the next statement in sequence.
    Stmt* getNext() { return next; }
    void setNext(Stmt* nextStmt) {
      if (next != nullptr) {
        errout << "Unexpected parser error: trying to set next, but next already set!" << endl;
        delete next;
        children.pop_back();
      }
      children.push_back(nextStmt);
      next = nextStmt;
    }

    /* This is the command that must be implemented everywhere to
     * execute this Stmt - that is, do whatever it is that this statement
     * says to do. */
    virtual void exec(Frame* f) = 0;
};

/* This class is necessary to terminate a sequence of statements. */
class NullStmt :public Stmt {
  public:
    NullStmt() { }

    // Nothing to execute!
    void exec(Frame* f) override { }
};

/* This is a statement for a block of code, i.e., code enclosed
 * in curly braces { and }.
 * Eventually, this is where scopes will begin and end.
 */
class Block :public Stmt {
  private:
    Stmt* body;

  public:
    Block(Stmt* b) {
      body = b;
      ASTchild(body);
    }

    void exec(Frame* f) override {
      Frame* newFrame = new Frame(f);
      body->exec(newFrame);
      getNext()->exec(f);
    }
};

/* This class is for "if" AND "ifelse" statements. */
class IfStmt :public Stmt {
  private:
    Exp* clause;
    Stmt* ifblock;
    Stmt* elseblock;

  public:
    IfStmt(Exp* e, Stmt* ib, Stmt* eb) {
      clause = e;
      ifblock = ib;
      elseblock = eb;
      ASTchild(clause);
      ASTchild(ifblock);
      ASTchild(elseblock);
    }

    void exec(Frame* f) override {
      if (clause->eval(f).tf()) ifblock->exec(f);
      else elseblock->exec(f);
      getNext()->exec(f);
    }
};

/* Class for while statements. */
class WhileStmt :public Stmt {
  private:
    Exp* clause;
    Stmt* body;

  public:
    WhileStmt(Exp* c, Stmt* b) {
      clause = c;
      body = b;
      ASTchild(clause);
      ASTchild(body);
    }

    void exec(Frame* f) override {
      while (clause->eval(f).tf()) {
        body->exec(f);
      }
      getNext()->exec(f);
    }
};

/* A "new" statement creates a new binding of the variable to the
 * stated value.  */
class NewStmt :public Stmt {
  private:
    Id* lhs;
    Exp* rhs;

  public:
    NewStmt(Id* l, Exp* r) {
      lhs = l;
      rhs = r;
      ASTchild(lhs);
      ASTchild(rhs);
    }

    void exec(Frame* f) override {
      f->bind(lhs->getVal(), rhs->eval(f));
      getNext()->exec(f);
    }
};

/* An assignment statement. This represents a RE-binding in the symbol table. */
class Asn :public Stmt {
  private:
    Id* lhs;
    Exp* rhs;

  public:
    Asn(Id* l, Exp* r) {
      lhs = l;
      rhs = r;
      ASTchild(lhs);
      ASTchild(rhs);
    }

    void exec(Frame* f) override {
      f->rebind(lhs->getVal(), rhs->eval(f));
      getNext()->exec(f);
    }
};

/* A write statement. */
class Write :public Stmt {
  private:
    Exp* val;

  public:
    Write(Exp* v) {
      val = v;
      ASTchild(val);
    }

    void exec(Frame* f) override {
      Value res = val->eval(f);
      if (!error) {
        res.writeTo(resout);
        resout << endl;
      }
      getNext()->exec(f);
    }
};

/* A debugging statement embedded in the code. */
class Debug :public Stmt {
  private:
    string msg;

  public:
    Debug(const string& themsg) {
      msg = themsg;
    }

    void exec(Frame* f) override {
      if (!error) {
        resout << msg << endl;
      }
      getNext()->exec(f);
    }
};

/* A lambda expression consists of a parameter name and a body. */
class Lambda :public Exp {
  private:
    Id* var;
    Stmt* body;

  public:
    Lambda(Id* v, Stmt* b) {
      var = v;
      body = b;
      ASTchild(var);
      ASTchild(body);
    }

    // These getter methods are necessary to support actually calling
    // the lambda sometime after it gets created.
    string& getVar() { return var->getVal(); }
    Stmt* getBody() { return body; }

    Value eval(Frame* f) override {
      return Value(this,f);

    }
};

/* A function call consists of the function name, and the actual argument.
 * Note that all functions are unary. */
class Funcall :public Exp {
  private:
    Exp* funexp;
    Exp* arg;

  public:
    Funcall(Exp* f, Exp* a) {
      funexp = f;
      arg = a;
      ASTchild(funexp);
      ASTchild(arg);
    }

    Value eval(Frame* f) override {
        Closure closure = funexp->eval(f).func();

        // Create the new frame
        Frame* new_frame = new Frame(closure.env);

        //bind the ret value
        new_frame->bind("ret",Value());

        // Evaluate and bind the argument to the parameter name
        Value argument = arg->eval(f);
        new_frame->bind(closure.lam->getVar(), argument);

        // Evaluate the function body
        closure.lam->getBody()->exec(new_frame);

        // return
        return new_frame->lookup("ret");
    }
};

#endif //AST_HPP
