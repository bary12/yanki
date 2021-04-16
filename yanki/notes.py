import genanki
import yaml

from yanki.exceptions import ValidationError
from yanki.models import YamlModel
from pathlib import Path
from typing import List, Iterable
from dataclasses import dataclass


@dataclass
class YamlNote:
    guid: str
    fields: dict
    model: str

    @staticmethod
    def from_file(path: Path) -> List['YamlNote']:
        with path.open() as notes_file:
            documents = list(yaml.safe_load_all(notes_file))

        if len(documents) < 2:
            raise ValidationError(f'notes file {path} should have a header specifying `model: ...`, seperated from the rest of the document by ---')
        header, notes_document = documents
        if not isinstance(header, dict) or not isinstance(header.get('model', None), str):
            raise ValidationError(f'notes file {path} header should contain `model: "model string"`')
        if not isinstance(notes_document, dict):
            raise ValidationError(f'notes file {path} is not a dict')

        model = header['model']

        return [
            YamlNote(guid=guid, fields=fields, model=model)
            for guid, fields in notes_document.items()
        ]

    def to_genanki_note(self, models: List[genanki.Model]) -> genanki.Note:
        return genanki.Note(
            model=next(model for model in models if model.name == self.model),
            fields=[
                self.fields['front'],
                self.fields['back'],
            ],
            guid=self.guid)
