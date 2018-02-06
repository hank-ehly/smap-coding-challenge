$(document).ready(function () {
    var DetailView = {
        onDetailDataLoaded: function (summaryResponse, detailResponse) {
            var summaryData = SCC.readSummaryConsumptionData(summaryResponse[0]);
            var userData = SCC.readDetailConsumptionData(detailResponse[0]);
            var userId = $('#detail-average-chart').data('user-id');

            var sumLineChart = new SCC.LineChart('#detail-sum-chart', {
                labels: userData['labels'],
                datasets: [
                    {
                        label: 'User ' + userId + ' Total Consumption',
                        data: userData['sum']
                    }
                ]
            });

            var averageLineChart = new SCC.LineChart('#detail-average-chart', {
                labels: summaryData['labels'],
                datasets: [
                    {
                        label: 'User ' + userId + ' Average Consumption',
                        data: userData['average'],
                        color: SCC.colors.blue
                    },
                    {
                        label: 'All Users Average Consumption',
                        data: summaryData['average']
                    }
                ]
            });
        },

        onDetailDataError: function () {
            $('#alert').show();
        }
    };

    var $chart = $('#detail-sum-chart');

    if ($chart.length) {
        SCC.showLoadingSpinnerOnChart('#detail-sum-chart');

        var options = {dataType: 'json'};
        var userId = $chart.data('user-id');
        var summary = $.ajax(['/api', 'v1', 'consumptions'].join('/'), options);
        var detail = $.ajax(['/api', 'v1', 'consumptions', userId].join('/'), options);

        $.when(summary, detail)
            .then(DetailView.onDetailDataLoaded, DetailView.onDetailDataError)
            .always(SCC.hideLoadingSpinner);
    }
});
