"""Shared visual language for Vigilantae Streamlit screens."""

import streamlit as st


def apply_theme() -> None:
    """Apply the classified investigation-console styling used throughout the app."""
    # st.html places the shared CSS in Streamlit's event container. This keeps the
    # visual system active when Streamlit switches between multipage screens.
    st.html(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700;800&display=swap');
        :root {
            --ink: #050607;
            --panel: #0e1114;
            --panel-raised: #15191d;
            --line: #30383e;
            --paper: #ecede7;
            --muted: #9da4a4;
            --signal: #dc1e28;
            --signal-dark: #8e1119;
            --amber: #dcab54;
            --steel: #879197;
        }
        .stApp {
            background:
                linear-gradient(90deg, rgba(3, 4, 5, .95) 0%, rgba(3, 4, 5, .88) 43%, rgba(3, 4, 5, .78) 100%),
                linear-gradient(180deg, rgba(5, 6, 7, .20), rgba(5, 6, 7, .88)),
                url('/app/static/vigilantae-classified-backdrop.png') center / cover fixed,
                var(--ink);
            color: var(--paper);
            font-family: Inter, sans-serif;
        }
        .stApp::before { content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0; opacity: .32; background: repeating-linear-gradient(0deg, transparent 0, transparent 3px, rgba(255,255,255,.025) 4px); }
        [data-testid="stHeader"] { background: rgba(5, 6, 7, .88); border-bottom: 1px solid rgba(220, 30, 40, .3); }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #0a0c0e, #080a0b); border-right: 1px solid #293136; }
        [data-testid="stSidebar"] * { color: var(--paper); }
        [data-testid="stSidebarNav"]::before { content: "VIGILANTAE // FIELD BUREAU"; display: block; color: var(--signal); font-family: 'IBM Plex Mono', monospace; font-size: .68rem; font-weight: 600; letter-spacing: .14em; padding: 1.25rem 1rem 1rem; border-bottom: 1px solid #2d181b; }
        [data-testid="stSidebarNav"] a { border-left: 3px solid transparent; border-radius: 0; margin: .18rem .55rem; padding: .62rem .7rem; font-size: .88rem; text-transform: uppercase; letter-spacing: .04em; }
        [data-testid="stSidebarNav"] a:hover, [data-testid="stSidebarNav"] a[aria-current="page"] { background: linear-gradient(90deg, #291115, transparent); border-left-color: var(--signal); }
        .block-container { max-width: 1180px; padding-top: 2.4rem; padding-bottom: 3rem; }
        h1, h2, h3, p, label, .stMarkdown { color: var(--paper); }
        h1, h2, h3 { font-family: 'Barlow Condensed', Impact, sans-serif; text-transform: uppercase; }
        h1 { letter-spacing: .015em; font-weight: 800; }
        h2, h3 { letter-spacing: .02em; }
        .vigilantae-kicker { color: #f04b52; font-family: 'IBM Plex Mono', monospace; font-size: .68rem; font-weight: 600; letter-spacing: .16em; margin-bottom: .55rem; }
        .vigilantae-heading { position: relative; border-left: 4px solid var(--signal); padding: .2rem 0 .2rem 1.1rem; margin: .7rem 0 1.8rem; }
        .vigilantae-heading::after { content: "RESTRICTED"; position: absolute; right: 0; top: .3rem; color: rgba(220,30,40,.55); font: 600 .6rem 'IBM Plex Mono', monospace; letter-spacing: .14em; border: 1px solid rgba(220,30,40,.35); padding: .3rem .45rem; }
        .vigilantae-heading h1 { margin: 0; font-size: clamp(2.25rem, 4vw, 3.55rem); line-height: .9; }
        .vigilantae-heading p { color: var(--muted); margin: .45rem 0 0; max-width: 45rem; }
        [data-testid="stMetric"], [data-testid="stForm"], [data-testid="stExpander"], [data-testid="stFileUploader"], [data-testid="stDataFrame"] { background: linear-gradient(140deg, rgba(11,13,15,.98), rgba(3,4,5,.96)); border: 1px solid var(--line); border-radius: 2px; box-shadow: inset 0 1px rgba(255,255,255,.025), 0 14px 32px rgba(0,0,0,.46); }
        [data-testid="stMetric"] { padding: 1rem; border-top: 2px solid var(--signal); position: relative; overflow: hidden; }
        [data-testid="stMetric"]::after { content: ""; position: absolute; width: 50px; height: 1px; background: var(--signal); right: -10px; bottom: 9px; transform: rotate(-45deg); opacity: .7; }
        [data-testid="stMetricLabel"] p { color: var(--muted) !important; font-family: 'IBM Plex Mono', monospace; font-size: .68rem; letter-spacing: .08em; text-transform: uppercase; }
        [data-testid="stMetricValue"] { color: var(--paper); }
        [data-testid="stForm"] { padding: 1.2rem; }
        [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stNumberInput"] input, [data-baseweb="select"] > div {
            background: #0e1218 !important; color: var(--paper) !important; border-color: #3b4654 !important; border-radius: 7px !important;
        }
        [data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus { border-color: var(--signal) !important; box-shadow: 0 0 0 1px var(--signal) !important; }
        [data-testid="stButton"] button, [data-testid="stDownloadButton"] button, [data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #e2333c, #a4141c) !important; color: white !important; border: 1px solid #f15b62 !important; border-radius: 2px !important; font-family: 'IBM Plex Mono', monospace !important; font-weight: 600 !important; letter-spacing: .05em; text-transform: uppercase; box-shadow: 0 4px 15px rgba(156, 12, 20, .25); }
        [data-testid="stButton"] button:hover, [data-testid="stDownloadButton"] button:hover, [data-testid="stFormSubmitButton"] button:hover { background: #7f1017 !important; border-color: #ff817b !important; transform: translateY(-1px); }
        [data-testid="stAlert"] { border-radius: 8px; }
        hr { border-color: var(--line); margin: 1.6rem 0; }
        [data-testid="stFileUploaderDropzone"] { background: #10151c; border: 1px dashed #6d3740; border-radius: 9px; }
        .stProgress > div > div { background-color: var(--signal); }
        .classification-ribbon { position: relative; z-index: 1; height: 28px; margin: -1.55rem 0 1.5rem; overflow: hidden; background: #a71118; border-block: 1px solid #f35b60; box-shadow: 0 4px 15px rgba(0,0,0,.32); }
        .classification-ribbon__track { display: inline-block; white-space: nowrap; min-width: 100%; padding-top: 5px; color: #fff3ea; font: 600 .66rem 'IBM Plex Mono', monospace; letter-spacing: .19em; animation: security-ticker 22s linear infinite; }
        .classification-ribbon__track span { margin-right: 3rem; }
        .security-status { display: flex; align-items: center; gap: .65rem; padding: .6rem .75rem; margin: 0 0 1.2rem; border: 1px solid #363c40; background: rgba(12,15,17,.86); color: var(--muted); font: .64rem 'IBM Plex Mono', monospace; letter-spacing: .1em; }
        .security-status b { color: #f24b52; font-weight: 600; }
        .security-status i { width: 7px; height: 7px; background: #e12a33; border-radius: 50%; box-shadow: 0 0 10px #e12a33; animation: status-blink 1s steps(2, jump-none) infinite; }
        @keyframes security-ticker { from { transform: translateX(0); } to { transform: translateX(-39%); } }
        @keyframes status-blink { 50% { opacity: .2; } }
        @media (prefers-reduced-motion: reduce) { .classification-ribbon__track, .security-status i { animation: none; } }
        .agent-identity { display: flex; align-items: center; gap: 1rem; margin: -.15rem 0 1.5rem; padding: 1rem 1.15rem; background: linear-gradient(100deg, rgba(30,15,17,.86), rgba(14,17,20,.9)); border: 1px solid #3d3032; border-left: 3px solid var(--signal); }
        .agent-identity__seal { width: 38px; height: 38px; display: grid; place-items: center; border: 1px solid #e0444b; border-radius: 50%; color: #f04a52; font-size: 1.1rem; }
        .agent-identity__label { color: var(--muted); font: .63rem 'IBM Plex Mono', monospace; letter-spacing: .13em; text-transform: uppercase; }
        .agent-identity__name { margin-top: .15rem; color: var(--paper); font: 700 1.5rem 'Barlow Condensed', sans-serif; letter-spacing: .06em; text-transform: uppercase; }
        .agent-identity__meta { margin-left: auto; text-align: right; color: var(--muted); font: .68rem 'IBM Plex Mono', monospace; line-height: 1.6; }
        .agent-role { display: inline-block; color: #fff; background: #8c161d; padding: .12rem .42rem; font-weight: 600; }
        @media (max-width: 640px) { .block-container { padding: 1.15rem .9rem 2rem; } .vigilantae-heading h1 { font-size: 2rem; } }
        </style>
        <div class="classification-ribbon" aria-label="Security notice"><div class="classification-ribbon__track"><span>⚠ AUTHORIZED PERSONNEL ONLY</span><span>VIGILANTAE // ACTIVE CASE INTELLIGENCE</span><span>⚠ DO NOT DISTRIBUTE</span><span>AUTHORIZED PERSONNEL ONLY</span><span>VIGILANTAE // ACTIVE CASE INTELLIGENCE</span><span>⚠ DO NOT DISTRIBUTE</span></div></div>
        <div class="security-status"><i></i><b>LIVE / SECURE CHANNEL</b><span>CASE INTELLIGENCE NETWORK · ENCRYPTED SESSION · ACCESS LOGGED</span></div>
        """,
    )


def page_header(title: str, description: str, kicker: str = "CASE MANAGEMENT SYSTEM") -> None:
    """Render a compact, consistent title treatment for an app screen."""
    st.markdown(
        f'''<div class="vigilantae-heading"><div class="vigilantae-kicker">{kicker}</div><h1>{title}</h1><p>{description}</p></div>''',
        unsafe_allow_html=True,
    )
