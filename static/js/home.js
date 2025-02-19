document.addEventListener("DOMContentLoaded", () => {
  const dateHeader = document.getElementById("todays-date-header");
  dateHeader.innerText = formatDate();

  const greetingHeader = document.getElementById("greeting-header-wrapper");
  const greeting = formatGreeting("Ca'Sandra");

  for (let char of greeting) {
    const letterSpan = document.createElement("span");
    letterSpan.innerText = char;
    letterSpan.classList.add("flip-letter");
    greetingHeader.appendChild(letterSpan);
  }

  const todayTaskCount = document.getElementById("total-task-count");
  const todayTasks = document.getElementsByClassName(
    "today-all-tasks-wrapper"
  )[0].children;
  todayTaskCount.innerText = todayTasks.length;

  const completionStatusButtons =
    document.getElementsByClassName("completion-circle");

  Array.from(completionStatusButtons).forEach((button) => {
    button.addEventListener("click", () => {
      if (button.classList.contains("fa-regular")) {
        button.classList.remove("fa-regular");
        button.classList.add("fa-solid");
      } else {
        button.classList.add("fa-regular");
        button.classList.remove("fa-solid");
      }
    });
  });

  const priorityWrapper = document.getElementById("custom-priority-wraper")
  const priorityButtons = document.getElementsByClassName("open-priority-menu")

  const prioritySelectMenu = document.createElement("ul")
  prioritySelectMenu.classList.add("hidden")
  prioritySelectMenu.classList.add("priority-options")
  const highPriorityOption = document.createElement("li")
  highPriorityOption.innerHTML = '<i class="fa-solid fa-plane-circle-exclamation"></i>'
  prioritySelectMenu.appendChild(highPriorityOption)
  const mediumPriorityOption = document.createElement("li")
  mediumPriorityOption.innerHTML = '<i class="fa-solid fa-plane-departure"></i>'
  prioritySelectMenu.appendChild(mediumPriorityOption)
  const lowPriorityOption = document.createElement("li")
  lowPriorityOption.innerHTML = '<i class="fa-solid fa-paper-plane"></i>'
  prioritySelectMenu.appendChild(lowPriorityOption)
  priorityWrapper.appendChild(prioritySelectMenu)

  Array.from(priorityButtons).forEach(button => {
    button.addEventListener("click", () => {
      if (prioritySelectMenu.classList.contains("hidden")) {
        prioritySelectMenu.classList.remove("hidden")
      } else {
        prioritySelectMenu.classList.add("hidden")
      }
    })
  })
});

function formatDate() {
  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  const today = new Date();
  const month = today.getMonth();
  const day = today.getDate();
  const year = today.getFullYear();

  return `${months[month]} ${day}, ${year}`;
}

function formatGreeting(name) {
  const hours = new Date().getHours();
  let greeting = "";

  if (hours <= 4 || hours >= 20) {
    greeting = "Good night";
  } else if (hours >= 5 && hours <= 11) {
    greeting = "Good morning";
  } else if (hours >= 12 && hours <= 16) {
    greeting = "Good afternoon";
  } else {
    greeting = "Good evening";
  }

  return `${greeting} ${name}`;
}
