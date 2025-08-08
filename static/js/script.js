// Reserved for future interaction (search, login detection, etc.)
console.log("BitByte frontend loaded.");

// Hamburger Nav Menu
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('nav');

hamburger?.addEventListener('click', () => {
  hamburger.classList.toggle('active');
  navMenu.classList.toggle('active');
});

// Filter function for search (your original)
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

// On DOM content loaded: notification fade & feature cards fade-in
window.addEventListener('DOMContentLoaded', () => {
  const notif = document.querySelector('.notification');
  if (notif) {
    setTimeout(() => {
      notif.classList.add('hide');
      setTimeout(() => notif.remove(), 1000); // wait for fade-out
    }, 15000);
  }

  // Animate feature cards fade-in
  const cards = document.querySelectorAll('.feature-card');
  cards.forEach(card => {
    card.classList.add('visible');
  });
});
