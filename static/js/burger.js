const menuButton = document.querySelector(".burger");
const menu = document.querySelector(".menu");
menuButton.addEventListener("click", () => {
  const expanded = menuButton.getAttribute("aria-expanded") === "true";
  menuButton.setAttribute("aria-expanded", String(!expanded));
  menuButton.classList.toggle("burger_open");
  document.body.classList.toggle("body_lock");
  menu.classList.toggle("menu_open");
});
