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
    console.log("Updating chart with data:", data);
    if (data.length > 0) {
        expenseChart.data.labels = data.map(item => item.category_title);
        expenseChart.data.datasets[0].data = data.map(item => parseFloat(item.total_amount));
    } else {
        expenseChart.data.labels = [];
        expenseChart.data.datasets[0].data = [];
    }
    expenseChart.update();
}

// Fetch data from the server
function fetchData() {
    const year = $('#year').val();
    console.log("Fetching data for year:", year);

    // Handle fiscal year logic
    const startMonth = 4; // Start from April
    const endMonth = 3;   // End in March

    $.ajax({
        url: filterDataUrl,
        data: { year, startMonth, endMonth },
        success: function(response) {
            console.log("Fetched data:", response);
            updateChart(response.expenses); // Update pie chart with expenses
            updateTables(response.expenses, response.incomes); // Update income and expense sections

            // Update totals dynamically
            const totalIncome = Number(response.total_income) || 0;
            const totalExpense = Number(response.total_expense) || 0;
            const balance = Number(response.balance) || 0;
            const taxPercentage = Number(response.tax_percentage) || 0;
            const taxAmount = Number(response.tax_amount) || 0;

            console.log("Total Income:", totalIncome);
            console.log("Total Expense:", totalExpense);
            console.log("Balance:", balance);
            console.log("Tax Percentage:", taxPercentage);
            console.log("Tax Amount:", taxAmount);

            $('#totalIncome').text(totalIncome.toFixed(2));
            $('#totalExpense').text(totalExpense.toFixed(2));
            $('#balance').text(balance.toFixed(2));
            $('#taxPercentage').text(taxPercentage.toFixed(2) + '%');
            $('#taxAmount').text(taxAmount.toFixed(2));
        },
        error: function(error) {
            console.error("Error fetching data:", error);
            console.log("Response Text:", error.responseText);
        }
    });
}

// Update the income and expense sections dynamically
function updateTables(expenses, incomes) {
    console.log("Updating tables with expenses:", expenses);
    console.log("Updating tables with incomes:", incomes);

    const expenseContainer = $('#expense-container');
    const incomeContainer = $('#income-container');

    expenseContainer.empty(); // Clear existing data
    incomeContainer.empty(); // Clear existing data

    // Group by category for expenses
    const expenseGroups = expenses.reduce((acc, item) => {
        const category = item.category_title || 'Uncategorized';
        if (!acc[category]) acc[category] = [];
        acc[category].push(item);
        return acc;
    }, {});

    // Group by category for incomes
    const incomeGroups = incomes.reduce((acc, item) => {
        const category = item.category_title || 'Uncategorized';
        if (!acc[category]) acc[category] = [];
        acc[category].push(item);
        return acc;
    }, {});

    // Render grouped incomes
    for (const [category, items] of Object.entries(incomeGroups)) {
        const totalAmount = items.reduce((sum, item) => sum + parseFloat(item.total_amount || 0), 0);

        incomeContainer.append(`
            <div>
                <h4>${category} (Total: ${totalAmount.toFixed(2)})</h4>
                <ul>
                    ${items.map(item => `
                        <li>${item.subcategory_title || 'N/A'}: ${parseFloat(item.total_amount || 0).toFixed(2)}</li>
                    `).join('')}
                </ul>
            </div>
        `);
    }

    // Render grouped expenses
    for (const [category, items] of Object.entries(expenseGroups)) {
        const totalAmount = items.reduce((sum, item) => sum + parseFloat(item.total_amount || 0), 0);

        expenseContainer.append(`
            <div>
                <h4>${category} (Total: ${totalAmount.toFixed(2)})</h4>
                <ul>
                    ${items.map(item => `
                        <li>${item.subcategory_title || 'N/A'}: ${parseFloat(item.total_amount || 0).toFixed(2)}</li>
                    `).join('')}
                </ul>
            </div>
        `);
    }
}

// Attach event listeners to filter inputs to clear others when one is chosen
$('#year').on('change', function () {
    console.log("Year changed:", $(this).val());
    fetchData();
});

// Fetch current year's data on page load
$(document).ready(() => {
    const currentYear = new Date().getFullYear();
    $('#year').val(`${currentYear}-${currentYear + 1}`); // Set default to current year
    fetchData(); // Fetch initial data
});
