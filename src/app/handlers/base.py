import logging
import os
import webapp2
from webapp2_extras import jinja2

from app.models.bracket import Bracket
from app.models.event import Event


def jinja2_factory(app):
    logging.info("template path: %s", os.path.join(os.path.dirname(__file__), '../../templates'))
    j = jinja2.Jinja2(app, {'template_path': os.path.join(os.path.dirname(__file__), '../../templates')})
    j.environment.globals.update({
        # Set global variables.
        'uri_for': webapp2.uri_for
        # ...
    })
    return j

class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(factory=jinja2_factory, app=self.app)

    def redirect(self, uri, permanent=False, abort=True, code=None, body=None):
        super(BaseHandler, self).redirect(uri, permanent=permanent, abort=abort, code=code, body=body)

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.

        # append global context stuff (for navbar etc)
        event = context.get('event')
        if event:
            brackets = Bracket.get_by_event(event.id, order='weightclass_code, name')
            context.update({'brackets': brackets})

        events = Event.get_all(order='start_date desc')
        context['events'] = [{'id': event.id, 'name': event.name} for event in events]

        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)