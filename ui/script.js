const rangeForm = document.getElementById('range-form');
const referenceForm = document.getElementById('reference-form');
const resolutionForm = document.getElementById('resolution-form');
const activeTraceForm = document.getElementById('active-trace-form');

async function fetchData(url, method, data) {
  try {
    const response = await fetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Fetch error:', error);
    alert('Error communicating with the server.');
    return null;
  }
}

rangeForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const startWl = parseFloat(document.getElementById('start-wl').value);
  const stopWl = parseFloat(document.getElementById('stop-wl').value);

  const data = { start_wl: startWl, stop_wl: stopWl };
  const result = await fetchData('/range', 'POST', data);

  if (result && result.message) {
    alert(result.message);
  }
});

referenceForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const reference = parseFloat(document.getElementById('reference').value);

  const data = { reference: reference };
  const result = await fetchData('/reference', 'POST', data);

  if (result && result.message) {
    alert(result.message);
  }
});

resolutionForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const resolution = parseFloat(document.getElementById('resolution').value);

  const data = { resolution: resolution };
  const result = await fetchData('/resolution', 'POST', data);

  if (result && result.message) {
    alert(result.message);
  }
});

activeTraceForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const trace = document.getElementById('active-trace').value;

  const data = { trace: trace };
  const result = await fetchData('/active_trace', 'POST', data);

  if (result && result.message) {
    alert(result.message);
  }
});