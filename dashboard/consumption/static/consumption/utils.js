var SCC = (function () {
    var colors = {
        red: 'rgba(255, 88, 121, 1)',
        blue: 'rgba(47, 152, 232, 1)'
    };

    var showLoadingSpinnerOnChart = function (selector) {
        if (!$(selector).length) {
            return;
        }

        var $spinner = $('.lds-ring');
        var yOffset = $(selector).position().top + ($(selector).outerHeight() / 2) - ($spinner.outerHeight() / 2);

        $spinner.css({top: yOffset + 'px'});
        $spinner.show();
    };

    var hideLoadingSpinner = function () {
        $('.lds-ring').hide();
    };

    var replaceChartData = function (chart, data) {
        chart.data.labels = data.labels;
        chart.data.datasets = data.datasets;
        chart.update();
    };

    var readSummaryConsumptionData = function (data) {
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
    };

    var readDetailConsumptionData = function (data) {
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
    };

    function numberWithCommas(number) {
        return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    function LineChart(selector, data) {
        function buildDatasets(datasets) {
            return datasets.map(function (dataset) {
                var color = dataset.color || colors.red;
                return Object.assign(dataset, {
                    backgroundColor: color,
                    borderColor: color,
                    fill: false
                });
            });
        }

        this.replaceData = function (data) {
            this.chart.data.labels = data.labels;
            this.chart.data.datasets = buildDatasets(data.datasets);
            this.chart.update();
        };

        this.chart = new Chart($(selector), {
            type: 'line',
            options: {
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
            },
            data: {
                labels: data.labels || [],
                datasets: buildDatasets(data.datasets)
            }
        });
    }

    return {
        colors: colors,
        showLoadingSpinnerOnChart: showLoadingSpinnerOnChart,
        hideLoadingSpinner: hideLoadingSpinner,
        replaceChartData: replaceChartData,
        readSummaryConsumptionData: readSummaryConsumptionData,
        readDetailConsumptionData: readDetailConsumptionData,
        LineChart: LineChart
    }
})();