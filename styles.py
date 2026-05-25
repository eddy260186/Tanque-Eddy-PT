import streamlit as st


def aplicar_diseno_elite():
    st.markdown("""
    <style>
    :root {
        --elite-bg: #0b0e14;
        --elite-surface: #121722;
        --elite-surface-2: #171d2a;
        --elite-border: rgba(212, 175, 55, 0.36);
        --elite-gold: #d4af37;
        --elite-gold-soft: #f4d47c;
        --elite-text: #f7f7f2;
        --elite-muted: #b7bdca;
        --elite-danger: #ff6b6b;
    }

    .stApp {
        background: var(--elite-bg) !important;
        color: var(--elite-text) !important;
        font-family: "Segoe UI", Arial, sans-serif;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    section[data-testid="stSidebar"] {
        background: var(--elite-surface) !important;
        border-right: 1px solid var(--elite-border) !important;
        box-shadow: 6px 0 24px rgba(0, 0, 0, 0.24);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    h1, h2, h3 {
        color: var(--elite-gold-soft) !important;
        font-weight: 750 !important;
        letter-spacing: 0 !important;
        line-height: 1.18 !important;
    }

    h4, h5, h6, p, label, span, div {
        letter-spacing: 0 !important;
    }

    .stMarkdown, .stCaption, label, p {
        color: var(--elite-text);
    }

    .stCaption, small, [data-testid="stCaptionContainer"] {
        color: var(--elite-muted) !important;
    }

    .stButton > button,
    .stDownloadButton > button,
    .stLinkButton > a {
        min-height: 44px;
        border-radius: 8px !important;
        border: 1px solid rgba(244, 212, 124, 0.55) !important;
        background: linear-gradient(180deg, #f2d177 0%, #d4af37 100%) !important;
        color: #111318 !important;
        font-weight: 750 !important;
        box-shadow: 0 8px 18px rgba(212, 175, 55, 0.16) !important;
        transition: transform 120ms ease, box-shadow 120ms ease, filter 120ms ease;
        width: 100%;
        white-space: normal;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stLinkButton > a:hover {
        transform: translateY(-1px);
        filter: brightness(1.04);
        box-shadow: 0 10px 22px rgba(212, 175, 55, 0.24) !important;
    }

    .stButton > button:disabled {
        background: var(--elite-surface-2) !important;
        border-color: rgba(212, 175, 55, 0.22) !important;
        color: var(--elite-muted) !important;
        box-shadow: none !important;
        transform: none !important;
    }

    [data-testid="stMetric"] {
        background: var(--elite-surface-2) !important;
        padding: 16px !important;
        border-radius: 8px !important;
        border: 1px solid var(--elite-border) !important;
        box-shadow: none !important;
    }

    [data-testid="stMetricLabel"] p {
        color: var(--elite-muted) !important;
        font-size: 0.92rem !important;
    }

    [data-testid="stMetricValue"] {
        color: var(--elite-gold-soft) !important;
        font-weight: 750 !important;
        font-size: clamp(1.2rem, 2vw, 1.8rem) !important;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"] textarea,
    .stNumberInput input,
    .stTextInput input {
        background-color: var(--elite-surface-2) !important;
        border: 1px solid rgba(212, 175, 55, 0.28) !important;
        border-radius: 8px !important;
        color: var(--elite-text) !important;
        box-shadow: none !important;
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="textarea"] textarea:focus,
    .stNumberInput input:focus,
    .stTextInput input:focus {
        border-color: var(--elite-gold-soft) !important;
        box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.18) !important;
    }

    div[data-testid="stTabs"] button {
        color: var(--elite-muted) !important;
        font-weight: 700 !important;
        white-space: normal;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--elite-gold-soft) !important;
    }

    hr, [data-testid="stDivider"] {
        border-color: rgba(212, 175, 55, 0.16) !important;
    }

    .stAlert {
        border-radius: 8px !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 1rem 2rem !important;
            max-width: 100% !important;
        }

        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.45rem !important; }
        h3 { font-size: 1.18rem !important; }

        [data-testid="stMetric"] {
            padding: 14px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
