#!/usr/bin/env python3

from dataclasses import dataclass

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
        self.strings = [ FBString(pos, line) for pos, line in enumerate(lines[1:]) ]

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
    margin: int = 10
    note_radius: int = 15
    start_position_space: int = 40


class SvgGenerator:
    main_template = """<svg version="1.1"
     xmlns="http://www.w3.org/2000/svg"  
     xmlns:xlink="http://www.w3.org/1999/xlink"
     xmlns:svgjs="http://svgjs.com/svgjs" 
     preserveAspectRatio="xMidYMid meet"
     viewBox="0 0 {width} {height}">
{start_position}
{frets}
{strings}
{notes}
</svg>"""
    line_template = '<line x1="{start_x}" y1="{start_y}"  x2="{end_x}" y2="{end_y}"  stroke-width="2" stroke="#000000"></line>'
    note_template = '<circle r="{radius}" cx="{x}" cy="{y}" fill="#000000" stroke-width="0" stroke="#000000"></circle>'
    start_position_template = '<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" text-anchor="middle" dominant-baseline="central" fill="#000000">{position}</text>'

    def __init__(self, view_config):
        self.view_config = view_config

    def generate(self, fretboard):
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
        notes = '\n'.join([
            self.note_template.format(
                radius=cfg.note_radius,
                x=n.position * cfg.fret_distance + cfg.margin + (cfg.fret_distance/2),
                y=s.position * cfg.string_distance + y_offest
            )
            for s in fretboard.strings for n in s.notes
        ])
        start_position = self.start_position_template.format(
            x=cfg.margin + (cfg.start_position_space/2),
            y=cfg.margin + (cfg.start_position_space/2),
            size=cfg.start_position_space,
            position=fretboard.start_position
        )

        return self.main_template.format(
                    width=width, 
                    height=height, 
                    start_position=start_position,
                    frets=frets,
                    strings=strings,
                    notes=notes
                )


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