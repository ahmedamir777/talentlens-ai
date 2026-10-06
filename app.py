import streamlit as st
import requests
import pandas as pd
import json
import re

from pypdf import PdfReader
from io import BytesIO
from html import escape


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="TalentLens AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONFIGURATION
# ============================================================

# IMPORTANT:
# Replace this whenever your Colab/ngrok URL changes.
MODEL_API_URL = "https://amplify-ivy-poster.ngrok-free.dev/generate"

API_KEY = "ahmed772005"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ============================================================
       GLOBAL
       ============================================================ */

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 80% 0%,
                rgba(99, 102, 241, 0.10),
                transparent 28%
            ),
            radial-gradient(
                circle at 0% 35%,
                rgba(14, 165, 233, 0.06),
                transparent 25%
            ),
            #080b12;
    }

    /* Main container */

    .block-container {
        max-width: 1450px;
        padding-top: 1.8rem;
        padding-bottom: 4rem;
    }


    /* ============================================================
       SIDEBAR
       ============================================================ */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0c1019 0%,
                #080b12 100%
            );

        border-right:
            1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }


    /* ============================================================
       STREAMLIT DEFAULT ELEMENTS
       ============================================================ */

    div[data-testid="stVerticalBlock"] {
        gap: 0.6rem;
    }

    .stButton > button {
        border-radius: 12px;
        min-height: 48px;

        border: 1px solid
            rgba(129,140,248,0.28);

        background:
            linear-gradient(
                135deg,
                #6366f1,
                #7c3aed
            );

        color: white;

        font-weight: 700;

        box-shadow:
            0 10px 30px
            rgba(99,102,241,0.20);

        transition:
            all 0.18s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        border-color:
            rgba(165,180,252,0.45);

        box-shadow:
            0 15px 40px
            rgba(99,102,241,0.32);
    }

    .stDownloadButton > button {
        border-radius: 12px;

        min-height: 46px;

        background:
            linear-gradient(
                135deg,
                #059669,
                #10b981
            );

        color: white;

        border: none;

        font-weight: 700;

        box-shadow:
            0 10px 25px
            rgba(16,185,129,0.18);
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 15px 35px
            rgba(16,185,129,0.28);
    }


    /* ============================================================
       SIDEBAR BRAND
       ============================================================ */

    .brand {
        display: flex;
        align-items: center;

        gap: 12px;

        padding: 8px 4px 28px;
    }

    .brand-icon {
        width: 44px;
        height: 44px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 13px;

        background:
            linear-gradient(
                135deg,
                #6366f1,
                #8b5cf6
            );

        color: white;

        font-size: 22px;

        font-weight: 800;

        box-shadow:
            0 10px 30px
            rgba(99,102,241,0.28);
    }

    .brand-name {
        color: #f8fafc;

        font-size: 18px;

        font-weight: 800;
    }

    .brand-sub {
        color: #64748b;

        font-size: 9px;

        letter-spacing: 0.6px;

        margin-top: 3px;
    }


    /* ============================================================
       SIDEBAR LABEL
       ============================================================ */

    .sidebar-label {
        color: #475569;

        font-size: 9px;

        font-weight: 800;

        letter-spacing: 1.6px;

        text-transform: uppercase;

        margin:
            18px 0 10px;
    }


    /* ============================================================
       PIPELINE
       ============================================================ */

    .pipeline-item {
        display: flex;
        align-items: center;

        gap: 11px;

        padding: 9px 10px;

        margin-bottom: 4px;

        border-radius: 10px;

        color: #64748b;

        font-size: 12px;
    }

    .pipeline-item.active {
        background:
            linear-gradient(
                90deg,
                rgba(99,102,241,0.13),
                rgba(99,102,241,0.03)
            );

        color: #e2e8f0;

        border:
            1px solid rgba(99,102,241,0.10);
    }

    .pipeline-number {
        width: 25px;
        height: 25px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 7px;

        background: #151a25;

        color: #818cf8;

        font-size: 9px;

        font-weight: 800;
    }


    /* ============================================================
       SIDEBAR SERVER
       ============================================================ */

    .server-card {
        margin-top: 20px;

        padding: 15px;

        border-radius: 13px;

        background:
            rgba(255,255,255,0.025);

        border:
            1px solid rgba(255,255,255,0.06);
    }

    .server-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .server-title {
        color: #cbd5e1;

        font-size: 11px;

        font-weight: 700;
    }

    .server-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #34d399;

        box-shadow:
            0 0 12px
            rgba(52,211,153,0.8);
    }

    .server-info {
        color: #475569;

        font-size: 9px;

        line-height: 1.5;

        margin-top: 7px;
    }


    /* ============================================================
       TOP NAV
       ============================================================ */

    .topbar {
        display: flex;

        justify-content: space-between;

        align-items: center;

        margin-bottom: 22px;
    }

    .topbar-left {
        color: #64748b;

        font-size: 11px;
    }

    .topbar-left span {
        color: #a5b4fc;
    }

    .online-badge {
        display: inline-flex;

        align-items: center;

        gap: 7px;

        padding: 7px 12px;

        border-radius: 999px;

        background:
            rgba(16,185,129,0.07);

        border:
            1px solid rgba(16,185,129,0.15);

        color: #6ee7b7;

        font-size: 10px;

        font-weight: 700;
    }

    .online-dot {
        width: 6px;
        height: 6px;

        border-radius: 50%;

        background: #34d399;

        box-shadow:
            0 0 9px
            rgba(52,211,153,0.8);
    }


    /* ============================================================
       HERO
       ============================================================ */

    .hero {
        position: relative;

        overflow: hidden;

        padding: 38px 40px;

        min-height: 270px;

        border-radius: 24px;

        background:
            linear-gradient(
                135deg,
                rgba(30,35,74,0.94),
                rgba(16,20,38,0.95) 55%,
                rgba(10,14,24,0.98)
            );

        border:
            1px solid
            rgba(129,140,248,0.17);

        box-shadow:
            0 25px 80px
            rgba(0,0,0,0.22);
    }

    .hero::before {
        content: "";

        position: absolute;

        width: 420px;
        height: 420px;

        right: -150px;
        top: -200px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(99,102,241,0.24),
                transparent 68%
            );
    }

    .hero::after {
        content: "";

        position: absolute;

        width: 260px;
        height: 260px;

        right: 180px;
        bottom: -180px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(14,165,233,0.10),
                transparent 70%
            );
    }

    .hero-content {
        position: relative;

        z-index: 2;

        max-width: 750px;
    }

    .hero-eyebrow {
        color: #818cf8;

        font-size: 10px;

        font-weight: 800;

        letter-spacing: 2px;

        margin-bottom: 12px;
    }

    .hero-title {
        color: #f8fafc;

        font-size: 40px;

        line-height: 1.08;

        letter-spacing: -1.8px;

        font-weight: 800;
    }

    .hero-title span {
        color: #818cf8;
    }

    .hero-description {
        color: #94a3b8;

        font-size: 13px;

        line-height: 1.7;

        max-width: 650px;

        margin-top: 14px;
    }

    .hero-actions {
        display: flex;

        align-items: center;

        gap: 10px;

        margin-top: 22px;
    }

    .hero-tag {
        display: inline-flex;

        align-items: center;

        gap: 7px;

        padding: 8px 12px;

        border-radius: 999px;

        background:
            rgba(255,255,255,0.04);

        border:
            1px solid
            rgba(255,255,255,0.07);

        color: #94a3b8;

        font-size: 9px;

        font-weight: 600;
    }


    /* ============================================================
       UPLOAD CARD
       ============================================================ */

    .upload-card {
        margin-top: 22px;

        padding: 23px;

        border-radius: 19px;

        background:
            rgba(13,18,30,0.88);

        border:
            1px solid rgba(255,255,255,0.06);
    }

    .upload-heading {
        color: #f1f5f9;

        font-size: 16px;

        font-weight: 750;
    }

    .upload-subtitle {
        color: #64748b;

        font-size: 11px;

        margin-top: 4px;

        margin-bottom: 15px;
    }

    .upload-icon {
        font-size: 20px;

        margin-right: 6px;
    }


    /* ============================================================
       FILE UPLOADER
       ============================================================ */

    [data-testid="stFileUploader"] {
        background:
            rgba(255,255,255,0.018);

        border:
            1px dashed
            rgba(129,140,248,0.30);

        border-radius: 14px;

        padding: 8px;

        transition:
            border-color 0.2s ease;
    }

    [data-testid="stFileUploader"]:hover {
        border-color:
            rgba(129,140,248,0.55);
    }

    [data-testid="stFileUploaderDropzone"] {
        background: transparent;
    }


    /* ============================================================
       SECTION HEADER
       ============================================================ */

    .section-header {
        display: flex;

        align-items: center;

        justify-content: space-between;

        margin-top: 35px;

        margin-bottom: 14px;
    }

    .section-left {
        display: flex;

        align-items: center;

        gap: 10px;
    }

    .section-icon {
        width: 31px;
        height: 31px;

        display: flex;

        align-items: center;

        justify-content: center;

        border-radius: 9px;

        background:
            rgba(99,102,241,0.10);

        border:
            1px solid
            rgba(99,102,241,0.14);

        color: #a5b4fc;

        font-size: 13px;
    }

    .section-title {
        color: #f1f5f9;

        font-size: 17px;

        font-weight: 750;
    }

    .section-caption {
        color: #475569;

        font-size: 10px;
    }


    /* ============================================================
       PROFILE
       ============================================================ */

    .profile-card {
        position: relative;

        overflow: hidden;

        min-height: 160px;

        padding: 25px;

        border-radius: 19px;

        background:
            linear-gradient(
                135deg,
                rgba(30,41,59,0.75),
                rgba(15,23,42,0.80)
            );

        border:
            1px solid rgba(255,255,255,0.07);
    }

    .profile-glow {
        position: absolute;

        right: -70px;
        top: -70px;

        width: 190px;
        height: 190px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(99,102,241,0.20),
                transparent 70%
            );
    }

    .avatar {
        width: 54px;
        height: 54px;

        display: flex;

        align-items: center;

        justify-content: center;

        border-radius: 15px;

        background:
            linear-gradient(
                135deg,
                #6366f1,
                #8b5cf6
            );

        color: white;

        font-size: 19px;

        font-weight: 800;

        box-shadow:
            0 10px 25px
            rgba(99,102,241,0.25);
    }

    .profile-label {
        color: #64748b;

        font-size: 9px;

        font-weight: 800;

        letter-spacing: 1.3px;

        text-transform: uppercase;

        margin-top: 15px;
    }

    .profile-name {
        color: #f8fafc;

        font-size: 24px;

        font-weight: 800;

        margin-top: 4px;
    }

    .profile-email {
        color: #818cf8;

        font-size: 12px;

        margin-top: 5px;
    }


    /* ============================================================
       METRIC CARDS
       ============================================================ */

    .metric-card {
        padding: 19px;

        min-height: 118px;

        border-radius: 16px;

        background:
            rgba(15,23,42,0.70);

        border:
            1px solid rgba(255,255,255,0.06);
    }

    .metric-icon {
        color: #818cf8;

        font-size: 15px;
    }

    .metric-value {
        color: #f8fafc;

        font-size: 25px;

        font-weight: 800;

        margin-top: 10px;
    }

    .metric-label {
        color: #64748b;

        font-size: 9px;

        font-weight: 600;

        margin-top: 2px;
    }


    /* ============================================================
       EDUCATION
       ============================================================ */

    .edu-card {
        position: relative;

        padding: 22px;

        border-radius: 17px;

        background:
            rgba(15,23,42,0.70);

        border:
            1px solid rgba(255,255,255,0.06);

        margin-bottom: 10px;
    }

    .edu-top {
        display: flex;

        justify-content: space-between;

        gap: 20px;
    }

    .edu-degree {
        color: #f1f5f9;

        font-size: 15px;

        font-weight: 750;
    }

    .edu-institution {
        color: #818cf8;

        font-size: 11px;

        margin-top: 6px;
    }

    .edu-year {
        white-space: nowrap;

        color: #64748b;

        background:
            rgba(255,255,255,0.04);

        padding: 6px 9px;

        border-radius: 7px;

        font-size: 9px;

        height: fit-content;
    }


    /* ============================================================
       SKILLS
       ============================================================ */

    .skills-container {
        display: flex;

        flex-wrap: wrap;

        gap: 8px;
    }

    .skill {
        display: inline-flex;

        padding: 8px 11px;

        border-radius: 8px;

        background:
            linear-gradient(
                135deg,
                rgba(99,102,241,0.11),
                rgba(139,92,246,0.06)
            );

        border:
            1px solid
            rgba(129,140,248,0.15);

        color: #c7d2fe;

        font-size: 10px;

        font-weight: 600;
    }


    /* ============================================================
       EXPERIENCE
       ============================================================ */

    .exp-card {
        position: relative;

        padding: 20px 21px;

        border-radius: 16px;

        background:
            rgba(15,23,42,0.70);

        border:
            1px solid rgba(255,255,255,0.06);

        margin-bottom: 10px;

        transition:
            transform 0.18s ease,
            border-color 0.18s ease;
    }

    .exp-card:hover {
        transform: translateX(3px);

        border-color:
            rgba(129,140,248,0.20);
    }

    .exp-indicator {
        position: absolute;

        left: 0;
        top: 20px;
        bottom: 20px;

        width: 3px;

        border-radius: 3px;

        background:
            linear-gradient(
                180deg,
                #6366f1,
                #8b5cf6
            );
    }

    .exp-role {
        color: #f1f5f9;

        font-size: 14px;

        font-weight: 700;

        padding-left: 8px;
    }

    .exp-company {
        color: #818cf8;

        font-size: 11px;

        padding-left: 8px;

        margin-top: 5px;
    }

    .exp-years {
        display: inline-block;

        color: #64748b;

        font-size: 9px;

        padding: 5px 8px;

        border-radius: 6px;

        background:
            rgba(255,255,255,0.035);

        margin:
            9px 0 0 8px;
    }


    /* ============================================================
       PROJECTS
       ============================================================ */

    .project-card {
        min-height: 245px;

        padding: 22px;

        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(15,23,42,0.88),
                rgba(10,15,25,0.94)
            );

        border:
            1px solid rgba(255,255,255,0.06);

        transition:
            all 0.20s ease;

        position: relative;

        overflow: hidden;
    }

    .project-card::before {
        content: "";

        position: absolute;

        left: 0;
        top: 0;

        width: 100%;
        height: 2px;

        background:
            linear-gradient(
                90deg,
                #6366f1,
                #8b5cf6,
                #10b981
            );

        opacity: 0.7;
    }

    .project-card:hover {
        transform: translateY(-4px);

        border-color:
            rgba(52,211,153,0.25);

        box-shadow:
            0 18px 45px
            rgba(0,0,0,0.22);
    }

    .project-icon {
        width: 38px;
        height: 38px;

        display: flex;

        align-items: center;

        justify-content: center;

        border-radius: 11px;

        background:
            linear-gradient(
                135deg,
                rgba(99,102,241,0.14),
                rgba(16,185,129,0.08)
            );

        border:
            1px solid rgba(129,140,248,0.15);

        color: #a5b4fc;

        font-size: 16px;

        margin-bottom: 15px;
    }

    .project-name {
        color: #f1f5f9;

        font-size: 15px;

        font-weight: 750;

        line-height: 1.4;

        margin-bottom: 12px;
    }

    .project-summary-label {
        color: #64748b;

        font-size: 8px;

        font-weight: 800;

        letter-spacing: 1.2px;

        text-transform: uppercase;

        margin-bottom: 5px;
    }

    .project-summary {
        color: #94a3b8;

        font-size: 11px;

        line-height: 1.75;

        margin-top: 5px;

        display: -webkit-box;

        -webkit-line-clamp: 6;

        -webkit-box-orient: vertical;

        overflow: hidden;
    }


    /* ============================================================
       EXPORT
       ============================================================ */

    .export-card {
        position: relative;

        overflow: hidden;

        margin-top: 35px;

        padding: 25px;

        border-radius: 19px;

        background:
            linear-gradient(
                135deg,
                rgba(6,78,59,0.25),
                rgba(15,23,42,0.85)
            );

        border:
            1px solid
            rgba(52,211,153,0.14);
    }

    .export-card::after {
        content: "";

        position: absolute;

        right: -80px;
        bottom: -100px;

        width: 250px;
        height: 250px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(16,185,129,0.12),
                transparent 70%
            );
    }

    .export-title {
        color: #f1f5f9;

        font-size: 16px;

        font-weight: 750;
    }

    .export-text {
        color: #64748b;

        font-size: 10px;

        margin-top: 5px;
    }


    /* ============================================================
       JSON EXPANDER
       ============================================================ */

    [data-testid="stExpander"] {
        margin-top: 18px;

        border-radius: 13px;

        border:
            1px solid rgba(255,255,255,0.06);

        background:
            rgba(15,23,42,0.60);
    }


    /* ============================================================
       FOOTER
       ============================================================ */

    .footer {
        text-align: center;

        margin-top: 50px;

        padding-top: 20px;

        border-top:
            1px solid rgba(255,255,255,0.05);

        color: #334155;

        font-size: 9px;

        letter-spacing: 0.4px;
    }


    /* ============================================================
       HIDE STREAMLIT FOOTER
       ============================================================ */

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def html_escape(value):
    """
    Safely convert any value to HTML-safe text.
    """

    if value is None:
        return ""

    return escape(str(value))


def extract_pdf_text(uploaded_file):
    """
    Extract text from uploaded PDF using PyPDF.
    """

    pdf_bytes = uploaded_file.read()

    reader = PdfReader(
        BytesIO(pdf_bytes)
    )

    text_parts = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text_parts.append(page_text)

    return "\n".join(text_parts).strip()


def clean_model_response(response):
    """
    Convert the API response into a Python dictionary.

    Handles:
    1. Direct dictionary
    2. JSON string
    3. Markdown ```json ... ```
    """

    if isinstance(response, dict):
        return response

    if not isinstance(response, str):
        raise ValueError(
            "Unexpected model response type."
        )

    text = response.strip()

    # Remove markdown JSON fences
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    text = text.strip()

    try:

        return json.loads(text)

    except json.JSONDecodeError:

        # Try to find the JSON object
        match = re.search(
            r"\{.*\}",
            text,
            flags=re.DOTALL
        )

        if match:

            return json.loads(
                match.group(0)
            )

        raise ValueError(
            "The model returned invalid JSON."
        )


def analyze_cv(cv_text):
    """
    Send extracted CV text to the FastAPI/Colab model.
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "cv_input": cv_text
    }

    response = requests.post(
        MODEL_API_URL,
        headers=headers,
        json=payload,
        timeout=300
    )

    if response.status_code != 200:

        raise Exception(
            f"Model API returned HTTP "
            f"{response.status_code}\n\n"
            f"{response.text}"
        )

    data = response.json()

    if "response" not in data:

        raise Exception(
            "API response does not contain "
            "the 'response' field."
        )

    return clean_model_response(
        data["response"]
    )


def create_excel(candidate):
    """
    Create a multi-sheet Excel workbook.
    """

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        # --------------------------------------------
        # Candidate
        # --------------------------------------------

        candidate_data = pd.DataFrame([
            {
                "Full Name":
                    candidate.get(
                        "full_name",
                        ""
                    ),

                "Email":
                    candidate.get(
                        "email",
                        ""
                    )
            }
        ])

        candidate_data.to_excel(
            writer,
            sheet_name="Candidate",
            index=False
        )

        # --------------------------------------------
        # Education
        # --------------------------------------------

        education = candidate.get(
            "education",
            []
        )

        if education:

            pd.DataFrame(
                education
            ).to_excel(
                writer,
                sheet_name="Education",
                index=False
            )

        else:

            pd.DataFrame(
                columns=[
                    "degree",
                    "institution",
                    "year"
                ]
            ).to_excel(
                writer,
                sheet_name="Education",
                index=False
            )

        # --------------------------------------------
        # Skills
        # --------------------------------------------

        skills = candidate.get(
            "skills",
            []
        )

        pd.DataFrame(
            {
                "Skill": skills
            }
        ).to_excel(
            writer,
            sheet_name="Skills",
            index=False
        )

        # --------------------------------------------
        # Experience
        # --------------------------------------------

        experience = candidate.get(
            "experience",
            []
        )

        if experience:

            pd.DataFrame(
                experience
            ).to_excel(
                writer,
                sheet_name="Experience",
                index=False
            )

        else:

            pd.DataFrame(
                columns=[
                    "role",
                    "company",
                    "years"
                ]
            ).to_excel(
                writer,
                sheet_name="Experience",
                index=False
            )

        # --------------------------------------------
        # Projects
        # --------------------------------------------

        projects = candidate.get(
            "projects",
            []
        )

        if projects:

            pd.DataFrame(
                projects
            ).to_excel(
                writer,
                sheet_name="Projects",
                index=False
            )

        else:

            pd.DataFrame(
                columns=[
                    "name",
                    "summary"
                ]
            ).to_excel(
                writer,
                sheet_name="Projects",
                index=False
            )

    output.seek(0)

    return output.getvalue()


def initials(name):
    """
    Generate avatar initials.
    """

    if not name:
        return "CV"

    parts = str(name).split()

    if len(parts) == 1:
        return parts[0][:2].upper()

    return (
        parts[0][0] +
        parts[-1][0]
    ).upper()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
        <div class="brand">

            <div class="brand-icon">
                ◈
            </div>

            <div>

                <div class="brand-name">
                    TalentLens
                </div>

                <div class="brand-sub">
                    AI RECRUITMENT INTELLIGENCE
                </div>

            </div>

        </div>
        """
    )

    st.html(
        """
        <div class="sidebar-label">
            Analysis Pipeline
        </div>
        """
    )

    pipeline = [
        ("01", "Upload CV"),
        ("02", "Extract content"),
        ("03", "AI analysis"),
        ("04", "Structure data"),
        ("05", "Review candidate"),
        ("06", "Export profile"),
    ]

    for number, name in pipeline:

        active = (
            " active"
            if number in ["01", "02", "03"]
            else ""
        )

        st.html(
            f"""
            <div class="pipeline-item{active}">

                <div class="pipeline-number">
                    {number}
                </div>

                <div>
                    {name}
                </div>

            </div>
            """
        )

    st.html(
        """
        <div class="sidebar-label">
            AI Infrastructure
        </div>

        <div class="server-card">

            <div class="server-row">

                <div class="server-title">
                    AI Extraction Engine
                </div>

                <div class="server-dot"></div>

            </div>

            <div class="server-info">
                Google Colab · FastAPI · ngrok<br>
                Custom LLM inference
            </div>

        </div>
        """
    )


# ============================================================
# TOP BAR
# ============================================================

st.html(
    """
    <div class="topbar">

        <div class="topbar-left">
            Workspace / <span>Candidate Intelligence</span>
        </div>

        <div class="online-badge">

            <div class="online-dot"></div>

            AI ENGINE ONLINE

        </div>

    </div>
    """
)


# ============================================================
# HERO
# ============================================================

st.html(
    """
    <div class="hero">

        <div class="hero-content">

            <div class="hero-eyebrow">
                AI-POWERED TALENT INTELLIGENCE
            </div>

            <div class="hero-title">
                Turn resumes into
                <span>recruitment intelligence.</span>
            </div>

            <div class="hero-description">
                Upload a candidate CV and let your AI engine
                transform unstructured resume content into
                structured candidate data that can be reviewed,
                compared and exported.
            </div>

            <div class="hero-actions">

                <div class="hero-tag">
                    ◈ AI Extraction
                </div>

                <div class="hero-tag">
                    ◉ Structured Data
                </div>

                <div class="hero-tag">
                    ↗ Excel Export
                </div>

            </div>

        </div>

    </div>
    """
)


# ============================================================
# UPLOAD SECTION
# ============================================================

st.html(
    """
    <div class="upload-card">

        <div class="upload-heading">
            <span class="upload-icon">↥</span>
            Upload candidate CV
        </div>

        <div class="upload-subtitle">
            PDF resumes are extracted locally and sent securely
            to your AI analysis endpoint.
        </div>

    </div>
    """
)


uploaded_file = st.file_uploader(
    "Choose a PDF CV",
    type=["pdf"],
    label_visibility="collapsed"
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

if uploaded_file:

    st.markdown(
        f"""
        <div style="
            margin-top:10px;
            margin-bottom:10px;
            color:#64748b;
            font-size:10px;
        ">
            Selected file:
            <span style="color:#a5b4fc;">
                {html_escape(uploaded_file.name)}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    analyze_button = st.button(
        "✦  Analyze Candidate",
        use_container_width=True
    )

    if analyze_button:

        # ================================================
        # STEP 1 — PDF EXTRACTION
        # ================================================

        with st.status(
            "Analyzing candidate...",
            expanded=True
        ) as status:

            st.write(
                "Extracting text from PDF..."
            )

            try:

                cv_text = extract_pdf_text(
                    uploaded_file
                )

            except Exception as e:

                status.update(
                    label="PDF extraction failed",
                    state="error"
                )

                st.error(
                    str(e)
                )

                st.stop()

            if not cv_text:

                status.update(
                    label="No readable text found",
                    state="error"
                )

                st.error(
                    "The PDF does not contain readable text."
                )

                st.stop()

            st.write(
                f"Extracted approximately "
                f"{len(cv_text):,} characters."
            )

            # ============================================
            # STEP 2 — SEND TO AI
            # ============================================

            st.write(
                "Sending candidate data to AI engine..."
            )

            try:

                candidate = analyze_cv(
                    cv_text
                )

            except Exception as e:

                status.update(
                    label="AI analysis failed",
                    state="error"
                )

                st.error(
                    f"AI analysis failed:\n\n{e}"
                )

                st.stop()

            status.update(
                label="Candidate analyzed successfully",
                state="complete"
            )

        st.session_state["candidate"] = candidate

        st.session_state["cv_text"] = cv_text

        st.rerun()


# ============================================================
# DISPLAY RESULT
# ============================================================

if "candidate" in st.session_state:

    candidate = st.session_state["candidate"]

    # ========================================================
    # NORMALIZE DATA
    # ========================================================

    full_name = candidate.get(
        "full_name",
        "Unknown Candidate"
    )

    email = candidate.get(
        "email",
        "Email not provided"
    )

    education = candidate.get(
        "education",
        []
    )

    skills = candidate.get(
        "skills",
        []
    )

    experience = candidate.get(
        "experience",
        []
    )

    projects = candidate.get(
        "projects",
        []
    )


    # ========================================================
    # CANDIDATE PROFILE
    # ========================================================

    st.html(
        """
        <div class="section-header">

            <div class="section-left">

                <div class="section-icon">
                    ◉
                </div>

                <div class="section-title">
                    Candidate Intelligence
                </div>

            </div>

            <div class="section-caption">
                AI-generated profile
            </div>

        </div>
        """
    )

    profile_col, stats_col = st.columns(
        [1.55, 1],
        gap="medium"
    )


    # --------------------------------------------------------
    # PROFILE
    # --------------------------------------------------------

    with profile_col:

        safe_name = html_escape(
            full_name
        )

        safe_email = html_escape(
            email
        )

        avatar = initials(
            full_name
        )

        st.html(
            f"""
            <div class="profile-card">

                <div class="profile-glow"></div>

                <div class="avatar">
                    {html_escape(avatar)}
                </div>

                <div class="profile-label">
                    Candidate
                </div>

                <div class="profile-name">
                    {safe_name}
                </div>

                <div class="profile-email">
                    {safe_email}
                </div>

            </div>
            """
        )


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    with stats_col:

        m1, m2 = st.columns(2)

        with m1:

            st.html(
                f"""
                <div class="metric-card">

                    <div class="metric-icon">
                        ✦
                    </div>

                    <div class="metric-value">
                        {len(skills)}
                    </div>

                    <div class="metric-label">
                        Skills detected
                    </div>

                </div>
                """
            )

        with m2:

            st.html(
                f"""
                <div class="metric-card">

                    <div class="metric-icon">
                        ◈
                    </div>

                    <div class="metric-value">
                        {len(experience)}
                    </div>

                    <div class="metric-label">
                        Experience records
                    </div>

                </div>
                """
            )

        m3, m4 = st.columns(2)

        with m3:

            st.html(
                f"""
                <div class="metric-card">

                    <div class="metric-icon">
                        ⬡
                    </div>

                    <div class="metric-value">
                        {len(projects)}
                    </div>

                    <div class="metric-label">
                        Projects
                    </div>

                </div>
                """
            )

        with m4:

            st.html(
                f"""
                <div class="metric-card">

                    <div class="metric-icon">
                        🎓
                    </div>

                    <div class="metric-value">
                        {len(education)}
                    </div>

                    <div class="metric-label">
                        Education records
                    </div>

                </div>
                """
            )


    # ========================================================
    # EDUCATION + SKILLS
    # ========================================================

    education_col, skills_col = st.columns(
        [1.1, 0.9],
        gap="medium"
    )


    # --------------------------------------------------------
    # EDUCATION
    # --------------------------------------------------------

    with education_col:

        st.html(
            """
            <div class="section-header">

                <div class="section-left">

                    <div class="section-icon">
                        🎓
                    </div>

                    <div class="section-title">
                        Education
                    </div>

                </div>

            </div>
            """
        )

        if education:

            for edu in education:

                degree = html_escape(
                    edu.get(
                        "degree",
                        "Degree not specified"
                    )
                )

                institution = html_escape(
                    edu.get(
                        "institution",
                        "Institution not specified"
                    )
                )

                year = html_escape(
                    edu.get(
                        "year",
                        ""
                    )
                )

                year_html = ""

                if year:

                    year_html = f"""
                    <div class="edu-year">
                        {year}
                    </div>
                    """

                st.html(
                    f"""
                    <div class="edu-card">

                        <div class="edu-top">

                            <div>

                                <div class="edu-degree">
                                    {degree}
                                </div>

                                <div class="edu-institution">
                                    {institution}
                                </div>

                            </div>

                            {year_html}

                        </div>

                    </div>
                    """
                )

        else:

            st.info(
                "No education information detected."
            )


    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

    with skills_col:

        st.html(
            """
            <div class="section-header">

                <div class="section-left">

                    <div class="section-icon">
                        ✦
                    </div>

                    <div class="section-title">
                        Skills
                    </div>

                </div>

            </div>
            """
        )

        if skills:

            skills_html = """
            <div class="skills-container">
            """

            for skill in skills:

                skills_html += f"""
                <div class="skill">
                    {html_escape(skill)}
                </div>
                """

            skills_html += """
            </div>
            """

            st.html(
                skills_html
            )

        else:

            st.info(
                "No skills detected."
            )


    # ========================================================
    # EXPERIENCE
    # ========================================================

    st.html(
        """
        <div class="section-header">

            <div class="section-left">

                <div class="section-icon">
                    ◈
                </div>

                <div class="section-title">
                    Professional Experience
                </div>

            </div>

        </div>
        """
    )

    if experience:

        for exp in experience:

            role = html_escape(
                exp.get(
                    "role",
                    "Role not specified"
                )
            )

            company = html_escape(
                exp.get(
                    "company",
                    "Company not specified"
                )
            )

            years = html_escape(
                exp.get(
                    "years",
                    ""
                )
            )

            years_html = ""

            if years:

                years_html = f"""
                <div class="exp-years">
                    {years}
                </div>
                """

            st.html(
                f"""
                <div class="exp-card">

                    <div class="exp-indicator"></div>

                    <div class="exp-role">
                        {role}
                    </div>

                    <div class="exp-company">
                        {company}
                    </div>

                    {years_html}

                </div>
                """
            )

    else:

        st.info(
            "No professional experience detected."
        )


    # ========================================================
    # PROJECTS
    # ========================================================

    st.html(
        """
        <div class="section-header">

            <div class="section-left">

                <div class="section-icon">
                    ⬡
                </div>

                <div class="section-title">
                    Projects
                </div>

            </div>

            <div class="section-caption">
                Project portfolio and summaries
            </div>

        </div>
        """
    )

    if projects:

        number_of_columns = min(
            3,
            len(projects)
        )

        project_columns = st.columns(
            number_of_columns,
            gap="medium"
        )

        for index, project in enumerate(projects):

            # ------------------------------------------------
            # PROJECT NAME
            # ------------------------------------------------

            project_name = html_escape(
                project.get(
                    "name",
                    "Unnamed Project"
                )
            )

            # ------------------------------------------------
            # PROJECT SUMMARY
            # ------------------------------------------------

            project_summary = project.get(
                "summary",
                ""
            )

            # ------------------------------------------------
            # BACKWARD COMPATIBILITY
            #
            # If the old model still returns "link",
            # do NOT display the GitHub link.
            # Instead show a useful fallback message.
            # ------------------------------------------------

            if not project_summary:

                project_summary = (
                    project.get(
                        "description",
                        ""
                    )
                )

            if not project_summary:

                project_summary = (
                    "No project summary was extracted "
                    "from the candidate CV."
                )

            project_summary = html_escape(
                project_summary
            )

            # ------------------------------------------------
            # PROJECT CARD
            # ------------------------------------------------

            with project_columns[
                index % number_of_columns
            ]:

                st.html(
                    f"""
                    <div class="project-card">

                        <div class="project-icon">
                            ◇
                        </div>

                        <div class="project-name">
                            {project_name}
                        </div>

                        <div class="project-summary-label">
                            Project Overview
                        </div>

                        <div class="project-summary">
                            {project_summary}
                        </div>

                    </div>
                    """
                )

    else:

        st.info(
            "No projects detected."
        )


    # ========================================================
    # RAW AI JSON
    # ========================================================

    st.html(
        """
        <div class="section-header">

            <div class="section-left">

                <div class="section-icon">
                    {}
                </div>

                <div class="section-title">
                    Structured AI Data
                </div>

            </div>

            <div class="section-caption">
                Machine-readable output
            </div>

        </div>
        """
    )

    with st.expander(
        "View extracted JSON"
    ):

        st.json(
            candidate
        )


    # ========================================================
    # EXPORT
    # ========================================================

    st.html(
        """
        <div class="export-card">

            <div class="export-title">
                Export candidate intelligence
            </div>

            <div class="export-text">
                Download the structured candidate profile
                as an Excel workbook containing separate
                sheets for candidate information, education,
                skills, experience and projects with project
                summaries.
            </div>

        </div>
        """
    )

    excel_data = create_excel(
        candidate
    )

    filename_base = str(
        full_name
    ).strip().replace(
        " ",
        "_"
    )

    if not filename_base:
        filename_base = "candidate"

    st.download_button(
        label="↓  Download Candidate Excel Profile",
        data=excel_data,
        file_name=f"{filename_base}_profile.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument"
            ".spreadsheetml.sheet"
        ),
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">
        TALENTLENS AI · CV INTELLIGENCE PLATFORM
        · POWERED BY YOUR CUSTOM LLM
    </div>
    """
)