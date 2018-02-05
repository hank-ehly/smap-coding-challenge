$(document).ready(function () {
    var $detailAvgChart = $('#detail-average-chart');

    if ($detailAvgChart.length) {
        showLoadingSpinnerOnChart('#detail-chart');

        var options = {dataType: 'json'};
        var userId = $detailAvgChart.data('user-id');
        var summaryDataReq = $.ajax(['/api', 'v1', 'consumptions'].join('/'), options);
        var detailDataReq = $.ajax(['/api', 'v1', 'consumptions', userId].join('/'), options);

        $.when(summaryDataReq, detailDataReq)
            .then(onDetailDataLoaded, onDetailDataError)
            .always(hideLoadingSpinner);
    }
});

function onDetailDataLoaded(summaryResponse, detailResponse) {
    var summaryData = readSummaryConsumptionData(summaryResponse[0]);
    var userData = readDetailConsumptionData(detailResponse[0]);

    var blue = 'rgba(47, 152, 232, 1)';
    var red = 'rgba(255, 88, 121, 1)';
    var options = defaultChartOptions();
    var $detailAvgChart = $('#detail-average-chart');
    var $detailSumChart = $('#detail-sum-chart');
    var userId = $detailAvgChart.data('user-id');

    var sumLineChart = new Chart($detailSumChart, {
        type: 'line',
        options: options,
        data: {
            labels: userData['labels'],
            datasets: [
                {
                    label: 'User ' + userId + ' Total Consumption',
                    data: userData['sum'],
                    backgroundColor: red,
                    borderColor: red,
                    fill: false
                }
            ]
        }
    });

    var averageLineChart = new Chart($detailAvgChart, {
        type: 'line',
        options: options,
        data: {
            labels: userData['labels'],
            datasets: [
                {
                    label: 'User ' + userId + ' Average Consumption',
                    data: userData['average'],
                    backgroundColor: blue,
                    borderColor: blue,
                    fill: false
                },
                {
                    label: 'All Users Average Consumption',
                    data: summaryData['average'],
                    backgroundColor: red,
                    borderColor: red,
                    fill: false
                }
            ]
        }
    });
}

function onDetailDataError() {
    $('#alert').show();
}
