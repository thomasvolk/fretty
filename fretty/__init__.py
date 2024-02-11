__version__ = '2.0'

from .fretty import generate_svg, write_image


def main():
    import argparse

    parser = argparse.ArgumentParser(
                prog='fretty',
                description='Fretty is a guitar fretboard generator'
                )
    parser.add_argument('input_file')
    parser.add_argument('-o', '--output-file', help="output file name, defualt is svg format - if the file name ends with .png a png image will be created")
    parser.add_argument('-V', '--verbose', action='store_true')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    args = parser.parse_args()

    with open(args.input_file) as f:
        svg_output = generate_svg(f.readlines())
        if args.output_file:
            if args.verbose:
                print(f"write file: {args.output_file}")
            write_image(args.output_file, svg_output)
        else:
            print(output)


if __name__ == '__main__':
    main()