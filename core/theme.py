"""Visual treatment for the Vigilantae portfolio console."""

import streamlit as st


def apply_console_theme():
    st.html("""
    <style>
      .stApp { background-image: linear-gradient(rgba(3, 5, 7, .82), rgba(3, 5, 7, .92)), url('/app/static/vigilantae-classified-backdrop.png'); background-position: center; background-size: cover; background-attachment: fixed; color: #f5f2ed; }
      [data-testid='stSidebar'] { background: rgba(8, 10, 12, .96); border-right: 1px solid #4e2429; }
      [data-testid='stSidebar'] * { color: #f5f2ed; }
      h1, h2, h3 { letter-spacing: .06em; text-transform: uppercase; }
      [data-testid='stMetric'], [data-testid='stForm'], [data-testid='stDataFrame'] { border: 1px solid #493239; background: rgba(11, 14, 17, .90); padding: 1rem; }
      [data-testid='stMetric'] { border-top: 3px solid #df2d38; }
      [data-testid='stButton'] button { background: linear-gradient(135deg, #dc2834, #8e151e); color: white; border: 1px solid #f34c55; border-radius: 2px; font-weight: 800; letter-spacing: .04em; }
      .vigilantae-ribbon { position: relative; width: 100%; overflow: hidden; padding: .62rem 0; margin: 0 0 1rem; background: #b81724; color: #fff; border-top: 1px solid #f35a62; border-bottom: 1px solid #7d0d16; font: 700 .78rem ui-monospace, SFMono-Regular, Menlo, monospace; letter-spacing: .14em; white-space: nowrap; }
      .vigilantae-ribbon span { display: inline-block; min-width: 120%; animation: vigilantae-sweep 16s linear infinite; }
      .status-pulse { color: #ff4a55; animation: vigilantae-pulse 1.15s ease-in-out infinite; }
      @keyframes vigilantae-sweep { from { transform: translateX(0); } to { transform: translateX(-18%); } }
      @keyframes vigilantae-pulse { 50% { opacity: .25; text-shadow: 0 0 12px #f22; } }
    </style>
    <div class='vigilantae-ribbon'><span>◆ LOCAL DEMONSTRATION &nbsp; ◆ HUMAN REVIEW REQUIRED &nbsp; ◆ VIGILANTAE CASE CONSOLE &nbsp; ◆ NO EMERGENCY DISPATCH &nbsp; ◆ LOCAL DEMONSTRATION &nbsp; ◆ HUMAN REVIEW REQUIRED &nbsp; ◆</span></div>
    """)
