$(document).ready(function () {
    var $summaryChart = $('#summary-chart');

    if ($summaryChart.length) {
        $('#users').DataTable({searching: false});

        showLoadingSpinnerOnChart('#summary-chart');

        var url = ['/api', 'v1', 'consumptions'].join('/');

        $.ajax(url, {dataType: 'json'})
            .then(onSummaryDataLoaded, onSummaryDataError)
            .always(hideLoadingSpinner);
    }
});

function onSummaryDataLoaded(response) {
    var red = 'rgba(255, 88, 121, 1)';
    var blue = 'rgba(47, 152, 232, 1)';
    var data = readSummaryConsumptionData(response);
    var options = defaultChartOptions();

    var lineChart = new Chart($('#summary-chart'), {
        type: 'line',
        options: options,
        data: {
            labels: data['labels'],
            datasets: [
                {
                    label: 'Total User Consumption',
                    data: data['sum'],
                    backgroundColor: red,
                    borderColor: red,
                    fill: false
                }
            ]
        }
    });

    $('input[type=radio][name=display]').change(function (e) {
        var fn = e.target.value;
        var label = fn === 'sum' ? 'Total User Consumption' : 'Average User Consumption';
        var color = fn === 'sum' ? red : blue;

        var dataset = {
            label: label,
            data: data[fn],
            backgroundColor: color,
            borderColor: color,
            fill: false
        };

        replaceChartData(lineChart, {labels: data['labels'], datasets: [dataset]});
    });
}

function onSummaryDataError() {
    $('#alert').show();
}
