#!/usr/bin/env python3


class FBString:
    def __init__(self, line):
        self.notes = dict()
        for position, c in enumerate(line.strip()):
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

    def __repr__(self):
        return f"Fretboard({self.strings})"


class SvgGenerator:
    template = """<svg version="1.1"
     xmlns="http://www.w3.org/2000/svg"  
     xmlns:xlink="http://www.w3.org/1999/xlink"
     xmlns:svgjs="http://svgjs.com/svgjs" 
     preserveAspectRatio="xMidYMid meet"
     viewBox="0 0 {width} {height}">
</svg>"""
    def __init__(self, width = 600, height = 400):
        self.width = width
        self.height = height

    def generate(self, fretboard):
        return self.template.format(width=self.width, height=self.height)


def generate_svg(lines):
    fb = Fretboard(lines)
    svg = SvgGenerator()
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