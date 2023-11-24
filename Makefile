all: test

test:
	./fretty.py --version
	./fretty.py --help
	./fretty.py example/C-major-scale-box1.ft -o test-img-01.svg
	./fretty.py -p xml example/document.xhtml -o test-doc-01.html
	./fretty.py -p xhtml example/document.xhtml -o test-doc-02.html
	./fretty.py -p xhtml --png example/document.xhtml -o test-doc-03.html
	./fretty.py example/Amaj7-chord.ft -o test-img-02.svg
	./fretty.py example/Cm-chord.ft -o test-img-03.svg

clean:
	rm -f *.html *.svg *.png
