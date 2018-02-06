$(document).ready(function () {
    var SummaryView = {
        onSummaryDataLoaded: function (response) {
            var data = SCC.readSummaryConsumptionData(response);

            var chart = new SCC.LineChart('#summary-chart', {
                labels: data['labels'],
                datasets: [{
                    label: 'Total User Consumption',
                    data: data['sum']
                }]
            });

            $('input[type=radio][name=display]').change(function (e) {
                var fn = e.target.value;
                var label = fn === 'sum' ? 'Total User Consumption' : 'Average User Consumption';
                var color = fn === 'sum' ? SCC.colors.red : SCC.colors.blue;
                chart.replaceData({labels: data['labels'], datasets: [{label: label, data: data[fn], color: color}]});
            });
        },

        onSummaryDataError: function () {
            $('#alert').show();
        }
    };

    var $chart = $('#summary-chart');

    if ($chart.length) {
        $('#users').DataTable({searching: false});

        SCC.showLoadingSpinnerOnChart('#summary-chart');

        $.ajax(['/api', 'v1', 'consumptions'].join('/'), {dataType: 'json'})
            .then(SummaryView.onSummaryDataLoaded, SummaryView.onSummaryDataError)
            .always(SCC.hideLoadingSpinner);
    }
});
