EMNotifySuccess = function(text) {
    $.gritter.add({
        title: 'Success',
        text: text,
        image: '/static/images/success.png',
        time: 2000
    });
};

EMNotifyError = function(text) {
    $.gritter.add({
        title: 'Error',
        text: text,
        image: '/static/images/error.png',
        time: 2000
    });
};