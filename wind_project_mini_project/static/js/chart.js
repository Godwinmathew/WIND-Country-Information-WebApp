document.addEventListener("DOMContentLoaded", function () {
  const chartDataElem = document.getElementById("chart-data");
  if (!chartDataElem) return;

  const chartData = JSON.parse(chartDataElem.textContent);
  const fromCurrency = chartData.from_currency;
  const toCurrency = chartData.to_currency;

  const ctx = document.getElementById("rateChart").getContext("2d");

  new Chart(ctx, {
    type: "line",
    data: {
      labels: chartData.dates,
      datasets: [{
        label: `${fromCurrency} to ${toCurrency}`,
        data: chartData.rates,
        borderColor: "crimson",
        backgroundColor: "rgba(220, 20, 60, 0.2)",
        borderWidth: 3,
        pointBackgroundColor: "#fff",
        pointBorderColor: "crimson",
        pointRadius: 5,
        tension: 0.4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: "#fff",
            font: {
              size: 14,
              family: "Segoe UI"
            }
          }
        }
      },
      scales: {
        x: {
          ticks: { color: "#eee" },
          grid: { color: "rgba(255,255,255,0.1)" }
        },
        y: {
          beginAtZero: false,
          ticks: { color: "#eee" },
          grid: { color: "rgba(255,255,255,0.1)" }
        }
      }
    }
  });
});
