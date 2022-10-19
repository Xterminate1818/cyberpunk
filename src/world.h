#pragma once
#include <unordered_map>
#include <string>
#include <memory>
#include "gob.h"
#include "raylib.h"

    
class World: public Gob {
protected:
    static const int WORLD_SIZE = 500;
    std::unique_ptr<int[WORLD_SIZE][WORLD_SIZE]> data;
public: 
    void input() {

    }

    void process(float delta) {

    }

    void draw() {
        
    }
};


