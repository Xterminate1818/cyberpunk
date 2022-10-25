#pragma once
#include "./gob.h"
#include <queue>
#include <raylib.h>
#include <string>
#include <vector>

class Painter {
protected:
  Texture atlas;
  std::vector<int> layer_vec;
  std::vector<Rectangle> source_vec;
  std::vector<Rectangle> destination_vec;
  std::vector<Vector2> origin_vec;
  std::vector<float> rotation_vec;
  std::vector<Color> tint_vec;

public:
  Painter(std::string path);
  index_t test;
};
