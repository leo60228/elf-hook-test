CC=gcc
CXX=g++

all: do_math.bin hook.o

do_math.bin: do_math.c
	$(CC) $^ -g3 -o $@ -lm
	chmod u+rx $@

hook.o: hook.c
	$(CC) -nostdlib -nodefaultlibs -fPIC -c $^ -o $@

run: all
	unset LD_LIBRARY_PATH
	./do_math.bin 1
	python3 insert_hook.py
	LD_LIBRARY_PATH=. ./do_math.bin 1

.PHONY: clean

clean:
	rm -rf *.o *~ *.so *.bin hook libm.so.6
