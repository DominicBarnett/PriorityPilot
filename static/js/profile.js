import { fetchCurrentUser } from './sharedFunctions.js';

document.addEventListener("DOMContentLoaded", async function () {
  const currentUser = await fetchCurrentUser();

  // Set user rank information
  const rankHeaderFrom = document.getElementById("rank-headging");
  const rankHeaderTo = document.getElementById("rank-heading-goal");
  const rankHeaderPoints = document.getElementById("rank-heading-points");
  const [from, to, difference] = formatRank(currentUser.points);
  rankHeaderFrom.innerText = from;
  rankHeaderTo.innerText = to;
  rankHeaderPoints.innerText = `${difference} points`;

  // Set user name and username
  const userFirstNameHeader = document.getElementById("user-first-name");
  userFirstNameHeader.innerText = currentUser.first_name;
  const userUsernameHeader = document.getElementById("user-username");
  userUsernameHeader.innerText = `@${currentUser.username}`;

  // Set missions completed (total completed tasks)
  const missionsCompletedElement = document.querySelector('.arrival-departure-info div:nth-child(6) h2');
  const completedTasks = currentUser.completed_tasks || 0;
  missionsCompletedElement.innerText = completedTasks;

  // Set on-time departures
  const onTimeDeparturesElement = document.querySelector('.arrival-departure-info div:nth-child(7) h2');
  const onTimeTasks = currentUser.on_time_tasks || 0;
  onTimeDeparturesElement.innerText = onTimeTasks;

  // Set emergency landings (overdue tasks)
  const emergencyLandingsElement = document.getElementById('emergency-landings-count');
  const overdueTasks = currentUser.overdue_tasks || 0;
  emergencyLandingsElement.innerText = overdueTasks;

  // Update flight board with actual task data
  updateFlightBoard(currentUser);

  // Flip animation for flight board
  const flipElements = document.querySelectorAll("td");
  function triggerFlip() {
    flipElements.forEach((element) => {
      element.classList.remove("flip");
      setTimeout(() => {
        element.classList.add("flip");
      }, 10);
    });
  }

  // Update cabin pressure gauge
  const cabinPressure = currentUser.cabin_pressure || 0;
  updateGauge(cabinPressure);
});

function formatRank(points) {
  let currentRank = "";
  let nextRank = "";
  let difference = 0;

  if (points <= 200) {
    currentRank = "Student";
    nextRank = "Amateur";
    difference = 201 - points;
  } else if (points <= 400) {
    currentRank = "Amateur";
    nextRank = "First Officer";
    difference = 401 - points;
  } else if (points <= 600) {
    currentRank = "First Officer";
    nextRank = "Captain";
    difference = 601 - points;
  } else if (points <= 800) {
    currentRank = "Captain";
    nextRank = "Instructor";
    difference = 801 - points;
  } else {
    currentRank = "Instructor";
    nextRank = "Instructor";
    difference = 0;
  }

  return [currentRank, nextRank, difference];
}

function updateGauge(percentage) {
  let progressArc = document.getElementById("progress");
  let offset = 180 - (percentage / 100) * 180; // Converts percentage to arc offset
  progressArc.style.strokeDashoffset = offset;
  progressArc.style.opacity = percentage > 0 ? 1 : 0; // Hide when at 0%

  let needleAngle = -135 + (percentage / 100) * 270; // Convert to 270° rotation range
  document.querySelector(
    ".needle"
  ).style.transform = `rotate(${needleAngle}deg)`;

  document.querySelector(".percentage").textContent = percentage + "%";
}

function updateFlightBoard(userData) {
  // Get flight board rows
  const flightRows = document.querySelectorAll('.flight-board-wrapper tbody tr');
  
  // Row 1: Final Call (high priority tasks)
  if (flightRows[0]) {
    const highPriorityCount = userData.high_priority_tasks || 0;
    flightRows[0].querySelector('td:nth-child(3)').textContent = highPriorityCount;
    
    // Update status based on if there are any high priority tasks
    const status = highPriorityCount > 0 ? 'BOARDING' : 'COMPLETED';
    const statusCell = flightRows[0].querySelector('td:nth-child(4)');
    statusCell.textContent = status;
    
    // Update classes based on status
    statusCell.classList.remove('boarding', 'on-time');
    statusCell.classList.add(status === 'BOARDING' ? 'boarding' : 'on-time');
  }
  
  // Row 2: Goal Getter (medium priority tasks)
  if (flightRows[1]) {
    const mediumPriorityCount = userData.medium_priority_tasks || 0;
    flightRows[1].querySelector('td:nth-child(3)').textContent = mediumPriorityCount;
    
    // Medium priority tasks are typically "on time"
    const statusCell = flightRows[1].querySelector('td:nth-child(4)');
    statusCell.textContent = 'ON TIME';
  }
  
  // Row 3: Retry Runway (low priority or overdue tasks)
  if (flightRows[2]) {
    const lowPriorityCount = userData.low_priority_tasks || 0;
    flightRows[2].querySelector('td:nth-child(3)').textContent = lowPriorityCount;
    
    // Update status based on overdue tasks
    const overdueCount = userData.overdue_tasks || 0;
    const status = overdueCount > 0 ? 'DELAYED' : 'SCHEDULED';
    const statusCell = flightRows[2].querySelector('td:nth-child(4)');
    statusCell.textContent = status;
    
    // Update classes based on status
    statusCell.classList.remove('delayed', 'on-time');
    statusCell.classList.add(status === 'DELAYED' ? 'delayed' : 'on-time');
  }
}