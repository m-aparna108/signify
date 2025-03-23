/*====== MENU =====*/ 

const showMenu = (toggleId, navId) => { 

    const toggle = document.getElementById(toggleId), 

        nav = document.getElementById(navId); 

 

    if (toggle && nav) { 

        toggle.addEventListener('click', () => { 

            nav.classList.toggle('show'); 

        }); 

    } 

}; 

showMenu('nav-toggle', 'nav-menu'); 

 

/*====== RELLAX (PARALLAX EFFECT) =====*/ 

document.addEventListener("DOMContentLoaded", function () { 

    var rellax = new Rellax('.parallax', { 

        speed: -3, 

        center: true, 

        wrapper: null 

    }); 

}); 

 

/*====== ANIMATE GSAP =====*/ 

gsap.from('.nav__logo', { opacity: 0, duration: 3, delay: 0.5, y: 30, ease: 'expo.out' }); 

gsap.from('.nav__toggle', { opacity: 0, duration: 3, delay: 0.7, y: 30, ease: 'expo.out' }); 

gsap.from('.nav__item', { opacity: 0, duration: 3, delay: 0.7, y: 35, ease: 'expo.out', stagger: 0.2 }); 

 

/*====== SCROLL REVEAL SECTION =====*/ 

const sr = ScrollReveal({ 

    duration: 2500, 

    reset: true 

}); 

 

sr.reveal('.content', { origin: 'bottom', distance: '50px', delay: 200 }); 

 

 