#pragma once
#include <memory>
#include "./gob.h"

class World : public Gob {
 protected:
  static const int WORLD_SIZE = 100;
  static const int TILE_SIZE = 16;
  std::unique_ptr<int[WORLD_SIZE][WORLD_SIZE]> data;

 public:
  World();

  void input();

  void process(float delta);

  void draw();
};
