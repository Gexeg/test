
function render_query_line_chart(chartDataInput, element_id) {
    const ctx = document.getElementById(element_id).getContext("2d")

    if (Chart.getChart(element_id)) {
        console.log('got chart instance')
        Chart.getChart(ctx).destroy();
    }

    datasets = chartDataInput.lines.reduce((acc, lineData) => {
        const line = {
            label: lineData.label,
            data: lineData.data
        }
        line.borderColor = lineData.lineFormat.borderColor
        line.borderDash = lineData.lineFormat.borderDash,
        line.pointRadius = lineData.lineFormat.pointRadius
        acc.push(line)
        return acc 
    }, [])

    chartData = {
        data: {
            labels: chartDataInput['labels'],
            datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: chartDataInput.title
                },
                customCanvasBackgroundColor: {
                  color: 'white',
                }
            }
        }
    }

    new Chart(ctx, {
      type: 'line',
      data: chartData.data,
      options: chartData.options
    })
    if (Chart.getChart(element_id)) {
        console.log('got chart instance2')
    }
}