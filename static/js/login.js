document.addEventListener("DOMContentLoaded", function () {
  let cloud1 = document.createElement("img");
  cloud1.src = "/static/images/cloud-gif.gif";
  cloud1.id = "cloud1";
  cloud1.classList.add("cloud");

  let lastMouseEntry = null;

  // Show the cloud when the mouse enters the screen
  document.addEventListener("mouseenter", function () {
    document.body.appendChild(cloud1);
  });

  document.addEventListener("mousemove", function (event) {
    if (!cloud1) return;
    let mainDiv = document.getElementById("login-main-content");

    let divRect = mainDiv.getBoundingClientRect();
    let cloudSize = 280;

    let newX = event.clientX + 10;
    let newY = event.clientY + 10;

    // Detect if the mouse enters the div from the left or right
    if (event.clientX < divRect.left) {
      lastMouseEntry = "left";
    } else if (event.clientX > divRect.right) {
      lastMouseEntry = "right";
    }

    // Stop at the left border if coming from the left
    if (
      lastMouseEntry === "left" &&
      newX + cloudSize > divRect.left &&
      newX < divRect.right
    ) {
      newX = divRect.left - cloudSize;
    }

    // Stop at the right border if coming from the right
    if (
      lastMouseEntry === "right" &&
      newX < divRect.right &&
      newX + cloudSize > divRect.left
    ) {
      newX = divRect.right;
    }

    cloud1.style.left = newX + "px";
    cloud1.style.top = newY + "px";
  });

  // Hide the cloud when the mouse leaves the screen
  document.addEventListener("mouseleave", function () {
    cloud1.remove();
  });
});
