let cloudRight = document.getElementById('cloud-right');
let cloudLeft = document.getElementById('cloud-left');
let imageHero = document.querySelector('.image-hero');

// window.addEventListener('scroll', () => {
//   var value = window.scrollY;
//   cloudRight.style.left = value * 1 + 'px';
//   cloudLeft.style.left = -value * 1 + 'px';
// });

window.addEventListener('scroll', () => {
  let value = window.scrollY;
  let scrollSpeed = 0.15; // Reduced speed for smoother effect
  
  // Move left cloud leftward
  cloudLeft.style.transform = `translateX(${-value * scrollSpeed}px) translateY(-50%)`;
  
  // Move right cloud rightward
  cloudRight.style.transform = `translateX(${value * scrollSpeed}px) translateY(-50%)`;
  
  // Optional: add bounds to limit movement
  if (value * scrollSpeed > 300) {
      value = 300 / scrollSpeed;
  }
});
