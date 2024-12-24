
// swiper JS
const swiper = new Swiper('.swiper', {
    direction: 'horizontal',
    loop: true,
  
    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
    },
  
    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  
});

const sliders = document.querySelectorAll(".sliders");
const slidersAns = document.querySelectorAll(".sliderAns");
sliders.forEach((slider, index) => { 
  slider.addEventListener("click", () => {
        if (slidersAns[index].classList.contains("h-max")) {
            gsap.to(slider.children[1], {
                duration: 0.2,
                delay: 0.2,
                rotate: 0
            });
            slidersAns[index].classList.remove("h-max");
            slidersAns[index].classList.remove("p-4");
            slidersAns[index].classList.add("h-0");
        }
        else {
            gsap.to(slider.children[1], {
                duration: 0.2,
                delay: 0.2,
                rotate: 45
            });
            slidersAns[index].classList.add("h-max");
            slidersAns[index].classList.add("p-4");
            slidersAns[index].classList.remove("h-0");
        }
    })
})