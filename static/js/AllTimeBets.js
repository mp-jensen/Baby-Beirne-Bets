        {% if bDateData[3] %}
        var allBTimeEle = document.getElementById('allTimeBets');
        var allTimeBets = [];
        var allTimeCounts = [];
        {% for value in bTimeData[3] %}
            allTimeCounts.push({{ value[0] }});
            allTimeBets.push('{{ value[1] }}h{{ value[2] }}m');
        {% endfor %}
        var allbTimeChar = new Chart(allBTimeEle, {
            type: 'horizontalBar',
            data: {
                labels: allTimeBets,
                datasets: [{
                    data: allTimeCounts
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
