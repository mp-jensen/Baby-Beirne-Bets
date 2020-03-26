        {% if bDateData[3] %}
        var allBDateEle = document.getElementById('allDateBets');
        var allDateBets = [];
        var allDateCounts = [];
        {% for value in bDateData[3] %}
            allDateCounts.push({{ value[0] }});
            allDateBets.push('{{ value[1] }}');
        {% endfor %}
        var allbDateChar = new Chart(allBDateEle, {
            type: 'horizontalBar',
            data: {
                labels: allDateBets,
                datasets: [{
                    data: allDateCounts
                }]
            },
            options: {
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: "# of Bets"
                        },
                        ticks: {
                            beginAtZero: true,
                            stepSize: 1,
                            suggestedMax: 3
                        }
                    }]
                }
            }
        });
        {% endif %}
