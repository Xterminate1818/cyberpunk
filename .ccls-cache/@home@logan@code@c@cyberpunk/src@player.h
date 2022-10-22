#pragma once
#include <raylib.h>
#include "gob.h"

class Player: public Gob {
public:
    Vector2 position, velocity;
    float radius = 20.f;
    float speed = 100.f;

    inline Player() {
        position = Vector2{0.f, 0.f};
    }

    inline void input() {
        int x, y;
        x = IsKeyDown(KEY_D) - IsKeyDown(KEY_A);
        y = IsKeyDown(KEY_S) - IsKeyDown(KEY_W);
        velocity.x += x * speed;
        velocity.y += y * speed;
    }

    inline void process(float delta) {
        position.x += velocity.x * delta;
        position.y += velocity.y * delta;

        velocity.x = 0.f;
        velocity.y = 0.f;
    }

    inline void draw() {
        DrawCircleV(position, radius, GREEN);
    }

};
   
