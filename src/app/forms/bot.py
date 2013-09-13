from wtforms import Form, FileField, SubmitField, validators


class ImportBotsForm(Form):
    file = FileField('Import Bots', validators=[validators.required()])
    submit = SubmitField('Import')