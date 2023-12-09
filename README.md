# fretty

fretty is a guitar fretboard generator.

```
III
- - o - o #
- - o o - o
- o # - o -
o - o - o -
# - o - o -
o - o - o -
```

The first line is the position of the starting fret.
Every line which follows is the representation on string.

* 'o' is a node
* '#' is a note as square shape
* '-' is an empty place



how to run:

    ./fretty.py my-scale.ft -o my-scale.svg

This will produce the file my-scale.svg

