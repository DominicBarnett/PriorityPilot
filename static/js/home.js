// Array of possible characters
const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".split("");

// Function to get a random character
function getRandomChar() {
  return chars[Math.floor(Math.random() * chars.length)];
}

// Function to flip text before settling on the final letter
function flipToFinalLetter(span, finalLetter, duration = 2000) {
  let counter = 0;
  let maxFlips = Math.floor(duration / 100); // Number of random flips before stopping

  const interval = setInterval(() => {
    if (counter < maxFlips) {
      span.textContent = getRandomChar(); // Show random letters during flip
    } else {
      clearInterval(interval);
      span.textContent = finalLetter === " " ? "\u00A0" : finalLetter; // Ensure spaces are visible
      span.classList.remove("flipping"); // Remove animation class
    }
    counter++;
  }, 100); // Change every 100ms
}

// Function to start the flip animation
function startFlipAnimation(greeting) {
  const wrapper = document.getElementById("greeting-header-wrapper");
  wrapper.innerHTML = ""; // Clear existing spans

  // Create spans for each character, including spaces
  greeting.split("").forEach((char, index) => {
    const span = document.createElement("span");
    span.textContent = "\u00A0"
    wrapper.appendChild(span);

    const delay = index * 300; // Staggered start for a realistic effect
    setTimeout(() => {
      flipToFinalLetter(span, char);
    }, delay);
  });
}


document.addEventListener("DOMContentLoaded", () => {
  const dateHeader = document.getElementById("todays-date-header");
  dateHeader.innerText = formatDate();

  const todayTaskCount = document.getElementById("total-task-count");
  const todayTasks = document.getElementsByClassName(
    "today-all-tasks-wrapper"
  )[0];
  todayTaskCount.innerText = todayTasks.children.length;

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

  const addTodayTaskButton = document.getElementById("add-today-task-button");

  addTodayTaskButton.addEventListener("click", () => {
    const newTask = document.createElement("div");
    newTask.classList.add("today-single-task-wrapper");
    newTask.innerHTML = `<i class="fa-regular fa-circle completion-circle"></i>
                <form>
                  <input value="" />
                  <div class="custom-priority-wraper">
                    <button class="open-priority-menu" type="button">
                      <i class="fa-solid fa-paper-plane"></i>
                    </button>
                    <ul class="hidden priority-options">
                      <li data-value="high-priority"><i class="fa-solid fa-plane-circle-exclamation"></i></li>
                      <li data-value="medium-priority"><i class="fa-solid fa-plane-departure"></i></li>
                      <li data-value="low-priority"><i class="fa-solid fa-paper-plane"></i></li>
                    </ul>
                  </div>
                  <input type="hidden" name="priority" value="low-priority" />
                </form>`;
    todayTasks.appendChild(newTask);
    const newInput = newTask.querySelector('input[value=""]');
    newInput.focus();

    // Attach event listeners to the new elements
    const priorityButton = newTask.querySelector(".open-priority-menu");
    const priorityMenu = newTask.querySelector(".priority-options");
    const priorityOptions = newTask.querySelectorAll(".priority-options li");
    const hiddenInput = newTask.querySelector('input[type="hidden"]');

    // Toggle dropdown visibility
    priorityButton.addEventListener("click", () => {
      priorityMenu.classList.toggle("hidden");
    });

    // Handle option selection
    priorityOptions.forEach((option) => {
      option.addEventListener("click", () => {
        priorityButton.innerHTML = option.innerHTML; // Update button icon
        hiddenInput.value = option.dataset.value; // Update hidden input value
        priorityMenu.classList.add("hidden"); // Hide menu
      });
    });

    // Close dropdown when clicking outside
    document.addEventListener("click", (event) => {
      if (!newTask.contains(event.target)) {
        priorityMenu.classList.add("hidden");
      }
    });

    todayTaskCount.innerText = todayTasks.children.length;
  });

  startFlipAnimation(formatGreeting("Ca'Sandra").toUpperCase())
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
    greeting = "Good Night";
  } else if (hours >= 5 && hours <= 11) {
    greeting = "Good Morning";
  } else if (hours >= 12 && hours <= 16) {
    greeting = "Good Afternoon";
  } else {
    greeting = "Good Evening";
  }

  return `${greeting} ${name}`;
}
