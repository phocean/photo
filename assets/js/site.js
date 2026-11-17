// Réglages du visiteur : thème clair / sombre et langue.
(() => {
  const racine = document.documentElement;

  // Thème. Sans choix du visiteur, le site suit le réglage du système.
  const bouton = document.querySelector(".bouton-theme");
  if (bouton) {
    const systemeSombre = window.matchMedia("(prefers-color-scheme: dark)");
    const actuel = () => racine.dataset.theme || (systemeSombre.matches ? "sombre" : "clair");
    const etiqueter = () => {
      const texte = actuel() === "sombre" ? bouton.dataset.versClair : bouton.dataset.versSombre;
      bouton.setAttribute("aria-label", texte);
      bouton.title = texte;
    };
    bouton.addEventListener("click", () => {
      const suivant = actuel() === "sombre" ? "clair" : "sombre";
      racine.dataset.theme = suivant;
      try { localStorage.setItem("theme", suivant); } catch (e) { /* navigation privée : le choix vaut pour la page */ }
      etiqueter();
    });
    systemeSombre.addEventListener("change", etiqueter);
    etiqueter();
    bouton.hidden = false;
  }

  // Langue : un choix explicite dans le sélecteur l'emporte ensuite sur la langue du navigateur.
  document.querySelectorAll(".langues a[data-langue]").forEach((lien) => {
    lien.addEventListener("click", () => {
      try { localStorage.setItem("langue", lien.dataset.langue); } catch (e) { /* le lien suffit */ }
    });
  });
})();
