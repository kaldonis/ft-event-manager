from webapp2 import Route
from app.handlers.static import StaticFileHandler


ROUTES = [
    Route('/bootstrap/', handler='bootstrap.Bootstrap', name='bootstrap'),

    # Event Handlers
    Route('/', handler='app.handlers.event.CreateEventHandler', name='home'),
    Route('/<event_id:\d+>/', handler='app.handlers.event.SelectEventHandler', name='event'),

    # Bot Handlers
    Route('/<event_id:\d+>/bots/', handler='app.handlers.bot.BotListHandler', name='bot-table'),
    Route('/<event_id:\d+>/bots/add/', handler='app.handlers.bot.AddBotHandler', name='add-bot'),
    Route('/<event_id:\d+>/bots/delete/<bot_id:\d+>/', handler='app.handlers.bot.DeleteBotHandler', name='delete-bot'),
    Route('/<event_id:\d+>/bots/update/<bot_id:\d+>/', handler='app.handlers.bot.UpdateBotHandler', name='update-bot'),
    Route('/<event_id:\d+>/bots/register/<bot_id:\d+>/', handler='app.handlers.bot.RegisterBotHandler', name='register-bot'),
    Route('/<event_id:\d+>/bots/registerall/', handler='app.handlers.bot.RegisterAllBotsHandler', name='register-all-bots'),
    Route('/<event_id:\d+>/bots/unregister/<bot_id:\d+>/', handler='app.handlers.bot.UnregisterBotHandler', name='unregister-bot'),
    Route('/<event_id:\d+>/bots/unregisterall/', handler='app.handlers.bot.UnregisterAllBotsHandler', name='unregister-all-bots'),

    # Bracket Handlers
    Route('/<event_id:\d+>/brackets/', handler='app.handlers.bracket.BracketListHandler', name='bracket'),
    Route('/<event_id:\d+>/brackets/<bracket_id:\d+>/', handler='app.handlers.bracket.SingleBracketHandler', name='single-bracket'),
    Route('/<event_id:\d+>/brackets/generate/', handler='app.handlers.bracket.GenerateBracketHandler', name='generate-bracket'),

    # Session Handlers
    Route('/<event_id:\d+>/sessions/', handler='app.handlers.session.SessionListHandler', name='session'),

    # Schedule Handlers
    Route('/<event_id:\d+>/schedule/', handler='app.handlers.schedule.ScheduleListHandler', name='schedule'),
    (r'/static/(.+)', StaticFileHandler)
]