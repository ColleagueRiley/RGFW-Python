CC = gcc

CUSTOM_CFLAGS = 

LIBS := -w -lgdi32 -lm -lopengl32 -ggdb -lwinmm
LIB_EXT = .dll

ifneq (,$(filter $(CC),winegcc x86_64-w64-mingw32-gcc))
    detected_OS := Windows
	LIB_EXT = .dll
else
	ifeq '$(findstring ;,$(PATH))' ';'
		detected_OS := Windows
	else
		detected_OS := $(shell uname 2>/dev/null || echo Unknown)
		detected_OS := $(patsubst CYGWIN%,Cygwin,$(detected_OS))
		detected_OS := $(patsubst MSYS%,MSYS,$(detected_OS))
		detected_OS := $(patsubst MINGW%,MSYS,$(detected_OS))
	endif
endif

ifeq ($(detected_OS),Windows)
	LIBS := -ggdb -lshell32 -lgdi32 -lopengl32 -lwinmm
	LIB_EXT = .dll
endif
ifeq ($(detected_OS),Darwin)        # Mac OS X
	LIBS := -lm -framework Foundation -framework AppKit -framework OpenGL -framework CoreVideo -w
	LIB_EXT = .dylib
endif
ifeq ($(detected_OS),Linux)
    LIBS := -lXrandr -lX11 -lm -lGL
	LIB_EXT = .so
endif

all:
	make libRGFW$(LIB_EXT)
	python3 basic.py

build-RGFW:
	make libRGFW$(LIB_EXT)	

clean:
	rm -f libRGFW.so libRGFW.dll libRGFW.dylib RGFW.o

debug:
	make clean
	make libRGFW$(LIB_EXT)
	python3 basic.py

RGFW.o:
	$(CC) $(CUSTOM_CFLAGS) -x c -c -D RGFW_OPENGL -D RGFW_BUFFER -D RGFW_IMPLEMENTATION -D RGFW_NO_JOYSTICK_CODES -fPIC RGFW.h

libRGFW$(LIB_EXT):
	make RGFW.o
	$(CC) $(CUSTOM_CFLAGS) -shared RGFW.o $(LIBS) -o libRGFW$(LIB_EXT)
