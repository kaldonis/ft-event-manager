EditTable = function() {
    var self = this;

    self.rows = ko.observableArray();

    self.RowViewModel = function(data) {
        var self = this;

        self.FieldViewModel = function(name, value) {
            var self = this;
            self.name = ko.observable(name);
            self.value = ko.observable(value);
        };

        self.compare = function(left, right) {
            if(left.name() < right.name()) {
                return -1
            }
            else {
                return 1;
            }
        };

        self.toPostDict = function () {
            var d = {
                id: self.id
            };
            $.each(self.fields(), function(index, item) {
                d[item.name()] = item.value();
            });

            return d;
        };

        self.id = '';
        self.fields = ko.observableArray();

        var fieldsTemp = [];
        $.each(data, function(name, value) {
            if(name == 'id') {
                self.id = value;
            }
            else {
                fieldsTemp.push(new self.FieldViewModel(name, value));
            }
        });
        fieldsTemp.sort(self.compare);
        self.fields(fieldsTemp);
    };

    self.saveRow = function(row) {
        $.ajax({
            url: 'edit/',
            type: 'POST',
            data: row.toPostDict(),
            dataType: 'json',
            success: function(data) {
                if(data.successful) {
                    EMNotifySuccess('Update Successful');
                    row.id = data.id;
                }
                else {
                    EMNotifyError('Update Failed. ' + data.message);
                }
            },
            error: function() {
                EMNotifyError('Update Failed. Unknown error.');
            }
        });
    };

    self.addRow = function() {
        self.rows.push(new self.RowViewModel(self.rowTemplate));
    }

    self.deleteRow = function(row) {
        var r = confirm("Are you sure you want to delete this entry?");
        if(r) {
            $.ajax({
                url: 'delete/',
                type: 'POST',
                data: row.toPostDict(),
                dataType: 'json',
                success: function(data) {
                    if(data.successful) {
                        EMNotifySuccess('Delete Successful');
                        self.rows.remove(row);
                    }
                    else {
                        EMNotifyError('Delete Failed. ' + data.message);
                    }
                },
                error: function() {
                    EMNotifyError('Delete Failed. Unknown error.');
                }
            });
        }
    };

    self.init = function(rows, rowTemplate) {
        var mappedData = ko.utils.arrayMap(rows, function(item) {
           return new self.RowViewModel(item);
        });
        self.rows(mappedData);
        self.rowTemplate = rowTemplate;
    };
};