// Reserved for future interaction (search, login detection, etc.)
console.log("BitByte frontend loaded.");


// Hamburger Nav Menu
  const hamburger = document.querySelector('.hamburger');
  const navMenu = document.querySelector('nav');

  hamburger?.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
  });




function filterItems() {
  const input = document.getElementById("searchBar").value.toLowerCase();
  const cards = document.getElementById("itemsGrid").children;

  for (let card of cards) {
    const name = card.querySelector("h3").innerText.toLowerCase();
    if (name.includes(input)) {
      card.style.display = "block";
    } else {
      card.style.display = "none";
    }
  }
}


window.addEventListener('DOMContentLoaded', () => {
  const notif = document.getElementById('notification');
  if (notif) {
    setTimeout(() => {
      notif.remove();
    }, 15000); // 15 seconds
  }
});
