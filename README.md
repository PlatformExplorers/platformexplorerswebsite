# Platform Explorers website

Official website: https://platformexplorers.com

This repository contains the static website for Platform Explorers, a registered nonprofit company in Ireland. It includes the homepage, About us, Contact, and Partner with us pages.

## GitHub Pages

The website files are at the repository root. For branch-based publishing, use the `main` branch and `/(root)` as the Pages publishing source. Keep the custom domain set to `platformexplorers.com` in repository Settings > Pages. The root CNAME file contains the same domain. No build or package installation is needed.

`.nojekyll` tells Pages to serve the static files directly.

## Preview

Run `python -m http.server 8080` from this repository and open http://localhost:8080.

## Editing

- `index.html`, `home.css`: homepage
- `about.html`, `about.css`: About us and team/mentor cards
- `contact.html`, `contact.css`: email, Discord, and social profiles
- `partners.html`, `partners.css`: partnership opportunities
- `styles.css`, `script.js`: shared styles and mobile navigation
- `assets/`: logo, portraits, and placeholder assets

Keep the existing relative links so pages and assets work on GitHub Pages. Canonical URLs and the sitemap use https://platformexplorers.com.
