# Streamlit Chess — Deploy Guide

This repo contains a Streamlit app at `app.py`. Below are quick steps to run locally, build a Docker container, push to a private GitHub repo, and deploy on hosts that support persistent web services.

Prerequisites
- Python 3.10+ or Docker
- Git and a GitHub account (for remote deploy)

Files added
- `requirements.txt` — Python dependencies
- `Dockerfile` — container image for the app

Run locally (quick)
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Run with Docker (local)
```bash
# build
docker build -t streamlit-chess:latest .
# run (maps port 8501)
docker run -p 8501:8501 streamlit-chess:latest
```

Push to GitHub (private repo)
```bash
git init
git add .
git commit -m "Add Streamlit chess app + deployment files"
# create a private repo on GitHub, then:
git remote add origin git@github.com:<your-username>/<your-private-repo>.git
git branch -M main
git push -u origin main
```

Deploy options (private GitHub supported)

- Streamlit Community Cloud (recommended):
  - Connect your GitHub account to Streamlit Cloud and select the private repo and branch. Streamlit reads `requirements.txt` and runs the app automatically.
  - Configure any secrets/environment variables in the Streamlit Cloud dashboard.

- Render / Fly / Railway (containers or native):
  - Connect GitHub and allow access to the private repo. Use `Dockerfile` (recommended) or have the platform run `pip install -r requirements.txt` and `streamlit run app.py`.

- If you must use Vercel: not recommended — Vercel is serverless and not suitable for long‑running Streamlit processes. You would need a container host instead.

Notes
- If your repo is private, grant the deployment platform access to the repo via the OAuth flow in the platform dashboard.
- For environment variables or secrets (API keys), set them in the deployment platform’s secrets/settings — do NOT commit secrets to the repo.

If you want, I can:
- create a Git commit for you here, or
- walk through connecting the private repo to Streamlit Cloud or Render step-by-step.
