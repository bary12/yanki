import genanki

main_model = genanki.Model(
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
}'''
)
