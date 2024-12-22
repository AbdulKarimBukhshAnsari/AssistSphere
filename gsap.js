gsap.from("a", {
    opacity: 0,
    delay: 0.5,
    duration: 1, 
    x: 100,
    stagger: 0.3
});
gsap.from(".bannerText", {
    opacity: 0,
    delay: 0.5,
    duration: 1, 
    y: 100,
    stagger: 0.3
});
gsap.from("#info1", {
    opacity: 0,
    delay: 0.5,
    duration: 1, 
    y: 100,
    stagger: 0.3
});
gsap.from("#info2", {
    opacity: 0,
    duration: 1, 
    delay: 0.5,
    y: 100,
    scrollTrigger: "#info2",
});