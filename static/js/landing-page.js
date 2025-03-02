document.addEventListener('DOMContentLoaded', () => {
  const cloudLeft = document.querySelector('#cloud-left');
  const cloudRight = document.querySelector('#cloud-right');
  const penguinPlane = document.querySelector('.penguin-plane');
  
  window.addEventListener('scroll', () => {
    let value = window.scrollY;
    let scrollSpeed = 0.1;
    let penguinSpeed = 2;
    
    // Move left cloud leftward
    cloudLeft.style.transform = `translateX(${-value * scrollSpeed}px) translateY(-50%)`;
    
    // Move right cloud rightward
    cloudRight.style.transform = `translateX(${value * scrollSpeed}px) translateY(-50%)`;
    
    // Move plane image
    // penguinPlane.style.transform = `translate(${-value * penguinSpeed}px, -50%)`;
    // let penguinMovement = Math.min(value * penguinSpeed, maxScroll);

    // Bounds to limit movement
    if (value * scrollSpeed > 400) {
        value = 400 / scrollSpeed;
    }
  });
});



