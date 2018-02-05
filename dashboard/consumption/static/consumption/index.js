$(document).ready(function () {
    $('#users').DataTable({searching: false});

    if ($('#summary-chart').length) {
        showLoadingSpinnerOnChart(true, $('#summary-chart'));
        $.ajax('/api/v1/consumptions', {dataType: 'json'}).done(onSummaryDataLoaded).fail(onSummaryDataError).always(onRequestComplete);
    } else if ($('#detail-chart')) {
        showLoadingSpinnerOnChart(true, $('#detail-chart'));
        $.ajax('/api/v1/consumptions', {
            data: {user_id: 3000},
            dataType: 'json'
        }).done(onDetailDataLoaded).fail(onDetailDataError).always(onRequestComplete);

    }
});

function onRequestComplete() {
    showLoadingSpinnerOnChart(false);
}

function showLoadingSpinnerOnChart(show, $chart) {
    if (show) {
        var $spinner = $('.lds-ring');
        var yOffset = $chart.position().top + ($chart.outerHeight() / 2) - ($spinner.outerHeight() / 2);
        $spinner.css({top: yOffset + 'px'});
        $spinner.show();
    } else {
        $('.lds-ring').hide();
    }
}

function onSummaryDataLoaded(response) {
    var red = 'rgba(255, 88, 121, 1)';
    var data = readConsumptionData(response.data);

    var lineChart = new Chart($('#summary-chart'), {
        type: 'line',
        options: {
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        callback: numberWithCommas
                    }
                }]
            }
        },
        data: {
            labels: data['labels'],
            datasets: [
                {
                    label: 'Consumption of all users',
                    data: data['consumption'],
                    backgroundColor: red,
                    borderColor: red,
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

function onDetailDataLoaded(response) {
    var blue = 'rgba(47, 152, 232, 1)';

    var data = readConsumptionData(response.data);

    var lineChart = new Chart($('#detail-chart'), {
        type: 'line',
        options: {
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        callback: numberWithCommas
                    }
                }]
            }
        },
        data: {
            labels: data['labels'],
            datasets: [
                {
                    label: 'User Data',
                    data: data['consumption'],
                    backgroundColor: blue,
                    borderColor: blue,
                    fill: false
                }
            ]
        }
    });
}

function onDetailDataError() {

}

function readConsumptionData(data) {
    var dates = data.map(function (row) {
        return row['time'].substr(0, 10);
    });

    var consumption = data.map(function (row) {
        return row['consumption']
    });

    return {
        labels: dates,
        consumption: consumption
    }
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
