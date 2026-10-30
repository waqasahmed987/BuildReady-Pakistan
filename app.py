from datetime import datetime
from io import BytesIO
from urllib.parse import quote_plus
from zoneinfo import ZoneInfo

import requests
import streamlit as st
from bs4 import BeautifulSoup
from docx import Document
from pypdf import PdfReader

st.set_page_config(page_title="BuildReady Pakistan", page_icon="🏗️", layout="wide")

st.title("🏗️ BuildReady Pakistan")
st.caption("A practical launch and tender-readiness guide for construction management consultants")
st.info("This guide is informational. Confirm current forms, fee vouchers, tax obligations, tender terms and provincial rules with PEC, FBR, SECP / the relevant registrar, and the procuring agency before acting.")

PEC = "https://www.pec.org.pk/firm-registration-new/"
CE_PORTAL = "https://ceportal.pec.org.pk/User/SignUp"
CE_FAQ = "https://ceportal.pec.org.pk/User/Faqs"
LOCAL_FORM = "https://www.pec.org.pk/wp-content/uploads/2021/05/Consulting-Engineers-Registration-Form-Local-Consultants.pdf"
BYLAWS = "https://www.pec.org.pk/wp-content/uploads/2024/10/PEC-Consulting-Engr-Bye-laws-1986-amended-upto-MARCH-14-2024.pdf"
PPRA = "https://ppra.gov.pk/"
EPADS = "https://vendors.epads.gov.pk/register"
PPRA_FAQ = "https://ppra.gov.pk/faqs"
FEDERAL_TENDERS = "https://epms.ppra.gov.pk/public/tenders/active-tenders?procurement_category=3"
REGIONAL_PORTALS = {
    "Punjab": "https://ppra.punjab.gov.pk/",
    "Sindh": "https://ppms.pprasindh.gov.pk/PPMS/public/portal/notice-inviting-tender",
    "Khyber Pakhtunkhwa": "https://portalkp.eprocure.gov.pk/#/tenders/Epadtenders",
    "Balochistan": "https://bppqa.vdc.services/",
    "Azad Jammu & Kashmir": "https://www.ajkppra.gov.pk/",
    "Gilgit-Baltistan": "https://gbppra.gov.pk/",
}
RELEVANT_TERMS = (
    "construction", "supervision", "civil", "infrastructure", "building",
    "road", "bridge", "engineering consultant", "design review", "design and",
    "renovation", "architect", "survey", "boq", "feasibility", "urban",
    "project management", "project planning", "water supply", "drainage",
)
PROFILE_SKILLS = {
    "Construction supervision": ("construction supervision", "site supervision", "supervision", "site execution"),
    "Project controls and scheduling": ("primavera", "scheduling", "schedule", "progress reporting", "cash flow", "s-curve", "recovery plan"),
    "Cost, BOQ, and tender support": ("boq", "bill of quantities", "cost estimate", "tender documentation", "tender preparation", "procurement scheduling"),
    "QA/QC and HSE": ("qa/qc", "quality assurance", "quality control", "itp", "inspection request", "hse"),
    "Civil buildings and infrastructure": ("civil works", "building", "high-rise", "infrastructure", "road", "bridge"),
    "Foundations and geotechnical works": ("bored piling", "bored pile", "piling", "diaphragm wall", "ground improvement", "stone column", "cmc", "ric"),
    "Water and energy projects": ("water supply", "wastewater", "hydropower", "power plant", "substation", "solar"),
    "Contract administration and claims": ("contract administration", "eot", "claims", "time impact analysis", "contract administration"),
    "Design and engineering review": ("design review", "engineering design", "design and", "technical design"),
}
FREELANCE_SEARCHES = [
    {
        "title": "Primavera P6 construction scheduling",
        "query": "Primavera P6 construction scheduler project controls",
        "domains": {"Project controls and scheduling"},
        "offer": "Baseline schedules, schedule updates, look-ahead plans, progress reporting, and recovery schedules.",
    },
    {
        "title": "Construction schedule review and project controls",
        "query": "construction schedule review project controls delay analysis",
        "domains": {"Project controls and scheduling", "Construction supervision"},
        "offer": "Schedule health reviews, critical-path checks, progress tracking, and clear review comments.",
    },
    {
        "title": "Construction BOQ and cost-estimation support",
        "query": "construction BOQ quantity takeoff cost estimation tender",
        "domains": {"Cost, BOQ, and tender support", "Civil buildings and infrastructure"},
        "offer": "BOQ review, quantity take-off support, cost tracking, and tender-document coordination.",
    },
    {
        "title": "Civil construction QA/QC documentation",
        "query": "civil construction QA QC documentation ITP method statement",
        "domains": {"QA/QC and HSE", "Civil buildings and infrastructure"},
        "offer": "Inspection records, ITPs, method statements, material-test coordination, and close-out documentation.",
    },
    {
        "title": "Foundation and geotechnical project coordination",
        "query": "foundation piling geotechnical construction project coordination",
        "domains": {"Foundations and geotechnical works"},
        "offer": "Piling and ground-improvement coordination, test planning, and foundation work reporting.",
    },
    {
        "title": "Engineering contract administration and claims support",
        "query": "construction contract administration EOT claims time impact analysis",
        "domains": {"Contract administration and claims"},
        "offer": "Project records, time-impact documentation, EOT support, and contract-administration reporting.",
    },
]


def extract_portfolio_text(uploaded_file):
    """Extract text in memory from a PDF, DOCX, or TXT portfolio file."""
    content = uploaded_file.getvalue()
    suffix = uploaded_file.name.rsplit(".", 1)[-1].lower()
    if suffix == "pdf":
        reader = PdfReader(BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == "docx":
        document = Document(BytesIO(content))
        parts = [paragraph.text for paragraph in document.paragraphs]
        for table in document.tables:
            for row in table.rows:
                parts.append(" ".join(cell.text for cell in row.cells))
        return "\n".join(parts)
    if suffix == "txt":
        return content.decode("utf-8", errors="replace")
    raise ValueError("Please upload a PDF, DOCX, or TXT file.")


def compare_portfolio_to_tender(portfolio_text, tender_text):
    profile = portfolio_text.casefold()
    tender = tender_text.casefold()
    profile_domains = {
        label for label, phrases in PROFILE_SKILLS.items()
        if any(phrase in profile for phrase in phrases)
    }
    tender_domains = {
        label for label, phrases in PROFILE_SKILLS.items()
        if any(phrase in tender for phrase in phrases)
    }
    overlaps = sorted(profile_domains & tender_domains)
    if not tender_domains:
        return 0, overlaps
    score = round(100 * len(overlaps) / len(tender_domains))
    return score, overlaps


def portfolio_skill_domains(portfolio_text):
    profile = portfolio_text.casefold()
    return {
        label for label, phrases in PROFILE_SKILLS.items()
        if any(phrase in profile for phrase in phrases)
    }


def freelance_search_matches(portfolio_text):
    if not portfolio_text.strip():
        return FREELANCE_SEARCHES[:4]
    domains = portfolio_skill_domains(portfolio_text)
    matched = [item for item in FREELANCE_SEARCHES if item["domains"] & domains]
    return matched[:5]


@st.cache_data(ttl=3600, show_spinner=False)
def get_federal_construction_tenders(page_count=3):
    """Read current consultancy-category notices from the official federal PPRA portal."""
    results = []
    session = requests.Session()
    session.headers.update({"User-Agent": "BuildReadyPakistan/1.0 (public tender discovery)"})
    for page in range(1, page_count + 1):
        url = FEDERAL_TENDERS if page == 1 else f"{FEDERAL_TENDERS}&page={page}"
        response = session.get(url, timeout=25)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for row in soup.select("tr"):
            tender_no = row.select_one('td[data-label="Tender No"] strong')
            details_cell = row.select_one('td[data-label="Tender Details"]')
            title_node = details_cell.select_one("strong") if details_cell else None
            closing_cell = row.select_one('td[data-label="Closing"]')
            if not (tender_no and title_node and closing_cell):
                continue
            tender_id = tender_no.get_text(" ", strip=True)
            title = title_node.get_text(" ", strip=True)
            date_node = closing_cell.select_one("strong")
            time_node = closing_cell.select_one("small")
            if not date_node:
                continue
            closing_text = date_node.get_text(" ", strip=True)
            closing_time = time_node.get_text(" ", strip=True) if time_node else "11:59 PM"
            try:
                closing = datetime.strptime(
                    f"{closing_text} {closing_time}", "%b %d, %Y %I:%M %p"
                ).replace(tzinfo=ZoneInfo("Asia/Karachi"))
            except ValueError:
                continue
            if closing <= datetime.now(ZoneInfo("Asia/Karachi")):
                continue
            listing_context = details_cell.get_text(" ", strip=True).casefold() if details_cell else title.casefold()
            if not any(term in listing_context for term in RELEVANT_TERMS):
                continue

            status_cell = row.select_one('td[data-label="Status"]')
            advertised_cell = row.select_one('td[data-label="Advertised"]')
            detail_row = row.find_next_sibling("tr", class_="cb-rt-detail")
            agency = "Federal procuring agency"
            if detail_row:
                agency_node = detail_row.select_one(".cb-rt-grid .cb-rt-dv")
                if agency_node:
                    agency = agency_node.get_text(" ", strip=True)
            action = row.select_one('td[data-label="Actions"] a[href*="tender-details"]')
            notice_url = (
                requests.compat.urljoin("https://epms.ppra.gov.pk", action["href"])
                if action and action.get("href")
                else f"https://epms.ppra.gov.pk/public/tenders/tender-details/{tender_id}"
            )
            results.append({
                "Project / tender": title,
                "Listing summary": details_cell.get_text(" ", strip=True) if details_cell else title,
                "Agency and listed office": agency,
                "Closing (Pakistan time)": closing.strftime("%d %b %Y, %I:%M %p"),
                "Status": status_cell.get_text(" ", strip=True) if status_cell else "Listed",
                "Advertised": advertised_cell.get_text(" ", strip=True) if advertised_cell else "",
                "Tender ID": tender_id,
                "Official notice": notice_url,
                "_closing": closing,
            })
    unique = {item["Tender ID"]: item for item in results}
    return sorted(unique.values(), key=lambda item: item["_closing"])


st.header("Current construction and engineering consultancy tenders")
st.caption(
    "Live matches from the official federal PPRA consultancy list, filtered for "
    "construction, engineering, infrastructure, design, and supervision terms. "
    "Closing dates are shown in Pakistan time."
)
refresh_col, search_col, count_col = st.columns([1, 3, 1])
with refresh_col:
    refresh_tenders = st.button("Refresh tenders", use_container_width=True)
with search_col:
    tender_search = st.text_input("Filter by project, agency, city, or tender ID", key="tender_search")
with count_col:
    tender_limit = st.selectbox("Show", [10, 20, 50], index=1, key="tender_limit")

with st.expander("Upload a CV or portfolio to find matching tenders", expanded=False):
    st.write(
        "Upload a PDF, DOCX, or TXT file. The app extracts text in memory and compares stated "
        "experience with the tender title and public listing summary. The uploaded file is not saved by the app."
    )
    uploaded_portfolio = st.file_uploader(
        "Portfolio or CV",
        type=["pdf", "docx", "txt"],
        key="portfolio_upload",
    )

portfolio_text = ""
if uploaded_portfolio is not None:
    if uploaded_portfolio.size > 10 * 1024 * 1024:
        st.error("Please upload a file smaller than 10 MB.")
    else:
        try:
            portfolio_text = extract_portfolio_text(uploaded_portfolio)[:200000]
            if portfolio_text.strip():
                st.success("Portfolio text extracted. Tender matching will use only the current listing title and summary.")
            else:
                st.warning("No readable text was extracted. Scanned PDFs may need OCR before upload.")
        except Exception as exc:
            st.error(f"Could not read this file. Please try a valid PDF, DOCX, or TXT document. ({exc})")

if refresh_tenders:
    get_federal_construction_tenders.clear()
    st.rerun()

try:
    with st.spinner("Loading current federal procurement notices…"):
        tender_rows = get_federal_construction_tenders()
    now_pakistan = datetime.now(ZoneInfo("Asia/Karachi"))
    tender_rows = [row for row in tender_rows if row["_closing"] > now_pakistan]
    if portfolio_text.strip():
        for row in tender_rows:
            score, overlaps = compare_portfolio_to_tender(
                portfolio_text,
                f"{row['Project / tender']} {row['Listing summary']}",
            )
            row["_portfolio_score"] = score
            row["_portfolio_overlaps"] = overlaps
        tender_rows.sort(
            key=lambda row: (row.get("_portfolio_score", 0), -row["_closing"].timestamp()),
            reverse=True,
        )
    if tender_search.strip():
        query = tender_search.casefold().strip()
        tender_rows = [
            row for row in tender_rows
            if query in " ".join(
                str(value) for key, value in row.items() if not key.startswith("_")
            ).casefold()
        ]
    if tender_rows:
        display_rows = []
        for row in tender_rows[:tender_limit]:
            clean = {key: value for key, value in row.items() if not key.startswith("_")}
            if portfolio_text.strip():
                clean["Portfolio overlap"] = f"{row.get('_portfolio_score', 0)}%"
                clean["Matching experience"] = ", ".join(row.get("_portfolio_overlaps", [])) or "No direct text overlap found"
            display_rows.append(clean)
        if portfolio_text.strip():
            best_score = max(row.get("_portfolio_score", 0) for row in tender_rows)
            overlap_count = sum(row.get("_portfolio_score", 0) > 0 for row in tender_rows)
            st.success(
                f"Portfolio text overlaps with {overlap_count} current listing(s). "
                f"Highest textual overlap: {best_score}%. Review each tender's full documents before deciding to bid."
            )
        st.dataframe(
            display_rows,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Project / tender": st.column_config.TextColumn("Project / tender", width="large"),
                "Listing summary": st.column_config.TextColumn("Listing summary", width="large"),
                "Agency and listed office": st.column_config.TextColumn("Agency and listed office", width="medium"),
                "Closing (Pakistan time)": st.column_config.TextColumn("Closing (Pakistan time)", width="medium"),
                "Official notice": st.column_config.LinkColumn("Official notice", display_text="Open tender"),
                "Portfolio overlap": st.column_config.TextColumn("Portfolio overlap", width="small"),
                "Matching experience": st.column_config.TextColumn("Matching experience", width="large"),
            },
        )
        st.caption(
            f"Showing {min(len(tender_rows), tender_limit)} of {len(tender_rows)} matching future-dated federal notices. "
            "Federal PPRA listings include projects across Pakistan; the office shown may be the agency office, not the project site."
        )
        if portfolio_text.strip():
            st.caption(
                "Portfolio matching is keyword overlap against public listing text only. It does not evaluate PEC category, "
                "project profile codes, minimum years of experience, tax registration, bid security, or other eligibility criteria."
            )
    else:
        st.info(
            "No matching future-dated notices were found in the loaded federal PPRA pages. "
            "Try a broader search or open a regional portal below."
        )
except requests.RequestException:
    st.warning(
        "The live federal tender feed is temporarily unavailable. Use the official portal links below to check current notices."
    )

st.header("Worldwide freelance searches matched to the portfolio")
if portfolio_text.strip():
    st.caption("Search themes below are selected from the experience and skills detected in the uploaded CV or portfolio.")
else:
    st.caption("Upload a CV or portfolio above to personalize these searches. Until then, searches use the app's construction-management focus.")

freelance_matches = freelance_search_matches(portfolio_text)
for start in range(0, len(freelance_matches), 2):
    cols = st.columns(2)
    for col, item in zip(cols, freelance_matches[start:start + 2]):
        query = quote_plus(item["query"])
        upwork_url = f"https://www.upwork.com/nx/search/jobs/?q={query}"
        freelancer_url = f"https://www.freelancer.com/search/projects?q={query}"
        with col:
            with st.container(border=True):
                st.markdown(f"#### {item['title']}")
                st.write(item["offer"])
                st.link_button("Search Upwork", upwork_url, use_container_width=True)
                st.link_button("Search Freelancer.com", freelancer_url, use_container_width=True)
st.caption(
    "These buttons open live marketplace searches; listings, location eligibility, and deadlines are controlled by each platform. "
    "The app does not import, verify, or apply to individual freelance jobs."
)

st.header("Pakistan jobs and construction opportunities")
st.caption(
    "Fixed job searches for civil engineering roles in Pakistan and Saudi Arabia. These are employment opportunities, "
    "separate from consultancy tenders above. This section does not use the uploaded CV or portfolio."
)
job_roles = [
    "Civil Engineer",
    "Project Engineer Civil",
    "Project Manager Civil",
    "Quality Engineer Civil",
]
for role_start in range(0, len(job_roles), 2):
    role_cols = st.columns(2)
    for col, role in zip(role_cols, job_roles[role_start:role_start + 2]):
        with col:
            with st.container(border=True):
                st.markdown(f"#### {role} jobs")
                query = quote_plus(role)
                pakistan_url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location=Pakistan"
                saudi_url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location=Saudi%20Arabia"
                st.link_button("Search in Pakistan", pakistan_url, use_container_width=True)
                st.link_button("Search in Saudi Arabia", saudi_url, use_container_width=True)
                if role == "Civil Engineer":
                    st.markdown(
                        f"[More Pakistan jobs on Rozee.pk](https://www.rozee.pk/job/jsearch/q/Civil) · "
                        f"[Saudi engineering jobs on Naukrigulf](https://www.naukrigulf.com/civil-engineer-jobs-in-saudi-arabia)"
                    )
st.caption(
    "Links open live searches on external job boards; the app does not import or verify individual advertisements. "
    "Vacancies and closing dates change frequently, so confirm eligibility, location, documents and deadline in the employer's original advertisement. "
    "Never pay an individual to secure a job or share sensitive identity/bank details outside an official application process."
)

with st.expander("Open official procurement portals by region"):
    st.write(
        "There is no single official live feed combining federal and every provincial authority. "
        "Use these authority portals for additional regional notices; coverage and portal formats vary."
    )
    for region, url in REGIONAL_PORTALS.items():
        st.markdown(f"- [{region} procurement portal]({url})")
    st.markdown(f"- [Federal PPRA active consultancy tenders]({FEDERAL_TENDERS})")
st.caption(
    "Listings are discovery aids, not eligibility checks. Open the tender notice and all corrigenda "
    "to confirm scope, requirements, fees, security, and deadline before bidding."
)

tabs = st.tabs(["Launch roadmap", "PEC checklist", "Tender fit & cash", "Revenue plan", "Freelancing", "Sources"])

with tabs[0]:
    st.header("Choose the right lane")
    st.markdown("For independent construction management advice, project controls, contract administration, supervision or engineering consultancy, start by checking PEC’s **Consulting Engineer** firm route. PEC constructor/operator licences cover construction execution categories and are not interchangeable with consulting registration.")
    st.markdown(f"[PEC firm registration hub]({PEC}) · [Consultant portal]({CE_PORTAL}) · [Consulting bye-laws]({BYLAWS})")
    st.subheader("Recommended sequence")
    steps = [
        ("1. Define services", "Write a clear scope (planning, scheduling, cost control, site monitoring, contract administration, reporting). Keep regulated engineering design/sign-off within appropriately registered disciplines and qualified people."),
        ("2. Select legal form", "Choose individual/sole proprietor, partnership, or company. Align ownership, management and engineering credentials with the current consulting bye-laws; use SECP / registrar and FBR procedures applicable to your form."),
        ("3. Assemble your proof", "Collect identity and legal documents, PEC engineer cards, affidavits, current-year biometric slips, CVs and experience certificates, firm NTN, bank account certificate, and any government-employer NOCs."),
        ("4. Apply to PEC", "Create a new firm account on the Consulting Engineer portal, complete the application, upload readable documents in its accepted formats and pay the current fee voucher. Track portal messages and respond to deficiencies."),
        ("5. Prepare to sell", "Build a one-page capability statement, CVs, service methodology, sample schedule/cost-control report, references and a rate card. Register as a supplier in EPADS and relevant provincial/agency systems where required."),
        ("6. Bid selectively", "For each opportunity, check the required PEC consultant category / disciplines, project profile codes, experience, tax status, JV rules, bid fee, bid security, delivery dates and contract terms. Price only work you can resource and finance."),
    ]
    for title, body in steps:
        with st.expander(title, expanded=False):
            st.write(body)
    st.warning("There is no general guarantee that a new firm will be hired or awarded a tender. Awards depend on eligibility, evaluation criteria, competition and the procuring agency’s decision.")

with tabs[1]:
    st.header("Local PEC consulting firm: document checklist")
    st.write("The PEC local-consultant summary form currently lists these items. Use it as a working checklist and confirm the latest portal-specific requirements before submission.")
    items = [
        "Completed PEC-1A application form",
        "Current PEC fee deposit evidence / portal voucher",
        "Firm covering letter on letterhead",
        "Valid CNIC copies of owners / partners / shareholders",
        "Partnership deed and registrar proof, if partnership",
        "For a company: incorporation certificate, updated Forms 29 and A, memorandum and articles",
        "Degrees of allied non-engineer professionals, where applicable",
        "Verified owner / partner / director / shareholder affidavits, CNICs and valid PEC renewal cards",
        "Verified employee-engineer affidavits, CNICs and valid PEC renewal cards",
        "Current-year biometric verification / re-verification slips for relevant engineers",
        "Detailed engineer CVs with experience certificates supporting requested project profile codes",
        "Department NOC for engineers in government service / public organizations, where applicable",
        "Firm / company NTN certificate",
        "Bank certificate showing satisfactory maintenance of firm account",
    ]
    checked = []
    for i, item in enumerate(items):
        if st.checkbox(item, key=f"pec_{i}"):
            checked.append(item)
    st.progress(len(checked) / len(items), text=f"{len(checked)} of {len(items)} checklist items marked ready")
    st.caption("The PEC portal FAQ says average processing is about 15 days when documents are complete; this is an indicative average, not a service guarantee.")
    st.markdown(f"[Download PEC local application / checklist (PDF)]({LOCAL_FORM}) · [Portal FAQ]({CE_FAQ})")

with tabs[2]:
    st.header("Tender fit and cash check")
    left, right = st.columns(2)
    with left:
        service = st.selectbox("What are you bidding to provide?", ["Construction management / project controls consultancy", "Engineering design or supervision consultancy", "Construction execution / works contract", "Unsure"])
        pec_ready = st.checkbox("My firm holds the PEC registration / licence explicitly required by this tender")
        profile_ready = st.checkbox("Our disciplines, project profile codes, staff and experience meet the tender criteria")
        tax_ready = st.checkbox("Our NTN / tax status and other registrations required by this tender are current")
    with right:
        tender_fee = st.number_input("Tender document / participation fee (PKR)", min_value=0, step=1000)
        security = st.number_input("Bid security required (PKR; enter 0 if none)", min_value=0, step=10000)
        cash_available = st.number_input("Cash available for this bid (PKR)", min_value=0, step=10000)
        use_security = st.checkbox("Tender accepts bid securing declaration instead of cash/guarantee (verify exact wording)")
    required_cash = tender_fee + (0 if use_security else security)
    st.metric("Minimum direct cash indicated", f"PKR {required_cash:,.0f}")
    if required_cash > cash_available:
        st.error("This opportunity exceeds the cash you entered. Do not assume e-bidding removes the security requirement; check the original tender documents and arrange an eligible partner or skip it.")
    else:
        st.success("Cash entered covers the fee and stated security only. Allow separately for PEC / tax setup, bid preparation, travel, insurance, staff, taxes, performance guarantee and working capital.")
    st.markdown("**Readiness signal**")
    if service.startswith("Construction management") or service.startswith("Engineering"):
        st.write("Treat this as a consulting-services procurement and verify the required PEC consulting firm category / disciplines in the actual RFP.")
    elif service.startswith("Construction execution"):
        st.write("This is a works bid: verify the required PEC constructor category and codes. A consulting registration alone may not qualify.")
    else:
        st.write("Check the scope first: consultancy and construction works can require different PEC registrations and evidence.")
    if not (pec_ready and profile_ready and tax_ready):
        st.warning("One or more eligibility checks are not marked ready. Registration alone does not establish tender eligibility.")
    st.caption("On federal PPRA procurement, EPADS vendor signup is the entry point. The bid document controls fees, security, hard-copy security delivery and other conditions. Provincial procurement portals have separate rules.")

with tabs[3]:
    st.header("Low-cash route to first revenue")
    st.markdown("### Start by selling a defined service")
    st.write("Offer a small, clearly bounded engagement to private developers, contractors, architects or established consultants: baseline schedule review, weekly progress reporting, quantity / cost tracking, site coordination log, risk register, or claims-document support. Use a signed scope, acceptance criteria, payment milestones and exclusions.")
    st.markdown("### Build evidence before chasing large tenders")
    st.write("Create sample deliverables using a public or hypothetical project, document your own past experience accurately, request references from former clients (with permission), and build a capability statement. Never present another firm’s experience as yours.")
    st.markdown("### Ways to reduce upfront tender cash")
    st.write("Prioritize private-sector direct engagements; pursue subcontracting under an established prime; explore a compliant JV/association where the tender permits it; and filter for tenders with no bid security or a permitted declaration. Each partner must meet its own registration and tender requirements.")
    st.markdown("### Be realistic about costs")
    st.write("A free supplier portal is not a free business launch. Budget for current PEC fees, NTN/business setup, proposal preparation, any tender fee, security or guarantee costs, travel, insurance, professional staff, taxes and the time between doing work and receiving payment.")
    st.markdown("### Simple engagement economics")
    fee = st.number_input("Expected contract fee (PKR)", min_value=0, step=50000, key="fee")
    cost = st.number_input("Estimated delivery costs (PKR)", min_value=0, step=10000, key="cost")
    buffer = st.slider("Contingency buffer (%)", 0, 40, 10)
    margin = fee - cost * (1 + buffer / 100)
    st.metric("Estimated surplus before tax and overhead", f"PKR {margin:,.0f}")
    if margin < 0:
        st.error("The estimate is negative after the selected buffer. Reprice or refine scope and costs before committing.")
    else:
        st.info("This is a planning estimate, not a quote. Include overhead, payment delay, tax and contract risk before setting your price.")

with tabs[4]:
    st.header("Freelancing options for a construction consultant")
    st.write(
        "Start with remote deliverables that can be completed from project records and agreed inputs. "
        "For site-based work, clearly state travel, location, visit frequency, and any local registration requirements."
    )

    st.subheader("Service offers supported by the portfolio")
    freelance_services = [
        ("Primavera P6 schedule support", "Baseline schedules, updates, look-ahead plans, progress reports, S-curves, and recovery schedules."),
        ("Schedule and project-controls review", "Critical-path and schedule-health review, delay notes, progress tracking, and action registers."),
        ("BOQ, cost, and tender support", "BOQ and quantity review, cost tracking, tender programme support, and subcontractor comparison."),
        ("QA/QC documentation support", "ITPs, inspection requests, method statements, test registers, quality records, and close-out documents."),
        ("Foundation and ground-improvement coordination", "Planning and reporting support for piling, CMC / rigid inclusions, stone columns, and related testing."),
    ]
    for title, description in freelance_services:
        with st.expander(title):
            st.write(description)

    st.subheader("Set up a profile that clients can evaluate")
    st.markdown(
        """
        1. Create profiles on one or two marketplaces and complete identity/payment verification there.
        2. Use a specific headline, such as **Construction Project Controls Engineer | Primavera P6 | Site Delivery**.
        3. Add two or three sample outputs using hypothetical or permission-cleared project data: a baseline schedule, a weekly progress report, and a QA/QC register.
        4. Describe your individual role accurately. Get permission before using client names, drawings, photos, or confidential project information.
        5. Start with a small, defined milestone and agree inputs, revisions, delivery date, price, and exclusions in writing.
        """
    )

    st.subheader("Search global marketplaces")
    st.write("Use the portfolio-matched searches on the main page, or open a marketplace and search for a service directly.")
    platform_cols = st.columns(3)
    with platform_cols[0]:
        st.link_button("Upwork freelance jobs", "https://www.upwork.com/freelance-jobs/primavera/", use_container_width=True)
    with platform_cols[1]:
        st.link_button("Freelancer projects", "https://www.freelancer.com/jobs/project-scheduling", use_container_width=True)
    with platform_cols[2]:
        st.link_button("PeoplePerHour projects", "https://www.peopleperhour.com/freelance-jobs", use_container_width=True)

    st.info(
        "Marketplace searches show projects that may be worldwide or remote, but each client can set country, time-zone, "
        "experience, and on-site restrictions. Check the full listing and platform fees before applying."
    )

with tabs[5]:
    st.header("Official sources")
    sources = [
        ("PEC Firm Registration hub", PEC, "Official route links for local consulting firms and related PEC information."),
        ("PEC Consulting Engineer Portal", CE_PORTAL, "New account/application portal for consultant firms."),
        ("PEC Consultant Portal FAQ", CE_FAQ, "Signup, document upload guidance, indicative processing time, status and engineer consent process."),
        ("PEC Local Consultant application and document summary (PDF)", LOCAL_FORM, "PEC-1A and local firm supporting document list; fee figures in this form may be dated, so confirm the current voucher."),
        ("PEC Consulting Engineers Bye-laws", BYLAWS, "Professional registration framework and project profile code provisions."),
        ("PEC Constructor/Operator registration policy (2024)", "https://www.pec.org.pk/wp-content/uploads/2024/09/Updated-Registration-Policy-July-30-2024.pdf", "Constructor/operator categories; useful to distinguish works contracting from consulting."),
        ("Federal PPRA", PPRA, "Federal procurement opportunities, rules and e-PADS vendor access."),
        ("Federal PPRA active consultancy tenders", FEDERAL_TENDERS, "Live federal listing used by the home-page tender board."),
        ("Punjab PPRA", REGIONAL_PORTALS["Punjab"], "Punjab procurement notices and e-tender resources."),
        ("Sindh PPMS / SPPRA", REGIONAL_PORTALS["Sindh"], "Sindh public procurement notice portal."),
        ("Khyber Pakhtunkhwa e-procurement", REGIONAL_PORTALS["Khyber Pakhtunkhwa"], "Khyber Pakhtunkhwa EPADS tender portal."),
        ("Balochistan PPRA", REGIONAL_PORTALS["Balochistan"], "Balochistan procurement authority portal."),
        ("AJK PPRA", REGIONAL_PORTALS["Azad Jammu & Kashmir"], "Azad Jammu and Kashmir procurement notices."),
        ("Gilgit-Baltistan PPRA", REGIONAL_PORTALS["Gilgit-Baltistan"], "Gilgit-Baltistan procurement notices."),
        ("EPADS vendor registration", EPADS, "Federal supplier registration portal."),
        ("PPRA FAQ", PPRA_FAQ, "Bid security and e-PADS submission guidance. Confirm current applicable rules and tender text."),
    ]
    for label, url, desc in sources:
        st.markdown(f"- [{label}]({url}) — {desc}")
    st.caption("Sources checked 30 October 2026. Federal procurement rules and portal versions can change; confirm applicable notices and provincial rules at the time you apply.")

st.divider()
st.caption("BuildReady Pakistan · Independent planning aid · No guarantee of PEC approval, tender eligibility, selection or revenue")
