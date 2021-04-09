import genanki
import yaml

from yanki.exceptions import ValidationError
from yanki.models import main_model
from pathlib import Path
from typing import List, Iterable
from dataclasses import dataclass


@dataclass
class YamlNote:
    guid: str
    fields: dict

    @staticmethod
    def from_file(path: Path) -> List['YamlNote']:
        with path.open() as notes_file:
            dct = yaml.safe_load(notes_file)

        if not isinstance(dct, dict):
            raise ValidationError(f'notes file {path} is not a dict')

        return [
            YamlNote(guid=guid, fields=fields)
            for guid, fields in dct.items()
        ]

    def to_genanki_note(self) -> genanki.Note:
        return genanki.Note(
            model=main_model,
            fields=[
                self.fields['front'],
                self.fields['back'],
            ],
            guid=self.guid)
