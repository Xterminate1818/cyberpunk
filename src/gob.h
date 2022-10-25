#pragma once
#include <stdint.h>

typedef uint64_t index_t;

class Gob {
 public:
  inline virtual void input() {}
  inline virtual void process(float delta) {}
  inline virtual void draw() {}
};
