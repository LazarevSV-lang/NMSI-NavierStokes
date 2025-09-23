# Release Checklist – NMSI–π*–γ_diss–e

## Pre-release
- [ ] Actualizează `README.md` cu ultimele rezultate și badge-uri de workflow
- [ ] Rulează toate **GitHub Actions** workflows (`notebooks`, `2D demo`, `3D TGV`) – toate trebuie să fie **green**
- [ ] Verifică că `.gitignore` este actualizat și exclude artefactele numerice și grafice
- [ ] Curăță folderele de output (`out_2d/`, `out_3d/`, `artifacts/`, `runs/`) din repo

## Tagging
- [ ] Creează un nou **tag semantic**: `vX.Y.Z`
- [ ] Descrie modificările în **Release Notes**

## Packaging
- [ ] Integrează documentele EN (`.docx`) și notebook-urile în folderul `docs/` sau `notebooks/`
- [ ] Atașează pachetul ZIP (cu docs + notebook) la pagina Release

## Publication
- [ ] Publică release-ul pe GitHub
- [ ] Postează anunțul pe X/Twitter cu link la Release
- [ ] Opțional: trimite DOI update la Zenodo pentru această versiune
