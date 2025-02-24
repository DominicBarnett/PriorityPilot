function initLandingPage() {
  // Cache key elements
  const imageHero = document.querySelector(".image-hero");
  const cloudLeft = document.getElementById("cloud-left");
  const cloudRight = document.getElementById("cloud-right");
  const heroText = document.querySelector(".hero-text");

  // Pin the hero section so it remains visible
  imageHero.style.position = "fixed";
  imageHero.style.top = "0";
  imageHero.style.left = "0";
  imageHero.style.width = "100%";
  imageHero.style.height = "100vh"; // Full viewport height

  // Scroll event handler to animate clouds and fade out hero text
  window.addEventListener("scroll", function() {
    const scrollY = window.scrollY;
    const threshold = 500; // Adjust this threshold based on your design
    const progress = Math.min(scrollY / threshold, 1);

    // Move the clouds horizontally based on scroll progress
    cloudLeft.style.transform = `translateX(${progress * -100}px) translateY(-50%)`;
    cloudRight.style.transform = `translateX(${progress * 100}px) translateY(-50%)`;

    // Once the clouds have reached their farthest positions, fade out the hero text
    // and change the hero container's positioning so the About Us section is revealed.
    if (progress === 1) {
      heroText.classList.add("hero-hidden");
      imageHero.style.position = "relative";
    } else {
      heroText.classList.remove("hero-hidden");
      imageHero.style.position = "fixed";
    }
  });
}

// Call the initialization function
initLandingPage();
