// Selects all DOM elements
const toggleButton = document.getElementById('toggle-btn');
const sidebar = document.getElementById('sidebar');
const main = document.querySelector('main');
const dropdownButttons = document.querySelectorAll('.dropdown-btn');

function toggleSidebar(){
  sidebar.classList.toggle('close');
  toggleButton.classList.toggle('rotate');

  const close_sidebar = sidebar.classList.contains('close')

  // Close all submenus when sidebar is collapsed
  if (close_sidebar) {
    main.style.width = "90vw";
    closeAllSubMenus();
  } else {
    main.style.width = "77vw";
  }
}

function toggleSubMenu(button){
  const subMenu = button.nextElementSibling

  if (!subMenu) return; // If no submenu exists, exit

  if (subMenu.classList.contains("show")) {
      subMenu.classList.remove("show"); // If already open, close it
  } else {
      closeAllSubMenus(); // Close all other submenus first
      subMenu.classList.add("show"); // Then open this submenu
  }
}

function closeAllSubMenus(){
  Array.from(sidebar.getElementsByClassName('show')).forEach(ul => {
    ul.classList.remove('show')
    ul.previousElementSibling.classList.remove('rotate')
  })
}

function setInitialMainWidth() {
  if (!sidebar || !main) return; // Prevent errors

  main.style.width = sidebar.classList.contains("close") ? "90vw" : "77vw";
}


// Ensure the main content has the correct width on load
window.onload = function () {
  setInitialMainWidth(); 

  if (toggleBtn) {
      toggleBtn.onclick = toggleSidebar; 
  }

  dropdownButtons.forEach(button => {
      button.onclick = function () {
          toggleSubMenu(this);
      };
  });
};
