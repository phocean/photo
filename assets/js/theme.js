// Bouton clair / sombre. Sans choix du visiteur, le site suit le réglage du système.
(() => {
  const bouton = document.querySelector(".bouton-theme");
  if (!bouton) return;
  const racine = document.documentElement;
  const systemeSombre = window.matchMedia("(prefers-color-scheme: dark)");
  const actuel = () => racine.dataset.theme || (systemeSombre.matches ? "sombre" : "clair");
  const etiqueter = () => {
    const texte = actuel() === "sombre" ? "Passer en thème clair" : "Passer en thème sombre";
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
})();
