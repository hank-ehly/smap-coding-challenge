$(document).ready(function () {
    $('#users').DataTable();


    var ctx = $('#chart');

    var lineChart = new Chart(ctx, {
        type: 'line',
        data: {

            // these will be date time values
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],

            // this will be the aggregation data for all users
            datasets: [
                {
                    label: 'All users',
                    data: [10, 8, 6, 5, 12, 8, 16, 17, 6, 7, 6, 10],
                    backgroundColor: 'rgba(255, 88, 121, 1)',
                    borderColor: 'rgba(255, 88, 121, 1)',
                    fill: false
                }
            ]
        }
    })

});

// 47 152 232 (blue)