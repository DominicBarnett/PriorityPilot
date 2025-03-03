import { fetchCurrentUser } from './sharedFunctions.js';

document.addEventListener("DOMContentLoaded", async function () {
  const currentUser = await fetchCurrentUser()
  console.log("points", currentUser.points)
  console.log("user", currentUser)

  const rankHeaderFrom = document.getElementById("rank-headging");
  const rankHeaderTo = document.getElementById("rank-heading-goal");
  const rankHeaderPoints = document.getElementById("rank-heading-points");
  const [from, to, difference] = formatRank(currentUser.points);
  rankHeaderFrom.innerText = from;
  rankHeaderTo.innerText = to;
  rankHeaderPoints.innerText = `${difference} points`;

  const userFirstNameHeader = document.getElementById("user-first-name");
  userFirstNameHeader.innerText = currentUser.first_name
  const userUsernameHeader = document.getElementById("user-username");
  userUsernameHeader.innerText = `@${currentUser.username}`

  const flipElements = document.querySelectorAll("td");

  function triggerFlip() {
    flipElements.forEach((element) => {
      element.classList.remove("flip");
      setTimeout(() => {
        element.classList.add("flip");
      }, 10);
    });
  }

  setInterval(triggerFlip, 10 * 1000);

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

  updateGauge(40);
});

function formatRank(points) {
  let currentRank = "";
  let nextRank = "";
  let difference = 0;

  if (points <= 200) {
    currentRank = "Student";
    nextRank = "Amature";
    difference = 201 - points;
  } else if (points <= 400) {
    currentRank = "Amature";
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
  }

  return [currentRank, nextRank, difference];
}
