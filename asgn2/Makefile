all:
	mkdir bin
	python -m compileall src/*
	mv src/codegen.pyc bin/codegen.pyc
	mv src/main.pyc bin/codegen
	chmod +x bin/codegen

clean:
	rm -rf bin
	rm -rf src/__*