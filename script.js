document.getElementById('location-form').addEventListener('submit', async function (e) {
    e.preventDefault();
  
    const location = document.getElementById('location').value;
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
  
    const response = await fetch('http://127.0.0.1:5000/weather', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ location, start_date: startDate, end_date: endDate }),
    });
  
    const result = await response.json();
  
    if (response.ok) {
      const weatherData = result.data;
  
      // Update UI
      let tableContent = `
        <table>
          <tr>
            <th>Date</th>
            <th>Temperature (°C)</th>
            <th>Condition</th>
          </tr>`;
      weatherData.forEach(day => {
        if (day.error) {
          tableContent += `
            <tr>
              <td>${day.date}</td>
              <td colspan="2">${day.error}</td>
            </tr>`;
        } else {
          tableContent += `
            <tr>
              <td>${day.date}</td>
              <td>${day.temp}</td>
              <td>${day.condition}</td>
            </tr>`;
        }
      });
      tableContent += `</table>`;
  
      document.getElementById('weather-results').innerHTML = tableContent;
    } else {
      alert(result.error);
    }
  });
  