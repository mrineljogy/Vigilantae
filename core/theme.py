"""Visual system for the Vigilantae evidence-review console."""

import streamlit as st


def apply_console_theme():
    st.html("""
    <style>
      :root { --paper: #f5f3ed; --muted: #b9bec3; --red: #f23a45; --deep-red: #8b121c; --panel: rgba(10, 13, 16, .84); --edge: rgba(255,255,255,.12); }
      .stApp { background-image: linear-gradient(105deg, rgba(3, 5, 8, .90), rgba(4, 7, 10, .76)), url('/app/static/vigilantae-classified-backdrop.png'); background-position: center; background-size: cover; background-attachment: fixed; color: var(--paper); }
      .main .block-container { max-width: 1240px; padding-top: 1.5rem; padding-bottom: 3rem; }
      [data-testid='stSidebar'] { background: linear-gradient(180deg, rgba(7,9,12,.98), rgba(13,15,18,.96)); border-right: 1px solid rgba(242,58,69,.25); }
      [data-testid='stSidebar'] [data-testid='stRadio'] { border-top: 1px solid rgba(255,255,255,.1); padding-top: 1rem; }
      [data-testid='stSidebar'] label { border-left: 2px solid transparent; padding: .32rem .45rem; transition: .2s ease; }
      [data-testid='stSidebar'] label:hover { background: rgba(242,58,69,.10); border-left-color: var(--red); }
      h1 { font-size: clamp(2rem, 4vw, 3.4rem) !important; letter-spacing: .08em !important; line-height: 1.05 !important; text-transform: uppercase; }
      h2, h3 { letter-spacing: .05em; text-transform: uppercase; }
      [data-testid='stForm'], [data-testid='stMetric'], [data-testid='stDataFrame'], [data-testid='stVerticalBlockBorderWrapper'] { background: var(--panel); border: 1px solid var(--edge); border-radius: 10px; backdrop-filter: blur(12px); }
      [data-testid='stForm'] { padding: 1.35rem; }
      [data-testid='stMetric'] { padding: 1rem; border-top: 3px solid var(--red); box-shadow: 0 12px 30px rgba(0,0,0,.2); }
      [data-testid='stTextInput'] input, [data-testid='stTextArea'] textarea, [data-testid='stNumberInput'] input { background: rgba(3,5,8,.72) !important; border: 1px solid rgba(255,255,255,.15) !important; border-radius: 7px !important; color: var(--paper) !important; }
      [data-testid='stTextInput'] input:focus, [data-testid='stTextArea'] textarea:focus { border-color: var(--red) !important; box-shadow: 0 0 0 1px var(--red) !important; }
      [data-testid='stButton'] button, [data-testid='stFormSubmitButton'] button { min-height: 2.65rem; padding: 0 .95rem; background: linear-gradient(135deg, #ef3c48, #981923) !important; color: white !important; border: 1px solid #ff626b !important; border-radius: 7px !important; font-weight: 800 !important; letter-spacing: .04em; box-shadow: 0 8px 22px rgba(128, 12, 20, .28); transition: transform .18s ease, box-shadow .18s ease; }
      [data-testid='stButton'] button:hover, [data-testid='stFormSubmitButton'] button:hover { transform: translateY(-1px); box-shadow: 0 12px 28px rgba(210, 25, 39, .42); }
      .vigilantae-ribbon { position: relative; width: 100%; overflow: hidden; padding: .72rem 0; margin: 0 0 1.25rem; background: linear-gradient(90deg, #750d15, #d42230 42%, #8b111b); color: #fff; border: 1px solid rgba(255,255,255,.32); font: 800 .72rem ui-monospace, SFMono-Regular, Menlo, monospace; letter-spacing: .15em; white-space: nowrap; box-shadow: 0 8px 22px rgba(0,0,0,.22); }
      .vigilantae-ribbon span { display: inline-block; min-width: 150%; animation: vigilantae-sweep 16s linear infinite; }
      .status-pulse { display: inline-flex; align-items: center; gap: .5rem; color: #ff6871; font: 700 .76rem ui-monospace, SFMono-Regular, Menlo, monospace; letter-spacing: .09em; }
      .status-pulse::before { content: ''; width: 8px; height: 8px; background: var(--red); border-radius: 100%; animation: vigilantae-pulse 1.2s ease-in-out infinite; }
      .console-hero { position: relative; overflow: hidden; padding: 1.75rem 1.8rem; margin: .25rem 0 1.35rem; background: linear-gradient(110deg, rgba(16,19,23,.92), rgba(16,19,23,.54)); border: 1px solid var(--edge); border-left: 4px solid var(--red); border-radius: 10px; }
      .console-hero::after { content: 'VIGILANTAE'; position:absolute; right: 1.2rem; top: .6rem; color: rgba(255,255,255,.04); font: 900 4rem/1 sans-serif; letter-spacing: .08em; }
      .console-hero .eyebrow { color: #ff747c; font: 700 .72rem ui-monospace, SFMono-Regular, Menlo, monospace; letter-spacing: .17em; }
      .console-hero .title { margin: .45rem 0 .35rem; color: var(--paper); font-size: clamp(1.6rem,3vw,2.5rem); font-weight: 800; letter-spacing: .055em; text-transform: uppercase; }
      .console-hero .subtitle { color: var(--muted); max-width: 48rem; }
      .face-scan-panel { position: relative; overflow: hidden; margin: .2rem 0 1rem; padding: 1rem 1.1rem; background: linear-gradient(135deg, rgba(155,19,31,.22), rgba(6,10,13,.84)); border: 1px solid rgba(242,58,69,.45); border-radius: 8px; }
      .face-scan-panel .scan-line { position: absolute; left: 0; right: 0; top: 0; height: 2px; background: #ff5661; box-shadow: 0 0 16px #ff5661; animation: scan 2.8s linear infinite; }
      .face-scan-panel strong { display:block; font: 800 .77rem ui-monospace, SFMono-Regular, Menlo, monospace; letter-spacing:.12em; color:#ff747c; }
      .face-scan-panel small { color: var(--muted); }
      @keyframes vigilantae-sweep { from { transform: translateX(0); } to { transform: translateX(-33%); } }
      @keyframes vigilantae-pulse { 50% { opacity: .18; transform: scale(.65); box-shadow: 0 0 14px var(--red); } }
      @keyframes scan { from { transform: translateY(0); } to { transform: translateY(112px); } }
    </style>
    <div class='vigilantae-ribbon'><span>◆ LOCAL DEMONSTRATION &nbsp; ◆ HUMAN REVIEW REQUIRED &nbsp; ◆ VIGILANTAE CASE CONSOLE &nbsp; ◆ PHOTO ANALYSIS ACTIVE &nbsp; ◆ NO EMERGENCY DISPATCH &nbsp; ◆ LOCAL DEMONSTRATION &nbsp; ◆</span></div>
    """)


def render_hero(eyebrow: str, title: str, subtitle: str):
    st.html(f"""<section class='console-hero'><div class='eyebrow'>{eyebrow}</div><div class='title'>{title}</div><div class='subtitle'>{subtitle}</div></section>""")


def render_face_scan_panel():
    st.html("""<div class='face-scan-panel'><div class='scan-line'></div><strong>PHOTO ANALYSIS ENGINE</strong><small>Front-facing face detection and visual lead signal. Human validation is always required.</small></div>""")
