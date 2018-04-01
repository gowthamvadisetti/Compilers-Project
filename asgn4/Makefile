all:
	mkdir bin
	python -m compileall src/*
	mv src/lexer.pyc bin/lexer.pyc
	mv src/main.pyc bin/main.pyc
	mv src/parser2.pyc bin/irgen
	chmod +x bin/irgen

clean:
	rm -rf bin
	rm -rf src/__*
	rm -rf src/*.pyc
	rm -rf src/*.out
	rm -rf test/*.html
	rm -rf demo/*.html
	# rm -rf test/*.ir
	rm -rf src/parsetab.py
