# Course Project

A Flask application for the final course project.

## Set up

From this directory, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies and run the app. On first startup, the application creates
the five Phase 1 tables in `instance/strength_training.db` and seeds them with
sample records (9 or more in each table). It does not create a Users table.

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## GitHub

After creating an empty repository on GitHub, connect it and push this project:

```bash
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git branch -M main
git add .
git commit -m "Set up Flask course project"
git push -u origin main
```
