#!/usr/bin/env python3

from dataclasses import dataclass
import sys
from xml.dom.minidom import parseString

@dataclass
class Note:
    position: int 
    value: str

    
class FBString:
    def __init__(self, position, line):
        self.position = position
        self.notes = []
        self.frets = 0
        for position, c in enumerate(line.strip()):
            self.frets += 1
            if c != '-':
                self.notes.append(Note(position, c))
    
    def __repr__(self):
        return f"FBString({self.position}, {self.notes})"


class Fretboard:
    def __init__(self, lines):
        self.start_position = lines[0].strip()
        self.strings = [ FBString(pos, line) for pos, line in enumerate(lines[1:]) if len(line) > 0]

    @property
    def string_count(self):
        return len(self.strings)

    @property
    def fret_count(self):
        return max([ s.frets for s in self.strings ])

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
    main_template = """<svg {attributes} {size_attribues}
     viewBox="0 0 {width} {height}">
{start_position}
{frets}
{strings}
{notes}
</svg>"""
    line_template = '<line x1="{start_x}" y1="{start_y}"  x2="{end_x}" y2="{end_y}"  stroke-width="2" stroke="#000000"/>'
    circle_template = '<circle r="{radius}" cx="{x}" cy="{y}" fill="#000000" stroke-width="0" stroke="#000000"/>'
    rect_template = '<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="#000000" stroke-width="0" stroke="#000000"/>'
    text_template = '<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" text-anchor="{anchor}" dominant-baseline="{baseline}" fill="{color}">{text}</text>'

    def __init__(self, view_config):
        self.view_config = view_config

    def generate(self, fretboard, width=None, height=None, embedded=False):
        attributes = ""
        if not embedded:
            attributes = self.stand_alone_attributes
        size_attribues = ""
        if width:
            size_attribues += f' width="{width}" '
        if height:
            size_attribues += f' height="{height}"'

        cfg = self.view_config
        width = fretboard.fret_count * cfg.fret_distance + (2 * cfg.margin)
        height = fretboard.string_count * cfg.string_distance + (2 * cfg.margin)
        y_offest = cfg.margin + cfg.start_position_space
        strings = '\n'.join([ 
            self.line_template.format(
                start_y=i*cfg.string_distance + y_offest,
                end_y=i*cfg.string_distance + y_offest,
                start_x=cfg.margin,
                end_x=width - cfg.margin
            ) 
            for i in range(0, fretboard.string_count) 
        ])
        frets = '\n'.join([ 
            self.line_template.format(
                start_y=y_offest,
                end_y=height - cfg.margin,
                start_x=i*cfg.fret_distance + cfg.margin,
                end_x=i*cfg.fret_distance + cfg.margin
            ) 
            for i in range(0, fretboard.fret_count + 1) 
        ])
        def make_note_entry(position, n):
            x = n.position * cfg.fret_distance + cfg.margin + (cfg.fret_distance/2)
            y = position * cfg.string_distance + y_offest
            if n.value == '#':
                return self.rect_template.format(
                    width=cfg.note_radius*2,
                    height=cfg.note_radius*2,
                    x=x - cfg.note_radius,
                    y=y - cfg.note_radius
                )
            else:
                result = self.circle_template.format(
                    radius=cfg.note_radius,
                    x=x,
                    y=y
                )
                if n.value != 'o':
                    result += '\n' + self.text_template.format(
                        x=x,
                        y=y,
                        anchor='middle',
                        baseline='middle',
                        color='#FFFFFF',
                        size=cfg.note_radius,
                        text=n.value
                    )
                return result
        notes = '\n'.join([
            make_note_entry(s.position, n)
            for s in fretboard.strings for n in s.notes
        ])
        start_position = self.text_template.format(
            x=cfg.margin,
            y=cfg.margin + (cfg.start_position_space/2),
            anchor='start',
            baseline='auto',
            color='#000000',
            size=cfg.start_position_space,
            text=fretboard.start_position
        )

        return self.main_template.format(
                    attributes=attributes,
                    size_attribues=size_attribues,
                    width=width, 
                    height=height, 
                    start_position=start_position,
                    frets=frets,
                    strings=strings,
                    notes=notes
                )


def generate_svg(lines, width=None, height=None, embedded=False):
    fb = Fretboard(lines)
    cfg = ViewConfig()
    svg = SvgGenerator(cfg)
    return svg.generate(fb, width=width, height=height, embedded=embedded)

def process_html(html):
    dom = parseString(html)
    for node in dom.getElementsByTagName("fretty"):
        lines = node.firstChild.data.strip().split("\n")
        svg = generate_svg(lines, width=node.getAttribute('width'), height=node.getAttribute('height'), embedded=True)
        svgNode = parseString(svg).documentElement
        node.parentNode.replaceChild(svgNode, node) 
    return dom.toxml()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
                prog='fretty',
                description='Fretty is a guitar fretboard generator'
                )
    parser.add_argument('input_file')
    parser.add_argument('-o', '--output-file')
    parser.add_argument('-p', '--processor', default="ft")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--version', action='version', version='%(prog)s 1.2')
    args = parser.parse_args()

    with open(args.input_file) as f:
        if args.processor == 'ft':
            output = generate_svg(f.readlines())
        elif args.processor == 'html':
            output = process_html(f.read())
        else:
            print(f"ERROR: unknow processor: {args.processor}")
            sys.exit(1)
        if args.output_file:
            if args.verbose:
                print(f"write file: {args.output_file}")
            with open(args.output_file, 'w') as o:
                o.write(output)
        else:
            print(output)