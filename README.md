# Vigilantae

Vigilantae is a local-first case-review portfolio application. It demonstrates a complete operator workflow for registering U.S. case records, collecting photo-based public reports, reviewing visual similarity, and tracking outcomes on a map.

> This is a demonstration project. It is not connected to law enforcement, emergency services, or any government agency. For an urgent situation, contact the appropriate official service.

## What it does

- Creates local case records with a U.S. city, last-known location, notes, and optional reference photo.
- Accepts photo-only public observations. Video upload is intentionally not supported.
- Detects front-facing faces in uploaded photos and produces an **experimental photo comparison signal** during manual review.
- Ranks leads using transparent, non-biometric clues (city and submitted descriptors) alongside the optional photo signal.
- Links human-reviewed evidence to cases, records the case outcome, and displays city-level markers on a U.S. map.
- Keeps records in a local SQLite file that is never committed to Git.
- Protects the local console with an administrator passphrase that can be changed from Settings.

## Run locally

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py --server.port 8505
```

Open `http://localhost:8505`. On a brand-new local database, sign in with `admin` / `ChangeMe!2026`, then immediately change the passphrase in **Settings**.

## Suggested demo flow

1. Sign in and open **Register case**.
2. Add a case in one of the listed U.S. cities and attach a clear, front-facing reference photo.
3. Open **Public report** and submit a photo-based observation.
4. In **Ranked lead review**, inspect the ranked evidence signals, choose a lead, and confirm a manual decision.
5. Show **Case archive** and **U.S. map** for portfolio screenshots.

The comparison score is not identity confirmation. Treat it as a visual sorting signal only; final decisions remain with the operator. The app supports submitted photos, not live or video tracking.

## Repository checks

```powershell
python scripts/check.py
```

The included GitHub Actions workflow runs the same test suite on pushes and pull requests.

## Local data

Local records, uploaded photos, passwords, and Streamlit settings are excluded through `.gitignore`.

See [THIRD_PARTY.md](THIRD_PARTY.md) for the external components used by this project.
