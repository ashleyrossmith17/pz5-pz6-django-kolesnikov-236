document.addEventListener('DOMContentLoaded', () => {
  const source = document.getElementById('dashboard-data');
  if (!source) return;
  const data = JSON.parse(source.textContent);
  const colors = ['#2b9c87', '#4883cb', '#e2b444', '#d4717b'];
  Chart.defaults.font.family = 'Arial, sans-serif';
  Chart.defaults.color = '#56636e';
  for (const [id, key, type] of [
    ['coursesChart', 'courses', 'doughnut'],
    ['groupsChart', 'groups', 'bar'],
    ['usersChart', 'users', 'pie'],
  ]) {
    new Chart(document.getElementById(id), {
      type,
      data: {
        labels: data[key].labels,
        datasets: [{label: 'Количество', data: data[key].values,
          backgroundColor: colors, borderWidth: type === 'bar' ? 0 : 2}],
      },
      options: {
        animation: false,
        responsive: true,
        maintainAspectRatio: false,
        plugins: {legend: {display: type !== 'bar', position: 'bottom'}},
        ...(type === 'bar' ? {scales: {y: {beginAtZero: true, ticks: {stepSize: 1}}}} : {}),
      },
    });
  }
});
