# fretty

Fretty is a guitar fretboard generator.


## Installation

    pip install fretty

## Usage

how to run fretty:

    fretty example/C-major-scale-box1.ft -o C-major-scale-box1.svg

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

<img src="example/C-major-scale-box1.svg" width="200">

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

<img src="example/C-major-arpeggio.svg" width="200">

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

<img src="example/Cm-chord.svg" width="200">

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

<img src="example/D-chord.svg" width="200">

## Extended Format

You can enclose any text with branches.
* '(' - ')' for circle notes
* '[' - ']' for square notes

```
III
  -    -    (vi)    -   (vii)  [I]
  -    -    (iii)  (IV)   -    (V)
  -  (vii)  [I]     -    (ii)   -
(IV)   -    (V)     -    (vi)   -
[I]    -    (ii)    -    (iii)  -
(V)    -    (vi)    -    (vii)  -
```

<img src="example/C-major.svg" width="200">

If you close the note by using the barre synbol, instead of the closing branch,
the note will be part of a barre symbol.

```
V
(5|   -   -   -
|    (3)  -   -
(7|   -   -   -
|     -  (5)  -
(1|   -   -   -
X     -   -   -
```

<img src="example/Dm7-chord.svg" width="200">


## Additional Information

This project was inspired by 
[svguitar](https://github.com/omnibrain/svguitar).