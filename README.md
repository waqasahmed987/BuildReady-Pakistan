# BuildReady Pakistan

A Streamlit launch and tender-readiness guide for construction management consulting firms in Pakistan.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment.

   Windows PowerShell:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   macOS or Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install the app dependency:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   streamlit run app.py
   ```

6. Open the local URL printed in your terminal, usually `http://localhost:8501`.

## Deploy with GitHub and Streamlit Community Cloud

1. Create or sign in to a GitHub account.
2. Create a repository named `buildready-pakistan`.
3. Open a terminal in this project folder and run these commands. Replace `YOUR-USERNAME` with your GitHub username.

   ```bash
   git init
   git add app.py requirements.txt README.md .gitignore
   git commit -m "Add BuildReady Pakistan Streamlit app"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/buildready-pakistan.git
   git push -u origin main
   ```

4. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub.
5. Authorize Streamlit to access your repository.
6. Choose **Create app**.
7. Select your repository, the `main` branch, and `app.py` as the main file.
8. Click **Deploy**.
9. Open the Streamlit app URL provided after deployment.
10. To publish updates, commit and push them to GitHub. Streamlit Community Cloud updates the deployed app from the repository.

Do not add passwords, API keys, CNICs, bid documents, or client information to the GitHub repository.

## What the app does

- Provides a PEC consulting firm launch roadmap.
- Displays a PEC document checklist.
- Helps assess tender registration fit and estimated fee/security cash needs.
- Includes a basic engagement margin planner.
- Links to official PEC, PPRA, and EPADS resources.

## Limitations

This app is a planning guide. It does not submit PEC applications or tenders, provide legal or tax advice, or guarantee registration, eligibility, selection, or revenue.

Tender requirements are set by current official rules and the individual tender documents. PEC's linked local consultant form may contain outdated fee figures, so confirm the current amount through PEC's official portal or voucher. Check provincial procurement requirements separately.
