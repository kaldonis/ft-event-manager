from webapp2 import uri_for
from app.domain.format import FORMATS
from app.forms.bracket import GenerateBracketForm
from app.handlers.base import BaseHandler
from app.models.bot import Bot
from app.models.bracket import Bracket
from app.models.event import Event
from app.models.match import Match
from app.models.weightclass import Weightclass


class BracketListHandler(BaseHandler):
    """
    list of brackets for an event
    """
    def get(self, event_id):
        event = Event.get_by_id(event_id)
        if not event:
            self.redirect(uri_for('home'))

        generate_form = GenerateBracketForm()
        brackets = {}
        weightclasses = Weightclass.get_by_event(event_id)
        for weightclass in weightclasses:
            bracket = Bracket.get_by_event_and_class(event_id, weightclass.code)
            if bracket:
                matches = Match.get_by_bracket(bracket.id)
                completed_matches = [match for match in matches if match.winning_bot_id]
            else:
                matches = None
                completed_matches = None

            bots = Bot.get_by_weightclass(weightclass.code, event.id)

            brackets[weightclass.code] = {
                'generated': True if bracket else False,
                'total_matches': len(matches) if matches else 0,
                'completed_matches': len(completed_matches) if completed_matches else 0,
                'total_bots': len(bots) if bots else 0,
                'bracket': bracket,
            }

        context = {
            'event_brackets': brackets,
            'event': event,
            'generate_form': generate_form
        }
        self.render_response('brackets.html', **context)

class GenerateBracketHandler(BaseHandler):
    """
    generate/regenerate the bracket for a given weightclass
    """
    def post(self, event_id):
        event = Event.get_by_id(event_id)
        if not event:
            self.redirect(uri_for('home'))

        weightclass = Weightclass.get_by_code(self.request.POST['weightclass'])
        if not weightclass:
            raise ValueError("bad weightclass")

        format = FORMATS.get(self.request.POST['format'])
        if not format:
            raise ValueError("bad format")

        bracket = Bracket.get_by_event_and_class(event_id, weightclass.code)
        if bracket:
            bracket.regenerate(format['code'])
        else:
            bracket = Bracket(event_id=event.id,
                              match_length=weightclass.default_match_length,
                              format_code=format['code'],
                              weightclass_code=weightclass.code)
            bracket.put()
            if not bracket.generate():
                bracket.delete()

        self.redirect(uri_for('single-bracket', event_id=event_id, bracket_id=bracket.id))