from webapp2 import Route
from app.handlers.static import StaticFileHandler


ROUTES = [
    Route('/bootstrap/', handler='bootstrap.Bootstrap', name='bootstrap'),

    # Event Handlers
    Route('/', handler='app.handlers.event.CreateEventHandler', name='home'),
    Route('/<event_id:\d+>/', handler='app.handlers.event.ViewEventHandler', name='event'),

    # Bot Handlers
    Route('/<event_id:\d+>/bots/', handler='app.handlers.bot.BotListHandler', name='bots'),
    Route('/<event_id:\d+>/bots/add/', handler='app.handlers.bot.AddBotHandler', name='add-bot'),
    Route('/<event_id:\d+>/bots/delete/<bot_id:\d+>/', handler='app.handlers.bot.DeleteBotHandler', name='delete-bot'),
    Route('/<event_id:\d+>/bots/update/<bot_id:\d+>/', handler='app.handlers.bot.UpdateBotHandler', name='update-bot'),
    Route('/<event_id:\d+>/bots/register/<bot_id:\d+>/', handler='app.handlers.bot.RegisterBotHandler', name='register-bot'),
    Route('/<event_id:\d+>/bots/registerall/', handler='app.handlers.bot.RegisterAllBotsHandler', name='register-all-bots'),
    Route('/<event_id:\d+>/bots/unregister/<bot_id:\d+>/', handler='app.handlers.bot.UnregisterBotHandler', name='unregister-bot'),
    Route('/<event_id:\d+>/bots/unregisterall/', handler='app.handlers.bot.UnregisterAllBotsHandler', name='unregister-all-bots'),

    # Bracket Handlers
    Route('/<event_id:\d+>/brackets/', handler='app.handlers.bracket.BracketListHandler', name='brackets'),
    Route('/<event_id:\d+>/brackets/generate/', handler='app.handlers.bracket.GenerateBracketHandler', name='generate-bracket'),
    Route('/<event_id:\d+>/brackets/<bracket_id:\d+>/', handler='app.handlers.bracket.SingleBracketHandler', name='single-bracket'),
    Route('/<event_id:\d+>/brackets/<bracket_id:\d+>/seed/', handler='app.handlers.bracket.ManualSeedingHandler', name='manual-seed'),
    Route('/<event_id:\d+>/brackets/<bracket_id:\d+>/match/', handler='app.handlers.bracket.MatchReportHandler', name='match-report'),
    Route('/<event_id:\d+>/brackets/<bracket_id:\d+>/delete/', handler='app.handlers.bracket.DeleteBracketHandler', name='delete-bracket'),
    Route('/<event_id:\d+>/brackets/<bracket_id:\d+>/regenerate/', handler='app.handlers.bracket.RegenerateBracketHandler', name='regenerate-bracket'),

    # Session Handlers
    Route('/<event_id:\d+>/sessions/', handler='app.handlers.session.SessionListHandler', name='sessions'),

    # Schedule Handlers
    Route('/<event_id:\d+>/schedule/', handler='app.handlers.schedule.ScheduleListHandler', name='schedule'),

    # Admin Handlers
    Route('/admin/', handler='app.handlers.admin.AdminHandler', name='admin'),
    Route('/admin/table/<table:\w+>/', handler='app.handlers.admin.EditTableHandler', name='edit-code-table'),
    Route('/admin/table/<table:\w+>/<action:\w+>/', handler='app.handlers.admin.EditTableHandler', name='edit-or-delete-code-table'),

    (r'/static/(.+)', StaticFileHandler)
]