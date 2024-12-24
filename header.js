let menu = document.querySelector("#menu");
let menulist = document.querySelector("#menuList");
let close = document.querySelector("#close");

menu.addEventListener("click", () => {
    menulist.classList.remove("translate-y-[-300%]");
    menulist.classList.add("translate-y-[-96px]");
})
close.addEventListener("click", () => {
    menulist.classList.add("translate-y-[-300%]");
    menulist.classList.remove("translate-y-[-96px]");
    console.log("close");
})