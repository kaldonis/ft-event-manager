from wtforms import Form, SubmitField, validators, SelectField, StringField, BooleanField

from app.domain.format import FORMATS


class GenerateBracketForm(Form):
    format = SelectField(label='Format',
                         validators=[validators.required()],
                         choices=[(key, value.get('name')) for key, value in FORMATS.iteritems()])
    weightclass = SelectField(label='Class',
                              validators=[validators.required()],
                              choices=[])
    name = StringField(label='Bracket Name (optional)')
    manual_seeding = BooleanField(label='Seed Manually (no effect on Round Robin)')
    submit = SubmitField(label='Generate')