.PHONY: build clean run

HS_FILE := countdown.hs
HS_BIN := countdown
GHC_FLAGS := -O2

build:
	ghc $(GHC_FLAGS) -o $(HS_BIN) $(HS_FILE)

clean:
	rm -f $(HS_BIN) *.hi *.o

run: build
	./$(HS_BIN) 765 1 3 7 10 25 50