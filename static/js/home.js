import { fetchCurrentUser } from './sharedFunctions.js';

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

    span.classList.add("flipping"); // Add animation class

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
    if (!wrapper) return; // Exit if the wrapper doesn't exist

    wrapper.innerHTML = ""; // Clear existing spans

    greeting.split("").forEach((char, index) => {
        const span = document.createElement("span");
        span.textContent = "\u00A0"; // Non-breaking space for empty characters
        wrapper.appendChild(span);

        const delay = index * 300; // Staggered start for a realistic effect
        setTimeout(() => {
            flipToFinalLetter(span, char);
        }, delay);
    });
}

// Function to set up priority menu logic
function setupPriorityMenu(wrapper) {
  const button = wrapper.querySelector(".open-priority-menu");
  const priorityMenu = wrapper.querySelector(".priority-options");
  const hiddenInput = wrapper.querySelector('input[type="hidden"][name="priority"]'); 

  if (!hiddenInput) {
      console.error("Hidden input for priority not found within wrapper:", wrapper);
      return; // Stop execution to prevent further errors
  }

  button.addEventListener("click", () => {
      priorityMenu.classList.toggle("hidden");
  });

  priorityMenu.querySelectorAll("li").forEach((option) => {
      option.addEventListener("click", () => {
          const selectedPriority = option.dataset.value; // Get the selected priority
          if (!selectedPriority) {
              console.error("No data-value found for selected priority option", option);
              return;
          }

          console.log(`Priority selected: ${selectedPriority}`); // Debugging

          button.innerHTML = option.innerHTML; // Update button icon
          hiddenInput.value = selectedPriority; // Correctly update hidden input
          priorityMenu.classList.add("hidden"); // Hide menu
      });
  });

  document.addEventListener("click", (event) => {
      if (!wrapper.contains(event.target)) {
          priorityMenu.classList.add("hidden");
      }
  });
}



// Function to format the date
function formatDate() {
    const months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ];
    const today = new Date();
    return `${months[today.getMonth()]} ${today.getDate()}, ${today.getFullYear()}`;
}

// Function to format the greeting based on the time of day
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

// Function to handle form submission asynchronously
function handleFormSubmit(event) {
  event.preventDefault(); 

  const form = event.target;
  const formData = new FormData(form);

  console.log("Submitting task with priority:", formData.get("priority")); // Debugging

  fetch(form.action, {
      method: form.method,
      body: formData,
  })
  .then((response) => {
      if (response.ok) {
          window.location.reload();
      } else {
          console.error("Error:", response.statusText);
      }
  })
  .catch((error) => console.error("Error:", error));
}


// DOMContentLoaded event listener
document.addEventListener("DOMContentLoaded", async() => {
    // Set today's date
    const dateHeader = document.getElementById("todays-date-header");
    if (dateHeader) {
        dateHeader.textContent = formatDate();
    }

    // Toggle task completion
    const completionButtons = document.querySelectorAll(".completion-circle");
    completionButtons.forEach((button) => {
        button.addEventListener("click", (event) => {
            event.preventDefault(); // Prevent default form submission

            const form = button.closest("form");
            const taskId = form.action.split("/").pop(); // Get the task ID from the form action

            fetch(`/toggle-completion/${taskId}`, { method: "POST" })
                .then((response) => {
                    if (response.ok) {
                        // Toggle the completion circle
                        const icon = button.querySelector("i");
                        icon.classList.toggle("fa-regular");
                        icon.classList.toggle("fa-solid");
                        icon.classList.toggle("fa-circle-check");

                        // Apply strike-through for completed tasks
                        const taskInput = button
                            .closest(".today-single-task-wrapper")
                            .querySelector("input[name='task']");
                        taskInput.classList.toggle("task-completed");
                    }
                })
                .catch((error) => console.error("Error:", error));
        });
    });

    // Set up priority menus
    const priorityWrappers = document.querySelectorAll(".custom-priority-wrapper");
    priorityWrappers.forEach((wrapper) => {
        setupPriorityMenu(wrapper);
    });

    // Add new task
    const addTodayTaskButton = document.getElementById("add-today-task-button");
    if (addTodayTaskButton) {
        addTodayTaskButton.addEventListener("click", () => {
            const todayTasks = document.querySelector(".today-all-tasks-wrapper");
            const newTask = document.createElement("div");
            newTask.classList.add("today-single-task-wrapper");
            newTask.innerHTML = `
                <i class="fa-regular fa-circle completion-circle"></i>
                <form class="task-form" action="/add-task" method="POST">
                    <input name="task" value="" />
                    <div class="custom-priority-wrapper">
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
                    <button type="submit" class="save-task-btn">Save</button>
                </form>
                <form class="task-form" action="/delete-task" method="POST">
                    <button type="submit" class="delete-task-btn"><i class="fa-solid fa-trash"></i></button>
                </form>`;

            todayTasks.appendChild(newTask);
            const newInput = newTask.querySelector('input[name="task"]');
            newInput.focus();

            // Attach event listeners to the new elements
            const priorityWrapper = newTask.querySelector(".custom-priority-wrapper");
            setupPriorityMenu(priorityWrapper);

            // Attach form submission handler to the new form
            const newForm = newTask.querySelector(".task-form");
            newForm.addEventListener("submit", handleFormSubmit);
        });
    }

    // Attach form submission handlers to all existing forms
    const taskForms = document.querySelectorAll(".task-form");
    taskForms.forEach((form) => {
        form.addEventListener("submit", handleFormSubmit);
    });

    // Start flip animation for the greeting
    const currentUser = await fetchCurrentUser()
    startFlipAnimation(formatGreeting(currentUser.first_name).toUpperCase());
});
