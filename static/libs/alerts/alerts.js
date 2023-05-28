const alertsContainer = document.querySelector(".alerts");
alertsContainer.addEventListener("click", ({target}) => {
  if (target.classList.contains("alert__close")) {
    const alertElement = target.parentNode;
    alertElement.classList.add("alert-fade");
    alertElement.addEventListener("animationend", () => {
      alertElement.remove();
      if (alertsContainer.children.length === 0) {
        alertsContainer.remove();
      }
    });
  }
});