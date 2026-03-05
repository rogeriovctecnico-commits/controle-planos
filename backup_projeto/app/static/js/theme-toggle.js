(function () {
  const root = document.documentElement;
  const key = 'theme_pref';
  const saved = localStorage.getItem(key);
  const prefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
  const initial = saved || (prefersLight ? 'light' : 'dark');
  root.setAttribute('data-theme', initial);

  window.toggleTheme = function () {
    const current = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    const sidebarBtn = document.getElementById("sidebarToggle");
    if (sidebarBtn) {
      sidebarBtn.addEventListener("click", () => {
        root.setAttribute('data-theme', current);    // ação
      });
    }


    localStorage.setItem(key, current);
  };

  // opcional: expõe função para atualizar ícone/label
  window.getTheme = () => root.getAttribute('data-theme');
})();