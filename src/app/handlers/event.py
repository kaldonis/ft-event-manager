from webapp2 import redirect, uri_for
from app.forms.event import CreateEventForm
from app.handlers.base import BaseHandler
from app.models.bot import Bot
from app.models.event import Event


class CreateEventHandler(BaseHandler):
    """
    home page
    """
    def get_context(self):
        create_form = CreateEventForm()

        events = Event.get_all(order='start_date desc')

        context = {
            'create_form': create_form,
            'events': [{'id': 'create', 'name': 'Create new event'}] if not events else
                      [{'id': event.id, 'name': event.name} for event in events]
        }
        return context

    def get(self):
        context = self.get_context()
        self.render_response('home.html', **context)

    def post(self):
        create_form = CreateEventForm(self.request.POST)

        if not create_form.validate():
            context = self.get_context()
            context.update({'create_form': create_form})
            self.render_response('home.html', **context)
        else:
            event = Event(**(create_form.data))
            event.put()


class SelectEventHandler(BaseHandler):
    """
    view specific event
    """
    def get(self, event_id):
        if isinstance(event_id, basestring):
            event_id = int(event_id)

        event = Event.get_by_id(event_id)
        if not event:
            return redirect(uri_for('home'))

        bots = Bot.get_by_event(event_id)
        registered_bots = [bot for bot in bots if bot.registered_ind == 'Y']

        context = {
            'event': event,
            'bots_registered': len(registered_bots),
            'bots_total': len(bots)
        }

        self.render_response('event.html', **context)