import argparse
from pathlib import Path
from yanki.package import Package

parser = argparse.ArgumentParser('Generate Anki decks from YAML files')

parser.add_argument(
    'directory',
    help='Main deck directory containing subdecks and/or note files.',
    type=Path)

parser.add_argument(
    '-o',
    '--output-file',
    help='Path to output .apkg file',
    type=str,
    default=None
)

args = parser.parse_args()

directory: Path = args.directory.absolute()
output_file: str = args.output_file

output_file_path: Path = Path(
    args.output_file
    if args.output_file is not None
    else directory.name + '.apkg').absolute()

Package.from_dir(directory).to_genanki_package().write_to_file(output_file_path)

print(f'wrote to output file {output_file_path}')
