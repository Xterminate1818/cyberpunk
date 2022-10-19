#include <raylib.h>
#include "player.h"

int main() {
    const int screenWidth = 500;
    const int screenHeight = 500;
    Player p = Player();
    p.position.x = 100;
    p.position.y = 100;
    InitWindow(screenWidth, screenHeight, "raylib");
    SetTargetFPS(60);

    while (!WindowShouldClose()) {
        float delta = GetFrameTime();
        p.input();
        p.process(delta);
        BeginDrawing();
            ClearBackground(BLACK);
            p.draw(); 
        EndDrawing();
    }
    CloseWindow();
    return 0;    
}

