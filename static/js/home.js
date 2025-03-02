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
    // Look for the hidden input in the parent form rather than directly in the wrapper
    const hiddenInput = wrapper.closest('.task-form').querySelector('input[type="hidden"][name="priority"]');
  
    if (!button || !priorityMenu) {
      console.error("Button or priority menu not found within wrapper:", wrapper);
      return;
    }
    
    if (!hiddenInput) {
      console.error("Hidden input for priority not found - looking in parent form of:", wrapper);
      return;
    }
  
    button.addEventListener("click", (e) => {
      e.stopPropagation(); // Stop event from bubbling up
      console.log("Priority button clicked"); // Debug log
      priorityMenu.classList.toggle("hidden");
    });
  
    priorityMenu.querySelectorAll("li").forEach((option) => {
      option.addEventListener("click", (e) => {
        e.stopPropagation(); // Stop event from bubbling up
        const selectedPriority = option.dataset.value;
        console.log(`Priority selected: ${selectedPriority}`); // Debug log
  
        // Update the button icon
        button.innerHTML = option.innerHTML;
        
        // Update the hidden input value
        hiddenInput.value = selectedPriority;
        
        // Hide the menu
        priorityMenu.classList.add("hidden");
      });
    });
  
    // Close priority menu when clicking elsewhere
    document.addEventListener("click", () => {
      priorityMenu.classList.add("hidden");
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

    // Try to get the username from the page, or fall back to the provided name
    const username = document.querySelector('.user-name')?.textContent?.trim() || name;
    return `${greeting} ${username}`;
}

// Function to handle form submission asynchronously
function handleFormSubmit(event) {
    event.preventDefault();  // Prevent default form submission
  
    const form = event.target;
    const formData = new FormData(form);
    
    console.log("Submitting form:", form.action, form.method);
    
    // Log form data for debugging
    for (let [key, value] of formData.entries()) {
      console.log(`${key}: ${value}`);
    }
  
    fetch(form.action, {
      method: form.method,
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          console.log("Form submission successful");
          window.location.reload();  // Reload the page to reflect changes
        } else {
          console.error("Error:", response.statusText);
        }
      })
      .catch((error) => console.error("Error:", error));
}
  
// Function to toggle task completion
function toggleTaskCompletion(taskId) {
    console.log("Toggling completion for task:", taskId);
    
    fetch(`/toggle-completion/${taskId}`, { 
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        }
    })
    .then((response) => {
        if (response.ok) {
            console.log("Task completion toggled successfully");
            window.location.reload();  // Reload the page to reflect changes
        } else {
            console.error("Error toggling task completion:", response.statusText);
        }
    })
    .catch((error) => console.error("Error toggling task completion:", error));
}

// DOMContentLoaded event listener - MAIN EVENT HANDLER
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM loaded - initializing task management");
    
    // Set today's date
    const dateHeader = document.getElementById("todays-date-header");
    if (dateHeader) {
        dateHeader.textContent = formatDate();
    }
    
    // Attach event listeners to task forms for submission
    document.querySelectorAll(".task-form").forEach((form) => {
        form.addEventListener("submit", handleFormSubmit);
    });
    
    // Attach event listeners to completion circles
    document.querySelectorAll(".completion-circle").forEach((circle) => {
        circle.addEventListener("click", (event) => {
            event.preventDefault();
            const taskId = circle.dataset.taskId;
            if (taskId) {
                toggleTaskCompletion(taskId);
            } else {
                console.error("No task ID found on completion circle");
            }
        });
    });

    // Set up priority menus
    document.querySelectorAll(".custom-priority-wrapper").forEach((wrapper) => {
        setupPriorityMenu(wrapper);
    });

    // Add new task button functionality
    const addTodayTaskButton = document.getElementById("add-today-task-button");
    if (addTodayTaskButton) {
        addTodayTaskButton.addEventListener("click", () => {
            const todayTasks = document.querySelector(".today-all-tasks-wrapper");
            const newTask = document.createElement("div");
            newTask.classList.add("today-single-task-wrapper");
            
            // Create a unique temporary ID for this new task element
            const tempId = 'new-task-' + Date.now();
            newTask.id = tempId;
            
            newTask.innerHTML = `
                <i class="fa-regular fa-circle completion-circle"></i>
                <form class="task-form" action="/add-task" method="POST">
                    <input name="task" value="" placeholder="Enter your task..." />
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
                <button class="delete-task-btn temp-delete"><i class="fa-solid fa-trash"></i></button>`;

            todayTasks.appendChild(newTask);
            const newInput = newTask.querySelector('input[name="task"]');
            newInput.focus();

            // Set up the priority menu
            const priorityWrapper = newTask.querySelector(".custom-priority-wrapper");
            setupPriorityMenu(priorityWrapper);

            // Add form submission handler
            const newForm = newTask.querySelector(".task-form");
            newForm.addEventListener("submit", handleFormSubmit);
            
            // Add handler for the temporary delete button
            const tempDeleteBtn = newTask.querySelector('.temp-delete');
            if (tempDeleteBtn) {
                tempDeleteBtn.addEventListener('click', () => {
                    newTask.remove();
                    updateTaskCount();
                });
            }

            // Update task count
            updateTaskCount();
        });
    }

    // Helper function to update task count
    function updateTaskCount() {
        const todayTaskCount = document.getElementById("total-task-count");
        const taskCount = document.querySelectorAll(".today-single-task-wrapper").length;
        if (todayTaskCount) {
            todayTaskCount.textContent = taskCount;
        }
    }

    // Start flip animation for the greeting - extract username if possible
    const username = document.querySelector("meta[name='username']")?.content || "User";
    startFlipAnimation(formatGreeting(username).toUpperCase());
});