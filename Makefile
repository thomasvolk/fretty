all: test

test:
	python3 -m pip install -e .
	mkdir -p out
	@echo "check help ..."
	fretty -v
	fretty -h
	@echo "start tests ..."
	fretty example/C-major-arpeggio.ft -o out/C-major-arpeggio.svg
	diff out/C-major-arpeggio.svg example/C-major-arpeggio.svg
	fretty example/C-major-scale-box1.ft -o out/C-major-scale-box1.svg
	diff out/C-major-scale-box1.svg example/C-major-scale-box1.svg
	fretty example/C-major-scale-box2.ft -o out/C-major-scale-box2.svg
	fretty example/Amaj7-chord.ft -o out/Amaj7-chord.svg
	fretty example/Cm-chord.ft -o out/Cm-chord.svg
	diff out/Cm-chord.svg example/Cm-chord.svg
	fretty example/Dm7-chord.ft -o out/Dm7-chord.svg
	diff out/Dm7-chord.svg example/Dm7-chord.svg
	fretty example/D-chord.ft -o out/D-chord.svg
	diff out/D-chord.svg example/D-chord.svg
	fretty example/C-major.ft -o out/C-major.svg
	diff out/C-major.svg example/C-major.svg
	fretty -V example/C-major.ft -o out/C-major.png


clean:
	rm -rf out build dist *.egg-info

uninstall:
	python3 -m pip uninstall fretty