// Select all DOM elements that have class input from contact-us.js
const inputs = document.querySelectorAll(".input");

// When a user clicks or tabs into the input field
function focusFunc() {
  // this - refers to the input element that received focus.
  // which retrieves the element's parent node and stores it in a variable
  let parent = this.parentNode;
  // add CSS class  called "focus"
  parent.classList.add("focus");
}

function blurFunc() {
  let parent = this.parentNode;
  if (this.value == "") {
    parent.classList.remove("focus");
  }
}

inputs.forEach((input) => {
  input.addEventListener("focus", focusFunc);
  input.addEventListener("blur", blurFunc);
});

// On page load, if an input has a value, add the "focus" class to its parent
inputs.forEach((input) => {
  if (input.value.trim() !== "") {
    input.parentNode.classList.add("focus");
  }
});

// Function to display a flash message at the top of the page
function showFlashMessage(message, duration = 3000, type = "success") {
  // Remove any existing flash message
  const existingFlash = document.querySelector(".flash-message");
  if (existingFlash) {
    existingFlash.remove();
  }

  // Create the flash message element
  const flash = document.createElement("div");
  flash.className = "flash-message " + type; // Use type to determine styling (success or error)
  flash.textContent = message;

  // Prepend the flash message to the body
  document.body.prepend(flash);

  // After the specified duration, remove the flash message and reload the page
  setTimeout(() => {
    flash.remove();
    location.reload();
  }, duration);
}

// Validate required fields and display flash messages accordingly
function validateAndSend() {
  const fullName = document.querySelector('input[name="name"]').value.trim();
  const email = document.querySelector('input[name="email"]').value.trim();
  const message = document.querySelector('textarea[name="message"]').value.trim();

  if (!fullName || !email || !message) {
    showFlashMessage("Please fill out all required fields: Full Name, Email, and Message.", 3000, "error");
    return;
  }

  showFlashMessage("Thank you for reaching out. Our team is processing your inquiry and will get back to you as soon as possible.", 3000, "success");
}

document.getElementById("send-button").addEventListener("click", validateAndSend);
