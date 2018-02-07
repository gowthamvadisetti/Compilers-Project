all:
	mkdir bin
	python -m compileall src/lexer.py
	mv src/lexer.pyc bin/lexer
	chmod +x bin/lexer
clean:
	rm -f bin/*
	rm -f lex
	rm -f sys