$(document).ready(function() {
    // Enable hover for all dropdowns
    $('.dropdown').hover(function() {
      $(this).find('.dropdown-menu').first().stop(true, true).slideDown();
    }, function() {
      $(this).find('.dropdown-menu').first().stop(true, true).slideUp();
    });

    // Handle submenus specifically to avoid being closed inadvertently
    $('.dropdown-submenu').hover(function() {
      $(this).children('.dropdown-menu').stop(true, true).slideDown();
    }, function() {
      $(this).children('.dropdown-menu').stop(true, true).slideUp();
    });
});