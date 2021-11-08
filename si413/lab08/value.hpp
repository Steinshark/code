/* SI 413 Fall 2021
 * Lab 8
 * C++ header file for the Value class.
 */

#ifndef VALUE_HPP
#define VALUE_HPP

#include <iostream>
#include <cstdlib>
using namespace std;

// Forward declarations needed for the closure class.
class Lambda;
class Frame;

// A closure is a simple struct to tie a Lambda* function node
// in the AST to a Frame* representing the referencing environment
// where the Lambda should be executed.
struct Closure {
  Lambda* lam;
  Frame* env;
};

// This gives the type of what's stored in the Value object.
// NONE_T means nothing has been set yet.
enum VType {
  NUM_T, BOOL_T, FUN_T, NONE_T
};

class Value {
  private:
    // The value is either an int, a bool, or a pointer to a Lambda.
    union {
      int num;
      bool tf;
      Closure func;
    } val;

    VType type;

  public:
    /* default constructor, set to NONE TYPE */
    explicit Value() { type = NONE_T; }

    /* set the type to NUM */
    explicit Value(int n) {
      type = NUM_T;
      val.num = n;
    }

    /* set the type to BOOL */
    explicit Value(bool b) {
      type = BOOL_T;
      val.tf = b;
    }

    /* set the type to FUN */
    explicit Value(Lambda* lam, Frame* env) {
      type = FUN_T;
      val.func.lam = lam;
      val.func.env = env;
    }

    VType getType() { return type; }
    void setType(VType t) { type = t; }

    int num() { return val.num; }

    bool tf() { return val.tf; }

    Closure func() { return val.func; }

    /* Writes a representation of this Value object to the
     * named output stream, according to the stored type.
     */
    void writeTo(ostream& out) {
      switch(type) {
        case NUM_T: out << val.num; break;
        case BOOL_T: out << (val.tf ? "true" : "false"); break;
        case FUN_T: out << "closure"; break;
        case NONE_T: out << "UNSET"; break;
      }
    }

    /* This function makes equality testing work using the == operator.
     * So for instance if we have
     * Value v1, v2;
     * then we can write
     * v1 == v2
     * and get a bool back only if they have the same type and value.
     * Note that != is NOT implemented.
     */
    bool operator==(const Value& other) {
      if (type != other.type) return false;
      switch(type) {
        case NUM_T: return val.num == other.val.num;
        case BOOL_T: return val.tf == other.val.tf;
        case FUN_T: return val.func.lam == other.val.func.lam
                           && val.func.env == other.val.func.env;
        case NONE_T: return true;
      }
    }
};


#endif // VALUE_HPP
