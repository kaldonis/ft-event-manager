from wtforms import Form, TextField, DateField, SelectField, SubmitField, validators, ValidationError


class CreateEventForm(Form):
    name = TextField('Event Name', validators=[validators.required()])
    location = TextField('Location', validators=[validators.required()])
    start_date = DateField('Start Date', validators=[validators.required()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[validators.required()], format='%Y-%m-%d')
    submit = SubmitField('Submit')

    def validate_end_date(form, field):
        if form.start_date.data and field.data < form.start_date.data:
            raise ValidationError("End date must be after start date.")