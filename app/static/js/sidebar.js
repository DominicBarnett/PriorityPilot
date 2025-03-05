// Selects all DOM elements
const toggleButton = document.getElementById('toggle-btn');
const sidebar = document.getElementById('sidebar');
const main = document.querySelector('main');
const dropdownButttons = document.querySelectorAll('.dropdown-btn');

function toggleSidebar() {
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

function toggleSubMenu(button) {
  const subMenu = button.nextElementSibling

  if (!subMenu) return; // If no submenu exists, exit

  if (sidebar.classList.contains('close')) {
    sidebar.classList.remove('close');
    main.style.width = "77vw"; 
  }

  if (subMenu.classList.contains("show")) {
    subMenu.classList.remove("show"); // If already open, close it
  } else {
    closeAllSubMenus(); // Close all other submenus first
    subMenu.classList.add("show"); // Then open this submenu
  }
}

function closeAllSubMenus() {
  Array.from(sidebar.getElementsByClassName('show')).forEach(ul => {
    ul.classList.remove('show')
    ul.previousElementSibling.classList.remove('rotate')
  })
}

function setInitialMainWidth() {
  if (!sidebar || !main) return; // Prevent errors

  main.style.width = sidebar.classList.contains("close") ? "90vw" : "77vw";
}

function initializeSidebar() {
  // Set initial main width
  setInitialMainWidth();
  
  // Set click events
  if (toggleButton) {
    toggleButton.onclick = toggleSidebar;
  }
  
  dropdownButttons.forEach(button => {
    button.onclick = function() {
      toggleSubMenu(this);
    };
  });
  
  // Auto-expand submenus that contain active items
  const activeSubmenuItems = document.querySelectorAll('#sidebar .sub-menu li.active');
  activeSubmenuItems.forEach(item => {
    const parentSubMenu = item.closest('.sub-menu');
    if (parentSubMenu && !parentSubMenu.classList.contains('show')) {
      parentSubMenu.classList.add('show');
    }
  });

  // Auto-rotate dropdown buttons for expanded submenus
  const expandedSubmenus = document.querySelectorAll('#sidebar .sub-menu.show');
  expandedSubmenus.forEach(submenu => {
    const dropdownBtn = submenu.previousElementSibling;
    if (dropdownBtn && dropdownBtn.classList.contains('dropdown-btn')) {
      dropdownBtn.classList.add('rotate');
    }
  });
}


window.onload = initializeSidebar;
