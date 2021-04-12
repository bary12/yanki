import genanki
from typing import Optional


class ModelWithLatexPreamble(genanki.Model):
    def __init__(
            self,
            latex_pre: Optional[str] = None,
            latex_post: Optional[str] = None,
            latex_svg : bool = False,
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
        

main_model = ModelWithLatexPreamble(
    model_id=559856851,
    fields=[
        {
            'name': 'Front',
        },
        {
            'name': 'Back'
        }
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Front}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
        },
    ],
    css='''
.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}''',
    latex_pre=r'''
\documentclass[border=1px]{standalone}

\usepackage[utf8]{inputenc}

\usepackage{siunitx}
\sisetup{
  per-mode=fraction,
  inter-unit-product = \ensuremath{{}\cdot{}}
}
\DeclareSIUnit\atm{atm}
\DeclareSIUnit\psi{psi}

\usepackage{chemmacros}
\usepackage{chemfig}
\chemsetup{modules = newman}

\pagestyle{empty}
\setlength{\parindent}{0in}
\begin{document}
    ''',
    name='yanki_default_model',
    latex_svg=True
)
