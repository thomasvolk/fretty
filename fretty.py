#!/usr/bin/env python3

from dataclasses import dataclass


class FBString:
    def __init__(self, line):
        self.notes = dict()
        self.frets = 0
        for position, c in enumerate(line.strip()):
            self.frets += 1
            if c != '-':
                self.notes[position]= c
    
    def is_note(self, position):
        return self.notes.has_key(position)
    
    def __repr__(self):
        return f"FBString({self.notes.keys()})"


class Fretboard:
    def __init__(self, lines):
        self.position = lines[0]
        self.strings = [ FBString(line) for line in lines[1:] ]

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


class SvgGenerator:
    main_template = """<svg version="1.1"
     xmlns="http://www.w3.org/2000/svg"  
     xmlns:xlink="http://www.w3.org/1999/xlink"
     xmlns:svgjs="http://svgjs.com/svgjs" 
     preserveAspectRatio="xMidYMid meet"
     viewBox="0 0 {width} {height}">
{string_lines}
</svg>"""
    string_line_template = '<line x1="{start_x}" y1="{y}"  x2="{end_x}" y2="{y}"  stroke-width="2" stroke="#000000"></line>'
    def __init__(self, view_config):
        self.view_config = view_config

    def generate(self, fretboard):
        cfg = self.view_config
        width = fretboard.fret_count * cfg.fret_distance + (2 * cfg.margin)
        height = fretboard.string_count * cfg.string_distance + (2 * cfg.margin)
        string_lines = '\n'.join([ self.string_line_template.format(
                            y=i*cfg.string_distance + cfg.margin,
                            start_x=cfg.margin,
                            end_x=width - cfg.margin
                         ) 
                         for i in range(0, fretboard.string_count + 1) ])
        return self.main_template.format(width=width, height=height, string_lines=string_lines)


def generate_svg(lines):
    fb = Fretboard(lines)
    cfg = ViewConfig()
    svg = SvgGenerator(cfg)
    return svg.generate(fb)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
                prog='fretty',
                description='Fretty is a guitar fretboard generator')
    parser.add_argument('input_file')
    parser.add_argument('-o', '--output-file')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    with open(args.input_file) as f:
        svg = generate_svg(f.readlines())
        if args.output_file:
            if args.verbose:
                print(f"write file: {args.output_file}")
            with open(args.output_file, 'w') as o:
                o.write(svg)
        else:
            print(svg)