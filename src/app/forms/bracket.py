from wtforms import Form, SubmitField, validators, SelectField, TextField

from app.domain.format import FORMATS


class GenerateBracketForm(Form):
    format = SelectField('Format',
                         validators=[validators.required()],
                         choices=[(key, value.get('name')) for key, value in FORMATS.iteritems()])
    weightclass = SelectField('Class',
                              validators=[validators.required()],
                              choices=[])
    name = TextField('Bracket Name (optional)')
    submit = SubmitField('Generate')