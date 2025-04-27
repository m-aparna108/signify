let draggedUsername = "";

function handleDragStart(event, username) {
  draggedUsername = username;
  event.dataTransfer.setData("text/plain", username);
}

function allowDrop(event) {
  event.preventDefault();
}

function handleDrop(event) {
  event.preventDefault();
  const x = event.clientX;
  const y = event.clientY;
  showProfile(draggedUsername, x, y);
}

function showProfile(username, x = null, y = null) {
  // Fetch the user profile data based on username from leaderboard
  const user = leaderboardData.find(u => u.username === username);
  if (!user) return;

  const card = document.getElementById("profileCard");
  card.innerHTML = `
    <h4>👤 ${user.username}</h4>
    <p>📚 Quiz: ${user.quizTitle}</p>
    <p>⭐ Score: ${user.score}</p>
    <p>📅 Date: ${user.date}</p>
    <button class="btn btn-sm btn-danger mt-2" onclick="this.parentElement.style.display='none'">Close</button>
  `;
  card.style.display = 'block';

  if (x !== null && y !== null) {
    card.style.left = `${x}px`;
    card.style.top = `${y}px`;
    card.style.transform = "translate(-50%, 0)";
  }
}

function loadLeaderboardData() {
  const leaderboardBody = document.getElementById("leaderboardBody");
  leaderboardBody.innerHTML = ''; // Clear the leaderboard

  const timeFilter = document.getElementById("timeFilter").value;
  const quizFilter = document.getElementById("quizFilter").value;
  
  // Build the API URL with query parameters for filtering
  const apiUrl = `/api/leaderboard?timeFilter=${timeFilter}&quizFilter=${quizFilter}`;
  
  // Fetch data from the backend API
  fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      // Sort the leaderboard data by score
      data.sort((a, b) => b.score - a.score);

      // If no data is returned, show a message
      if (data.length === 0) {
        const row = document.createElement("tr");
        row.innerHTML = `<td colspan="4">🚫 No results found for selected filters.</td>`;
        leaderboardBody.appendChild(row);
        return;
      }

      // Iterate through the fetched data and create leaderboard rows
      data.forEach((entry, index) => {
        let medalIcon = '';
        if (index === 0) medalIcon = '<i class="fas fa-medal gold"></i>';
        else if (index === 1) medalIcon = '<i class="fas fa-medal silver"></i>';
        else if (index === 2) medalIcon = '<i class="fas fa-medal bronze"></i>';

        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${index + 1} ${medalIcon}</td>
          <td draggable="true" ondragstart="handleDragStart(event, '${entry.username}')" onclick="showProfile('${entry.username}', event.clientX, event.clientY)" style="cursor: pointer;">${entry.username}</td>
          <td>${entry.quizTitle}</td>
          <td class="${entry.score > 90 ? 'high-score' : ''}">
            ${entry.score}
            <div class="score-bar mt-2">
              <div class="score-fill" style="width: ${entry.score}%;"></div>
            </div>
          </td>
        `;
        leaderboardBody.appendChild(row);
      });
    })
    .catch(error => console.error('Error fetching leaderboard data:', error));
}

// Event listeners for the filters
document.getElementById('quizFilter').addEventListener('change', loadLeaderboardData);
document.getElementById('timeFilter').addEventListener('change', loadLeaderboardData);

// Call to load the data when the page loads
document.addEventListener('DOMContentLoaded', function () {
  loadLeaderboardData();
});
