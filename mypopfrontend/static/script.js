async function fetchJiraData() {
    const response = await fetch('/api/jira-data');
    const data = await response.json();
    return data;
}

async function generateChart() {
    const issues = await fetchJiraData();

    const statusCounts = issues.reduce((acc, issue) => {
        acc[issue.status] = (acc[issue.status] || 0) + 1;
        return acc;
    }, {});

    const ctx = document.getElementById('issueChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(statusCounts),
            datasets: [{
                label: '# of Issues',
                data: Object.values(statusCounts),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

generateChart();
