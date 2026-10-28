# Kavali Harshavardhan — Vercel-ready project portfolio
A responsive, accessible, framework-free HTML/CSS/JavaScript portfolio hosted inside this repository under `portfolio/`. Includes a filterable and searchable catalog of **all 21 repositories**, grounded project summaries, skill clusters, case-study detail panels, GitHub/LinkedIn/contact links, and links to verified demos. **The portfolio itself is a static website, not a live AI inference service.**

## Fast deploy to your Vercel account

[**Open the preconfigured Vercel deploy flow**](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fharshakavali81-collab%2FEnterprise-AI-Intelligence-Platform-Development&project-name=harshavardhan-ai-portfolio&root-directory=portfolio)

The Vercel link pre-fills the GitHub source repository, requested project name, and **root-directory=portfolio**. Sign in to the correct Vercel workspace, confirm the GitHub connection/permissions and deployment settings, then press **Deploy**. The deploy-button flow may offer to create a copy of the repository. If you want to import this *existing* GitHub repository without cloning, use **Add New → Project → Import** in your Vercel dashboard instead, and specify Root Directory `portfolio`.

Use **Other** for Framework Preset, with no build command. The directory intentionally has no `public` folder, so Vercel serves the static files from `.` by default. Production URLs are assigned by Vercel after a successful deployment. Avoid guessing a link from the proposed project name.

After you connect the repository, Vercel automatically creates a deployment on new commits to `main` by default. The project is a static portfolio; Python ML/Streamlit backends and databases are not deployed with it.

## Deploy to Vercel
1. Create your Vercel account at https://vercel.com/signup (choose **Continue with GitHub**).
2. On Vercel choose **Add New → Project**, grant GitHub repository access, and import `harshakavali81-collab/Enterprise-AI-Intelligence-Platform-Development`.
3. Set **Root Directory** to `portfolio` (this is important; the repository root contains another application).
4. Set **Framework Preset** to **Other**. No install command and no build command are needed. Serve files directly from the selected root; leave Output Directory at the default.
5. Name the Vercel project `harshavardhan-ai-portfolio` if the name is available. Click **Deploy**.
6. Copy the actual production URL shown by Vercel; the suggested name does **not** guarantee a specific `*.vercel.app` URL. For automatic updates, keep GitHub integration enabled.

## Local preview
Open `portfolio/index.html` in a browser, or run `python -m http.server 4173 --directory portfolio` from the repository root, then visit http://localhost:4173.

## Project demos
- `demos/banking/`: mirror of the **static, synthetic-data** Banking Analytics HTML dashboard already committed in its original repository.
- `demos/marketing/`: mirror of the **static, synthetic-data** Marketing ROI HTML dashboard already committed in its original repository.
- Customer Churn's already-published browser companion is linked externally, not copied.
- Other AI/ML repositories link to verified GitHub source; their Python backends, models, databases, external APIs or worker processes are not silently claimed to run on Vercel.

## Maintenance
- Edit `script.js` to adjust the 21-project list, categories, details, links and demo paths.
- Edit `style.css` for styles, or `index.html` for section content.
- Do not add API secrets to these static files; use Vercel environment variables for future server-side features.
- The portfolio shows email and public social links intentionally; no phone number is published.
- Do not claim production certification, commercial outcomes, or real-world results for synthetic/demo projects.

## Notes on data and claims
GitHub repository names and descriptions were checked on October 28, 2026. Any reference to completed projects means portfolio code/documentation exists, not that every project is deployed publicly. The site is dependency-free and can be hosted on other static hosts as well.
