import webapp2
from webapp2_extras import jinja2

from app.models.bracket import Bracket

def jinja2_factory(app):
    j = jinja2.Jinja2(app)
    j.environment.globals.update({
        # Set global variables.
        'uri_for': webapp2.uri_for,
        # ...
    })
    return j

class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(factory=jinja2_factory, app=self.app)

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.

        # append global context stuff (for navbar etc)
        event = context.get('event')
        if event:
            brackets = Bracket.get_by_event(event.id, order='weightclass_code asc')
            context.update({'brackets': brackets})

        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)