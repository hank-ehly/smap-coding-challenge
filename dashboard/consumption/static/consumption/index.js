$(document).ready(function () {
    $('#users').DataTable({
        searching: false
    });

    showLoadingSpinner(true);

    $.ajax('/api/consumption_summary', {method: 'GET', dataType: 'json'})
        .done(onSummaryDataLoaded)
        .fail(onSummaryDataError);
});

function showLoadingSpinner(show) {
    if (show) {
        var $chart = $('#chart');
        var $spinner = $('.lds-ring');
        var yOffset = $chart.position().top + ($chart.outerHeight() / 2) - ($spinner.outerHeight() / 2);
        $spinner.css({top: yOffset + 'px'});
        $spinner.show();
    } else {
        $('.lds-ring').hide();
    }
}

function onSummaryDataLoaded(body) {
    var results = body.results;
    var ctx = $('#chart');
    var primaryRed = 'rgba(255, 88, 121, 1)';
    var secondaryBlue = 'rgba(47, 152, 232, 1)';

    showLoadingSpinner(false);

    var labels = results.map(function (row) {
        return row['time'].substr(0, 10);
    });

    var data = results.map(function (row) {
        return row['consumption']
    });

    var lineChart = new Chart(ctx, {
        type: 'line',
        options: {
            maintainAspectRatio: false
        },
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'All users',
                    data: data,
                    backgroundColor: primaryRed,
                    borderColor: primaryRed,
                    fill: false
                }
            ]
        }
    });
}

function onSummaryDataError() {
    showLoadingSpinner(false);
    $('.summary-chart-error-alert').show();
}
