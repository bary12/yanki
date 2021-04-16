import itertools
import genanki
import yaml
from typing import List, Iterable
from dataclasses import dataclass
from pathlib import Path
from yanki.notes import YamlNote
from yanki.models import YamlModel

DECK_YAML = 'deck.yaml'


@dataclass
class YamlDeck:
    name: str
    notes: List[YamlNote]
    id: int

    @staticmethod
    def from_dir(name: str, dir: Path) -> 'YamlDeck':
        files: Iterable[Path] = itertools.chain(
            dir.glob('*.yaml'), dir.glob('*.yml'))

        deck_file: Path = dir / DECK_YAML
        with deck_file.open() as deck_file_:
            deck_data = yaml.safe_load(deck_file_)
        deck_id = deck_data['id']

        file: Path
        note_files: List[Path] = [
            file for file in files if file.name != DECK_YAML]

        notes = []
        for notes_file in note_files:
            notes.extend(YamlNote.from_file(notes_file))

        return YamlDeck(notes=notes, name=name, id=deck_id)

    def to_genanki_deck(self, models: List[genanki.Model]) -> genanki.Deck:
        deck = genanki.Deck(deck_id=self.id, name=self.name, description='')
        for note in self.notes:
            deck.add_note(note.to_genanki_note(models=models))

        print(f'creating deck "{self.name}"')
        return deck
