$(document).ready(function(){
    $("[id='reject']").click(function(){
        const reject = $(this)
        $.ajax({
            type: 'POST',
            async: true,
            url: '/reject/' + reject.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    })

    $("[id='approve']").click(function(){
        const approve = $(this)
        $.ajax({
            type: 'POST',
            async: true,
            url: '/approve/' + approve.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    })

    $("[id='done']").click(function(){
        const done = $(this)
        $.ajax({
            type: 'POST',
            async: true,
            url: '/done/' + done.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    })
});