import genanki
from dataclasses import dataclass
from typing import List
from pathlib import Path
from .decks import YamlDeck, DECK_YAML


@dataclass
class Package:
    decks: List[YamlDeck]

    @staticmethod
    def from_dir(base_dir: Path):
        deck_files = base_dir.glob('**/' + DECK_YAML)
        decks: List[YamlDeck] = []

        deck_file: Path
        for deck_file in deck_files:
            deck_dir = deck_file.parent
            name = deck_dir \
                .relative_to(base_dir.parent) \
                .as_posix() \
                .replace('/', '::')
            decks.append(YamlDeck.from_dir(name=name, dir=deck_dir))

        return Package(decks=decks)

    def to_genanki_package(self):
        return genanki.Package([deck.to_genanki_deck() for deck in self.decks])
