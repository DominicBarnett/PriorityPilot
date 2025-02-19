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

  // Select all priority wrappers
  const priorityWrappers = document.querySelectorAll(".custom-priority-wraper");

  priorityWrappers.forEach((wrapper) => {
    const button = wrapper.querySelector(".open-priority-menu"); // Get the button inside the wrapper
    const hiddenInput = wrapper.nextElementSibling; // Get the hidden input (assumes it's right after the wrapper)

    const prioritySelectMenu = document.createElement("ul");
    prioritySelectMenu.classList.add("hidden", "priority-options");

    const priorities = [
      {
        value: "high-priority",
        icon: '<i class="fa-solid fa-plane-circle-exclamation"></i>',
      },
      {
        value: "medium-priority",
        icon: '<i class="fa-solid fa-plane-departure"></i>',
      },
      {
        value: "low-priority",
        icon: '<i class="fa-solid fa-paper-plane"></i>',
      },
    ];

    priorities.forEach((priority) => {
      const option = document.createElement("li");
      option.innerHTML = priority.icon;
      option.dataset.value = priority.value;
      prioritySelectMenu.appendChild(option);

      option.addEventListener("click", () => {
        button.innerHTML = priority.icon;
        hiddenInput.value = priority.value;
        prioritySelectMenu.classList.add("hidden");
      });
    });

    wrapper.appendChild(prioritySelectMenu);

    button.addEventListener("click", () => {
      prioritySelectMenu.classList.toggle("hidden");
    });

    document.addEventListener("click", (event) => {
      if (!wrapper.contains(event.target)) {
        prioritySelectMenu.classList.add("hidden");
      }
    });
  });
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
