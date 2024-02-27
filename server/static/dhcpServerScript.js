function fetchAndUpdate() {
    fetch('/update')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('hostsTableBody');
            tableBody.innerHTML = ''; // Clear the table body

            data.forEach(host => {
                const row = `<tr>
                                <td>${host.mac}</td>
                                <td>${host.ip}</td>
                                <td>${host.hostname}</td>
                                <td>${host.is_current ? 'Current' : 'Old'}</td>
                             </tr>`;
                tableBody.innerHTML += row; // Add the new row
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Fetch and update data every 5 seconds
setInterval(fetchAndUpdate, 5000);

// Fetch and update once on initial load
document.addEventListener('DOMContentLoaded', fetchAndUpdate);