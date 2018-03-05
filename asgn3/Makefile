all:
	mkdir bin
	python -m compileall src/*
	mv src/lexer.pyc bin/lexer.pyc
	mv src/parser.pyc bin/parser
	chmod +x bin/parser

clean:
	rm -rf bin
	rm -rf src/__*
	rm -rf src/*.pyc
	rm -rf src/*.out
