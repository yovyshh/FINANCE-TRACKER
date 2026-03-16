const ctx = document.getElementById('expenseChart').getContext('2d');
const expenseChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: [],
        datasets: [{
            label: 'Expenses',
            data: [],
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#FFA07A', '#20B2AA']
        }]
    }
});

// Update the chart with new data
function updateChart(data) {
    if (data.length > 0) {
        expenseChart.data.labels = data.map(item => item.title || item.name);
        expenseChart.data.datasets[0].data = data.map(item => parseFloat(item.amount || item.initial_amount));
    } else {
        expenseChart.data.labels = [];
        expenseChart.data.datasets[0].data = [];
    }
    expenseChart.update();
}

// Fetch data from the server
function fetchData() {
    const start_date = $('#start_date').val();
    const month = $('#month').val();
    const budget = $('#budget').val();
    const year = $('#year').val();
    const dataType = $('#data-type').val();

    // Handle fiscal year logic
    let startMonth = 1;
    let endMonth = 12;

    if (year) {
        startMonth = 4;  // Start from April
        endMonth = 3;    // End in March
    }

    $.ajax({
        url: filterDataUrl,
        data: { start_date, month, budget, year, startMonth, endMonth, dataType },
        success: function(response) {
            console.log("Fetched data:", response.data); // Debugging output
            updateChart(response.data);  // Update pie chart
            updateTable(response.data);  // Update table

            // Use default value of 0 if the value is null or undefined
            const currentMonthTotalIncome = Number(response.current_month.total_income) || 0;
            const currentMonthTotalExpense = Number(response.current_month.total_expense) || 0;
            const currentMonthBalanceIncome = Number(response.current_month.balance_income) || 0;
            const filteredTotalIncome = Number(response.filtered_data.total_income) || 0;
            const filteredTotalExpense = Number(response.filtered_data.total_expense) || 0;
            const filteredBalanceIncome = Number(response.filtered_data.balance_income) || 0;

            $('#currentMonthTotalIncome').text(currentMonthTotalIncome.toFixed(2));
            $('#currentMonthTotalExpense').text(currentMonthTotalExpense.toFixed(2));
            $('#currentMonthBalanceIncome').text(currentMonthBalanceIncome.toFixed(2));

            // Update filtered data totals
            $('#filteredTotalIncome').text(filteredTotalIncome.toFixed(2));
            $('#filteredTotalExpense').text(filteredTotalExpense.toFixed(2));
            $('#filteredBalanceIncome').text(filteredBalanceIncome.toFixed(2));
        },
        error: function(error) {
            console.error("Error fetching data:", error);
            console.log("Response Text:", error.responseText);
        }
    });
}

// Update the table dynamically with new data
function updateTable(data) {
    const tableBody = $('#data-table-body');
    tableBody.empty();  // Clear existing rows

    // Loop through the data and create new rows
    data.forEach(item => {
        const row = `<tr>
                        <td>${item.title || item.name}</td>
                        <td>${item.description || 'N/A'}</td>
                        <td>${item.amount || item.initial_amount}</td>
                        <td>${item.category__title || 'N/A'}</td>
                        <td>${item.subcategory__title || 'N/A'}</td>
                        <td>${item.budget__name || 'N/A'}</td>
                        <td>${item.date || item.start_date || 'N/A'}</td>
                    </tr>`;
        tableBody.append(row);  // Append the new row to the table
    });
}

// Attach event listeners to filter inputs to clear others when one is chosen
$('#start_date').on('change', function () {
    // $('#month').val('');
    // $('#year').val('');
    // $('#budget').val('');
    fetchData();
});

$('#month').on('change', function () {
    // $('#start_date').val('');
    // $('#year').val('');
    // $('#budget').val('');
    fetchData();
});

$('#year').on('change', function () {
    // $('#start_date').val('');
   
    // $('#data-type').val(''); 
    fetchData();
});

$('#budget').on('change', function () {
    // $('#start_date').val('');
    // $('#month').val('');
    // $('#year').val('');
    fetchData();
});

$('#data-type').on('change', function () {
    fetchData();
    $('#year').val('');
});

// Fetch current month's data on page load
$(document).ready(() => {
    const today = new Date();
    const currentMonth = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}`;
    $('#month').val(currentMonth);  // Set default to current month
    fetchData();  // Fetch initial data
});


