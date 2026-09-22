import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="AuditFlow - Enterprise AI Compliance Auditor",
    layout="wide"
)

st.title("🛡️ AuditFlow: Enterprise AI Compliance Auditor")
st.markdown("Automated RAG-powered expense claim auditing against the 2026 Global Enterprise Policy Handbook.")

# Sidebar for API Key Config
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter your Google Gemini API Key", type="password", value="")

if api_key:
    genai.configure(api_key=api_key)
    # Using the correct modern Gemini 1.5 Flash model
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Advanced Policy Context
    policy_context = """
    GLOBAL ENTERPRISE TRAVEL & EXPENSE COMPLIANCE HANDBOOK 2026 (REV 4.2)
    ======================================================================
    SECTION 1: AIR TRAVEL & TRANSIT GUIDELINES
    - 1.1 Domestic Flights: Economy class is mandatory for domestic flights under 4 hours (7 days advance booking). Non-compliance = 50% penalty.
    - 1.2 International Travel: Business class restricted to VP and above or flights > 8 hours.
    
    SECTION 2: ACCOMMODATION & LODGING POLICY
    - 2.1 Tier-1 Metros (Mumbai, Delhi, Bangalore, Chennai, Hyderabad, Kolkata): Max hotel cap is ₹5,000 per night inclusive of taxes and breakfast.
    - 2.2 Tier-2 & Tier-3 Cities: Max hotel cap is ₹3,000 per night.
    - 2.4 Incidental Expenses: Laundry, mini-bar, spa, and personal phone calls are strictly non-reimbursable.

    SECTION 3: FOOD, DINING & ENTERTAINMENT
    - 3.1 Daily Meal Allowance: Max daily cap for food/soft beverages is ₹1,800/day. Itemized invoices required.
    - 3.2 Alcohol & Tobacco Policy: Alcohol and bar bills are strictly non-reimbursable. Any claim containing alcohol triggers an automated red flag and rejection of that bill item.
    - 3.3 Client Entertainment: Max cap is ₹2,500 per attendee with valid corporate GSTIN.

    SECTION 4: LOCAL COMMUTE & TRANSPORTATION
    - 4.1 Taxis & Ride-sharing: Reimbursable up to ₹1,200 per day with digital receipts.

    SECTION 5: AUDIT ENFORCEMENT & PENALTIES
    - 5.1 Submission Window: Must be submitted within 14 days of trip completion. Late submissions auto-rejected.
    """

    # Main User Input Area inside a Form
    st.subheader("📝 Submit Expense Claim for Audit")
    
    with st.form("audit_form"):
        employee_name = st.text_input("Employee Name", "Rahul Sharma")
        claim_text = st.text_area(
            "Enter Expense Details & Bills", 
            "Stayed in Mumbai hotel for ₹5,200 per night, submitted a laundry bill of ₹300, and a bar bill of ₹600."
        )
        submit_button = st.form_submit_button("Run Enterprise Audit")

    if submit_button:
        if claim_text:
            with st.spinner("Analyzing claim against 2026 Enterprise Policy Handbook..."):
                try:
                    system_prompt = f"""
                    You are AuditFlow, an expert corporate financial compliance auditor. 
                    Audit the employee expense claim strictly against the provided policy context below.
                    
                    POLICY CONTEXT:
                    {policy_context}
                    
                    Provide the output in two parts:
                    1. An Audit Summary Table with columns: Expense Item | Amount Claimed | Approved Amount | Disallowed/Over-claim.
                    2. Auditor's Final Action Directive explaining exact section violations.
                    """

                    user_prompt = f"Employee Name: {employee_name}\nClaim Details: {claim_text}"

                    response = model.generate_content([system_prompt, user_prompt])
                    
                    st.markdown("---")
                    st.subheader("📊 Audit Report & Compliance Verdict")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"API Error: {e}")
        else:
              st.warning("Please enter expense details to audit.")
else:
    st.info("👈 Please enter your Gemini API Key in the sidebar to start auditing.")
