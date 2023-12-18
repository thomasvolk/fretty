# fretty

Fretty is a guitar fretboard generator.

how to run fretty:

    ./fretty.py example/C-major-scale-box1.ft -o C-major-scale-box1.svg

This will produce the file C-major-scale-box1.svg

## Basic Format

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

![C-major-scale-box1.svg](example/C-major-scale-box1.svg)

* numbers are displayed as notes

```
II
-5--
---3
--71
3--5
71--
-5--
```

![C-major-arpeggio.svg](example/C-major-arpeggio.svg)

* '|' is for a barre note
* 'X' is a muted string

```
III
|---
|o--
|-o-
|-o-
|---
X---
```

![Cm-chord.svg](example/Cm-chord.svg)

* '+' is a open string

```
I
--o-
---o
--o-
+---
X---
X---
```

![D-chord.svg](example/D-chord.svg)

## Extended Format

You can enclose any text with branches.
* '(' for circle notes
* '[' for square notes

```
III
  -    -    (vi)    -   (vii)  [I]
  -    -    (iii)  (IV)   -    (V)
  -  (vii)  [I]     -    (ii)   -
(IV)   -    (V)     -    (vi)   -
[I]    -    (ii)    -    (iii)  -
(V)    -    (vi)    -    (vii)  -
```

![C-major.svg](example/C-major.svg)


## Additional Information

This project was inspired by 
[svguitar](https://github.com/omnibrain/svguitar).