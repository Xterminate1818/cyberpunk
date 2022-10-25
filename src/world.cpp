#include "./world.h"
#include <raylib.h>

World::World() {}

void World::input() {}

void World::process(float _delta) {}

void World::draw() {
  for (int x = 0; x < WORLD_SIZE; x++) {
    for (int y = 0; y < WORLD_SIZE; y++) {
      DrawRectangle(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, BLUE);
    }
  }
}
