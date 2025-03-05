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

  button.addEventListener("click", (e) => {
    e.stopPropagation();
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
  .then(response =>{
    if (response.ok) {
          // If it's a completion toggle, update UI accordingly
          if (form.classList.contains("complete-status-form")) {
            const taskWrapper = form.closest(".today-single-task-wrapper");
            taskWrapper.style.display = "none";
        }
    } else {
        console.error("Error:", data.error);
    }
  })
  .catch(error => console.error("Error:", error));
}

function trackCompleteTaskButton(button) {
    button.addEventListener("click", (event) => {
        event.preventDefault(); // Prevent default form submission

        const taskWrapper = button.closest(".today-single-task-wrapper");
        const taskId = taskWrapper.getAttribute("data-taskId");

        fetch(`/toggle-completion/${taskId}`, { method: "POST" })
            .then((response) => {
                if (response.ok) {
                    // Toggle the completion circle
                    const icon = button.querySelector("i");
                    const isCompleting = icon.classList.contains("fa-regular");

                    icon.classList.toggle("fa-regular");
                    icon.classList.toggle("fa-solid");
                    icon.classList.toggle("fa-circle-check");
                    icon.classList.toggle("fa-circle");

                    // Apply strike-through for completed tasks
                    const taskInput = button
                        .closest(".today-single-task-wrapper")
                        .querySelector("input[name='task']");
                    taskInput.classList.toggle("task-completed");

                    // Update task summary
                    const completedTasksToday = document.querySelector(".home-main-tasks-summary h3:nth-child(3)");
                    if (completedTasksToday) {
                        let count = parseInt(completedTasksToday.textContent.split(" ")[0]);

                        // // If we're completing a task, increment; if uncompleting, decrement
                        // if (isCompleting) {
                        //     completedCount += 1;
                        //     overdueCount = Math.max(0, overdueCount - 1); // Decrease overdue count
                        // } else {
                        //     completedCount = Math.max(0, completedCount - 1);
                        //     overdueCount += 1; // Increase overdue count back
                        // }

                        completedTasksToday.textContent = `${count} completed today`;
                    }

                    // Remove the task from the list if completed
                    if (isCompleting) {
                        const taskWrapper = button.closest(".today-single-task-wrapper");
                        taskWrapper.style.display = "none";
                    }
                }
            })
            .catch((error) => console.error("Error:", error));
    });
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

    // In the event listener for completion buttons
    completionButtons.forEach((button) => {
        trackCompleteTaskButton(button)
    });
    

    // Set up priority menus
    const priorityWrappers = document.querySelectorAll(".custom-priority-wrapper");
    priorityWrappers.forEach((wrapper) => {
        setupPriorityMenu(wrapper);
    });

    // Add new task
    const addTaskButton = document.getElementById("add-today-task-button");
    const taskListContainer = document.getElementById("today-all-tasks-wrapper");
  
    addTaskButton.addEventListener("click", function () {
        addNewTaskInput();
    });

    function addNewTaskInput(task = null) {
        const taskElement = document.createElement("div");
        taskElement.classList.add("today-single-task-wrapper");
        taskElement.setAttribute("data-taskId", "None")
    
        taskElement.innerHTML = `
    <div class="today-single-task-left">
      <!-- Completion form (HIDDEN) -->
      <form class="task-form complete-status-form" style="display: none;">
        <button type="submit" class="completion-circle">
          <i class="fa-regular fa-circle"></i>
        </button>
      </form>

      <!-- Task input form -->
      <form class="task-form today-single-task-input-wrapper">
        <input
          name="task"
          value="${task ? task.task : ""}"
          class="${task && task.completed ? "task-completed" : ""}"
          placeholder="Enter task"
        />
        
        <!-- Priority Selection -->
        <div class="custom-priority-wrapper">
          <button class="open-priority-menu" type="button">
            <i class="fa-solid ${getPriorityIcon(task ? task.priority : "low-priority")}"></i>
          </button>
          <ul class="hidden priority-options">
            <li data-value="high-priority">
              <i class="fa-solid fa-plane-circle-exclamation"></i>
            </li>
            <li data-value="medium-priority">
              <i class="fa-solid fa-plane-departure"></i>
            </li>
            <li data-value="low-priority">
              <i class="fa-solid fa-paper-plane"></i>
            </li>
          </ul>
          <input type="hidden" name="priority" value="${task ? task.priority : "low-priority"}" />
        </div>

        <!-- Save button -->
        <button type="submit" class="save-task-btn">Save</button>
      </form>
    </div>

    <!-- Delete form -->
    <form class="task-form" action="/delete_task/${task ? task._id : ""}" method="POST">
      <button type="submit" class="delete-task-btn cancel-task-btn">
        <i class="fa-solid fa-trash"></i>
      </button>
    </form>
        `
        const taskForms = taskElement.querySelectorAll(".task-form");
        taskForms.forEach((form) => {
            form.addEventListener("submit", handleFormSubmit);
        });
    
        ;

        // track priority button click
        const priorityWrapper = taskElement.querySelector(".custom-priority-wrapper");
        setupPriorityMenu(priorityWrapper);
        
        // track complete button click
        const completionButton = taskElement.querySelector(".completion-circle");
        trackCompleteTaskButton(completionButton)

        taskListContainer.prepend(taskElement);
        taskElement.querySelector("[name='task']").focus()
    
        const saveButton = taskElement.querySelector(".save-task-btn");
        const cancelButton = taskElement.querySelector(".cancel-task-btn");
        const taskInput = taskElement.querySelector("[name='task']");
    
        saveButton.addEventListener("click", async function (e) {
            e.preventDefault()
          const taskName = taskInput.value.trim();
          const taskId = taskElement.getAttribute("data-taskId")
          const priorityInput = taskElement.querySelector("[name='priority']");
          const priority = priorityInput.value || "low-priority";

          if (!taskName) return
    
          let response;
          let newTask;
          
          if (taskId !== "None") {
            // Task already exists, update it
            response = await fetch(`/update_task/${taskId}`, {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ task: taskName, priority }),
            });
          } else {
            // New task, create it
            response = await fetch("/add-task", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ task: taskName, priority }),
            });
          }
    
          if (response.ok) {
            newTask = await response.json();
            updateTaskUI(taskElement, newTask);
          } else {
            alert("Failed to save task.");
          }
        });
    
        cancelButton.addEventListener("click", function () {
          taskElement.remove(); // Remove the input field if the user cancels
        });
      }
    
      function updateTaskUI(taskElement, task) {
        taskElement.setAttribute("data-taskId", task._id)
        taskElement.innerHTML = `
    <div class="today-single-task-left">
      <form class="task-form complete-status-form"" action="/toggle-completion/${task._id}" method="POST">
        <button type="submit" class="completion-circle">
          <i class="fa-regular fa-circle"></i>
        </button>
      </form>

      <!-- Task input form -->
      <form class="task-form today-single-task-input-wrapper" action="/update_task/${task._id}" method="POST">
        <input
          name="task"
          value="${task ? task.task : ""}"
        />
        
        <!-- Priority Selection -->
        <div class="custom-priority-wrapper">
          <button class="open-priority-menu" type="button">
            <i class="fa-solid ${getPriorityIcon(task ? task.priority : "low-priority")}"></i>
          </button>
          <ul class="hidden priority-options">
            <li data-value="high-priority">
              <i class="fa-solid fa-plane-circle-exclamation"></i>
            </li>
            <li data-value="medium-priority">
              <i class="fa-solid fa-plane-departure"></i>
            </li>
            <li data-value="low-priority">
              <i class="fa-solid fa-paper-plane"></i>
            </li>
          </ul>
          <input type="hidden" name="priority" value="${task ? task.priority : "low-priority"}" />
        </div>

        <!-- Save button -->
        <button type="submit" class="save-task-btn">Save</button>
      </form>
    </div>

    <!-- Delete form -->
    <form class="task-form" action="/delete_task/${task ? task._id : ""}" method="POST">
      <button type="submit" class="delete-task-btn cancel-task-btn">
        <i class="fa-solid fa-trash"></i>
      </button>
    </form>
        `;
        const taskForms = taskElement.querySelectorAll(".task-form");
        taskForms.forEach((form) => {
            form.addEventListener("submit", handleFormSubmit);
        });    
      }
    
      function getPriorityIcon(priority) {
        if (priority === "high-priority") return "fa-plane-circle-exclamation";
        if (priority === "medium-priority") return "fa-plane-departure";
        return "fa-paper-plane";
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
