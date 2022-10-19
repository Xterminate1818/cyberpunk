CC ?= g++
CCFLAGS := -Wall -g -lstdc++ 
LINKER_FLAGS = -lraylib 

# path
BIN_PATH := bin
SRC_PATH := src

# compile
TARGET_NAME := raycast 
TARGET := $(BIN_PATH)/$(TARGET_NAME)

SRC := $(foreach x, $(SRC_PATH), $(wildcard $(addprefix $(x)/*,.c*)))
OBJ := $(addprefix $(OBJ_PATH)/, $(addsuffix .o, $(notdir $(basename $(SRC)))))

all: $(TARGET)

run: $(TARGET) 
	$(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CCFLAGS) -o $@ $(SRC) $(LINKER_FLAGS)

clean:
	rm $(TARGET)



