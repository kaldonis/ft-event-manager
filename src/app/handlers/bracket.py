import json
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

        weightclasses = Weightclass.get_by_event(event_id)
        generate_form = GenerateBracketForm()
        weightclass_choices = []
        brackets = {}
        for weightclass in weightclasses:
            bots = Bot.get_by_weightclass_registered(weightclass.code, event.id)
            if len(bots) > 1:
                weightclass_choices.append((weightclass.code, '%s (%d bots)' % (weightclass.name, len(bots))))
            brackets[weightclass.name] = []
            weightclass_brackets = Bracket.get_by_event_and_class(event_id, weightclass.code)
            for bracket in weightclass_brackets:
                matches = Match.get_by_bracket(bracket.id)
                completed_matches = [match for match in matches if match.winning_bot_id]
                bots = Bot.get_by_bracket(bracket.id)

                brackets[weightclass.name].append({
                    'total_matches': len(matches) if matches else 0,
                    'completed_matches': len(completed_matches) if completed_matches else 0,
                    'total_bots': len(bots) if bots else 0,
                    'bracket': bracket,
                    'format': FORMATS.get(bracket.format_code)
                })
        generate_form.weightclass.choices = weightclass_choices

        context = {
            'event_brackets': brackets,
            'event': event,
            'generate_form': generate_form,
            'weightclasses': weightclasses
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

        manual_seed = self.request.POST.get('manual_seeding')
        bracket_id = self.request.POST.get('bracket_id')
        if not bracket_id:
            weightclass = Weightclass.get_by_code(self.request.POST['weightclass'])
            if not weightclass:
                raise ValueError("bad weightclass")

            format = FORMATS.get(self.request.POST['format'])
            if not format:
                raise ValueError("bad format")

            if format.get('code') == 'roundrobin':
                manual_seed = False

            name = self.request.POST['name']
            bracket = Bracket(event_id=event.id,
                              match_length=weightclass.default_match_length,
                              format_code=format['code'],
                              weightclass_code=weightclass.code,
                              name=name,
                              manual_seed=manual_seed or False,
                              generated=False)
            bracket.put()
        else:
            bracket = Bracket.get_by_id(bracket_id)

        seeding = self.request.POST.getall('seeding[]')
        if manual_seed and not seeding:
            self.redirect(uri_for('manual-seed', event_id=event_id, bracket_id=bracket.id))
        else:
            result = bracket.generate(seeding)
            if result:
                bracket.generated=True
                bracket.put()
            else:
                bracket.delete()

            self.redirect(uri_for('single-bracket', event_id=event_id, bracket_id=bracket.id), abort=False)


class ManualSeedingHandler(BaseHandler):
    """
    render the page for manually seeding a bracket
    """
    def get(self, event_id, bracket_id):
        event = Event.get_by_id(event_id)
        if not event:
            self.redirect(uri_for('home'))

        bracket = Bracket.get_by_id(bracket_id)
        if not bracket:
            self.redirect(uri_for('brackets', event_id=event_id))

        bots = Bot.get_by_weightclass_registered(bracket.weightclass_code, event.id)

        context = {
            'event': event,
            'bracket': bracket,
            'bots': json.dumps([{'id': bot.id, 'name': bot.name} for bot in bots])
        }
        self.render_response('seed.html', **context)


class RegenerateBracketHandler(BaseHandler):
    """
    handler to regenerate a bracket
    """
    def get(self, event_id, bracket_id):
        event = Event.get_by_id(event_id)
        if not event:
            self.redirect(uri_for('home'))

        bracket = Bracket.get_by_id(bracket_id)
        if not bracket:
            self.redirect(uri_for('brackets', event_id=event_id))

        bracket.regenerate(bracket.format_code)
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
        bots = Bot.get_by_bracket(bracket_id)
        bots.sort(key=lambda x: x.id)

        if bracket.manual_seed and not bracket.generated:
            self.redirect(uri_for('manual-seed', event_id=event_id, bracket_id=bracket.id))

        for match in matches:
            match.populate_bot_entities()

        ordered_matches = {'A': []}
        rounds = {'A': []}
        a_final_round = None
        b_final_round = None
        a_winner = None
        b_winner = None
        final_round = None
        margin_top = None

        if bracket.format_code != ROUND_ROBIN:
            if bracket.format_code == DOUBLE_ELIMINATION:
                ordered_matches['B'] = []
                rounds['B'] = []

            for match in matches:
                ordered_matches[match.bracket_side].append(match)

            # sort A side matches ascending by round, match number
            ordered_matches['A'] = sorted(ordered_matches['A'], key=attrgetter('round', 'number'))

            number_first_round_matches = sum(1 for m in ordered_matches['A'] if m.round == 'A')
            if bracket.format_code == SINGLE_ELIMINATION:
                a_final_round = chr(65+int((2*math.log(number_first_round_matches, 2))))
                final_round = chr(67+int((2*math.log(number_first_round_matches, 2))))
            else:
                a_final_round = chr(67+int((2*math.log(number_first_round_matches, 2))))
                final_round = chr(69+int((2*math.log(number_first_round_matches, 2))))

            a_winner = ordered_matches['A'][-1].winning_bot_id
            a_winner = Bot.get_by_id(a_winner) if a_winner else None

            if ordered_matches.get('B'):
                # sort B side matches desc by round, match number
                ordered_matches['B'] = sorted(ordered_matches['B'], key=attrgetter('round', 'number'), reverse=True)

                b_final_round = chr(66+int((4*(math.log(number_first_round_matches,2)))))

                for match in ordered_matches.get('B'):
                    if match.round not in rounds['B']:
                        rounds['B'].append(match.round)

                # determine b side winner, if applicable
                b_winner = ordered_matches['B'][0].winning_bot_id
                b_winner = Bot.get_by_id(b_winner) if b_winner else None

            for match in ordered_matches.get('A'):
                if match.round not in rounds['A']:
                    rounds['A'].append(match.round)

        else:
            # don't care for round robin about sort
            ordered_matches['A'] = matches
            number_first_round_matches = sum(1 for m in ordered_matches['A'] if m.round == 'A')

        if bracket.format_code != SINGLE_ELIMINATION:
            if number_first_round_matches <= 4:
                margin_top = "0px"
            elif number_first_round_matches <= 8:
                margin_top = "-50px"
            elif number_first_round_matches <= 16:
                margin_top = "-150px"
            elif number_first_round_matches <= 32:
                margin_top = "-400px"
        else:
            margin_top = "0px"

        context = {
            'format': format,
            'bracket': bracket,
            'weightclass': weightclass,
            'matches': ordered_matches,
            'rounds': rounds,
            'a_final_round': a_final_round,
            'b_final_round': b_final_round,
            'final_round': final_round,
            'a_winner': a_winner,
            'b_winner': b_winner,
            'number_first_round_matches': number_first_round_matches,
            'margin_top': margin_top,
            'event': event,
            'bots': bots
        }

        self.render_response('single-bracket.html', **context)

class MatchReportHandler(BaseHandler):
    """
    handler for match reporting
    """
    def get(self, event_id, bracket_id):
        """
        get
        """
        match_id = self.request.get('match_id')
        winning_bot_id = self.request.get('winning_bot_id')

        match = Match.get_by_id(match_id)
        match.winner(winning_bot_id)

        self.redirect_to('single-bracket', event_id=event_id, bracket_id=bracket_id)


class DeleteBracketHandler(BaseHandler):
    """
    handler for deleting brackets
    """
    def get(self, event_id, bracket_id):
        """
        get
        """
        bracket = Bracket.get_by_id(bracket_id)
        bracket.delete()

        self.redirect_to('brackets', event_id=event_id)