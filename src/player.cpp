#include "player.h"

Player::Player() {
    position = Vector2{0.f, 0.f};
}

void Player::input() {
    int x, y;
    x = IsKeyDown(KEY_D) - IsKeyDown(KEY_A);
    y = IsKeyDown(KEY_S) - IsKeyDown(KEY_W);
    velocity.x += x * speed;
    velocity.y += y * speed;
}

void Player::process(float delta) {
    position.x += velocity.x * delta;
    position.y += velocity.y * delta;

    velocity.x = 0.f;
    velocity.y = 0.f;
}

void Player::draw() {
    DrawCircleV(position, radius, GREEN);
}

