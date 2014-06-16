from wtforms import Form, DateField, SubmitField, validators, ValidationError, StringField


class CreateEventForm(Form):
    name = StringField('Event Name', validators=[validators.required()])
    location = StringField('Location', validators=[validators.required()])
    start_date = DateField('Start Date (YYYY-MM-DD)', validators=[validators.required()], format='%Y-%m-%d')
    end_date = DateField('End Date (YYYY-MM-DD)', validators=[validators.required()], format='%Y-%m-%d')
    submit = SubmitField('Submit')

    def validate_end_date(form, field):
        if form.start_date.data and field.data < form.start_date.data:
            raise ValidationError("End date must be after start date.")