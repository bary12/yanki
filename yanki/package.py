import genanki
import itertools
from dataclasses import dataclass
from typing import List, Iterable
from pathlib import Path
from .decks import YamlDeck, DECK_YAML

MEDIA_GLOBS = [
    '**/*.jpg', '**/*.png', '**/*.gif', '**/*.tiff', '**/*.svg', '**/*.tif', '**/*.jpeg', '**/*.mp3',
    '**/*.ogg', '**/*.wav', '**/*.avi', '**/*.ogv', '**/*.mpg', '**/*.mpeg', '**/*.mov', '**/*.mp4',
    '**/*.mkv', '**/*.ogx', '**/*.ogv', '**/*.oga', '**/*.flv', '**/*.swf', '**/*.flac', '**/*.webp',
    '**/*.m4a'
]


@dataclass
class Package:
    decks: List[YamlDeck]
    media: List[Path]

    @staticmethod
    def from_dir(base_dir: Path):
        deck_files = base_dir.glob('**/' + DECK_YAML)
        decks: List[YamlDeck] = []

        print('collecting subdesk...')

        deck_file: Path
        for deck_file in deck_files:
            deck_dir = deck_file.parent
            name = deck_dir \
                .relative_to(base_dir.parent) \
                .as_posix() \
                .replace('/', '::')
            decks.append(YamlDeck.from_dir(name=name, dir=deck_dir))

        print(f'Found subdecks: {len(decks)}')
        print('Collecting media...')
        media = list(itertools.chain.from_iterable(
            base_dir.glob(media_pattern) for media_pattern in MEDIA_GLOBS))
        print(f'Found media files: {len(media)}')
        return Package(decks=decks, media=media)

    def to_genanki_package(self):
        return genanki.Package(
            [deck.to_genanki_deck() for deck in self.decks],
            media_files=self.media)
