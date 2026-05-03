FRETTY_LOCAL=python -m fretty
COLOR=\#2d2d77

all: test

build:
	pip install build
	python -m build --wheel

install: build
	pip install -r requirements.txt
	pip install -e .

test:
	mkdir -p out
	@echo "check help ..."
	$(FRETTY_LOCAL) -v
	$(FRETTY_LOCAL) -h
	$(FRETTY_LOCAL) example/Dm7-chord.ft
	@echo "start tests ..."
	$(FRETTY_LOCAL) --drawing-color '$(COLOR)' example/C-major-arpeggio.ft -o out/C-major-arpeggio.svg
	diff out/C-major-arpeggio.svg example/C-major-arpeggio.svg
	$(FRETTY_LOCAL) --drawing-color '$(COLOR)' example/C-major-scale-box1.ft -o out/C-major-scale-box1.svg
	diff out/C-major-scale-box1.svg example/C-major-scale-box1.svg
	$(FRETTY_LOCAL) --drawing-color '$(COLOR)' example/C-major-scale-box2.ft -o out/C-major-scale-box2.svg
	$(FRETTY_LOCAL) --drawing-color '$(COLOR)' example/Amaj7-chord.ft -o out/Amaj7-chord.svg
	$(FRETTY_LOCAL) --drawing-color '$(COLOR)' example/Cm-chord.ft -o out/Cm-chord.svg
	diff out/Cm-chord.svg example/Cm-chord.svg
	$(FRETTY_LOCAL) --drawing-color '$(COLOR)' example/Dm7-chord.ft -o out/Dm7-chord.svg
	diff out/Dm7-chord.svg example/Dm7-chord.svg
	$(FRETTY_LOCAL) --drawing-color '$(COLOR)' example/D-chord.ft -o out/D-chord.svg
	diff out/D-chord.svg example/D-chord.svg
	$(FRETTY_LOCAL) --drawing-color '$(COLOR)' example/C-major.ft -o out/C-major.svg
	diff out/C-major.svg example/C-major.svg
	$(FRETTY_LOCAL) --drawing-color '$(COLOR)' -V example/C-major.ft -o out/C-major.png

upload: build
	pip install twine
	PYTHONIOENCODING=utf-8 twine upload --repository pypi dist/*

upload-test: build
	pip install twine
	PYTHONIOENCODING=utf-8 twine upload --repository testpypi dist/*

clean:
	rm -rf out build dist *.egg-info venv

