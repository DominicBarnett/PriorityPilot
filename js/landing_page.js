let cloudRight = document.getElementById('cloud-right');
let cloudLeft = document.getElementById('cloud-left');
let imageHero = document.querySelector('.image-hero');

window.addEventListener('scroll', () => {
  var value = window.scrollY;
  cloudRight.style.left = value * 0.5 + 'px';
  cloudLeft.style.right = value * 0.5 + 'px';
});
