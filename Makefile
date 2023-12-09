all: test

test:
	mkdir -p out
	./fretty.py --version
	./fretty.py --help
	./fretty.py example/C-major-scale-box1.ft -o out/C-major-scale-box1.svg
	./fretty.py example/C-major-scale-box2.ft -o out/C-major-scale-box2.svg
	./fretty.py -p xml example/document.xhtml -o out/test-doc-01.html
	./fretty.py -p xhtml example/document.xhtml -o out/test-doc-02.html
	./fretty.py -p xhtml --png example/document.xhtml -o out/test-doc-03.html
	./fretty.py example/Amaj7-chord.ft -o out/Amaj7-chord.svg
	./fretty.py example/Cm-chord.ft -o out/Cm-chord.svg
	./fretty.py example/D-chord.ft -o out/D-chord.svg

clean:
	rm -rf out
