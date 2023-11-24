all: test

test:
	./fretty.py --version
	./fretty.py --help
	./fretty.py example/C-major-scale-box1.ft -o test-img-01.svg
	./fretty.py -p xml example/document.xhtml -o test-doc-01.html
	./fretty.py -p xhtml example/document.xhtml -o test-doc-02.html
	./fretty.py -p xhtml --png example/document.xhtml -o test-doc-03.html

clean:
	rm -f *.html *.svg *.png
