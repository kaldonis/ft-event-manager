from webapp2 import Route
import webapp2_static


ROUTES = [
    Route('/', handler='app.handlers.event.CreateEventHandler', name='home'),
    Route('/event/<:\d+>/', handler='app.handlers.event.SelectEventHandler', name='event'),
    (r'/static/(.+)', webapp2_static.StaticFileHandler)
]