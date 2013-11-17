from operator import attrgetter
import math
from webapp2 import uri_for
from app.domain.format import FORMATS, ROUND_ROBIN, DOUBLE_ELIMINATION, SINGLE_ELIMINATION
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


class SingleBracketHandler(BaseHandler):
    """
    handler for displaying a single bracket
    """
    def get(self, event_id, bracket_id):
        event = Event.get_by_id(event_id)
        bracket = Bracket.get_by_id(bracket_id)
        weightclass = Weightclass.get_by_code(bracket.weightclass_code)
        format = FORMATS.get(bracket.format_code)
        matches = Match.get_by_bracket(bracket_id)

        ordered_matches = {'A': []}
        rounds = {'A': []}
        a_final_round = None
        b_final_round = None
        b_winner = None

        if bracket.format_code != ROUND_ROBIN:
            if bracket.format_code == DOUBLE_ELIMINATION:
                ordered_matches['B'] = []
                rounds['B'] = []

            for match in matches:
                match.populate_bot_entities()
                ordered_matches[match.bracket_side].append(match)

            # sort A side matches ascending by round, match number
            ordered_matches['A'] = sorted(ordered_matches['A'], key=attrgetter('round', 'number'))

            number_first_round_matches = sum(1 for m in ordered_matches['A'] if m.round == 'A')
            if bracket.format_code == SINGLE_ELIMINATION:
                a_final_round = chr(65+int((2*math.log(number_first_round_matches, 2))))
            else:
                a_final_round = chr(67+int((2*math.log(number_first_round_matches, 2))))

            if ordered_matches.get('B'):
                # sort B side matches desc by round, match number
                ordered_matches['B'] = sorted(ordered_matches['B'], key=attrgetter('round', 'number'), reverse=True)

                b_final_round = chr(66+int((4*(math.log(number_first_round_matches,2)))))

                for match in ordered_matches.get('B'):
                    if match.round not in rounds['B']:
                        rounds['B'].append(match.round)

                # determine b side winner, if applicable
                for match in ordered_matches['B']:
                    if match.round == b_final_round and match.number == 1:
                        b_winner = Bot.get_by_id(match.winning_bot_id)

        for match in ordered_matches.get('A'):
            if match.round not in rounds['A']:
                rounds['A'].append(match.round)

        else:
            # don't care for round robin about sort
            ordered_matches['A'] = matches
            number_first_round_matches = sum(1 for m in ordered_matches['A'] if m.round == 'A')

        if bracket.format_code != SINGLE_ELIMINATION:
            if number_first_round_matches < 4:
                margin_top = "-50px"
            elif number_first_round_matches < 8:
                margin_top = "-100px"
            elif number_first_round_matches < 16:
                margin_top = "-250px"
            elif number_first_round_matches < 32:
                margin_top = "-500px"
        else:
            margin_top = "-50px"

        context = {
            'format': format,
            'bracket': bracket,
            'weightclass': weightclass,
            'matches': ordered_matches,
            'rounds': rounds,
            'a_final_round': a_final_round,
            'b_final_round': b_final_round,
            'b_winner': b_winner,
            'number_first_round_matches': number_first_round_matches,
            'margin_top': margin_top,
            'event': event
        }

        self.render_response('single-bracket.html', **context)