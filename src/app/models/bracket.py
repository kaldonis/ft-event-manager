from random import shuffle
import math
from app.domain.constants import CONSTANTS
from app.models import EventSearchMixin
from app.models.bot import Bot
from app.models.database import DBObject, DataInterface
from app.models.match import Match


class Bracket(DBObject, EventSearchMixin):
    event_id = None
    match_length = None
    format_code = None
    weightclass_code = None
    name = None

    @classmethod
    def get_by_event_and_class(cls, event_id, weightclass_code):
        db = DataInterface(CONSTANTS.DB_NAME)
        sql = "SELECT * FROM %s WHERE event_id = %d AND weightclass_code = '%s'" % (cls.__name__, int(event_id), weightclass_code)
        result = db.fetch_multiple(sql)

        return [cls(**(item)) for item in result if item]

    def regenerate(self, format):
        """
        regenerate the bracket
        """

        # delete any matches that have taken place
        matches = Match.get_by_bracket(self.id)
        for match in matches:
            match.delete()

        self.format_code = format
        self.put()
        self.generate()

    def delete(self):
        """
        delete a bracket
        """
        # delete any matches that have taken place
        matches = Match.get_by_bracket(self.id)
        for match in matches:
            match.delete()

        super(Bracket, self).delete()

    def generate(self):
        """
        generate the bracket
        """
        # find all registered bots in the given class

        bots = Bot.get_by_weightclass(self.weightclass_code, self.event_id)

        # defines the order for matches to spread out the byes better, probably a formula for this but didn't take time to figure it out
        match_ordering = {
            2: [1, 2],
            4: [1, 3, 2, 4],
            8: [1, 8, 5, 4, 3, 6, 7, 2],
            16: [1, 16, 9, 8, 5, 12, 13, 4, 3, 14, 11, 6, 7, 10, 15, 2]
        }

        # need at least 2 bots to generate a chart
        if(len(bots) < 2):
            return False

        # generate a random array for the seeding
        seeds = range(0, len(bots))
        shuffle(seeds)

        # assign the seeds
        for i, bot in enumerate(bots):
            bot.seed_number = seeds[i]
            bot.bracket_id = self.id
            bot.put()

        # generate matches
        if self.format_code.upper() != 'ROUNDROBIN':
            chart_size = 2

            # find the first power of 2 higher than the number of bots in the bracket, this is our chart size
            num_rounds = 1
            while(len(bots) > chart_size):
                chart_size *= 2
                num_rounds += 1

            # create first round matches, do our best to avoid a team fighting itself first round
            # will regenerate up to 5 times until it gives up on avoiding first round team fighting self
            for _ in xrange(0,5):
                matches = []
                for i in xrange(0, chart_size/2):
                    bot1_seed = i
                    bot2_seed = chart_size - 1 - i

                    bot1 = Bot.get_by_bracket_seed(self.event_id, self.id, bot1_seed)
                    bot2 = Bot.get_by_bracket_seed(self.event_id, self.id, bot2_seed)
                    bot1_id = bot1.id
                    bot2_id = bot2.id if bot2 else 0

                    match = Match(number=match_ordering[chart_size/2][i],
                                  bracket_id=self.id,
                                  bracket_side="A",
                                  round="A",
                                  bot1_id=bot1_id,
                                  bot2_id=bot2_id)
                    matches.append(match)

                conflict = False
                for match in matches:
                    if match.bot1_id > 0 and match.bot2_id > 0:
                        bot1 = Bot.get_by_id(match.bot1_id)
                        bot2 = Bot.get_by_id(match.bot2_id)
                        if bot1.team_name == bot2.team_name:
                            conflict = True
                            break

                if not conflict:
                    break

            [match.put() for match in matches]

            # create the rest of the A side matches, one round at a time
            for i in xrange(2, num_rounds+1):
                round_letter = chr(63+(2*i))  #A,C,E etc
                for j in xrange(1, chart_size/pow(2, i)+1):
                    bot1_source = 'W%s%d' % (chr(63+(2*i)-2), (j*2-1))  # ie WA1 (Winner of A1)
                    bot2_source = 'W%s%d' % (chr(63+(2*i)-2), (j*2))
                    match = Match(number=j,
                                  bracket_id=self.id,
                                  bracket_side="A",
                                  round=round_letter,
                                  bot1_source_match=bot1_source,
                                  bot2_source_match=bot2_source)
                    match.put()

            # generate B side matches, if necessary
            if self.format_code.upper() == 'DOUBLEELIM' or self.format_code.upper() == 'DOUBLETRUE':
                num_b_rounds = num_rounds * 2 - 1
                for i in xrange(2, num_b_rounds + 1):
                    round_letter = chr(62+(2*i))
                    round_size = int(chart_size/pow(2, math.floor((i+2)/2)))
                    for j in xrange(1, round_size+1):
                        if i==2:  # only case where a loser moves into bot1 spot
                            bot1_source = 'LA%d' % (j*2-1)
                            bot2_source = 'LA%d' % (j*2)
                        else:
                            if i%2 == 1:  # means this round's bot2 is sourced from A side
                                # losing source bots need to be from opposite side of chart as to prevent rematches
                                bot1_source = 'W%s%d' % (chr(60+(2*i)), j)
                                bot2_source = 'L%s' % (chr(64+i))
                                # match order depends how far into B side we are
                                # 3 possibilities: normal, reverse, half shift
                                if i%7 == 0:  # normal
                                    bot2_source = '%s%d' % (bot2_source, j)
                                elif i%5 == 0:  # half shift
                                    if j < round_size/2:
                                        bot2_source = '%s%d' % (bot2_source, math.ceil((round_size/2) + j))
                                    else:
                                        bot2_source = '%s%d' % (bot2_source, math.ceil((0-(round_size/2))+j))
                                else:  # reverse
                                    bot2_source = '%s%d' % (bot2_source, round_size + 1 - j)
                            else:
                                bot1_source = 'W%s%d' % (chr(60+(2*i)), (j*2-1))
                                bot2_source = 'W%s%d' % (chr(60+(2*1)), (j*2))

                        match = Match(number=j,
                                      bracket_id=self.id,
                                      bracket_side="B",
                                      round=round_letter,
                                      bot1_source_match=bot1_source,
                                      bot2_source_match=bot2_source)
                        match.put()


                # insert final A-side match
                round_letter = chr(63+(2*(num_rounds+1)))
                bot1_source = 'W%s1' % chr(63+(2*num_rounds))
                bot2_source = 'W%s1' % chr(60+(2*(num_b_rounds+1)))
                match = Match(number=1,
                              bracket_id=self.id,
                              bracket_side="A",
                              round=round_letter,
                              bot1_source_match=bot1_source,
                              bot2_source_match=bot2_source)
                match.put()

            matches_to_update = Match.get_by_bracket_round(self.id, 'A')
            for match in matches_to_update:
                match.check()

        else:  #ROUNDROBIN
            bot_index = 1  # start at 1 because bot0 can't fight bot0 etc
            for bot in bots:
                match_index = 1
                for i in xrange(bot_index, len(bots)):
                    match = Match(number=match_index,
                                  round=chr(64+bot_index),
                                  bracket_id=self.id,
                                  bracket_side="A",
                                  bot1_id=bot.id,
                                  bot2_id=bots[i].id)
                    match.put()
                    match_index += 1
                bot_index += 1

        return True

    def check_matches(self):
        """
        loop through all matches checking for byes that can be updated
        """
        matches = Match.get_by_bracket(self.id)
        for match in matches:
            match.check()