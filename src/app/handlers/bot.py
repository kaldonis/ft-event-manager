import json
from webapp2 import redirect, uri_for
from src.app.forms.bot import ImportBotsForm
from src.app.handlers.base import BaseHandler
from src.app.models.bot import Bot
from src.app.models.event import Event


class BotTableHandler(BaseHandler):
    """
    renders the list of bots for the event
    """
    def get(self, event_id):
        event = Event.get_by_id(event_id)
        if not event:
            return redirect(uri_for('home'))

        bots = Bot.get_by_event(event.id, 'weightclass asc, name desc')
        import_form = ImportBotsForm()

        context = {
            'event': event,
            'bots': json.dumps([{
                'id': bot.id,
                'botName': bot.name,
                'teamName': bot.team_name,
                'teamEmail': bot.team_email,
                'teamCity': bot.team_city,
                'teamState': bot.team_state,
                'category': bot.category,
                'weightclass': bot.weightclass,
                'photoUrl': bot.photo_url,
                'multibot': True if bot.multibot_ind == 'Y' else False,
                'isRegistered': True if bot.registered_ind == 'Y' else False
            } for bot in bots]),
            'import_form': import_form
        }

        self.render_response('bots.html', **context)


class DeleteBotHandler(BaseHandler):
    """
    handler for deleting a bot
    """
    def post(self, event_id, bot_id):
        bot = Bot.get_by_id(bot_id)

        if bot:
            result = bot.delete()
            response = {
                'successful': True if result == None else False,
                'message': result
            }
        else:
            response = {
                'successful': False,
                'message': 'Invalid bot id %d' % bot_id
            }

        context = {
            'data': json.dumps(response)
        }

        self.render_response('json.json', **context)


class RegisterBotHandler(BaseHandler):
    """
    handler for registering a bot
    """
    def post(self, event_id, bot_id):
        bot = Bot.get_by_id(bot_id)

        if bot:
            result = bot.register()
            response = {
                'successful': True if result == None else False,
                'message': result
            }
        else:
            response = {
                'successful': False,
                'message': 'Invalid bot id %d' % bot_id
            }

        context = {
            'data': json.dumps(response)
        }

        self.render_response('json.json', **context)


class UnregisterBotHandler(BaseHandler):
    """
    handler for unregistering a bot
    """
    def post(self, event_id, bot_id):
        bot = Bot.get_by_id(bot_id)

        if bot:
            result = bot.unregister()
            response = {
                'successful': True if result == None else False,
                'message': result
            }
        else:
            response = {
                'successful': False,
                'message': 'Invalid bot id %d' % bot_id
            }

        context = {
            'data': json.dumps(response)
        }

        self.render_response('json.json', **context)