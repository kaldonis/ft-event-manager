from webapp2 import Route
from app.handlers.static import StaticFileHandler


ROUTES = [
    Route('/', handler='app.handlers.event.CreateEventHandler', name='home'),
    Route('/bootstrap/', handler='bootstrap.Bootstrap', name='bootstrap'),
    Route('/<:\d+>/bots/', handler='app.handlers.bot.BotTableHandler', name='bot-table'),
    Route('/<:\d+>/bracket/<:\d+>/', handler='app.handlers.bracket.BracketHandler', name='bracket'),
    Route('/<:\d+>/schedule/', handler='app.handlers.schedule.ScheduleHandler', name='schedule'),
    Route('/<:\d+>/', handler='app.handlers.event.SelectEventHandler', name='event'),
    Route('/<:\d+>/bots/delete/<:\d+>/', handler='app.handlers.bot.DeleteBotHandler', name='delete-bot'),
    Route('/<:\d+>/bots/update/<:\d+>/', handler='app.handlers.bot.UpdateBotHandler', name='update-bot'),
    Route('/<:\d+>/bots/register/<:\d+>/', handler='app.handlers.bot.RegisterBotHandler', name='register-bot'),
    Route('/<:\d+>/bots/unregister/<:\d+>/', handler='app.handlers.bot.UnregisterBotHandler', name='unregister-bot'),
    Route('/<:\d+>/bots/add/', handler='app.handlers.bot.AddBotHandler', name='add-bot'),
    (r'/static/(.+)', StaticFileHandler)
]