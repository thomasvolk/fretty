# fretty

fretty is a guitar fretboard generator.

    XII
    -o--
    --o-
    --R-
    ----
    ----

The first line is the position of the starting fret.
Every line which follows is the representation on string.

* 'o' is one node
* 'R' is the root note
* '-' is an empty place

how to run:

    ./fretty.py my-scale.ft -o my-scale.svg

This will produce the file my-scale.svg

