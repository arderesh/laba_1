import argparse
import sys

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def format_result(value):
    if value == int(value):
        return str(int(value))
    return str(value)


def build_parser():
    parser = argparse.ArgumentParser(
        prog='toolkit',
        description='калькулятор выражений и конвертер величин',
    )
    subparsers = parser.add_subparsers(dest='command')

    calc_parser = subparsers.add_parser('calc',
                                        help='вычислить арифметическое выражение')
    calc_parser.add_argument('expression',
                             help='выражение в кавычках, например "2+3.1*2"')

    convert_parser = subparsers.add_parser('convert',
                                           help='конвертер величин')
    convert_parser.add_argument('value', type=float, help='число')
    convert_parser.add_argument('--from',
                                dest='from_unit',
                                required=True,
                                metavar='UNIT',
                                help='из какой единицы переводить')
    convert_parser.add_argument('--to',
                                dest='to_unit',
                                required=True,
                                metavar='UNIT',
                                help='то, в какую единицу перевести исходную')

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    try:
        if args.command == 'calc':
            result = calculate(args.expression)
        else:
            result = convert(args.value, args.from_unit, args.to_unit)
    except ToolkitError as error:
        print(error, file=sys.stderr)
        return 2

    print(format_result(result))
    return 0


if __name__ == '__main__':
    sys.exit(main())