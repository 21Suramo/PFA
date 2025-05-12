const API_URL = "http://<IP_DU_SERVEUR>:5000/api/data";
const ctx = document.getElementById('chart').getContext('2d');

// Configuration initiale du graphique
const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [
      {
        label: 'Température (°C)',
        data: [],
        borderColor: 'red',
        fill: false
      },
      {
        label: 'Pression (Pa)',
        data: [],
        borderColor: 'blue',
        fill: false
      }
    ]
  },
  options: {
    scales: {
      x: { display: true, title: { display: true, text: 'Heure' } },
      y: { beginAtZero: false }
    },
    animation: false
  }
});

// Fonction pour charger et mettre à jour les données
async function updateData() {
  try {
    const res = await fetch(API_URL);
    const data = await res.json();

    chart.data.labels = data.map(d => new Date(d.timestamp * 1000).toLocaleTimeString());
    chart.data.datasets[0].data = data.map(d => d.temperature);
    chart.data.datasets[1].data = data.map(d => d.pression);
    chart.update();
  } catch (err) {
    console.error("Erreur récupération données :", err);
  }
}

// Rafraîchissement toutes les 5 s
setInterval(updateData, 5000);
updateData();
