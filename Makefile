all: test

PYTHON=./venv/bin/python3
FRETTY=./venv/bin/fretty
TWINE=./venv/bin/twine


venv:
	python3 -m venv venv
	$(PYTHON) -m pip install CairoSVG
	$(PYTHON) -m pip install build
	$(PYTHON) -m pip install twine
	

$(FRETTY): venv
	$(PYTHON) -m pip install -e .

test: $(FRETTY)
	mkdir -p out
	@echo "check help ..."
	$(FRETTY) -v
	$(FRETTY) -h
	$(FRETTY) example/Dm7-chord.ft
	@echo "start tests ..."
	$(FRETTY) example/C-major-arpeggio.ft -o out/C-major-arpeggio.svg
	diff out/C-major-arpeggio.svg example/C-major-arpeggio.svg
	$(FRETTY) example/C-major-scale-box1.ft -o out/C-major-scale-box1.svg
	diff out/C-major-scale-box1.svg example/C-major-scale-box1.svg
	$(FRETTY) example/C-major-scale-box2.ft -o out/C-major-scale-box2.svg
	$(FRETTY) example/Amaj7-chord.ft -o out/Amaj7-chord.svg
	$(FRETTY) example/Cm-chord.ft -o out/Cm-chord.svg
	diff out/Cm-chord.svg example/Cm-chord.svg
	$(FRETTY) example/Dm7-chord.ft -o out/Dm7-chord.svg
	diff out/Dm7-chord.svg example/Dm7-chord.svg
	$(FRETTY) example/D-chord.ft -o out/D-chord.svg
	diff out/D-chord.svg example/D-chord.svg
	$(FRETTY) example/C-major.ft -o out/C-major.svg
	diff out/C-major.svg example/C-major.svg
	$(FRETTY) -V example/C-major.ft -o out/C-major.png

build: test
	$(PYTHON) -m build --wheel

upload: build
	PYTHONIOENCODING=utf-8 $(TWINE) upload --repository pypi dist/*

upload-test: build
	PYTHONIOENCODING=utf-8 $(TWINE) upload --repository testpypi dist/*

clean:
	rm -rf out build dist *.egg-info venv

