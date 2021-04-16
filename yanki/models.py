import genanki
from dataclasses import dataclass
from typing import Optional, List
from pathlib import Path
import yaml
from yanki.exceptions import ValidationError

class ModelWithLatexPreamble(genanki.Model):
    def __init__(
            self,
            latex_pre: Optional[str] = None,
            latex_post: Optional[str] = None,
            latex_svg: bool = False,
            *args,
            **kwargs):
        super().__init__(*args, **kwargs)
        self.latex_pre = latex_pre
        self.latex_post = latex_post
        self.latex_svg = latex_svg

    def to_json(self, *args, **kwargs):
        json = super().to_json(*args, **kwargs)
        if self.latex_pre is not None:
            json['latexPre'] = self.latex_pre
        if self.latex_post is not None:
            json['latexPost'] = self.latex_post

        json['latexsvg'] = self.latex_svg

        return json


@dataclass
class YamlModel:
    name: str
    dct: dict

    @staticmethod
    def from_file(path: Path) -> List['YamlModel']:
        with path.open() as file:
            data = yaml.safe_load(file)

        if not isinstance(data, dict):
            raise ValidationError('models file is not a dict')

        data: dict

        return [
            YamlModel(name=name, dct=model)
            for name, model in data.items()
        ]

    def to_genanki_model(self) -> genanki.Model:
        return ModelWithLatexPreamble(name=self.name, **self.dct)
