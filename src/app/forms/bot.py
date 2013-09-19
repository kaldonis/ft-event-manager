from wtforms import Form, FileField, SubmitField, validators, BooleanField, TextField, SelectField, TextAreaField, HiddenField
from app.models.category import BotCategory
from app.models.weightclass import Weightclass


class ImportBotsForm(Form):
    file = FileField('Import Bots', validators=[validators.required()])
    submit = SubmitField('Import')


class AddBotForm(Form):
    id = HiddenField()
    name = TextField('Bot Name', validators=[validators.required()])
    team_name = TextField('Team Name', validators=[validators.required()])
    team_email = TextField('Email')
    team_city = TextField('City')
    team_state = TextField('State/Prov')
    category = SelectField('Category',
                           validators=[validators.required()],
                           choices=[(c.code, c.code) for c in BotCategory.get_all('name asc')])
    weightclass = SelectField('Class',
                              validators=[validators.required()],
                              choices=[(w.code, w.code) for w in Weightclass.get_all('name asc')])
    multibot_ind = BooleanField('Multibot?')
    notes = TextAreaField('Notes')
    photo_url = TextField('Photo URL')