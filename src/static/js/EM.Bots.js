Bots = function() {
    var self = this;

    self.bots = ko.observableArray();

    self.BotViewModel = function(id, botName, teamName, teamEmail, teamCity, teamState, category, weightclass, photoUrl, multibot, isRegistered) {
        var self = this;
        self.id = ko.observable(id);
        self.botName = ko.observable(botName);
        self.teamName = ko.observable(teamName);
        self.teamEmail = ko.observable(teamEmail);
        self.teamCity = ko.observable(teamCity);
        self.teamState = ko.observable(teamState);
        self.category = ko.observable(category);
        self.weightclass = ko.observable(weightclass);
        self.photoUrl = ko.observable(photoUrl);
        self.multibotInd = ko.observable(multibot);
        self.isRegistered = ko.observable(isRegistered);

        self.isRegistered.subscribe(function () {
            var url;
            var action;
            if(self.isRegistered()) {
                url = 'register/' + self.id() + '/';
                action = 'registered';
            }
            else {
                url = 'unregister/' + self.id() + '/';
                action = 'unregistered';
            }
            $.ajax({
                url: url,
                type: 'POST',
                dataType: 'json',
                success: function(data) {
                    if(data.successful) {
                        EMNotifySuccess(self.botName() + ' successfully ' + action + '.');
                    }
                    else {
                        EMNotifyError(self.botName() + ' NOT  ' + action + '. ' + data.message);
                    }
                },
                error: function() {
                    EMNotifyError(self.botName() + ' NOT  ' + action + '. Unknown error.');
                }
            });
        });
    };

    self.deleteBot = function(bot) {
        $.ajax({
            url: 'delete/' + bot.id() + '/',
            type: 'POST',
            dataType: 'json',
            success: function(data) {
                if(data.successful) {
                    EMNotifySuccess(bot.botName() + ' successfully deleted.');
                    self.bots.remove(bot);
                }
                else {
                    EMNotifyError(bot.botName() + ' NOT deleted. ' + data.message);
                }
            },
            error: function() {
                EMNotifyError(bot.botName() + ' NOT deleted. Unknown error.');
            }
        });
    };

    self.initBots = function(bots) {
        var mappedData = ko.utils.arrayMap(bots, function(item) {
           return new self.BotViewModel(item.id, item.botName, item.teamName, item.teamEmail, item.teamCity, item.teamState, item.category, item.weightclass, item.photoUrl, item.multibot, item.isRegistered);
        });

        self.bots(mappedData);
    };
};