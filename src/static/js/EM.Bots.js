Bots = function() {
    var self = this;

    self.bots = ko.observableArray();

    self.add_name = ko.observable('');
    self.add_team_name = ko.observable('');
    self.add_team_email = ko.observable('');
    self.add_team_city = ko.observable('');
    self.add_team_state = ko.observable('');
    self.add_category = ko.observable('');
    self.add_weightclass = ko.observable('');
    self.add_multibot_ind = ko.observable('');
    self.add_notes = ko.observable('');
    self.add_photo_url = ko.observable('');

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

        self.addBotParams = {
            add_name: new ko.observable(''),
            add_team_name: new ko.observable(''),
            add_team_email: new ko.observable(''),
            add_team_city: new ko.observable(''),
            add_team_state: new ko.observable(''),
            add_category: new ko.observable(''),
            add_weightclass: new ko.observable(''),
            add_multibot_ind: new ko.observable(''),
            add_notes: new ko.observable(''),
            add_photo_url: new ko.observable('')
        };

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

    self.find = function(bot_id) {
        return ko.utils.arrayFirst(self.bots(), function(item) {
            return item.id() === bot_id;
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

    self.cancelAddEditBot = function() {
        $('#add-bot-modal').modal('hide');
    }

    self.compare = function(left, right) {
        if(left.weightclass() < right.weightclass()) {
            return -1
        }
        else if(right.weightclass() < left.weightclass()) {
            return 1;
        }
        else {
            if(left.botName() < right.botName()) {
                return -1;
            }
            else if(right.botName() < left.botName()) {
                return 1;
            }
        }
        return 0;
    };

    self.editBot = function(bot) {
        $('#add-bot-modal').modal('show');
        $('input[name="id"]').val(bot.id());
        $('input[name="name"]').val(bot.botName());
        $('input[name="team_name"]').val(bot.teamName());
        $('input[name="team_email"]').val(bot.teamEmail());
        $('input[name="team_city"]').val(bot.teamCity());
        $('input[name="team_state"]').val(bot.teamState());
        $('select[name="category"]').val(bot.category());
        $('select[name="weightclass"]').val(bot.weightclass());
        $('input[name="multibot_ind"]').prop("checked", bot.multibotInd());
    };

    self.addEditBot = function() {
        var botData = $('#add-bot-form').serializeArray()
        var url = '';
        var action = '';
        if($('#add-bot-form')[0].id.value != '') {
            url = 'update/' + $('#add-bot-form')[0].id.value + '/';
            action = 'edit';
        }
        else {
            url = 'add/';
            action = 'add';
        }

        $.ajax({
            url: url,
            type: 'POST',
            data: botData,
            dataType: 'json',
            success: function(data) {
                if(data.successful) {
                    botJson = jQuery.parseJSON(data.message);

                    if(action == 'edit') {
                        bot = self.find(botJson.id);
                        self.bots.remove(bot);
                    }

                    bot = new self.BotViewModel(botJson.id, botJson.botName, botJson.teamName, botJson.teamEmail, botJson.teamCity, botJson.teamState, botJson.category, botJson.weightclass, botJson.photoUrl, botJson.multibot, botJson.isRegistered);
                    self.bots.push(bot);
                    self.bots.sort(self.compare);

                    EMNotifySuccess(bot.botName() + ' successfully updated.');
                    self.cancelAddEditBot();
                }
                else {
                    errorsJson = jQuery.parseJSON(data.message);
                    $.each(errorsJson, function(field, errors) {
                        $.each(errors, function(index, error) {
                            EMNotifyCustomError(field, error);
                        });
                    });
                }
            },
            error: function() {
                EMNotifyError('Bot not updated. Unknown error.');
            }
        });
    }

    self.initBots = function(bots) {
        var mappedData = ko.utils.arrayMap(bots, function(item) {
           return new self.BotViewModel(item.id, item.botName, item.teamName, item.teamEmail, item.teamCity, item.teamState, item.category, item.weightclass, item.photoUrl, item.multibot, item.isRegistered);
        });

        self.bots(mappedData);
    };
};