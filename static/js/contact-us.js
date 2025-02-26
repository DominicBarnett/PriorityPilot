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
