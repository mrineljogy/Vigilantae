import streamlit as st


def apply_console_theme():
    st.markdown(f"""<style>
    .stApp {{ background: radial-gradient(circle at 70% 0%, #251014 0%, #080a0c 42%); color: #f1f1ed; }}
    [data-testid='stSidebar'] {{ background: #0c0e11; border-right: 1px solid #402025; }}
    h1, h2, h3 {{ letter-spacing: .06em; text-transform: uppercase; }}
    [data-testid='stMetric'] {{ border: 1px solid #4d252b; border-top: 3px solid #dc2833; padding: 1rem; background: rgba(16, 19, 22, .92); }}
    [data-testid='stButton'] button {{ background: #bf202a; color: #fff; border: 0; border-radius: 2px; font-weight: 700; }}
    [data-testid='stDataFrame'], [data-testid='stForm'] {{ border: 1px solid #363b3f; background: rgba(16, 19, 22, .94); padding: 1rem; }}
    .classification-strip {{ background: #b91e28; color: #fff; font: 700 12px monospace; letter-spacing: .16em; padding: .65rem 1rem; text-align: center; white-space: nowrap; overflow: hidden; }}
    .classification-strip span {{ display: inline-block; animation: sweep 18s linear infinite; }}
    @keyframes sweep {{ from {{ transform: translateX(12%); }} to {{ transform: translateX(-12%); }} }}
    </style>
    <div class='classification-strip'><span>◆ LOCAL DEMONSTRATION · HUMAN REVIEW REQUIRED · VIGILANTAE CASE CONSOLE · NO EMERGENCY DISPATCH ◆</span></div>""", unsafe_allow_html=True)
