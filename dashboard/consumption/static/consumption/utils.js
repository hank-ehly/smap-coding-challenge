function showLoadingSpinnerOnChart(selector) {
    if (!$(selector).length) {
        return;
    }

    var $spinner = $('.lds-ring');
    var yOffset = $(selector).position().top + ($(selector).outerHeight() / 2) - ($spinner.outerHeight() / 2);

    $spinner.css({top: yOffset + 'px'});
    $spinner.show();
}

function hideLoadingSpinner() {
    $('.lds-ring').hide();
}

function numberWithCommas(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function defaultChartOptions() {
    return {
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    callback: function (label) {
                        if (Math.floor(label) === label) {
                            return numberWithCommas(label);
                        }
                    }
                }
            }]
        }
    };
}

function replaceChartData(chart, data) {
    chart.data.labels = data.labels;
    chart.data.datasets = data.datasets;
    chart.update();
}

function readSummaryConsumptionData(data) {
    data = JSON.parse(data);

    var dates = data.map(function (row) {
        return row['fields']['date'].substr(0, 10);
    });

    var sum = data.map(function (row) {
        return row['fields']['sum']
    });

    var average = data.map(function (row) {
        return row['fields']['average']
    });

    return {
        labels: dates,
        sum: sum,
        average: average
    }
}

function readDetailConsumptionData(response) {
    var data = response;

    var dates = data.map(function (row) {
        return row['date'].substr(0, 10);
    });

    var sum = data.map(function (row) {
        return row['sum']
    });

    var average = data.map(function (row) {
        return row['average']
    });

    return {
        labels: dates,
        sum: sum,
        average: average
    }
}
