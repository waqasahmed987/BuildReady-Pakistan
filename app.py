import streamlit as st

st.set_page_config(
    page_title="BuildReady Pakistan",
    page_icon="🏗️",
    layout="wide",
)

PEC_HUB = "https://www.pec.org.pk/firm-registration-new/"
CONSULTANT_PORTAL = "https://ceportal.pec.org.pk/User/SignUp"
CONSULTANT_FAQ = "https://ceportal.pec.org.pk/User/Faqs"
LOCAL_CONSULTANT_FORM = (
    "https://www.pec.org.pk/wp-content/uploads/2021/05/"
    "Consulting-Engineers-Registration-Form-Local-Consultants.pdf"
)
CONSULTING_BYLAWS = (
    "https://www.pec.org.pk/wp-content/uploads/2024/10/"
    "PEC-Consulting-Engr-Bye-laws-1986-amended-upto-MARCH-14-2024.pdf"
)
CONSTRUCTOR_POLICY = (
    "https://www.pec.org.pk/wp-content/uploads/2024/09/"
    "Updated-Registration-Policy-July-30-2024.pdf"
)
PPRA_HOME = "https://ppra.gov.pk/"
EPADS_VENDOR_REGISTRATION = "https://vendors.epads.gov.pk/register"
PPRA_FAQ = "https://ppra.gov.pk/faqs"

st.title("🏗️ BuildReady Pakistan")
st.caption(
    "A launch and tender-readiness guide for construction management "
    "consultants in Pakistan"
)
st.info(
    "This app is an informational planning aid. Confirm current forms, fees, "
    "tax obligations, tender terms, and provincial rules with PEC, FBR, "
    "SECP or the relevant registrar, and the procuring agency."
)

launch_tab, checklist_tab, tender_tab, revenue_tab, sources_tab = st.tabs(
    [
        "Launch roadmap",
        "PEC checklist",
        "Tender fit & cash",
        "Revenue plan",
        "Sources",
    ]
)

with launch_tab:
    st.header("Choose the right registration route")

    st.markdown(
        """
        For independent construction management advice, project controls,
        contract administration, supervision, or engineering consultancy,
        check PEC's **Consulting Engineer firm** route.

        PEC **Constructor/Operator** licences are for construction execution.
        They are different from consulting firm registration.
        """
    )

    st.markdown(
        f"[PEC registration hub]({PEC_HUB}) · "
        f"[Consultant portal]({CONSULTANT_PORTAL}) · "
        f"[Consulting bye-laws]({CONSULTING_BYLAWS})"
    )

    st.subheader("Recommended sequence")

    steps = [
        (
            "1. Define your services",
            "Write a clear service scope. Examples include planning, "
            "scheduling, cost control, site monitoring, contract "
            "administration, and project reporting. Confirm which services "
            "require specific PEC disciplines or professional sign-off.",
        ),
        (
            "2. Choose a legal form",
            "Consider an individual or sole proprietorship, partnership, "
            "or company. Check the current legal and PEC requirements for "
            "your chosen form before registering.",
        ),
        (
            "3. Assemble your documents",
            "Prepare identity and legal documents, PEC engineer records, "
            "affidavits, current-year biometric slips, CVs and experience "
            "certificates, firm NTN, bank account certificate, and any "
            "required government-employer NOCs.",
        ),
        (
            "4. Apply to PEC",
            "Create an account on the Consulting Engineer portal, complete "
            "the application, upload readable documents, pay the current "
            "official fee voucher, and respond to portal messages or "
            "document queries.",
        ),
        (
            "5. Prepare your sales material",
            "Create a capability statement, staff CVs, service methodology, "
            "sample schedule or cost-control report, references, and a "
            "rate card. Register on EPADS and any other procurement systems "
            "required by your target clients.",
        ),
        (
            "6. Check each tender before bidding",
            "Review the required PEC registration, disciplines, project "
            "profile codes, experience, tax status, bid fee, bid security, "
            "deadlines, and contract conditions. Only quote for work you "
            "can deliver and finance.",
        ),
    ]

    for title, description in steps:
        with st.expander(title):
            st.write(description)

    st.warning(
        "Registration does not guarantee that a company will hire you or "
        "that you will win a tender. Selection depends on eligibility, "
        "evaluation criteria, competition, and the client's decision."
    )


with checklist_tab:
    st.header("PEC local consulting firm document checklist")

    st.write(
        "Use this as a working checklist based on PEC's published local "
        "consultant form. Confirm the current portal requirements before "
        "submitting."
    )

    checklist_items = [
        "Completed PEC-1A application form",
        "Current PEC fee deposit evidence or portal voucher",
        "Firm covering letter on letterhead",
        "Valid CNIC copies of owners, partners, or shareholders",
        "Partnership deed and registrar proof, if applying as a partnership",
        (
            "For a company: incorporation certificate, updated Forms 29 "
            "and A, memorandum, and articles"
        ),
        "Degrees of allied non-engineer professionals, where applicable",
        (
            "Required owner, partner, director, or shareholder affidavits, "
            "CNICs, and valid PEC renewal cards"
        ),
        (
            "Required employee-engineer affidavits, CNICs, and valid "
            "PEC renewal cards"
        ),
        (
            "Current-year biometric verification or re-verification slips "
            "for relevant engineers"
        ),
        (
            "Detailed engineer CVs with experience certificates supporting "
            "requested project profile codes"
        ),
        (
            "Department NOC for engineers in government service or public "
            "organizations, where applicable"
        ),
        "Firm or company NTN certificate",
        "Bank certificate showing maintenance of the firm account",
    ]

    completed_items = []

    for number, item in enumerate(checklist_items):
        if st.checkbox(item, key=f"checklist_{number}"):
            completed_items.append(item)

    completion = len(completed_items) / len(checklist_items)
    st.progress(
        completion,
        text=(
            f"{len(completed_items)} of {len(checklist_items)} "
            "items marked ready"
        ),
    )

    st.caption(
        "PEC's portal FAQ gives an indicative average processing time of "
        "about 15 days when documents are complete. This is not a guarantee."
    )

    st.markdown(
        f"[PEC local consultant form and checklist (PDF)]"
        f"({LOCAL_CONSULTANT_FORM}) · "
        f"[PEC consultant portal FAQ]({CONSULTANT_FAQ})"
    )


with tender_tab:
    st.header("Tender fit and cash check")

    left_column, right_column = st.columns(2)

    with left_column:
        service_type = st.selectbox(
            "What are you bidding to provide?",
            [
                "Construction management or project controls consultancy",
                "Engineering design or supervision consultancy",
                "Construction execution or works contract",
                "Unsure",
            ],
        )

        pec_registration_ready = st.checkbox(
            "We hold the PEC registration or licence required by this tender"
        )
        experience_ready = st.checkbox(
            "Our disciplines, experience, staff, and project profile codes "
            "meet the tender criteria"
        )
        tax_status_ready = st.checkbox(
            "Our NTN, tax status, and other required registrations are current"
        )

    with right_column:
        tender_fee = st.number_input(
            "Tender document or participation fee (PKR)",
            min_value=0,
            step=1000,
        )
        bid_security = st.number_input(
            "Bid security required (PKR; enter 0 if none)",
            min_value=0,
            step=10000,
        )
        available_cash = st.number_input(
            "Cash available for this bid (PKR)",
            min_value=0,
            step=10000,
        )
        declaration_allowed = st.checkbox(
            "The tender permits a bid-securing declaration instead "
            "of cash or a guarantee"
        )

    cash_needed = tender_fee
    if not declaration_allowed:
        cash_needed += bid_security

    st.metric("Estimated tender fee and security cash", f"PKR {cash_needed:,.0f}")

    if cash_needed > available_cash:
        st.error(
            "The fee and security amount entered is higher than your "
            "available cash. Check the tender documents and consider an "
            "eligible partner or another opportunity."
        )
    else:
        st.success(
            "Your entered cash covers the fee and security amounts only. "
            "Also plan for bid preparation, travel, staff, taxes, insurance, "
            "performance guarantees, and working capital."
        )

    st.subheader("Registration route reminder")

    if service_type.startswith("Construction management"):
        st.write(
            "This is likely a consulting-services opportunity. Check the "
            "actual RFP for required PEC consulting firm category, "
            "disciplines, and experience."
        )
    elif service_type.startswith("Engineering"):
        st.write(
            "Check the actual RFP for the required PEC consulting "
            "registration, disciplines, staff, and project experience."
        )
    elif service_type.startswith("Construction execution"):
        st.write(
            "This is a works contract. Check whether a PEC "
            "Constructor/Operator category and specific codes are required. "
            "Consulting registration alone may not qualify."
        )
    else:
        st.write(
            "Read the scope first. Consulting services and construction "
            "works can require different registrations and evidence."
        )

    if not (
        pec_registration_ready
        and experience_ready
        and tax_status_ready
    ):
        st.warning(
            "One or more eligibility checks are not marked ready. "
            "Registration alone does not establish tender eligibility."
        )

    st.caption(
        "EPADS registration does not remove tender-specific fees or "
        "security requirements. Read the original tender documents and "
        "check the relevant provincial procurement system where applicable."
    )


with revenue_tab:
    st.header("Low-cash route to first revenue")

    st.subheader("Offer a defined service")
    st.write(
        "Start with a specific, manageable service for private developers, "
        "contractors, architects, or established consultants. Examples "
        "include schedule reviews, weekly progress reports, cost tracking, "
        "site coordination logs, risk registers, and claims-document support."
    )

    st.subheader("Agree on scope and payment")
    st.write(
        "Use a written scope, deliverables, acceptance criteria, exclusions, "
        "payment milestones, and change-request process. Agree how travel, "
        "site visits, taxes, and extra work will be handled."
    )

    st.subheader("Build evidence")
    st.write(
        "Create sample deliverables using a hypothetical or public project. "
        "Describe your own experience accurately, and get permission before "
        "using a client's name, reference, or project information."
    )

    st.subheader("Reduce upfront tender cash where possible")
    st.write(
        "Consider private-sector work, subcontracting for an established "
        "prime, or a compliant joint venture where the tender allows it. "
        "You can also look for opportunities with no bid security or a "
        "permitted bid-securing declaration. Check each tender's rules."
    )

    st.subheader("Estimate engagement economics")

    contract_fee = st.number_input(
        "Expected contract fee (PKR)",
        min_value=0,
        step=50000,
        key="contract_fee",
    )
    delivery_cost = st.number_input(
        "Estimated delivery costs (PKR)",
        min_value=0,
        step=10000,
        key="delivery_cost",
    )
    contingency_percent = st.slider(
        "Contingency buffer (%)",
        min_value=0,
        max_value=40,
        value=10,
    )

    estimated_surplus = contract_fee - (
        delivery_cost * (1 + contingency_percent / 100)
    )

    st.metric(
        "Estimated surplus before tax and overhead",
        f"PKR {estimated_surplus:,.0f}",
    )

    if estimated_surplus < 0:
        st.error(
            "The estimate is negative after the selected contingency. "
            "Review the price, delivery costs, and scope before committing."
        )
    else:
        st.info(
            "This is a planning estimate, not a quote. Account for overhead, "
            "tax, payment delays, and contract risks before pricing work."
        )

    st.warning(
        "Free supplier signup does not mean a free business launch. Budget "
        "for PEC fees, business and tax setup, tender charges, security, "
        "proposal preparation, travel, insurance, staff, and delayed payments."
    )


with sources_tab:
    st.header("Official sources")

    sources = [
        (
            "PEC firm registration hub",
            PEC_HUB,
            "Official PEC firm registration information and route links.",
        ),
        (
            "PEC Consulting Engineer portal",
            CONSULTANT_PORTAL,
            "Portal for new consulting firm accounts and applications.",
        ),
        (
            "PEC consultant portal FAQ",
            CONSULTANT_FAQ,
            "Portal guidance, document uploads, application status, "
            "and indicative processing information.",
        ),
        (
            "PEC local consultant form and checklist",
            LOCAL_CONSULTANT_FORM,
            "Application form and supporting document summary. Fee figures "
            "in the form may be dated; confirm the current voucher.",
        ),
        (
            "PEC Consulting Engineers Bye-laws",
            CONSULTING_BYLAWS,
            "Consulting engineer registration framework.",
        ),
        (
            "PEC Constructor/Operator policy",
            CONSTRUCTOR_POLICY,
            "Constructor and operator categories, which relate to "
            "construction execution.",
        ),
        (
            "Federal PPRA",
            PPRA_HOME,
            "Federal procurement information and EPADS access.",
        ),
        (
            "EPADS supplier registration",
            EPADS_VENDOR_REGISTRATION,
            "Federal supplier registration portal.",
        ),
        (
            "PPRA FAQ",
            PPRA_FAQ,
            "Procurement guidance including bid security and submission.",
        ),
    ]

    for label, url, description in sources:
        st.markdown(f"- [{label}]({url}) — {description}")

    st.caption(
        "Sources checked 30 October 2026. Rules, portals, fees, and tender "
        "requirements can change. Confirm current requirements before "
        "applying or submitting a bid."
    )

st.divider()
st.caption(
    "BuildReady Pakistan · Planning aid only · No guarantee of PEC approval, "
    "tender eligibility, selection, or revenue"
)
