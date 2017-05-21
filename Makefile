CC=gcc
FLAGS=-g

stress_strain: stress_strain.o randoms.o
	$(CC) -g -o stress_strain randoms.o stress_strain.o -lm

stress_strain.o: stress_strain.c
	$(CC) -g -c -o stress_strain.o stress_strain.c -lm

randoms.o: randoms.c
	$(CC) -g -c -o randoms.o randoms.c -lm

clean:
	rm stress_strain stress_strain.o randoms.o
