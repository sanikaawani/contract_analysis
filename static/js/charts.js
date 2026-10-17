/**
 * Chart.js Visualizations for Legal Contract Risk Analyzer
 */

let riskDoughnutChartInstance = null;
let categoryBarChartInstance = null;

function renderRiskCharts(riskScoreData, clausesData) {
  // 1. Risk Level Doughnut Chart
  const doughnutCtx = document.getElementById('riskDoughnutChart');
  if (doughnutCtx) {
    if (riskDoughnutChartInstance) {
      riskDoughnutChartInstance.destroy();
    }

    const highCount = riskScoreData.high_count || 0;
    const medCount = riskScoreData.medium_count || 0;
    const lowCount = riskScoreData.low_count || 0;

    riskDoughnutChartInstance = new Chart(doughnutCtx.getContext('2d'), {
      type: 'doughnut',
      data: {
        labels: ['High Risk', 'Medium Risk', 'Low Risk'],
        datasets: [{
          data: [highCount, medCount, lowCount],
          backgroundColor: ['#EF4444', '#F59E0B', '#10B981'],
          borderWidth: 2,
          borderColor: '#0F172A',
          hoverOffset: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: '#94A3B8',
              font: { size: 10 },
              boxWidth: 10,
              padding: 8
            }
          }
        },
        cutout: '70%'
      }
    });
  }

  // 2. Clause Category Bar Chart
  const barCtx = document.getElementById('categoryBarChart');
  if (barCtx) {
    if (categoryBarChartInstance) {
      categoryBarChartInstance.destroy();
    }

    const catDist = riskScoreData.category_distribution || {};
    const categories = Object.keys(catDist);
    const counts = Object.values(catDist);

    categoryBarChartInstance = new Chart(barCtx.getContext('2d'), {
      type: 'bar',
      data: {
        labels: categories.map(c => c.length > 14 ? c.substring(0, 12) + '..' : c),
        datasets: [{
          label: 'Detected Clauses',
          data: counts,
          backgroundColor: '#3B82F6',
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: {
            ticks: { color: '#94A3B8', font: { size: 9 } },
            grid: { display: false }
          },
          y: {
            beginAtZero: true,
            ticks: { color: '#94A3B8', font: { size: 9 }, stepSize: 1 },
            grid: { color: '#1E293B' }
          }
        }
      }
    });
  }
}
