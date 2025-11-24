// mobile menu toggle
document.addEventListener('DOMContentLoaded', function () {
  const menuToggle = document.getElementById('menuToggle');
  const mobileNav = document.getElementById('mobileNav');
  if (menuToggle) {
    menuToggle.addEventListener('click', () => {
      mobileNav.classList.toggle('open');
    });
  }

  // Small form client validation (prevent default submit if invalid)
  const forms = document.querySelectorAll('form[novalidate]');
  forms.forEach(form => {
    form.addEventListener('submit', (e) => {
      const invalid = [...form.querySelectorAll('input')].some(i => !i.checkValidity());
      if (invalid) {
        e.preventDefault();
        // simple shake + flash
        form.classList.remove('shake');
        // reflow
        void form.offsetWidth;
        form.classList.add('shake');
      }
    });
  });
});
