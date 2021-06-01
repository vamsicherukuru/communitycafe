!(function($) {
  "use strict";

  // Preloader
  $(window).on('load', function() {
    if ($('#preloader').length) {
      $('#preloader').delay(100).fadeOut('slow', function() {
        $(this).remove();
      });
    }
  });

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }


  // Smooth scroll for the navigation menu and links with .scrollto classes
  var scrolltoOffset = $('#header').outerHeight() - 2;
  $(document).on('click', '.nav-menu a, .mobile-nav a, .scrollto', function(e) {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      if (target.length) {
        e.preventDefault();

        var scrollto = target.offset().top - scrolltoOffset;
        if ($(this).attr("href") == '#header') {
          scrollto = 0;
        }

        $('html, body').animate({
          scrollTop: scrollto
        }, 1500, 'easeInOutExpo');

        if ($(this).parents('.nav-menu, .mobile-nav').length) {
          $('.nav-menu .active, .mobile-nav .active').removeClass('active');
          $(this).closest('li').addClass('active');
        }

        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
          $('.mobile-nav-overly').fadeOut();
        }
        return false;
      }
    }
  });

	/* Toggle sidebar
	-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
     
  $(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
       $('#sidebar').toggleClass('active');
       $(this).toggleClass('active');
    });
  });

  /*--------------------------
    Products Slider
    ------------------*/

    $(document).ready(function () {
      $(".sub > a").click(function() {
          var ul = $(this).next(),
                  clone = ul.clone().css({"height":"auto"}).appendTo(".mini-menu"),
                  height = ul.css("height") === "0px" ? ul[0].scrollHeight + "px" : "0px";
          clone.remove();
          ul.animate({"height":height});
          return false;
      });
         $('.mini-menu > ul > li > a').click(function(){
         $('.sub a').removeClass('active');
         $(this).addClass('active');
      }),
         $('.sub ul li a').click(function(){
         $('.sub ul li a').removeClass('active');
         $(this).addClass('active');
      });
  });

  $( function() {
    $( "#slider-range" ).slider({
      range: true,
      min: 0,
      max: 1000,
      values: [ 190, 728 ],
      slide: function( event, ui ) {
        $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
         var mi = ui.values[0];
              var mx = ui.values[1];
              filterSystem(mi, mx);
      }
    });
    $( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
      " - $" + $( "#slider-range" ).slider( "values", 1 ) );
  } );


  function filterSystem(minPrice, maxPrice) {
      $(".items div.item").hide().filter(function () {
          var price = parseInt($(this).data("price"), 10);
          return price >= minPrice && price <= maxPrice;
      }).show();
  }

   /*--------------------------
    Closed Products Slider
    ------------------*/

  $(document).ready(function () {
    $(".sub > a").click(function() {
        var ul = $(this).next(),
                clone = ul.clone().css({"height":"auto"}).appendTo(".mini-menu"),
                height = ul.css("height") === "0px" ? ul[0].scrollHeight + "px" : "0px";
        clone.remove();
        ul.animate({"height":height});
        return false;
    });
       $('.mini-menu > ul > li > a').click(function(){
       $('.sub a').removeClass('active');
       $(this).addClass('active');
    }),
       $('.sub ul li a').click(function(){
       $('.sub ul li a').removeClass('active');
       $(this).addClass('active');
    });
});
  

    /**
   * ads carousel indicators
   */
  let adsCarouselIndicators = select("#ads-carousel-indicators")
  let adsCarouselItems = select('#adsCarousel .carousel-item', true)

  adsCarouselItems.forEach((item, index) => {
    (index === 0) ?
    adsCarouselIndicators.innerHTML += "<li data-bs-target='#adsCarousel' data-bs-slide-to='" + index + "' class='active'></li>":
      adsCarouselIndicators.innerHTML += "<li data-bs-target='#adsCarousel' data-bs-slide-to='" + index + "'></li>"
  });


  // Activate smooth scroll on page load with hash links
  $(document).ready(function() {
    if (window.location.hash) {
      var initial_nav = window.location.hash;
      if ($(initial_nav).length) {
        var scrollto = $(initial_nav).offset().top - scrolltoOffset;
        $('html, body').animate({
          scrollTop: scrollto
        }, 1500, 'easeInOutExpo');
      }
    }
  });

  // Mobile Navigation
  if ($('.nav-menu').length) {
    var $mobile_nav = $('.nav-menu').clone().prop({
      class: 'mobile-nav d-lg-none'
    });
    $('body').append($mobile_nav);
    $('body').prepend('<button type="button" class="mobile-nav-toggle d-lg-none"><i class="icofont-navigation-menu"></i></button>');
    $('body').append('<div class="mobile-nav-overly"></div>');

    $(document).on('click', '.mobile-nav-toggle', function(e) {
      $('body').toggleClass('mobile-nav-active');
      $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
      $('.mobile-nav-overly').toggle();
    });

    $(document).on('click', '.mobile-nav .drop-down > a', function(e) {
      e.preventDefault();
      $(this).next().slideToggle(300);
      $(this).parent().toggleClass('active');
    });

    $(document).click(function(e) {
      var container = $(".mobile-nav, .mobile-nav-toggle");
      if (!container.is(e.target) && container.has(e.target).length === 0) {
        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
          $('.mobile-nav-overly').fadeOut();
        }
      }
    });
  } else if ($(".mobile-nav, .mobile-nav-toggle").length) {
    $(".mobile-nav, .mobile-nav-toggle").hide();
  }

  // Navigation active state on scroll
  var nav_sections = $('section');
  var main_nav = $('.nav-menu, #mobile-nav');

  $(window).on('scroll', function() {
    var cur_pos = $(this).scrollTop() + 200;

    nav_sections.each(function() {
      var top = $(this).offset().top,
        bottom = top + $(this).outerHeight();

      if (cur_pos >= top && cur_pos <= bottom) {
        if (cur_pos <= bottom) {
          main_nav.find('li').removeClass('active');
        }
        main_nav.find('a[href="#' + $(this).attr('id') + '"]').parent('li').addClass('active');
      }
      if (cur_pos < 300) {
        $(".nav-menu ul:first li:first").addClass('active');
      }
    });
  });

  // Toggle .header-scrolled class to #header when page is scrolled
  $(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
      $('#header').addClass('header-scrolled');
    } else {
      $('#header').removeClass('header-scrolled');
    }
  });

  if ($(window).scrollTop() > 100) {
    $('#header').addClass('header-scrolled');
  }

  // Back to top button
  $(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
      $('.back-to-top').fadeIn('slow');
    } else {
      $('.back-to-top').fadeOut('slow');
    }
  });

  $('.back-to-top').click(function() {
    $('html, body').animate({
      scrollTop: 0
    }, 1500, 'easeInOutExpo');
    return false;
  });

/***
 * Search Bar
 */


/**************
 * Services Section tabs
 */
 $(document).ready(function(){
  $('.searchbar').focus(function(){
      $('.dropdown-content').fadeIn(1000);
  }).focusout(function(){
      $('.dropdown-content').fadeOut(1000);
  });
});
 $(document).ready(function(){    

  //Tabs
  //When page loads...
      $("body .tab_content").addClass('hidden'); //Hide all content
      $("body ul.tabs li:first-child").addClass("active").removeClass('hidden'); //Activate first tab
      $("body .tab_content:first-child").removeClass('hidden'); //Show first tab content
   
      //On Click Event
      $("body ul.tabs li").click(function() {
   
          $(this).siblings().removeClass('active'); //Remove any "active" class
          $(this).addClass('active'); //Add "active" class to selected tab
          $('body .tab_content').addClass('hidden'); //Hide all tab content
   
          var activeTab = $(this).find("a").attr("href"); //Find the href attribute value to identify the active tab + content
          $(activeTab).removeClass('hidden');       //Fade in the active ID content
          $(activeTab).siblings().addClass('hidden');        
          return false;
      });
  //End Tabs
  
  });

  /**
     * Porfolio isotope and filter
     */
    window.addEventListener('load', () => {
      let servicesContainer = select('.services-container');
      if (servicesContainer) {
        let servicesIsotope = new Isotope(servicesContainer, {
          itemSelector: '.services-item',
          layoutMode: 'fitRows'
        });

        let servicesFilters = select('#services-flters li', true);

        on('click', '#services-flters li', function(e) {
          e.preventDefault();
          servicesFilters.forEach(function(el) {
            el.classList.remove('filter-active');
          });
          this.classList.add('filter-active');

          servicesIsotope.arrange({
            filter: this.getAttribute('data-filter')
          });
          aos_init();
        }, true);
      }

    });

    /**
     * Initiate services lightbox
     */
    const servicesLightbox = GLightbox({
      selector: '.portfokio-lightbox'
    });

    /**
     * services details slider
     */
    new Swiper('.services-details-slider', {
      speed: 400,
      autoplay: {
        delay: 5000,
        disableOnInteraction: false
      },
      pagination: {
        el: '.swiper-pagination',
        type: 'bullets',
        clickable: true
      }
    });

  /**
   * Testimonials slider
   */
   (function () {
   "use strict";

   var carousels = function () {
     $(".owl-carousel1").owlCarousel({
       loop: true,
       center: true,
       margin: 0,
       responsiveClass: true,
       nav: false,
       responsive: {
         0: {
           items: 1,
           nav: false
         },
         680: {
           items: 2,
           nav: false,
           loop: false
         },
         1000: {
           items: 3,
           nav: true
         }
       }
     });
   };

   (function ($) {
     carousels();
   })(jQuery);
 })();



  // Porfolio isotope and filter
  $(window).on('load', function() {
    var servicesIsotope = $('.services-container').isotope({
      itemSelector: '.services-item'
    });

    $('#services-flters li').on('click', function() {
      $("#services-flters li").removeClass('filter-active');
      $(this).addClass('filter-active');

      servicesIsotope.isotope({
        filter: $(this).data('filter')
      });
      aos_init();
    });

    // Initiate venobox (lightbox feature used in portofilo)
    $(document).ready(function() {
      $('.venobox').venobox({
        'share': false
      });
    });
  });

  // services details carousel
  $(".services-details-carousel").owlCarousel({
    autoplay: true,
    dots: true,
    loop: true,
    items: 1
  });

  // Init AOS
  function aos_init() {
    AOS.init({
      duration: 1000,
      once: true
    });
  }
  $(window).on('load', function() {
    aos_init();
  });

})(jQuery);

function myFunction() {

$(".message").text("Link Copied");
}


var $item = $('.carousel-item'); 
var $wHeight = $(window).height();
$item.eq(0).addClass('active');
$item.height($wHeight); 
$item.addClass('full-screen');

$('.carousel img').each(function() {
  var $src = $(this).attr('src');
  var $color = $(this).attr('data-color');
  $(this).parent().css({
    'background-image' : 'url(' + $src + ')',
    'background-color' : $color
  });
  $(this).remove();
});

$(window).on('resize', function (){
  $wHeight = $(window).height();
  $item.height($wHeight);
});

$('.carousel').carousel({
  interval: 6000,
  pause: "false"
});

/* Toggle sidebar
     -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
     function openNav() {
      document.getElementById("mySidepanel").style.width = "250px";
    }
    
    function closeNav() {
      document.getElementById("mySidepanel").style.width = "0";
    }