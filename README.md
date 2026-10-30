# BuildReady Pakistan

A Streamlit launch and tender-readiness guide for construction management consulting firms in Pakistan.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment:
   - Windows PowerShell: `py -m venv .venv` then ` .\.venv\Scripts\Activate.ps1`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the app: `streamlit run app.py`
6. Streamlit prints a local URL, usually `http://localhost:8501`.

## Deploy with GitHub and Streamlit Community Cloud

1. Create or sign in to a GitHub account.
2. Create a **public** repository (or use a private repository if your Streamlit plan supports it) named `buildready-pakistan`.
3. In this folder, initialize Git and push the app files:

   ```bash
   git init
   git add app.py requirements.txt README.md .gitignore
   git commit -m "Add BuildReady Pakistan Streamlit app"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/buildready-pakistan.git
   git push -u origin main
   ```

4. Sign in at [share.streamlit.io](https://share.streamlit.io/) with GitHub and authorize access to the repository.
5. Choose **Create app**, select the repository, branch `main`, and main file path `app.py`.
6. Select **Deploy**. Streamlit installs packages from `requirements.txt` and builds the app.
7. Open the provided `*.streamlit.app` URL. For changes, commit and push to `main`; Streamlit Cloud redeploys from that branch.
8. To change the public URL or visibility, use the app settings in Streamlit Community Cloud. Do not place passwords, API keys, CNICs, bid documents or client data in the repository.

## What the app does

- Provides a step-by-step PEC consulting firm launch roadmap and a document checklist.
- Shows live, future-dated construction/engineering consultancy matches from Federal PPRA on the home page, with official regional procurement portal links.
- Accepts PDF, DOCX, or TXT CVs/portfolios for preliminary keyword matching against live federal tender titles and listing summaries.
- Generates worldwide marketplace search links matched to portfolio experience and includes a freelancing profile and service-planning section.
- Adds fixed LinkedIn searches for Civil Engineer, Project Engineer Civil, Project Manager Civil and Quality Engineer Civil jobs in Pakistan and Saudi Arabia, plus Rozee and Naukrigulf links.
- Helps assess tender registration fit and estimate immediate fee/security cash needs.
- Includes a simple engagement margin planner and low-cash business development ideas.
- Links to official PEC and federal PPRA / EPADS resources.

## Important limitations

The home page accepts PDF, DOCX, and TXT CVs/portfolios for preliminary keyword matching. Text is processed in memory and is not saved by the app. The comparison uses public tender titles and listing summaries; it does not assess formal eligibility or read attached RFP documents.

Freelancing cards create portfolio-matched searches on marketplaces such as Upwork and Freelancer.com. These are live search links, not an imported or verified job feed; apply and verify each listing on the marketplace itself.

The home page provides fixed job searches for Civil Engineer, Project Engineer Civil, Project Manager Civil and Quality Engineer Civil roles in Pakistan and Saudi Arabia. These external links do not use the uploaded CV or portfolio and are not a verified vacancy feed; the app does not download job-advertisement attachments. Open the employer's original advertisement to confirm duties, eligibility, documents and closing date.

This is a guide, not a registration service, legal/tax opinion, or guarantee of selection or income. It does not submit forms or bids. The home-page tender feed reads the first three pages of Federal PPRA consultancy listings, filters titles for construction/engineering terms, and refreshes hourly (or when the user clicks **Refresh tenders**). It does not combine every provincial authority into one feed; use the regional portal links for additional notices. Listings are discovery aids, and the original notice and any corrigenda control. Tender eligibility, fees, bid security, formats and applicable procurement rules are set by the current official requirements and each individual tender. PEC's linked local consultant form contains fee values that may be dated; use the current official voucher amount.
