// Visionneuse plein écran d'une série. Sans JavaScript, chaque photo de la grille ouvre simplement sa grande version.
(() => {
  const grille = document.querySelector(".grille");
  if (!grille) return;
  const cases = [...grille.querySelectorAll("a.case")];
  if (!cases.length || typeof HTMLDialogElement === "undefined") return;

  // Les libellés viennent de la page, dans sa langue.
  const libelles = grille.dataset;
  const icone = (d) => `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="${d}"/></svg>`;
  const v = document.createElement("dialog");
  v.className = "visionneuse";
  v.innerHTML = `
    <div class="v-haut"><span class="v-serie"></span><button type="button" class="v-fermer">${icone("M5 5l14 14M19 5L5 19")}</button></div>
    <div class="v-centre">
      <button type="button" class="v-prec">${icone("M15 4l-8 8 8 8")}</button>
      <figure><img alt=""></figure>
      <button type="button" class="v-suiv">${icone("M9 4l8 8-8 8")}</button>
    </div>
    <div class="v-bas"><span class="v-titre"></span><span class="v-compte" aria-live="polite"></span></div>`;
  document.body.append(v);

  const img = v.querySelector("img");
  const prec = v.querySelector(".v-prec");
  const suiv = v.querySelector(".v-suiv");
  v.setAttribute("aria-label", libelles.visionneuse || "");
  v.querySelector(".v-fermer").setAttribute("aria-label", libelles.fermer || "");
  prec.setAttribute("aria-label", libelles.precedente || "");
  suiv.setAttribute("aria-label", libelles.suivante || "");
  v.querySelector(".v-serie").textContent = libelles.serie || "";
  let rang = 0;

  const precharger = (i) => {
    const a = cases[i];
    if (!a) return;
    const p = new Image();
    p.sizes = "100vw";
    p.srcset = a.dataset.srcset;
  };

  const montrer = (i) => {
    rang = Math.max(0, Math.min(cases.length - 1, i));
    const a = cases[rang];
    img.removeAttribute("src");
    img.sizes = "100vw";
    img.srcset = a.dataset.srcset;
    img.src = a.href;
    img.alt = a.dataset.alt || "";
    v.querySelector(".v-titre").textContent = a.dataset.titre || "";
    v.querySelector(".v-compte").textContent = `${rang + 1} / ${cases.length}`;
    prec.disabled = rang === 0;
    suiv.disabled = rang === cases.length - 1;
    history.replaceState(null, "", `#${rang + 1}`);
    precharger(rang + 1);
    precharger(rang - 1);
  };

  const ouvrir = (i) => {
    montrer(i);
    if (!v.open) v.showModal();
  };

  v.addEventListener("close", () => {
    history.replaceState(null, "", location.pathname + location.search);
    cases[rang].focus({ preventScroll: true });
    cases[rang].scrollIntoView({ block: "nearest" });
  });

  cases.forEach((a, i) => a.addEventListener("click", (e) => {
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    e.preventDefault();
    ouvrir(i);
  }));

  v.querySelector(".v-fermer").addEventListener("click", () => v.close());
  prec.addEventListener("click", () => montrer(rang - 1));
  suiv.addEventListener("click", () => montrer(rang + 1));
  // Un clic hors de la photo et des boutons ferme la visionneuse.
  v.querySelector(".v-centre").addEventListener("click", (e) => {
    if (e.target.closest("button") || e.target === img) return;
    v.close();
  });

  v.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") { e.preventDefault(); montrer(rang - 1); }
    else if (e.key === "ArrowRight") { e.preventDefault(); montrer(rang + 1); }
    else if (e.key === "Home") { e.preventDefault(); montrer(0); }
    else if (e.key === "End") { e.preventDefault(); montrer(cases.length - 1); }
  });

  // Balayage horizontal sur écran tactile.
  let depart = null;
  v.addEventListener("touchstart", (e) => {
    if (e.touches.length === 1) depart = { x: e.touches[0].clientX, y: e.touches[0].clientY };
  }, { passive: true });
  v.addEventListener("touchend", (e) => {
    if (!depart) return;
    const dx = e.changedTouches[0].clientX - depart.x;
    const dy = e.changedTouches[0].clientY - depart.y;
    depart = null;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) montrer(rang + (dx < 0 ? 1 : -1));
  });

  // Lien direct vers une photo : /la-rue-en-france/#5
  const m = location.hash.match(/^#(\d+)$/);
  if (m) {
    const i = parseInt(m[1], 10) - 1;
    if (i >= 0 && i < cases.length) ouvrir(i);
  }
})();
