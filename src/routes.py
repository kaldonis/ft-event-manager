from webapp2 import Route
from app.handlers.static import StaticFileHandler


ROUTES = [
    Route('/bootstrap/', handler='bootstrap.Bootstrap', name='bootstrap'),

    # Event Handlers
    Route('/', handler='app.handlers.event.CreateEventHandler', name='home'),
    Route('/<:\d+>/', handler='app.handlers.event.SelectEventHandler', name='event'),

    # Bot Handlers
    Route('/<:\d+>/bots/', handler='app.handlers.bot.BotListHandler', name='bot-table'),
    Route('/<:\d+>/bots/add/', handler='app.handlers.bot.AddBotHandler', name='add-bot'),
    Route('/<:\d+>/bots/delete/<:\d+>/', handler='app.handlers.bot.DeleteBotHandler', name='delete-bot'),
    Route('/<:\d+>/bots/update/<:\d+>/', handler='app.handlers.bot.UpdateBotHandler', name='update-bot'),
    Route('/<:\d+>/bots/register/<:\d+>/', handler='app.handlers.bot.RegisterBotHandler', name='register-bot'),
    Route('/<:\d+>/bots/registerall/', handler='app.handlers.bot.RegisterAllBotsHandler', name='register-all-bots'),
    Route('/<:\d+>/bots/unregister/<:\d+>/', handler='app.handlers.bot.UnregisterBotHandler', name='unregister-bot'),
    Route('/<:\d+>/bots/unregisterall/', handler='app.handlers.bot.UnregisterAllBotsHandler', name='unregister-all-bots'),

    # Bracket Handlers
    Route('/<:\d+>/brackets/', handler='app.handlers.bracket.BracketListHandler', name='bracket'),
    Route('/<:\d+>/brackets/<:\d+>/', handler='app.handlers.bracket.SingleBracketHandler', name='single-bracket'),
    Route('/<:\d+>/brackets/<:[A-z]+>/generate/', handler='app.handlers.bracket.GenerateBracketHandler', name='generate-bracket'),

    # Session Handlers
    Route('/<:\d+>/sessions/', handler='app.handlers.session.SessionListHandler', name='session'),

    # Schedule Handlers
    Route('/<:\d+>/schedule/', handler='app.handlers.schedule.ScheduleListHandler', name='schedule'),
    (r'/static/(.+)', StaticFileHandler)
]