all:
	mkdir bin
	python -m compileall src/*
	mv src/lexer.pyc bin/lexer.pyc
	mv src/main_parser.pyc bin/main_parser.pyc
	mv src/main_codegen.pyc bin/codegen
	mv src/codegen.pyc bin/codegen.pyc
	mv src/parser2.pyc bin/irgen
	chmod +x bin/irgen
	chmod +x bin/codegen

clean:
	rm -rf bin
	rm -rf src/__*
	rm -rf src/*.pyc
	rm -rf src/*.out
	rm -rf test/*.html
	rm -rf demo/*.html
	rm -rf test/*.ir
	rm -rf src/parsetab.py

spim:
	spim -file mips/test1.asm

codegen:
	bin/codegen ir/test1.ir
