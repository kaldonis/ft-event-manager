import webapp2
from webapp2_extras import jinja2

from src.app.models.bracket import Bracket


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.

        # append global context stuff (for navbar etc)
        event = context.get('event')
        if event:
            brackets = Bracket.get_by_event(event.id, order='weightclass_code asc')
            context.update({'brackets': brackets})

        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)