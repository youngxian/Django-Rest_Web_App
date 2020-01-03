var carousels = function () {
  $(".owl-carousel1").owlCarousel({
    loop: true,
    center: true,
    margin: 0,
    responsiveClass: true,
    nav: true,
    responsive: {
      0: {
        items: 1,
        nav: false,
      },
      800: {
        items: 2,
        nav: false,
        loop: false,
      },
      1000: {
        items: 3,
        nav: true,
      },
    },
    navText: [
      '<span class="left-icon"><img src="../../static/images/carsoul-left.svg"/></span>',
      '<span class="right-icon"><img src="../../static/images/carsoul-right.svg"/></span>',
    ],
  });
};

var hideDiv = () => {
  $(".logged-in-section-create").fadeOut(1000, function () {
    $(".logged-in-section-hidden").fadeIn(800);
  });
};
