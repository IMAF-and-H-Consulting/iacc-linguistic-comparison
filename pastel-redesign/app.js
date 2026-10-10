const input = document.querySelector('#term-search');
const terms = [...document.querySelectorAll('.term-list li')];
const status = document.querySelector('#search-status');
input.addEventListener('input', () => {
  const query = input.value.trim().toLowerCase();
  let shown = 0;
  for (const term of terms) {
    const match = term.dataset.term.includes(query);
    term.hidden = !match;
    if (match) shown += 1;
  }
  status.textContent = query ? `${shown} matching term${shown === 1 ? '' : 's'}.` : 'Showing all sample terms.';
});

const anchors = [...document.querySelectorAll('.chapter-rail a')];
const sections = anchors.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
const observer = new IntersectionObserver(entries => {
  const visible = entries.filter(e => e.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
  if (!visible) return;
  for (const anchor of anchors) anchor.classList.toggle('active', anchor.getAttribute('href') === `#${visible.target.id}`);
}, { rootMargin: '-20% 0px -65% 0px', threshold: [0, .1, .4] });
sections.forEach(section => observer.observe(section));
