# -*- coding: utf-8 -*-
from dataclasses import dataclass
from enum import Enum
import os


class Shape(Enum):
    CIRCLE = 1
    SQUARE = 2

    @staticmethod
    def get_shape(c):
        if c in ('[', '#'):
            return Shape.SQUARE
        return Shape.CIRCLE


@dataclass
class Note:
    fret: int
    string: int 
    value: str
    shape: Shape
    is_barre: bool = False


class FBString:
    NOTE_START = ('(', '[', '{', '<')
    NOTE_END = (')', ']', '}', '>', '|')

    def __init__(self, position, line):
        self.position = position
        self.notes = []
        self.frets = 0
        self.is_muted = False
        self.is_open = False
        current_note = None
        for c in line.replace(' ', '').strip():
            if c in self.NOTE_START and not current_note:
                current_note = Note(self.frets, self.position, '', Shape.get_shape(c))
                continue
            elif c in self.NOTE_END and current_note:
                current_note.is_barre = c == '|'
                self.notes.append(current_note)
                current_note = None
                self.frets += 1
                continue
            if current_note:
                current_note.value += c
                continue

            if c == 'X':
                self.is_muted = True
            elif c == '+':
                self.is_open = True
            elif c != '-':
                if c in ('o', '#', '|'):
                    value = ''
                else:
                    value = c
                self.notes.append(Note(self.frets, self.position, value, Shape.get_shape(c), c == '|'))
            self.frets += 1

    def __repr__(self):
        return f"FBString({self.position}, {self.notes})"


class Fretboard:
    def __init__(self, input_lines):
        lines = [l for l in input_lines if len(l.strip()) > 0]
        self.start_position = lines[0].strip()
        self.strings = [FBString(pos, line) for pos, line in enumerate(lines[1:]) if len(line) > 0]

    @property
    def string_count(self):
        return len(self.strings)

    @property
    def fret_count(self):
        return max([s.frets for s in self.strings])

    def get_note(self, f, s):
        for note in self.strings[s].notes:
            if note.fret == f:
                return note
        return None

    def __repr__(self):
        return f"Fretboard({self.strings})"


@dataclass
class ViewConfig:
    string_distance: int = 40
    fret_distance: int = 60
    margin: int = 20
    note_radius: int = 15
    start_position_space: int = 40


class SvgGenerator:
    stand_alone_attributes = """version="1.1"
     xmlns="http://www.w3.org/2000/svg"  
     xmlns:xlink="http://www.w3.org/1999/xlink"
     xmlns:svgjs="http://svgjs.com/svgjs" 
     preserveAspectRatio="xMidYMid meet" """
    main_template = """<svg {attributes} {size_attributes}
     viewBox="0 0 {width} {height}">
{start_position}
{frets}
{strings}
{barres}
{notes}
{muted}
{open_strings}
</svg>"""
    line_template = '<line x1="{start_x}" y1="{start_y}" x2="{end_x}" y2="{end_y}" stroke-width="2" stroke="#000000"/>'
    circle_template = '<circle r="{radius}" cx="{x}" cy="{y}" fill="none" stroke-width="2" stroke="#000000"/>'
    note_template = '<circle r="{radius}" cx="{x}" cy="{y}" fill="#000000" stroke-width="0" stroke="#000000"/>'
    rect_template = ('<rect x="{x}" y="{y}" width="{width}" height="{height}" ' +
                     'fill="#000000" stroke-width="0" stroke="#000000"/>')
    text_template = ('<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" text-anchor="{anchor}" '
                     + 'dominant-baseline="{baseline}" fill="{color}" font-weight="{weight}">{text}</text>')

    def __init__(self, view_config):
        self.view_config = view_config

    def generate(self, fretboard, width=None, height=None, embedded=False):
        attributes = ""
        if not embedded:
            attributes = self.stand_alone_attributes
        size_attributes = ""
        if width:
            size_attributes += f' width="{width}" '
        if height:
            size_attributes += f' height="{height}"'

        cfg = self.view_config
        width = fretboard.fret_count * cfg.fret_distance + (2 * cfg.margin)
        height = fretboard.string_count * cfg.string_distance + (2 * cfg.margin)
        y_offset = cfg.margin + cfg.start_position_space
        strings = '\n'.join([ 
            self.line_template.format(
                start_y=i*cfg.string_distance + y_offset,
                end_y=i*cfg.string_distance + y_offset,
                start_x=cfg.margin,
                end_x=width - cfg.margin
            ) 
            for i in range(0, fretboard.string_count) 
        ])
        frets = '\n'.join([ 
            self.line_template.format(
                start_y=y_offset,
                end_y=height - cfg.margin,
                start_x=i*cfg.fret_distance + cfg.margin,
                end_x=i*cfg.fret_distance + cfg.margin
            ) 
            for i in range(0, fretboard.fret_count + 1) 
        ])

        def make_note_entry(n):
            x = n.fret * cfg.fret_distance + cfg.margin + (cfg.fret_distance/2)
            y = n.string * cfg.string_distance + y_offset
            if n.shape == Shape.SQUARE:
                result = self.rect_template.format(
                    width=cfg.note_radius*2,
                    height=cfg.note_radius*2,
                    x=x - cfg.note_radius,
                    y=y - cfg.note_radius
                )
            else:
                result = self.note_template.format(
                    radius=cfg.note_radius,
                    x=x,
                    y=y
                )
            if n.value:
                result += '\n' + self.text_template.format(
                    x=x,
                    y=y,
                    anchor='middle',
                    baseline='middle',
                    color='#FFFFFF',
                    size=cfg.note_radius,
                    text=n.value,
                    weight='bold'
                )
            return result

        notes = '\n'.join([
            make_note_entry(n)
            for s in fretboard.strings for n in s.notes
        ])
        start_position = self.text_template.format(
            x=cfg.margin,
            y=cfg.margin + (cfg.start_position_space/2),
            anchor='start',
            baseline='auto',
            color='#000000',
            size=cfg.start_position_space,
            text=fretboard.start_position,
            weight='normal'
        )
        muted = '\n'.join([
            self.line_template.format(
                start_y=s.position * cfg.string_distance + y_offset - (cfg.note_radius * 0.7),
                end_y=s.position * cfg.string_distance + y_offset + (cfg.note_radius * 0.7),
                start_x=cfg.margin - (cfg.note_radius * 0.7),
                end_x=cfg.margin + (cfg.note_radius * 0.7)
            ) + '\n' +
            self.line_template.format(
                start_y=s.position * cfg.string_distance + y_offset + (cfg.note_radius * 0.7),
                end_y=s.position * cfg.string_distance + y_offset - (cfg.note_radius * 0.7),
                start_x=cfg.margin - (cfg.note_radius * 0.7),
                end_x=cfg.margin + (cfg.note_radius * 0.7)
            ) 
            for s in fretboard.strings if s.is_muted
        ])
        open_strings = '\n'.join([
            self.circle_template.format(
                    radius=cfg.note_radius * 0.7,
                    y=s.position * cfg.string_distance + y_offset,
                    x=cfg.margin
                )
            for s in fretboard.strings if s.is_open
        ])
        barre_list = []
        for f in range(0, fretboard.fret_count):
            barre = []
            for s in range(0, fretboard.string_count):
                n = fretboard.get_note(f, s)
                if n and n.is_barre:
                    barre.append(n)
            if len(barre) > 1:
                barre_list.append((barre[0], barre[-1]))
        barres = '\n'.join([
            self.rect_template.format(
                    width=cfg.note_radius*2,
                    height=(end.string - start.string)*cfg.string_distance,
                    x=start.fret * cfg.fret_distance + cfg.margin + (cfg.fret_distance/2) - cfg.note_radius,
                    y=start.string * cfg.string_distance + y_offset
            )
            for start, end in barre_list
        ])
            
        return self.main_template.format(
                    attributes=attributes,
                    size_attributes=size_attributes,
                    width=width, 
                    height=height, 
                    start_position=start_position,
                    frets=frets,
                    strings=strings,
                    notes=notes,
                    muted=muted,
                    barres=barres,
                    open_strings=open_strings
                )


def generate_svg(lines, width=None, height=None, embedded=False):
    fb = Fretboard(lines)
    cfg = ViewConfig()
    svg = SvgGenerator(cfg)
    return svg.generate(fb, width=width, height=height, embedded=embedded)


def write_image(name, svg, target_path=''):
    if name.lower().endswith('.png'):
        import cairosvg
        cairosvg.svg2png(bytestring=bytes(svg, 'utf-8'), write_to=os.path.join(target_path, name))
        return name
    else:
        with open(os.path.join(target_path, name), 'w') as f:
            f.write(svg)
        return name


