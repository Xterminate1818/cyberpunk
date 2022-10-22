#pragma once
#include <raylib.h>
#include "gob.h"

class Player: public Gob {
public:
    Vector2 position, velocity;
    float radius = 20.f;
    float speed = 100.f;

    Player();

    void input();

    void process(float delta);

    void draw();

};
   
