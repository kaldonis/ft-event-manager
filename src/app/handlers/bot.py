import json
from webapp2 import redirect, uri_for
from app.forms.bot import ImportBotsForm, AddBotForm
from app.handlers.base import BaseHandler
from app.models.bot import Bot
from app.models.event import Event


class BotTableHandler(BaseHandler):
    """
    renders the list of bots for the event
    """
    def get(self, event_id):
        event = Event.get_by_id(event_id)
        if not event:
            return redirect(uri_for('home'))

        bots = Bot.get_by_event(event.id, 'weightclass asc, name asc')
        import_form = ImportBotsForm()
        add_form = AddBotForm()

        context = {
            'event': event,
            'bots': json.dumps([bot.to_dict() for bot in bots]),
            'import_form': import_form,
            'add_form': add_form
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


class AddBotHandler(BaseHandler):
    """
    handler for adding a bot
    """
    def post(self, event_id):
        add_form = AddBotForm(self.request.POST)

        if add_form.validate():
            bot_data = add_form.data
            bot_data['event_id'] = int(event_id)
            bot_data['bid'] = 0
            bot_data['registered_ind'] = 'Y'
            bot = Bot(**bot_data)
            bot.put()
            response = {
                'successful': True,
                'message': json.dumps(bot.to_dict())
            }
        else:
            response = {
                'successful': False,
                'message': json.dumps(add_form.errors)
            }

        context = {
            'data': json.dumps(response)
        }

        self.render_response('json.json', **context)


class UpdateBotHandler(BaseHandler):
    """
    handler for updating a bot
    """
    def post(self, event_id, bot_id):
        update_form = AddBotForm(self.request.POST)

        if update_form.validate():
            bot_data = update_form.data
            del bot_data['id']  # don't want to update this, EVER
            bot_data['multibot_ind'] = 'Y' if bot_data['multibot_ind'] else 'N'
            bot = Bot.get_by_id(bot_id)
            bot.__dict__.update(bot_data)
            bot.put()
            response = {
                'successful': True,
                'message': json.dumps(bot.to_dict())
            }
        else:
            response = {
                'successful': False,
                'message': json.dumps(update_form.errors)
            }

        context = {
            'data': json.dumps(response)
        }

        self.render_response('json.json', **context)
