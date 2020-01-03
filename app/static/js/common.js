$(document).ready(() => {
  $(window).scroll(function () {
    var scroll = $(window).scrollTop();

    if (scroll >= 0) {
      $(".navbar").addClass("navbar-border-bottom");
    }
    if (scroll == 0) {
      $(".navbar").removeClass("navbar-border-bottom");
    }
  });
});

function openNav() {
  document.getElementById("myNav").style.height = "100%";
}

function closeNav() {
  document.getElementById("myNav").style.height = "0%";
}
