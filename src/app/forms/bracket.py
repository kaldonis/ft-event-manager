from wtforms import Form, SubmitField, validators, SelectField, HiddenField

from app.domain.format import FORMATS


class GenerateBracketForm(Form):
    format = SelectField('Format',
                              validators=[validators.required()],
                              choices=[(key, value.get('name')) for key, value in FORMATS.iteritems()])
    weightclass = HiddenField()
    submit = SubmitField('Generate')