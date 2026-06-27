import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
from io import BytesIO
import matplotlib.pyplot as plt
import urllib.parse
import textwrap
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

st.set_page_config(
    page_title="ProjectRescue AI",
    page_icon="🟥",
    layout="wide"
)

# -----------------------------
# PREMIUM UI STYLE
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(229,9,20,0.18), transparent 30%),
        radial-gradient(circle at top right, rgba(255,255,255,0.05), transparent 25%),
        linear-gradient(135deg, #050505 0%, #0B0B0B 50%, #111111 100%);
    color: #FFFFFF;
}

.block-container {
    padding-top: 1.5rem;
    padding-left: 3.5rem;
    padding-right: 3.5rem;
    max-width: 1500px;
}

h1, h2, h3, h4, h5, h6, p, label, span {
    color: #F5F5F5 !important;
}

.hero {
    background: linear-gradient(135deg, rgba(20,20,20,0.95), rgba(8,8,8,0.95));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 28px;
    padding: 34px 38px;
    margin-bottom: 28px;
    box-shadow: 0 28px 80px rgba(0,0,0,0.6);
}

.hero-title {
    font-size: 48px;
    font-weight: 900;
    letter-spacing: -1.5px;
    margin-bottom: 8px;
}

.hero-title span {
    color: #E50914 !important;
}

.hero-subtitle {
    font-size: 18px;
    color: #CCCCCC !important;
}

.hero-brand {
    font-size: 13px;
    color: #888888 !important;
    margin-top: 14px;
}

.panel {
    background: rgba(18,18,18,0.88);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 26px;
    margin-top: 18px;
    margin-bottom: 18px;
    box-shadow: 0 18px 50px rgba(0,0,0,0.45);
}

.result-card {
    padding: 32px;
    border-radius: 28px;
    margin: 28px 0;
    box-shadow: 0 28px 80px rgba(0,0,0,0.55);
}

.green-card {
    background: linear-gradient(135deg, #062C1B, #0E6B3A);
    border: 1px solid #2ECC71;
}

.amber-card {
    background: linear-gradient(135deg, #2D1C00, #A96A00);
    border: 1px solid #F39C12;
}

.red-card {
    background: linear-gradient(135deg, #2B0000, #990000);
    border: 1px solid #E50914;
}

.result-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 18px;
    margin-top: 26px;
}

.result-metric {
    background: rgba(0,0,0,0.32);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 18px;
}

.result-label {
    font-size: 12px;
    color: #BBBBBB !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.result-value {
    font-size: 30px;
    font-weight: 900;
    margin-top: 8px;
}

[data-testid="stTabs"] button {
    background: #151515 !important;
    border-radius: 14px 14px 0 0 !important;
    color: #BBBBBB !important;
    font-weight: 700 !important;
    padding: 14px 20px !important;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    color: #FFFFFF !important;
    border-bottom: 3px solid #E50914 !important;
}

/* Primary Streamlit buttons */
.stButton button {
    background: #181818 !important;
    color: #F5F5F5 !important;
    border: 1px solid #333333 !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    padding: 0.75rem 1.4rem !important;
    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
}

.stButton button:hover {
    background: #242424 !important;
    color: #FFFFFF !important;
    border: 1px solid #E50914 !important;
    box-shadow: 0 0 18px rgba(229,9,20,0.28);
}

.stLinkButton a {
    background: #181818 !important;
    color: #F5F5F5 !important;
    border: 1px solid #333333 !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    padding: 0.75rem 1.4rem !important;
    text-decoration: none !important;
    box-shadow: 0 12px 30px rgba(0,0,0,0.30);
}

.stLinkButton a:hover {
    background: #242424 !important;
    color: #FFFFFF !important;
    border: 1px solid #E50914 !important;
    box-shadow: 0 0 18px rgba(229,9,20,0.28);
}

.stDownloadButton button {
    background: linear-gradient(135deg, #E50914, #B00610) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    padding: 0.75rem 1.4rem !important;
    box-shadow: 0 12px 30px rgba(229,9,20,0.25);
}

.stDownloadButton button:hover {
    background: linear-gradient(135deg, #FF2333, #E50914) !important;
}

[data-testid="stFileUploader"] section {
    background: #181818 !important;
    border: 1px solid #333333 !important;
    border-radius: 14px !important;
}

[data-testid="stFileUploader"] section * {
    color: #F5F5F5 !important;
}

.stNumberInput input, .stTextInput input {
    background-color: #181818 !important;
    color: #FFFFFF !important;
    border: 1px solid #333333 !important;
    border-radius: 12px !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #181818 !important;
    color: #FFFFFF !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploader"] {
    background: #121212 !important;
    border: 1px dashed #444444 !important;
    border-radius: 18px !important;
    padding: 18px !important;
}

[data-testid="stFileUploader"] section {
    background: #181818 !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 16px !important;
}

[data-testid="stFileUploader"] button {
    background: #151515 !important;
    color: #F5F5F5 !important;
    border: 1px solid #333333 !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploader"] button:hover {
    border: 1px solid #E50914 !important;
    color: #FFFFFF !important;
}

.badge {
    padding: 6px 12px;
    border-radius: 999px;
    font-weight: 800;
    font-size: 13px;
}

.badge-green { background:#0E6B3A; color:#FFFFFF; }
.badge-amber { background:#A96A00; color:#FFFFFF; }
.badge-red { background:#990000; color:#FFFFFF; }

.footer {
    color: #777777;
    margin-top: 50px;
    padding-top: 22px;
    border-top: 1px solid #222222;
    font-size: 13px;
}

.health-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-top: 16px;
}
.health-tile {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 16px;
}
.health-name {
    font-size: 13px;
    color: #BDBDBD !important;
    margin-bottom: 8px;
}
.health-value {
    font-size: 18px;
    font-weight: 900;
}
.health-green { border-left: 5px solid #2ECC71; }
.health-amber { border-left: 5px solid #F39C12; }
.health-red { border-left: 5px solid #E74C3C; }
.driver-table {
    width:100%;
    border-collapse: collapse;
    margin-top: 14px;
    margin-bottom: 20px;
}
.driver-table th, .driver-table td {
    border-bottom: 1px solid rgba(255,255,255,0.10);
    padding: 12px;
    text-align: left;
}
.driver-table th { color:#BDBDBD !important; font-size:12px; text-transform:uppercase; }
.driver-badge { padding: 5px 10px; border-radius: 999px; font-weight: 800; font-size: 12px; }
.driver-high { background:#8B0000; color:white; }
.driver-medium { background:#9A6500; color:white; }
.driver-low { background:#0E6B3A; color:white; }
.driver-critical { background:#8B0000; color:white; }
.driver-watchlist { background:#9A6500; color:white; }



/* =============================
   FINAL INPUT BORDER FIX
   Removes white Streamlit/BaseWeb outlines
   ============================= */

.stTextInput input,
.stNumberInput input{
    background: linear-gradient(180deg, #161616 0%, #111111 100%) !important;
    color:#F5F5F5 !important;
    border:1px solid #2A2A2A !important;
    border-radius:14px !important;
    box-shadow:none !important;
    outline:none !important;
}

.stTextInput input:hover,
.stNumberInput input:hover{
    border:1px solid #3A3A3A !important;
    box-shadow:none !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextInput input:focus-visible,
.stNumberInput input:focus-visible{
    border:1px solid #E50914 !important;
    box-shadow:0 0 12px rgba(229,9,20,.35) !important;
    outline:none !important;
}

[data-baseweb="input"],
[data-baseweb="input"] > div{
    background:#141414 !important;
    border:1px solid #2A2A2A !important;
    border-radius:14px !important;
    box-shadow:none !important;
    outline:none !important;
}

[data-baseweb="input"]:focus-within,
[data-baseweb="input"] > div:focus-within{
    border:1px solid #E50914 !important;
    box-shadow:0 0 12px rgba(229,9,20,.35) !important;
    outline:none !important;
}

.stNumberInput button,
.stNumberInput [data-testid="stNumberInputStepUp"],
.stNumberInput [data-testid="stNumberInputStepDown"]{
    background:#181818 !important;
    border:1px solid #2A2A2A !important;
    color:#E5E5E5 !important;
    box-shadow:none !important;
}

.stNumberInput button:hover,
.stNumberInput [data-testid="stNumberInputStepUp"]:hover,
.stNumberInput [data-testid="stNumberInputStepDown"]:hover{
    background:#252525 !important;
    border:1px solid #E50914 !important;
    color:#FFFFFF !important;
}

.stSelectbox div[data-baseweb="select"],
.stSelectbox div[data-baseweb="select"] > div{
    background:#141414 !important;
    border:1px solid #2A2A2A !important;
    border-radius:14px !important;
    box-shadow:none !important;
    outline:none !important;
}

.stSelectbox div[data-baseweb="select"]:hover,
.stSelectbox div[data-baseweb="select"]:focus-within{
    border:1px solid #E50914 !important;
    box-shadow:0 0 12px rgba(229,9,20,.28) !important;
}

[data-testid="stFileUploader"] section{
    background:#141414 !important;
    border:1px solid #2A2A2A !important;
    border-radius:14px !important;
    box-shadow:none !important;
}

[data-testid="stFileUploader"] section:hover{
    border:1px solid #E50914 !important;
    box-shadow:0 0 12px rgba(229,9,20,.20) !important;
}

/* Remove browser autofill white flash */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus{
    -webkit-text-fill-color:#F5F5F5 !important;
    transition: background-color 9999s ease-in-out 0s !important;
    box-shadow:0 0 0px 1000px #141414 inset !important;
}



/* =============================
   EXECUTIVE SECTION / TABLE POLISH
   ============================= */
.exec-section-header {
    width: 100%;
    background: linear-gradient(135deg, rgba(120,0,0,0.62), rgba(28,12,12,0.96), rgba(16,16,16,0.96));
    border: 1px solid rgba(255,77,79,0.32);
    border-left: 8px solid #FF4D4F;
    border-radius: 18px;
    padding: 18px 22px;
    margin: 34px 0 22px 0;
    box-shadow: 0 18px 42px rgba(0,0,0,0.40), 0 0 24px rgba(229,9,20,0.14);
}
.exec-section-title {
    font-size: 27px;
    font-weight: 900;
    color: #FFFFFF !important;
    letter-spacing: -0.4px;
    margin: 0;
}
.exec-section-subtitle {
    font-size: 13px;
    color: #CFCFCF !important;
    margin-top: 6px;
}
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, rgba(229,9,20,0.55), rgba(255,255,255,0.08), transparent);
    margin: 26px 0;
}
.portfolio-summary-card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 18px 20px;
    margin: 10px 0 22px 0;
    line-height: 1.65;
}
.table-note {
    color: #BDBDBD !important;
    font-size: 13px;
    margin-top: 10px;
}
.driver-table th {
    text-align: center !important;
    font-weight: 900 !important;
    color: #FFFFFF !important;
    background: rgba(255,255,255,0.055) !important;
}
.driver-table td {
    vertical-align: middle !important;
}
.driver-table td:nth-child(2),
.driver-table td:nth-child(3),
.driver-table td:nth-child(4),
.driver-table td:nth-child(5) {
    text-align: center !important;
}
[data-testid="stDataFrame"] thead tr th,
[data-testid="stTable"] thead tr th {
    text-align: center !important;
    font-weight: 900 !important;
    color: #111827 !important;
}
[data-testid="stMetric"] {
    padding: 6px 0 12px 0;
}


/* =============================
   CREATOR JOURNEY - PREMIUM ROAD STORY
   ============================= */
/* =============================
   PREMIUM CREATOR JOURNEY UI
   ============================= */
.cj-wrap{
    background: radial-gradient(circle at 72% 18%, rgba(255,77,79,0.14), transparent 32%),
                linear-gradient(135deg, rgba(8,12,18,0.96), rgba(5,7,11,0.98));
    border:1px solid rgba(255,255,255,0.10);
    border-radius:22px;
    padding:18px 22px 20px 22px;
    margin:16px 0 24px 0;
    box-shadow:0 28px 90px rgba(0,0,0,.65), inset 0 0 0 1px rgba(255,255,255,.03);
}
.cj-topbar{display:grid; grid-template-columns:1.8fr 1fr; gap:18px; align-items:center; margin-bottom:20px;}
.cj-brand{display:flex; align-items:center; gap:14px;}
.cj-logo{width:56px; height:56px; border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:21px; font-weight:950; color:#FFF !important; background:linear-gradient(135deg, rgba(255,255,255,.09), rgba(10,10,10,.95)); border:1px solid rgba(255,77,79,.45); box-shadow:0 10px 28px rgba(0,0,0,.55);}
.cj-brand-title{font-size:26px; font-weight:950; color:#FFF !important; letter-spacing:-.4px; line-height:1.05;}
.cj-brand-title span{color:#FF4D4F !important;}
.cj-brand-sub{font-size:12px; color:#C9D1D9 !important; margin-top:5px;}
.cj-headline{text-align:center;}
.cj-headline h2{font-size:38px; margin:0; color:#FFF !important; font-weight:950; letter-spacing:-.8px;}
.cj-headline p{margin:6px 0 0 0; color:#C9D1D9 !important; font-size:15px;}
.cj-headline-line{height:3px; width:220px; margin:13px auto 0; background:linear-gradient(90deg, transparent, #FF4D4F, transparent); border-radius:999px;}
.cj-road-note{justify-self:end; display:flex; gap:14px; align-items:center; max-width:310px; padding:14px 18px; border-radius:16px; background:linear-gradient(135deg, rgba(255,77,79,.19), rgba(255,255,255,.05)); border:1px solid rgba(255,255,255,.08);}
.cj-road-note-icon{font-size:28px; color:#FF4D4F !important;}
.cj-road-note b{color:#FFF !important; font-size:15px;}
.cj-road-note div{color:#C9D1D9 !important; font-size:12px; line-height:1.35;}
.cj-grid{display:grid; grid-template-columns:390px 1fr; gap:22px; align-items:stretch;}
.cj-left{position:relative; min-height:650px; border-radius:22px; overflow:hidden; background:radial-gradient(circle at 35% 20%, rgba(255,77,79,.20), transparent 22%), linear-gradient(180deg, rgba(10,18,28,.92), rgba(3,6,10,.98)); border:1px solid rgba(255,255,255,.10); box-shadow:inset 0 0 0 1px rgba(255,255,255,.02);}
.cj-left:before{content:''; position:absolute; left:-42px; top:-18px; width:185px; height:550px; border-radius:50%; border-left:16px solid rgba(255,77,79,.80); border-right:14px solid rgba(255,255,255,.13); transform:rotate(9deg); filter:drop-shadow(0 0 18px rgba(255,77,79,.35)); opacity:.95;}
.cj-left:after{content:''; position:absolute; left:72px; top:60px; width:2px; height:470px; background:linear-gradient(180deg, rgba(255,255,255,.28), rgba(255,255,255,.05));}
.cj-route{position:relative; z-index:2; padding:35px 18px 20px 88px;}
.cj-route-item{display:grid; grid-template-columns:38px 42px minmax(0,1fr); gap:12px; align-items:center; margin-bottom:27px; opacity:.72; transition:all .35s ease; overflow:visible;}
.cj-route-item.active{opacity:1; transform:translateX(4px);}
.cj-num{width:34px; height:34px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:950; font-size:14px; color:#FFF !important; background:#101820; border:2px solid rgba(255,255,255,.55); box-shadow:0 8px 18px rgba(0,0,0,.5);}
.cj-route-item.active .cj-num{background:#FF4D4F; border-color:#FF7779; box-shadow:0 0 22px rgba(255,77,79,.70);}
.cj-icon{font-size:30px; text-align:center; filter:drop-shadow(0 6px 10px rgba(0,0,0,.45));}
.cj-route-title{font-size:16px; font-weight:950; color:#EAF0F6 !important;}
.cj-route-sub{font-size:11px; color:#9EA7B3 !important; margin-top:4px;}
.cj-porsche{position:absolute; z-index:3; left:36px; bottom:60px; width:230px; height:92px; filter:drop-shadow(0 18px 26px rgba(255,0,0,.25));}
.cj-porsche .body{position:absolute; left:12px; bottom:16px; width:196px; height:42px; border-radius:35px 38px 18px 18px; background:linear-gradient(180deg,#ff4f4f,#9d0000); box-shadow:inset 0 8px 14px rgba(255,255,255,.18), inset 0 -10px 14px rgba(0,0,0,.36);}
.cj-porsche .roof{position:absolute; left:70px; bottom:45px; width:85px; height:35px; border-radius:48px 48px 10px 10px; background:linear-gradient(180deg,#d90000,#540000);}
.cj-porsche .window{position:absolute; left:86px; bottom:53px; width:52px; height:18px; border-radius:20px 20px 5px 5px; background:linear-gradient(135deg,#0e1520,#5e6a78);}
.cj-porsche .tail{position:absolute; left:24px; bottom:27px; width:34px; height:7px; border-radius:999px; background:#ffb0b0; box-shadow:0 0 18px #ff4d4f;}
.cj-porsche .wheel{position:absolute; bottom:4px; width:42px; height:42px; border-radius:50%; background:#050505; border:7px solid #202020; box-shadow:inset 0 0 0 4px #555;}
.cj-porsche .w1{left:42px}.cj-porsche .w2{right:34px}
.cj-you{position:absolute; left:118px; bottom:22px; background:rgba(0,0,0,.55); border:1px solid rgba(255,255,255,.12); border-radius:12px; padding:9px 15px; color:#FFF !important; font-weight:850; font-size:13px;}
.cj-you span{display:inline-block; width:9px; height:9px; border-radius:50%; background:#FF4D4F; margin-right:9px; box-shadow:0 0 12px #FF4D4F;}
.cj-main{border-radius:22px; overflow:hidden; border:1px solid rgba(255,255,255,.12); min-height:650px; position:relative; background:#0A0D12; box-shadow:0 22px 70px rgba(0,0,0,.55);}
.cj-main:before{content:''; position:absolute; inset:0; background:radial-gradient(circle at 88% 18%, rgba(255,197,61,.35), transparent 22%), radial-gradient(circle at 40% 45%, rgba(72,105,145,.18), transparent 25%), linear-gradient(115deg, rgba(8,14,23,.98) 0%, rgba(9,16,27,.78) 34%, rgba(64,39,24,.45) 60%, rgba(255,120,50,.28) 100%);}
.cj-main:after{content:''; position:absolute; inset:0; background:linear-gradient(115deg, transparent 0%, transparent 47%, rgba(255,255,255,.08) 48%, transparent 50%), linear-gradient(150deg, transparent 0%, transparent 51%, rgba(0,0,0,.38) 52%, rgba(0,0,0,.08) 66%, transparent 68%); opacity:.75;}
.cj-content{position:relative; z-index:2; padding:44px 48px 28px 48px; min-height:650px; animation:cjFade .42s ease-in-out;}
@keyframes cjFade{from{opacity:.35; transform:translateY(10px)}to{opacity:1; transform:translateY(0)}}
.cj-kicker{font-size:13px; font-weight:950; text-transform:uppercase; color:#FF6B6D !important; letter-spacing:2px; margin-bottom:16px;}
.cj-title{font-size:38px; line-height:1.08; font-weight:950; color:#FFFFFF !important; letter-spacing:-.9px; max-width:600px;}
.cj-title-line{width:56px; height:3px; border-radius:999px; background:#FF4D4F; margin:20px 0; box-shadow:0 0 18px rgba(255,77,79,.65);}
.cj-body{font-size:16px; line-height:1.65; color:#EAF0F6 !important; max-width:560px;}
.cj-card-stack{display:grid; grid-template-columns:1fr; gap:12px; margin-top:28px; max-width:410px;}
.cj-info-card{background:rgba(12,18,27,.74); border:1px solid rgba(255,255,255,.12); border-radius:14px; padding:17px 18px; display:flex; gap:16px; align-items:flex-start; backdrop-filter:blur(8px);}
.cj-info-icon{font-size:31px; color:#FF4D4F !important; width:42px; text-align:center;}
.cj-info-title{font-size:18px; font-weight:950; color:#FFF !important; line-height:1.15;}
.cj-info-sub{font-size:13px; color:#C9D1D9 !important; margin-top:4px; line-height:1.4;}
.cj-side-badges{position:absolute; right:40px; top:265px; display:grid; gap:14px; width:250px;}
.cj-side-badge{display:flex; gap:14px; align-items:center; background:rgba(45,22,16,.74); border:1px solid rgba(255,255,255,.10); border-radius:14px; padding:15px 16px; backdrop-filter:blur(8px);}
.cj-side-icon{font-size:28px; color:#FF4D4F !important;}
.cj-side-title{font-weight:950; color:#FFF !important; font-size:15px;}.cj-side-sub{font-size:12px; color:#C9D1D9 !important; margin-top:3px;}
.cj-bottom-strip{position:absolute; z-index:3; left:42px; right:42px; bottom:28px; border-radius:14px; background:rgba(18,24,32,.78); border:1px solid rgba(255,255,255,.12); display:grid; grid-template-columns:repeat(4,1fr); overflow:hidden; backdrop-filter:blur(9px);}
.cj-strip-item{padding:18px; display:flex; gap:13px; align-items:center; border-right:1px solid rgba(255,255,255,.10);}.cj-strip-item:last-child{border-right:none;}.cj-strip-icon{font-size:25px;}.cj-strip-title{font-weight:950; color:#FFF !important;}.cj-strip-sub{font-size:12px; color:#C9D1D9 !important; margin-top:3px;}
.cj-chip-row{display:flex; flex-wrap:wrap; gap:10px; margin-top:22px; max-width:650px}.cj-chip{background:rgba(255,77,79,.16); border:1px solid rgba(255,77,79,.38); border-radius:999px; padding:10px 14px; color:#FFF !important; font-weight:900; font-size:13px;}
.cj-mini-grid{display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:24px; max-width:620px}.cj-mini-card{background:rgba(12,18,27,.72); border:1px solid rgba(255,255,255,.12); border-radius:14px; padding:17px; color:#FFF !important; font-weight:950;}.cj-mini-card span{display:block; color:#C9D1D9 !important; font-size:12px; font-weight:600; margin-top:6px; line-height:1.4;}
.cj-quote{margin-top:18px; max-width:410px; border-left:3px solid #FF4D4F; background:rgba(255,255,255,.055); border-radius:12px; padding:15px 18px; color:#EAF0F6 !important; font-size:15px; line-height:1.5;}
.cj-publication{margin-top:24px; max-width:690px; background:linear-gradient(135deg, rgba(255,197,61,.13), rgba(255,77,79,.08)); border:1px solid rgba(255,197,61,.34); border-radius:16px; padding:19px 21px; color:#FFF !important; line-height:1.55;}.cj-publication a{color:#FFD666 !important; font-weight:950; text-decoration:none !important}.cj-publication a:hover{text-decoration:underline !important}.cj-publication small{color:#FFD6D6 !important;}
.cj-navbox{margin:18px auto 0; max-width:760px; background:rgba(12,18,27,.78); border:1px solid rgba(255,255,255,.10); border-radius:18px; padding:14px 18px; display:grid; grid-template-columns:140px 1fr 140px; gap:16px; align-items:center;}
.cj-dots{display:flex; justify-content:center; gap:22px; align-items:center;}.cj-dot{width:12px; height:12px; border-radius:50%; background:#3A444F; box-shadow:0 0 0 5px rgba(255,255,255,.02);}.cj-dot.active{background:#FF4D4F; box-shadow:0 0 20px rgba(255,77,79,.7);}.cj-dot.done{background:#6D7580;}
.cj-footer{margin-top:14px; border:1px solid rgba(255,255,255,.08); border-radius:14px; padding:14px 18px; display:flex; justify-content:space-between; color:#9EA7B3 !important; font-size:13px;}.cj-footer a{color:#C9D1D9 !important; text-decoration:none !important; margin-left:22px;}
@media (max-width:1150px){.cj-topbar{grid-template-columns:1fr}.cj-road-note{justify-self:stretch}.cj-grid{grid-template-columns:1fr}.cj-left{display:none}.cj-main,.cj-content{min-height:720px}.cj-side-badges{position:relative; right:auto; top:auto; width:auto; margin-top:20px; grid-template-columns:1fr 1fr}.cj-bottom-strip{position:relative; left:auto; right:auto; bottom:auto; margin-top:24px; grid-template-columns:1fr 1fr}.cj-navbox{grid-template-columns:1fr}.cj-footer{display:block}.cj-footer div:last-child{margin-top:8px}.cj-mini-grid{grid-template-columns:1fr}.cj-headline h2{font-size:30px;}}


/* CREATOR JOURNEY CLEAN FIX */
.cj-topbar{display:block !important;text-align:center !important;margin-bottom:26px !important}.cj-headline{text-align:center !important;width:100%}.cj-headline h2{font-size:42px !important;margin:0 !important;font-weight:950 !important;letter-spacing:-1px !important;color:#fff !important}.cj-headline p{font-size:16px !important;margin:10px 0 0 0 !important;color:#C9D1D9 !important}.cj-headline-line{height:3px;width:260px;margin:16px auto 0 auto;background:linear-gradient(90deg,transparent,#FF4D4F,transparent);border-radius:999px}.cj-road-note{display:none !important}.cj-porsche,.cj-you{display:none !important}.cj-left{min-height:650px !important}.cj-route{padding:36px 20px 22px 74px !important}.cj-route-item{grid-template-columns:42px 42px minmax(0,1fr) !important;gap:13px !important;margin-bottom:27px !important}.cj-route-title{font-size:16px !important;line-height:1.2 !important;color:#F6F8FB !important}.cj-route-sub{font-size:11.5px !important;color:#AEB7C2 !important;line-height:1.25 !important}.cj-main,.cj-content{min-height:650px !important}.cj-content{padding:48px 54px 34px 54px !important}.cj-title{font-size:40px !important;max-width:720px !important}.cj-body{font-size:17px !important;max-width:760px !important}.cj-footer{margin-top:18px !important}.cj-publication{margin-top:24px;max-width:720px;background:linear-gradient(135deg,rgba(255,197,61,.13),rgba(255,77,79,.08));border:1px solid rgba(255,197,61,.34);border-radius:16px;padding:19px 21px;color:#fff !important;line-height:1.55}.cj-publication a{color:#FFD666 !important;font-weight:950;text-decoration:none !important}.cj-publication a:hover{text-decoration:underline !important}.cj-publication small{color:#FFD6D6 !important}



/* CREATOR JOURNEY RESPONSIVE + CHAPTER CLEANUP FIX */
.cj-wrap{max-width:100%; overflow:hidden !important; box-sizing:border-box !important;}
.cj-grid{grid-template-columns:minmax(280px, 360px) minmax(0,1fr) !important; gap:22px !important;}
.cj-left,.cj-main{min-width:0 !important; box-sizing:border-box !important;}
.cj-content{box-sizing:border-box !important; overflow:hidden !important;}
.cj-side-badges{position:relative !important; right:auto !important; top:auto !important; width:auto !important; max-width:720px !important; margin-top:20px !important; display:grid !important; grid-template-columns:repeat(2,minmax(0,1fr)) !important;}
.cj-bottom-strip{position:relative !important; left:auto !important; right:auto !important; bottom:auto !important; margin-top:22px !important; display:grid !important; grid-template-columns:repeat(4,minmax(0,1fr)) !important;}
.cj-card-stack{max-width:620px !important;}
.cj-route-title{word-break:normal !important; overflow-wrap:break-word !important;}
.cj-route-sub{overflow-wrap:break-word !important;}
@media (max-width:1350px){
    .cj-grid{grid-template-columns:minmax(260px, 330px) minmax(0,1fr) !important; gap:18px !important;}
    .cj-route{padding:34px 14px 20px 56px !important;}
    .cj-route-item{grid-template-columns:36px 34px minmax(0,1fr) !important; gap:10px !important; margin-bottom:24px !important;}
    .cj-icon{font-size:25px !important;}
    .cj-route-title{font-size:14px !important;}
    .cj-route-sub{font-size:10.5px !important;}
    .cj-content{padding:42px 42px 30px 42px !important;}
    .cj-title{font-size:34px !important; max-width:100% !important;}
    .cj-body{font-size:15.5px !important; max-width:100% !important;}
    .cj-bottom-strip{grid-template-columns:repeat(2,minmax(0,1fr)) !important;}
}
@media (max-width:1050px){
    .cj-grid{grid-template-columns:1fr !important;}
    .cj-left{min-height:auto !important; padding:18px !important;}
    .cj-left:before,.cj-left:after{display:none !important;}
    .cj-route{padding:0 !important; display:grid !important; grid-template-columns:repeat(2,minmax(0,1fr)) !important; gap:12px !important;}
    .cj-route-item{margin-bottom:0 !important; background:rgba(255,255,255,.04) !important; border:1px solid rgba(255,255,255,.08) !important; border-radius:14px !important; padding:12px !important;}
    .cj-main,.cj-content{min-height:auto !important;}
    .cj-side-badges{grid-template-columns:1fr !important;}
    .cj-bottom-strip{grid-template-columns:1fr !important;}
    .cj-footer{display:block !important;}
    .cj-footer div:last-child{margin-top:8px !important;}
}
@media (max-width:650px){
    .block-container{padding-left:1rem !important; padding-right:1rem !important;}
    .cj-wrap{padding:14px !important;}
    .cj-headline h2{font-size:30px !important;}
    .cj-headline p{font-size:13px !important;}
    .cj-route{grid-template-columns:1fr !important;}
    .cj-content{padding:30px 22px 24px 22px !important;}
    .cj-title{font-size:29px !important;}
    .cj-body{font-size:14.5px !important;}
    .cj-info-card{padding:14px !important; gap:12px !important;}
    .cj-info-title{font-size:16px !important;}
    .cj-dots{gap:12px !important;}
}

.cj-takeaway{margin-top:22px;max-width:720px;border-left:4px solid #FF4D4F;background:rgba(255,255,255,.055);border-radius:14px;padding:16px 18px;display:flex;gap:14px;align-items:flex-start;color:#EAF0F6 !important;}
.cj-takeaway-icon{font-size:24px;color:#FF4D4F !important;line-height:1;}
.cj-takeaway-title{font-size:16px;font-weight:950;color:#FFFFFF !important;margin-bottom:4px;}
.cj-takeaway-sub{font-size:13px;color:#C9D1D9 !important;line-height:1.45;}
.cj-publication-label{font-weight:950;color:#FFFFFF !important;margin-bottom:5px;}
.cj-publication-meta{color:#FFD6D6 !important;font-size:13px;margin-top:4px;}
.cj-publication-tag{color:#FFD666 !important;font-weight:850;margin-top:6px;}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# BRAND HEADER
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">ProjectRescue <span>AI</span></div>
    <div class="hero-subtitle">Enterprise Project Health & Recovery Advisor</div>
    <div class="hero-brand">Powered by ThinkLab.pm</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# CONFIG
# -----------------------------
# Executive PMO traffic-light palette.
# Critical and Watchlist are intentionally red/amber instead of blue so urgency is clear.
color_map = {
    "Green": "#52C41A", "Amber": "#FFC53D", "Red": "#FF4D4F",
    "On Track": "#52C41A", "Watchlist": "#FFC53D", "Critical": "#FF4D4F",
    "Critical Projects": "#FF4D4F", "Watchlist Projects": "#FFC53D"
}
risk_color_map = {
    "Critical": "#FF4D4F",
    "Watchlist": "#FFC53D",
    "Low": "#52C41A",
    "High": "#FF4D4F",
    "Medium": "#FFC53D"
}
health_icons = {"Green": "🟢 On Track", "Amber": "🟠 Watchlist", "Red": "🔴 Critical"}

features = [
    "cost_variance_percent", "schedule_variance_percent", "schedule_variance_days",
    "spi", "cpi", "completed_tasks_percent", "open_risks_count", "open_issues_count",
    "scope_changes_count", "resource_utilization_percent", "stakeholder_sentiment_score",
    "risk_score"
]

@st.cache_resource
def load_model():
    return joblib.load("project_rescue_model.pkl")

model = load_model()

def dark_plot(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0B0B0B",
        plot_bgcolor="#0B0B0B",
        font=dict(color="#F5F5F5", size=15, family="Inter"),
        title=dict(font=dict(size=24, color="#FFFFFF", family="Inter")),
        legend=dict(
            title=dict(text="<b>Project Health</b>", font=dict(size=18, color="#FFFFFF", family="Inter")),
            font=dict(size=16, color="#FFFFFF", family="Inter"),
            bgcolor="rgba(20,20,20,0.88)",
            bordercolor="rgba(255,255,255,0.25)",
            borderwidth=1
        )
    )
    return fig




def section_header(title, subtitle=None):
    """Full-width executive heading bar used consistently across Single and Portfolio views."""
    subtitle_html = f'<div class="exec-section-subtitle">{subtitle}</div>' if subtitle else ''
    st.markdown(
        f'<div class="exec-section-header"><div class="exec-section-title">{title}</div>{subtitle_html}</div>',
        unsafe_allow_html=True
    )


def styled_dataframe(df, center=True):
    """Return a pandas Styler with bold, centered table headings for executive readability."""
    styler = df.style.set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'center'), ('font-weight', '900')]},
        {'selector': 'td', 'props': [('text-align', 'center' if center else 'left')]}
    ])
    try:
        styler = styler.hide(axis='index')
    except Exception:
        pass
    return styler

def polish_3d_portfolio_chart(fig):
    """Make the 3D portfolio chart executive-readable with bold titles and clear legends."""
    fig.update_traces(marker=dict(size=5, opacity=0.9))
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title=dict(text="<b>Schedule Delay (Days)</b>", font=dict(size=16, color="#FFFFFF")),
                tickfont=dict(size=12, color="#FFFFFF"),
                gridcolor="rgba(255,255,255,0.20)"
            ),
            yaxis=dict(
                title=dict(text="<b>Cost Variance (%)</b>", font=dict(size=16, color="#FFFFFF")),
                tickfont=dict(size=12, color="#FFFFFF"),
                gridcolor="rgba(255,255,255,0.20)"
            ),
            zaxis=dict(
                title=dict(text="<b>Project Control Index (PCI)</b>", font=dict(size=16, color="#FFFFFF")),
                tickfont=dict(size=12, color="#FFFFFF"),
                gridcolor="rgba(255,255,255,0.20)"
            )
        ),
        legend=dict(
            title=dict(text="<b>Project Health</b>", font=dict(size=18, color="#FFFFFF", family="Inter")),
            font=dict(size=16, color="#FFFFFF", family="Inter"),
            bgcolor="rgba(20,20,20,0.90)",
            bordercolor="rgba(255,255,255,0.35)",
            borderwidth=1
        ),
        title=dict(text="<b>3D Portfolio Control View</b>", font=dict(size=24, color="#FFFFFF", family="Inter"))
    )
    return fig


# -----------------------------
# PMI / PMBOK-ALIGNED RULE ENGINE
# -----------------------------
# The ML model is retained as a secondary signal, but final health is governed by
# transparent PMO/EVM rules. This avoids contradictions such as Schedule = On Track
# while SPI is Critical.

SEVERITY_ORDER = {"Green": 0, "Amber": 1, "Red": 2}
STATUS_ORDER = {"Green": 0, "Amber": 1, "Red": 2}


def worst_health(*values):
    """Return the worst health value among Green/Amber/Red dimensions."""
    return max(values, key=lambda v: SEVERITY_ORDER.get(v, 0))


def status_label(status):
    """User-facing status labels."""
    return {"Green": "On Track", "Amber": "Watchlist", "Red": "Critical"}.get(status, status)


def evm_health(index_value):
    """PMI/EVM-aligned SPI/CPI health.

    SPI/CPI >= 0.95: within PMO tolerance
    0.85 - 0.94: management watchlist
    < 0.85: critical performance variance
    """
    if index_value >= 0.95:
        return "Green"
    if index_value >= 0.85:
        return "Amber"
    return "Red"


def variance_health(percent_value, green_limit=5, amber_limit=15):
    """Variance health for cost/schedule percentage variance."""
    if percent_value <= green_limit:
        return "Green"
    if percent_value <= amber_limit:
        return "Amber"
    return "Red"


def count_health(count_value, green_limit, amber_limit):
    if count_value <= green_limit:
        return "Green"
    if count_value <= amber_limit:
        return "Amber"
    return "Red"


def utilization_health(utilization):
    """Resource utilization aligned to overload risk.

    0-85%: sustainable
    86-95%: watchlist / potential overload
    >95%: critical overload risk
    """
    if utilization <= 85:
        return "Green"
    if utilization <= 95:
        return "Amber"
    return "Red"


def sentiment_health(sentiment):
    """Stakeholder alignment threshold.

    In real PMO reporting, 3.5/5 is usually managed/acceptable unless there are
    active escalations. 3.0-3.49 is watchlist; below 3.0 needs recovery action.
    """
    if sentiment >= 3.5:
        return "Green"
    if sentiment >= 3.0:
        return "Amber"
    return "Red"


def calculate_internal_model_signal(cost, schedule_pct, delay_days, spi, cpi, completed, risks, issues, scope, utilization, sentiment):
    """Internal model compatibility signal.

    This value is not displayed. PMI does not define a
    project-level score from SPI/CPI/variance inputs. The trained model
    expects a field named risk_score, so this signal is retained only as an
    internal feature to preserve model compatibility.
    """
    score = 0.0

    # Direct variance exposure
    score += max(cost, 0) * 0.80
    score += max(schedule_pct, 0) * 0.70

    # Risk, issue, and change exposure
    score += max(risks, 0) * 1.50
    score += max(issues, 0) * 1.20
    score += max(scope, 0) * 1.50

    # Resource and stakeholder exposure
    score += max(utilization - 85, 0) * 0.90
    score += max(3.5 - sentiment, 0) * 6.00

    # EVM performance penalties. Severe SPI/CPI should materially influence final score.
    if spi < 0.80:
        score += 25
    elif spi < 0.85:
        score += 20
    elif spi < 0.90:
        score += 12
    elif spi < 0.95:
        score += 6

    if cpi < 0.80:
        score += 27
    elif cpi < 0.85:
        score += 22
    elif cpi < 0.90:
        score += 14
    elif cpi < 0.95:
        score += 7

    # Late-stage projects with poor EVM performance have less room to recover.
    if completed >= 70 and (spi < 0.90 or cpi < 0.90):
        score += 5
    if completed >= 85 and (spi < 0.95 or cpi < 0.95):
        score += 5

    return round(min(score, 100), 2)


def classify_dimension(value, green_limit, amber_limit, reverse=False):
    """Backward-compatible helper for charts/legacy calls."""
    if reverse:
        if value >= green_limit:
            return "Green"
        elif value >= amber_limit:
            return "Amber"
        return "Red"
    if value <= green_limit:
        return "Green"
    elif value <= amber_limit:
        return "Amber"
    return "Red"


def health_breakdown(row):
    """Non-duplicated PMO dimension cards.

    SPI is embedded inside Schedule Performance.
    CPI is embedded inside Cost Performance.
    This removes duplicate Schedule/SPI and Cost/CPI cards while keeping the logic EVM-aligned.
    """
    spi_h = evm_health(float(row["spi"]))
    cpi_h = evm_health(float(row["cpi"]))
    schedule_delay_h = variance_health(float(row["schedule_delay_percent"]), 5, 15)
    cost_variance_h = variance_health(float(row["cost_variance_percent"]), 5, 15)

    schedule_h = worst_health(schedule_delay_h, spi_h)
    cost_h = worst_health(cost_variance_h, cpi_h)

    risk_h = count_health(int(row["open_risks_count"]), 4, 8)
    issue_h = count_health(int(row["open_issues_count"]), 4, 8)
    scope_h = count_health(int(row["scope_changes_count"]), 2, 5)
    pci_h = pci_health(row)

    return {
        "Schedule Performance": schedule_h,
        "Cost Performance": cost_h,
        "Project Control Index (PCI)": pci_h,
        "Scope Control": scope_h,
        "Resource Capacity": utilization_health(float(row["resource_utilization_percent"])),
        "Stakeholder Alignment": sentiment_health(float(row["stakeholder_sentiment_score"])),
        "Delivery Progress": progress_health(row)
    }


def progress_health(row):
    """Progress view used as a soft indicator, not a hard override.

    A completed-task percentage alone should not make a project critical because it depends
    on where the project is in its lifecycle. This only flags very low progress when EVM
    signals are also poor.
    """
    completed = float(row["completed_tasks_percent"])
    spi = float(row["spi"])
    if completed < 40 and spi < 0.85:
        return "Red"
    if completed < 60 and spi < 0.95:
        return "Amber"
    return "Green"


def calculate_evm_forecast(bac, cpi):
    """PMBOK/EVM forecasting.

    EAC = BAC / CPI assumes future cost performance continues at the current CPI.
    VAC = BAC - EAC. Negative VAC means expected budget overrun.
    """
    bac = max(float(bac), 0)
    cpi = max(float(cpi), 0.01)
    eac = bac / cpi
    vac = bac - eac
    vac_percent = (vac / bac) * 100 if bac > 0 else 0
    return round(eac, 2), round(vac, 2), round(vac_percent, 2)



def calculate_tcpi(bac, ev, ac):
    """To-Complete Performance Index.

    TCPI = (BAC - EV) / (BAC - AC). Values > 1.10 usually indicate that
    the remaining work needs materially better cost performance than current trend.
    """
    bac = max(float(bac), 0.0)
    ev = min(max(float(ev), 0.0), bac)
    ac = max(float(ac), 0.0)
    denom = bac - ac
    if bac <= 0 or denom <= 0:
        return None
    return round((bac - ev) / denom, 2)


def calculate_recovery_probability(row, final_status):
    """Practical PMO recovery probability from current health indicators.

    This is a decision-support estimate, not a promise. It uses EVM, PCI,
    stakeholder alignment, variance severity, and remaining delivery runway.
    Floors/caps are applied by final status so an On Track project cannot show
    an unrealistic 0% recovery probability.
    """
    probability = 92.0
    probability -= max(0.95 - float(row["spi"]), 0) * 140
    probability -= max(0.95 - float(row["cpi"]), 0) * 150
    probability -= max(float(row["cost_variance_percent"]) - 5, 0) * 0.9
    probability -= max(float(row["schedule_delay_percent"]) - 5, 0) * 0.8
    probability -= max(int(row["open_risks_count"]) - 3, 0) * 2.0
    probability -= max(int(row["open_issues_count"]) - 2, 0) * 2.5
    probability -= max(int(row["scope_changes_count"]) - 2, 0) * 2.0
    probability -= max(3.8 - float(row["stakeholder_sentiment_score"]), 0) * 8
    probability -= max(75 - float(row["pci_score"]), 0) * 0.5
    probability -= max(float(row["completed_tasks_percent"]) - 80, 0) * 0.4

    if final_status == "Red":
        probability -= 10
        probability = min(probability, 65)
    elif final_status == "Amber":
        probability -= 3
        probability = min(max(probability, 45), 85)
    else:
        probability = max(probability, 75)

    probability = round(max(min(probability, 95), 5), 1)
    if probability >= 75:
        label = "Likely Recoverable"
    elif probability >= 50:
        label = "Recoverable with Management Action"
    else:
        label = "Executive Intervention Required"
    return probability, label

def generate_executive_narrative(row, final_status, priority, timeline):
    """Human-readable steering-committee narrative for single project assessment."""
    status = status_label(final_status)
    dims = health_breakdown(row)

    # Separate operational health from PCI so a PCI Amber does not sound like
    # the primary reason an otherwise healthy project needs recovery.
    operational_dims = {k: v for k, v in dims.items() if k != "Project Control Index (PCI)"}
    watch_or_critical = [name for name, val in operational_dims.items() if val in ["Amber", "Red"]]
    stable = [name for name, val in operational_dims.items() if val == "Green"]
    pci_status = dims.get("Project Control Index (PCI)", "Green")

    if watch_or_critical:
        concern_text = ", ".join(watch_or_critical[:4])
    elif pci_status == "Amber":
        concern_text = "minor project-control improvement opportunities"
    elif pci_status == "Red":
        concern_text = "project-control discipline"
    else:
        concern_text = "no major control area"

    stable_text = ", ".join(stable[:3]) if stable else "limited control areas"

    if final_status == "Red":
        lead = "The project requires immediate recovery governance."
    elif final_status == "Amber":
        lead = "The project is manageable but showing early warning indicators."
    else:
        lead = "The project is operating within current PMO tolerance."

    return (
        f"{lead} Current health is {status}, with primary attention needed in {concern_text}. "
        f"Stable areas include {stable_text}. Recovery priority is {priority}, with an estimated timeline of {timeline}. "
        f"EVM forecast shows EAC {row['eac']:,.0f} against BAC {row['budget_at_completion']:,.0f}, "
        f"and PCI is {row['pci_score']}/100 ({row['pci_label']})."
    )


def build_trend_placeholder(row):
    """Current signal view when historical records are not available.

    PMI-defined EVM indicators are shown directly. PCI is a ProjectRescue AI
    control index, not a PMI formula.
    """
    return pd.DataFrame({
        "Indicator": ["SPI", "CPI", "Project Control Index (PCI)"],
        "Current Value": [
            float(row["spi"]),
            float(row["cpi"]),
            float(row["pci_score"])
        ],
        "Trend Signal": [
            "Within tolerance" if float(row["spi"]) >= 0.95 else "Below tolerance / Needs Review",
            "Within tolerance" if float(row["cpi"]) >= 0.95 else "Below tolerance / Needs Review",
            str(row.get("pci_label", ""))
        ]
    })

def pci_score(row):
    """Project Control Index (PCI) based only on inputs captured by ProjectRescue AI.

    PCI is a defensible PMO control score across five observable control domains:
    Schedule, Cost, Risk/Issue exposure, Scope Control, and Stakeholder Alignment.

    Formula:
    PCI = 30% Schedule Control + 30% Cost Control + 20% Risk/Issue Control
          + 10% Scope Control + 10% Stakeholder Alignment.
    """
    spi = float(row["spi"])
    cpi = float(row["cpi"])
    schedule_delay = max(float(row["schedule_delay_percent"]), 0.0)
    cost_variance = max(float(row["cost_variance_percent"]), 0.0)
    risks = max(int(row["open_risks_count"]), 0)
    issues = max(int(row["open_issues_count"]), 0)
    scope_changes = max(int(row["scope_changes_count"]), 0)
    sentiment = max(min(float(row["stakeholder_sentiment_score"]), 5.0), 0.0)

    schedule_index_score = min(max(spi, 0.0), 1.0) * 100
    schedule_delay_score = max(0.0, 100 - (schedule_delay * 3))
    schedule_score = (schedule_index_score * 0.70) + (schedule_delay_score * 0.30)

    cost_index_score = min(max(cpi, 0.0), 1.0) * 100
    cost_variance_score = max(0.0, 100 - (cost_variance * 3))
    cost_score = (cost_index_score * 0.70) + (cost_variance_score * 0.30)

    risk_issue_score = max(0.0, 100 - (risks * 6) - (issues * 8))
    scope_score = max(0.0, 100 - (scope_changes * 10))
    stakeholder_score = (sentiment / 5.0) * 100

    pci = (
        schedule_score * 0.30
        + cost_score * 0.30
        + risk_issue_score * 0.20
        + scope_score * 0.10
        + stakeholder_score * 0.10
    )

    return round(max(min(pci, 100.0), 0.0), 1)


def pci_health(row):
    score = float(row.get("pci_score", pci_score(row)))
    if score >= 90:
        return "Green"
    if score >= 75:
        return "Amber"
    return "Red"


def pci_label(score):
    score = float(score)
    if score >= 90:
        return "Excellent Control"
    if score >= 75:
        return "Good Control"
    if score >= 60:
        return "Needs Attention"
    return "Weak Control"


def kpi_severity_level(status):
    return {"Green": "Low", "Amber": "Watchlist", "Red": "Critical"}[status]


def kpi_severity_score(status):
    return {"Green": 1, "Amber": 2, "Red": 3}[status]


def get_top_kpis(row):
    """Executive-friendly drivers using actual KPI values, not arbitrary impact points."""
    kpis = []

    def add(driver, value, health, signal):
        kpis.append({
            "Driver": driver,
            "KPI Value": value,
            "Control Level": kpi_severity_level(health),
            "PMO Signal": signal,
            "Severity Score": kpi_severity_score(health)
        })

    add("CPI", f"{float(row['cpi']):.2f}", evm_health(float(row["cpi"])), "Cost efficiency / earned value")
    add("SPI", f"{float(row['spi']):.2f}", evm_health(float(row["spi"])), "Schedule efficiency / earned value")
    add("Cost Variance", f"{float(row['cost_variance_percent']):.1f}%", variance_health(float(row["cost_variance_percent"]), 5, 15), "Budget variance")
    add("Schedule Delay", f"{float(row['schedule_delay_percent']):.1f}% / {float(row['schedule_variance_days']):.0f} days", variance_health(float(row["schedule_delay_percent"]), 5, 15), "Time variance")
    add("Open Risks", f"{int(row['open_risks_count'])}", count_health(int(row["open_risks_count"]), 4, 8), "Open risk exposure")
    add("Open Issues", f"{int(row['open_issues_count'])}", count_health(int(row["open_issues_count"]), 4, 8), "Execution blockers")
    add("Scope Changes", f"{int(row['scope_changes_count'])}", count_health(int(row["scope_changes_count"]), 2, 5), "Change control")
    add("Resource Utilization", f"{float(row['resource_utilization_percent']):.0f}%", utilization_health(float(row["resource_utilization_percent"])), "Capacity / overload")
    add("Stakeholder Sentiment", f"{float(row['stakeholder_sentiment_score']):.1f}/5", sentiment_health(float(row["stakeholder_sentiment_score"])), "Stakeholder alignment")
    add("Project Control Index (PCI)", f"{float(row['pci_score']):.1f}/100", pci_health(row), "Project control discipline")

    return sorted(kpis, key=lambda x: x["Severity Score"], reverse=True)[:6]


# Backward-compatible name used by existing render/export code.
def get_top_drivers(row):
    return get_top_kpis(row)


def risk_driver_level(level_or_score):
    """Compatibility helper. Accepts either a severity score or a Control Level string."""
    if isinstance(level_or_score, str):
        return level_or_score
    if level_or_score >= 3:
        return "Critical"
    if level_or_score >= 2:
        return "Watchlist"
    return "Low"

def override_status(prediction, spi, cpi, delay_percent, risks, issues, sentiment):
    """Final project health rule.

    Rule-based PMO governance is the source of truth. The final status uses
    observable project controls and PMI/EVM indicators. No PMI-defined risk
    score is used because the app does not collect probability-impact risk data.
    """
    dimension_statuses = [
        variance_health(delay_percent, 5, 15),
        evm_health(spi),
        evm_health(cpi),
        count_health(risks, 4, 8),
        count_health(issues, 4, 8),
        sentiment_health(sentiment)
    ]

    return worst_health(*dimension_statuses)

def sanity_check_status(status, row):
    severe = []
    dims = health_breakdown(row)

    # Operational dimensions drive final RAG status.
    # PCI is a composite ProjectRescue AI control index, so an Amber PCI alone
    # must not downgrade an otherwise healthy project to Amber.
    # PCI Red still escalates because weak controls can materially affect delivery governance.
    operational_dims = {k: v for k, v in dims.items() if k != "Project Control Index (PCI)"}

    if dims.get("Schedule Performance") == "Red":
        severe.append("Schedule performance is critical")
    if dims.get("Cost Performance") == "Red":
        severe.append("Cost performance is critical")
    if dims.get("Project Control Index (PCI)") == "Red":
        severe.append("Project control discipline is weak")
    if dims.get("Scope Control") == "Red":
        severe.append("Scope control is critical")
    if dims.get("Resource Capacity") == "Red":
        severe.append("Resource capacity is critical")
    if dims.get("Stakeholder Alignment") == "Red":
        severe.append("Stakeholder alignment is low")

    # Escalate to Red if any operational dimension is Red, or if PCI is Red.
    if any(v == "Red" for v in operational_dims.values()) or dims.get("Project Control Index (PCI)") == "Red":
        status = "Red"
    else:
        # Amber should reflect real operational watchlist signals, not PCI alone.
        # If only PCI is Amber and all operational dimensions are Green, final status remains Green.
        operational_amber_count = sum(1 for v in operational_dims.values() if v == "Amber")
        if operational_amber_count > 0 and STATUS_ORDER[status] < STATUS_ORDER["Amber"]:
            status = "Amber"

    return status, severe


def recovery_timeline(status, row):
    if status == "Green":
        return "No recovery required"
    if status == "Amber":
        if row["cost_variance_percent"] >= 10 or row["cpi"] < 0.95:
            return "4-6 weeks"
        if row["schedule_delay_percent"] >= 10 or row["spi"] < 0.95:
            return "3-5 weeks"
        return "2-4 weeks"
    if row["schedule_delay_percent"] >= 25 or row["cpi"] < 0.75 or row.get("pci_score", 100) < 60:
        return "8-12 weeks"
    return "6-8 weeks"


def escalation_required(status, row):
    if status == "Red":
        return "Yes"
    if row["cost_variance_percent"] >= 20 or row["open_risks_count"] >= 10 or row["stakeholder_sentiment_score"] < 2.5:
        return "Yes"
    if status == "Amber":
        return "Monitor"
    return "No"


def summarize_dimension_watchlist(row, status):
    dims = health_breakdown(row)
    operational_dims = {k: v for k, v in dims.items() if k != "Project Control Index (PCI)"}

    red_dims = [name for name, value in operational_dims.items() if value == "Red"]
    amber_dims = [name for name, value in operational_dims.items() if value == "Amber"]
    pci_status = dims.get("Project Control Index (PCI)", "Green")

    if dims.get("Project Control Index (PCI)") == "Red":
        red_dims.append("Project Control Index (PCI)")

    if red_dims:
        return f"Critical concern areas: {', '.join(red_dims)}."
    if amber_dims:
        return f"Watchlist areas: {', '.join(amber_dims)}."
    if pci_status == "Amber":
        return "All operational dimensions are within acceptable PMO tolerance. PCI indicates minor project-control improvement opportunities."
    return "All assessed dimensions are within acceptable PMO tolerance."


def _unique_preserve_order(items):
    """Remove duplicates while preserving narrative order."""
    seen = set()
    cleaned = []
    for item in items:
        text = str(item).strip()
        if text and text not in seen:
            cleaned.append(text)
            seen.add(text)
    return cleaned


def _fmt_pct(value):
    return f"{float(value):.1f}%"


def generate_recovery_plan(row, status):
    """Generate fully data-driven reasons, actions, and executive summary.

    Nothing in this section is a fixed default paragraph. Every reason/action is
    selected from the actual KPI condition of the project and includes the KPI
    value that triggered it. PMI-defined EVM values are used directly; PCI and
    recovery probability remain ProjectRescue AI decision-support indicators.
    """
    reasons, actions = [], []

    project_type = row.get("project_type", "General Project")
    readable_status = status_label(status)

    duration = max(float(row.get("project_duration_days", 1)), 1)
    delay_days = float(row["schedule_variance_days"])
    delay_pct = float(row["schedule_delay_percent"])
    cost_var = float(row["cost_variance_percent"])
    spi = float(row["spi"])
    cpi = float(row["cpi"])
    risks = int(row["open_risks_count"])
    issues = int(row["open_issues_count"])
    scope = int(row["scope_changes_count"])
    utilization = float(row["resource_utilization_percent"])
    sentiment = float(row["stakeholder_sentiment_score"])
    completed = float(row["completed_tasks_percent"])
    pci = float(row.get("pci_score", pci_score(row)))
    pci_text = row.get("pci_label", pci_label(pci))

    # -------------------------
    # Schedule signals
    # -------------------------
    if delay_pct > 15 or delay_days >= 30 or spi < 0.85:
        reasons.append(
            f"Schedule control is critical: SPI is {spi:.2f} and schedule delay is {delay_days:.0f} days ({delay_pct:.1f}% of the planned {duration:.0f}-day duration)."
        )
        actions.extend([
            f"Rebaseline the schedule around the remaining {100-completed:.1f}% of work and confirm the revised critical path.",
            "Move blocked critical-path activities into a recovery tracker with owners and due dates.",
            "Increase schedule recovery reviews until SPI returns to at least 0.95."
        ])
    elif delay_pct > 5 or delay_days >= 15 or spi < 0.95:
        reasons.append(
            f"Schedule is on watchlist: SPI is {spi:.2f} and delay is {delay_days:.0f} days ({delay_pct:.1f}% of planned duration)."
        )
        actions.extend([
            "Review milestone dependencies and remove blockers affecting near-term deliverables.",
            "Validate planned-versus-earned work for the next reporting cycle.",
            "Track schedule variance weekly until SPI is back within PMO tolerance."
        ])
    else:
        reasons.append(
            f"Schedule performance is controlled: SPI is {spi:.2f} and delay is {delay_days:.0f} days ({delay_pct:.1f}% of planned duration)."
        )
        actions.append(
            f"Maintain the current schedule cadence and monitor SPI so it remains at or above 0.95."
        )

    # -------------------------
    # Cost/EVM signals
    # -------------------------
    if cost_var > 15 or cpi < 0.85:
        reasons.append(
            f"Cost control is critical: CPI is {cpi:.2f}, cost variance is {cost_var:.1f}%, and VAC is {row['vac']:,.0f}."
        )
        actions.extend([
            "Perform cost variance analysis by work package and isolate the largest burn-rate drivers.",
            f"Reforecast EAC immediately; current EAC is {row['eac']:,.0f} against BAC {row['budget_at_completion']:,.0f}.",
            "Freeze non-essential spend until cost-to-complete is reviewed and approved."
        ])
    elif cost_var > 5 or cpi < 0.95:
        reasons.append(
            f"Cost is on watchlist: CPI is {cpi:.2f}, cost variance is {cost_var:.1f}%, and VAC is {row['vac']:,.0f}."
        )
        actions.extend([
            "Validate remaining cost-to-complete against the current EAC and vendor/resource forecasts.",
            "Review controllable spend items before the next financial checkpoint.",
            "Track CPI weekly until cost performance returns to at least 0.95."
        ])
    else:
        reasons.append(
            f"Cost performance is controlled: CPI is {cpi:.2f}, cost variance is {cost_var:.1f}%, and VAC is {row['vac']:,.0f}."
        )
        actions.append(
            f"Maintain current cost controls and recheck EAC ({row['eac']:,.0f}) during the next status cycle."
        )

    # TCPI guidance
    tcpi_val = row.get("tcpi")
    if tcpi_val is not None:
        tcpi_val = float(tcpi_val)
        if tcpi_val > 1.10:
            reasons.append(f"TCPI is {tcpi_val:.2f}, meaning the remaining work requires materially better cost efficiency than the current baseline allows.")
            actions.append("Review whether the remaining budget is realistic; escalate funding, scope, or productivity trade-offs if needed.")
        elif tcpi_val > 1.00:
            reasons.append(f"TCPI is {tcpi_val:.2f}, so the remaining work must be completed slightly more efficiently than current spend performance.")
            actions.append("Keep cost-to-complete under close control because TCPI is above 1.00.")
        else:
            reasons.append(f"TCPI is {tcpi_val:.2f}, indicating the remaining work is achievable within the current budget trend if performance is maintained.")

    # -------------------------
    # Risk and issue exposure
    # -------------------------
    if risks > 8:
        reasons.append(f"Open risk exposure is high with {risks} active risks.")
        actions.extend([
            "Prioritize the top risks by impact and proximity, then assign mitigation owners and due dates.",
            "Escalate risks that threaten cost, schedule, scope, or go-live readiness to the steering committee."
        ])
    elif risks > 3:
        reasons.append(f"Risk exposure needs active management with {risks} open risks.")
        actions.append("Update the risk register and confirm mitigation owners for each open risk.")
    else:
        reasons.append(f"Risk exposure is manageable with {risks} open risks.")
        if risks > 0:
            actions.append(f"Review the {risks} open risks in the next governance meeting and close risks that are no longer active.")
        else:
            actions.append("Continue risk identification during weekly governance reviews to avoid late discovery.")

    if issues > 8:
        reasons.append(f"Execution issue load is high with {issues} open issues.")
        actions.extend([
            "Create an issue war-room for aging or high-impact blockers.",
            "Assign resolution owners and target dates for all critical open issues."
        ])
    elif issues > 3:
        reasons.append(f"Issue management needs attention with {issues} open issues.")
        actions.append("Review issue aging and resolve blockers before the next reporting cycle.")
    else:
        reasons.append(f"Issue load is manageable with {issues} open issues.")
        if issues > 0:
            actions.append(f"Close or reclassify the {issues} open issues during the next project checkpoint.")

    # -------------------------
    # Scope, resource, stakeholder, and PCI signals
    # -------------------------
    if scope > 5:
        reasons.append(f"Scope volatility is high with {scope} approved or pending scope changes.")
        actions.append("Freeze non-critical scope and route all changes through formal impact assessment.")
    elif scope > 2:
        reasons.append(f"Scope control needs monitoring with {scope} scope changes.")
        actions.append("Prioritize only business-critical changes and document schedule/cost impact before approval.")
    else:
        reasons.append(f"Scope remains controlled with {scope} scope change(s).")
        actions.append("Keep change-control discipline active so scope changes remain tied to approved business value.")

    if utilization > 95:
        reasons.append(f"Resource utilization is critically high at {utilization:.0f}%, creating delivery and burnout risk.")
        actions.append("Rebalance workload or add temporary support to reduce utilization below 90%.")
    elif utilization > 85:
        reasons.append(f"Resource utilization is elevated at {utilization:.0f}% and should be watched.")
        actions.append("Review workload distribution and protect capacity for critical-path activities.")
    elif utilization < 60:
        reasons.append(f"Resource utilization is low at {utilization:.0f}%, which may indicate underuse or planning inefficiency.")
        actions.append("Validate whether team capacity is aligned to upcoming work packages and milestones.")
    else:
        reasons.append(f"Resource utilization is healthy at {utilization:.0f}%.")
        actions.append("Maintain resource utilization within the sustainable 70% to 85% range where possible.")

    if sentiment < 3.0:
        reasons.append(f"Stakeholder sentiment is low at {sentiment:.1f}/5.")
        actions.append("Conduct a stakeholder alignment session and reset expectations, decisions, and communication cadence.")
    elif sentiment < 3.5:
        reasons.append(f"Stakeholder sentiment is watchlist-level at {sentiment:.1f}/5.")
        actions.append("Increase stakeholder updates and confirm decision owners for unresolved concerns.")
    else:
        reasons.append(f"Stakeholder sentiment is positive at {sentiment:.1f}/5.")
        actions.append("Maintain stakeholder engagement through planned governance updates and decision checkpoints.")

    if pci < 60:
        reasons.append(f"PCI is weak at {pci:.1f}/100 ({pci_text}), indicating project-control discipline needs improvement.")
        actions.append("Strengthen project-control routines across schedule, cost, issue, risk, scope, and stakeholder tracking.")
    elif pci < 75:
        reasons.append(f"PCI is {pci:.1f}/100 ({pci_text}), showing project controls need attention.")
        actions.append("Improve project-control discipline by tightening KPI review cadence and ownership tracking.")
    elif pci < 90:
        reasons.append(f"PCI is {pci:.1f}/100 ({pci_text}), showing good control with minor improvement opportunities.")
        actions.append("Use PCI watchlist signals to improve control discipline without escalating the overall project status.")
    else:
        reasons.append(f"PCI is strong at {pci:.1f}/100 ({pci_text}).")
        actions.append("Preserve current control routines because PCI indicates strong delivery governance. ")

    # -------------------------
    # Project-type specific actions, only when the related KPI condition exists.
    # -------------------------
    if project_type == "Cloud Migration":
        if delay_pct > 5 or spi < 0.95 or issues > 3:
            actions.append("Review migration wave plan, cutover readiness, rollback ownership, and dependency blockers.")
        else:
            actions.append("Keep migration wave readiness, cutover checklist, and rollback plan validated for upcoming milestones.")
    elif project_type == "ERP Implementation":
        if status in ["Amber", "Red"] or delay_pct > 5 or issues > 3:
            actions.append("Validate data migration readiness, testing completion, UAT defects, and go-live entry criteria.")
        else:
            actions.append("Maintain ERP readiness checks across data migration, testing, UAT, and go-live criteria.")
    elif project_type == "Cybersecurity Program":
        if status in ["Amber", "Red"] or risks > 3 or issues > 3:
            actions.append("Review unresolved vulnerabilities, compliance gaps, risk acceptances, and executive risk exposure.")
        else:
            actions.append("Continue compliance evidence tracking and confirm vulnerability closure remains on schedule.")
    elif project_type == "Procurement Automation":
        if cost_var > 5 or cpi < 0.95:
            actions.append("Review vendor contracts, invoices, approval delays, and procurement spend forecast.")
        else:
            actions.append("Maintain vendor, approval, and spend-control checks for the next procurement cycle.")

    reasons = _unique_preserve_order(reasons)[:8]
    actions = _unique_preserve_order(actions)[:8]

    timeline = recovery_timeline(status, row)
    escalation = escalation_required(status, row)
    dimension_note = summarize_dimension_watchlist(row, status)
    forecast_note = (
        f"EAC is {row['eac']:,.0f} against BAC {row['budget_at_completion']:,.0f}; "
        f"VAC is {row['vac']:,.0f} ({row['vac_percent']:.1f}%); "
        f"TCPI is {row['tcpi'] if row.get('tcpi') is not None else 'N/A'}; "
        f"PCI is {pci:.1f}/100 ({pci_text})."
    )

    if status == "Red":
        priority = "High"
        summary = (
            f"This {project_type} project is classified as {readable_status} because one or more control areas require immediate correction. "
            f"{dimension_note} {forecast_note} Priority should be placed on the highest-severity schedule, cost, risk, issue, scope, resource, or stakeholder signals listed below. "
            f"Estimated recovery timeline is {timeline}, with executive escalation set to {escalation}."
        )
    elif status == "Amber":
        priority = "Medium"
        summary = (
            f"This {project_type} project is classified as {readable_status} because at least one operational KPI is outside PMO tolerance. "
            f"{dimension_note} {forecast_note} The project remains recoverable if the specific corrective actions below are executed within {timeline}. "
            f"Executive escalation is currently {escalation}."
        )
    else:
        priority = "Low"
        summary = (
            f"This {project_type} project is classified as {readable_status} because schedule, cost, issue, risk, scope, resource, and stakeholder signals are within PMO tolerance. "
            f"{dimension_note} {forecast_note} No recovery intervention is required; the recommended actions focus on maintaining current performance and closing the remaining observable control items. "
            f"Executive escalation is {escalation}."
        )

    return summary, priority, reasons, actions, timeline, escalation


def assess_project(row):
    duration = max(float(row.get("project_duration_days", 180)), 1)
    schedule_days = max(float(row["schedule_variance_days"]), 0)
    schedule_pct = float(row.get("schedule_variance_percent", round((schedule_days / duration) * 100, 2)))

    risk_score = calculate_internal_model_signal(
        float(row["cost_variance_percent"]), schedule_pct, schedule_days,
        float(row["spi"]), float(row["cpi"]), float(row["completed_tasks_percent"]),
        int(row["open_risks_count"]), int(row["open_issues_count"]), int(row["scope_changes_count"]),
        float(row["resource_utilization_percent"]), float(row["stakeholder_sentiment_score"])
    )

    input_df = pd.DataFrame([{**{f: None for f in features},
        "cost_variance_percent": float(row["cost_variance_percent"]),
        "schedule_variance_percent": schedule_pct,
        "schedule_variance_days": schedule_days,
        "spi": float(row["spi"]),
        "cpi": float(row["cpi"]),
        "completed_tasks_percent": float(row["completed_tasks_percent"]),
        "open_risks_count": int(row["open_risks_count"]),
        "open_issues_count": int(row["open_issues_count"]),
        "scope_changes_count": int(row["scope_changes_count"]),
        "resource_utilization_percent": float(row["resource_utilization_percent"]),
        "stakeholder_sentiment_score": float(row["stakeholder_sentiment_score"])
    }])

    prediction = model.predict(input_df[features])[0]
    final_status = override_status(
        prediction, float(row["spi"]), float(row["cpi"]),
        schedule_pct, int(row["open_risks_count"]), int(row["open_issues_count"]),
        float(row["stakeholder_sentiment_score"])
    )

    result_row = {
        "project_name": row.get("project_name", "Manual Project"),
        "project_type": row.get("project_type", "General Project"),
        "project_duration_days": duration,
        "budget_at_completion": float(row.get("budget_at_completion", 100000)),
        "completed_tasks_percent": float(row["completed_tasks_percent"]),
        "cost_variance_percent": float(row["cost_variance_percent"]),
        "schedule_variance_days": schedule_days,
        "schedule_delay_percent": schedule_pct,
        "spi": float(row["spi"]),
        "cpi": float(row["cpi"]),
        "open_risks_count": int(row["open_risks_count"]),
        "open_issues_count": int(row["open_issues_count"]),
        "scope_changes_count": int(row["scope_changes_count"]),
        "resource_utilization_percent": float(row["resource_utilization_percent"]),
        "stakeholder_sentiment_score": float(row["stakeholder_sentiment_score"])
    }

    result_row["eac"], result_row["vac"], result_row["vac_percent"] = calculate_evm_forecast(
        result_row["budget_at_completion"], result_row["cpi"]
    )
    # EV/AC are estimated from BAC, completed %, and CPI because the current UI captures BAC, SPI, and CPI.
    # This enables practical PMBOK-style TCPI guidance without adding duplicate input fields.
    result_row["earned_value"] = round(result_row["budget_at_completion"] * (result_row["completed_tasks_percent"] / 100), 2)
    result_row["actual_cost"] = round(result_row["earned_value"] / max(result_row["cpi"], 0.01), 2)
    result_row["tcpi"] = calculate_tcpi(result_row["budget_at_completion"], result_row["earned_value"], result_row["actual_cost"])
    result_row["pci_score"] = pci_score(result_row)
    result_row["pci_label"] = pci_label(result_row["pci_score"])

    final_status, severe_drivers = sanity_check_status(final_status, result_row)
    recovery_probability, recovery_probability_label = calculate_recovery_probability(result_row, final_status)
    result_row["recovery_probability"] = recovery_probability
    result_row["recovery_probability_label"] = recovery_probability_label
    summary, priority, reasons, actions, timeline, escalation = generate_recovery_plan(result_row, final_status)
    result_row["executive_narrative"] = generate_executive_narrative(result_row, final_status, priority, timeline)

    return result_row, prediction, final_status, severe_drivers, summary, priority, reasons, actions, timeline, escalation

# PDF functions
def chart_to_buffer(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=160)
    plt.close(fig)
    buf.seek(0)
    return buf

def create_health_chart(dimensions):
    labels = list(dimensions.keys())
    colors_list = [color_map[dimensions[label]] for label in labels]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(labels, [1] * len(labels), color=colors_list)
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    ax.set_title("Health Breakdown by Dimension")
    return chart_to_buffer(fig)

def create_driver_chart(top_drivers):
    names = [x["Driver"] for x in top_drivers]
    scores = [x["Severity Score"] for x in top_drivers]
    labels = [x["KPI Value"] for x in top_drivers]
    colors_list = [risk_color_map[x["Control Level"]] for x in top_drivers]
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(names, scores, color=colors_list)
    ax.set_title("KPI Severity View")
    ax.set_ylabel("Severity")
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(["Low", "Watchlist", "Critical"])
    ax.tick_params(axis="x", rotation=25)
    for bar, label in zip(bars, labels):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03, label, ha="center", va="bottom", fontsize=8)
    return chart_to_buffer(fig)

def create_pdf_report(project_name, final_status, priority, timeline, escalation,
                      summary, dimensions, top_drivers, reasons, actions, result_row):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("ProjectRescue AI - Project Health Assessment Report", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Project Name:</b> {project_name}", styles["Normal"]))
    story.append(Paragraph(f"<b>Project Type:</b> {result_row['project_type']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Final Health Status:</b> {final_status}", styles["Normal"]))
    story.append(Paragraph(f"<b>BAC:</b> {result_row['budget_at_completion']:,.2f}", styles["Normal"]))
    story.append(Paragraph(f"<b>EAC:</b> {result_row['eac']:,.2f}", styles["Normal"]))
    story.append(Paragraph(f"<b>VAC:</b> {result_row['vac']:,.2f} ({result_row['vac_percent']:.1f}%)", styles["Normal"]))
    story.append(Paragraph(f"<b>TCPI:</b> {'N/A' if result_row.get('tcpi') is None else result_row['tcpi']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Recovery Probability:</b> {result_row.get('recovery_probability', 0):.1f}% - {escape(str(result_row.get('recovery_probability_label', '')))}", styles["Normal"]))
    story.append(Paragraph(f"<b>Project Control Index (PCI):</b> {result_row['pci_score']}/100 - {result_row['pci_label']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Recovery Priority:</b> {priority}", styles["Normal"]))
    story.append(Paragraph(f"<b>Recovery Timeline:</b> {timeline}", styles["Normal"]))
    story.append(Paragraph(f"<b>Executive Escalation:</b> {escalation}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Executive Narrative", styles["Heading2"]))
    story.append(Paragraph(escape(str(result_row.get("executive_narrative", summary))), styles["Normal"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Executive Summary", styles["Heading2"]))
    story.append(Paragraph(summary, styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Health Breakdown Chart", styles["Heading2"]))
    story.append(Image(create_health_chart(dimensions), width=470, height=240))
    story.append(Spacer(1, 12))

    if top_drivers:
        story.append(Paragraph("Top KPI Watchlist Drivers Chart", styles["Heading2"]))
        story.append(Image(create_driver_chart(top_drivers), width=470, height=240))
        story.append(Spacer(1, 12))

    story.append(Paragraph("Key Reasons", styles["Heading2"]))
    for reason in reasons:
        story.append(Paragraph(f"- {reason}", styles["Normal"]))

    story.append(Spacer(1, 12))
    action_heading = "Recommended Actions" if final_status == "Green" else "Recommended Recovery Actions"
    story.append(Paragraph(action_heading, styles["Heading2"]))

    for action in actions:
        story.append(Paragraph(f"- {action}", styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

def render_result(result_row, prediction, final_status, severe_drivers, summary, priority, reasons, actions, timeline, escalation):
    dimensions = health_breakdown(result_row)
    top_drivers = get_top_drivers(result_row)
    card_class = {"Green": "green-card", "Amber": "amber-card", "Red": "red-card"}[final_status]

    st.markdown(f"""
    <div class="result-card {card_class}">
        <div style="font-size:18px;font-weight:700;opacity:.85;">Assessment Result</div>
        <div style="font-size:42px;font-weight:900;margin-top:6px;">{health_icons[final_status]}</div>
        <div class="result-grid">
            <div class="result-metric"><div class="result-label">Health</div><div class="result-value">{status_label(final_status)}</div></div>
            <div class="result-metric"><div class="result-label">PCI</div><div class="result-value">{result_row['pci_score']}/100</div></div>
            <div class="result-metric"><div class="result-label">Recovery Priority</div><div class="result-value">{priority}</div></div>
            <div class="result-metric"><div class="result-label">Timeline</div><div class="result-value">{timeline}</div></div>
            <div class="result-metric"><div class="result-label">Escalation</div><div class="result-value">{escalation}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    section_header("Executive Narrative", "Single source of truth for the project assessment narrative")
    st.write(result_row.get("executive_narrative", summary))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    section_header("EVM Forecast, Recovery Probability & Project Control Index (PCI)", "PMBOK/EVM forecast and project control readiness")
    f1, f2, f3, f4, f5, f6 = st.columns(6)
    f1.metric("BAC", f"{result_row['budget_at_completion']:,.0f}")
    f2.metric("EAC", f"{result_row['eac']:,.0f}")
    f3.metric("VAC", f"{result_row['vac']:,.0f}", f"{result_row['vac_percent']:.1f}%")
    f4.metric("TCPI", "N/A" if result_row.get('tcpi') is None else f"{result_row['tcpi']:.2f}")
    f5.metric("Recovery Probability", f"{result_row.get('recovery_probability', 0):.1f}%", result_row.get('recovery_probability_label', ''))
    f6.metric("Project Control Index (PCI)", f"{result_row['pci_score']}/100", result_row['pci_label'])
    st.caption("EAC = BAC / CPI. VAC = BAC - EAC. TCPI estimates the cost performance needed to finish within BAC. Negative VAC indicates a forecast budget overrun.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    section_header("Health Breakdown by Dimension", "PMO control areas without duplicate SPI/CPI cards")
    health_html = '<div class="health-grid">'
    for dimension_name, health_value in dimensions.items():
        health_html += (
            f'<div class="health-tile health-{health_value.lower()}">'
            f'<div class="health-name">{dimension_name}</div>'
            f'<div class="health-value">{health_icons[health_value]}</div>'
            '</div>'
        )
    health_html += '</div>'
    st.markdown(health_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    section_header("Top KPI Watchlist Drivers", "Actual KPI values, control level, and PMO signal")

    if top_drivers:
        driver_df = pd.DataFrame(top_drivers)

        table_html = '<table class="driver-table"><tr><th>Driver</th><th>KPI Value</th><th>Control Level</th><th>PMO Signal</th></tr>'
        for _, rr in driver_df.iterrows():
            level = rr["Control Level"]
            table_html += (
                f'<tr><td>{rr["Driver"]}</td>'
                f'<td>{rr["KPI Value"]}</td>'
                f'<td><span class="driver-badge driver-{level.lower()}">{level}</span></td>'
                f'<td>{rr["PMO Signal"]}</td></tr>'
            )
        table_html += '</table>'
        st.markdown(table_html, unsafe_allow_html=True)

        fig_driver = px.bar(
            driver_df,
            x="Driver",
            y="Severity Score",
            color="Control Level",
            title="KPI Severity View",
            color_discrete_map=risk_color_map,
            text="KPI Value"
        )

        fig_driver.update_traces(
            textposition="outside",
            marker_line_color="rgba(255,255,255,0.9)",
            marker_line_width=2,
            opacity=0.96
        )

        fig_driver.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0B0B0B",
            plot_bgcolor="#0B0B0B",
            font=dict(color="#FFFFFF", size=15, family="Inter"),
            title=dict(text="<b>KPI Severity View</b>", font=dict(size=28, color="#FFFFFF")),
            xaxis=dict(
                title="<b>Driver</b>",
                title_font=dict(size=18, color="#FFFFFF"),
                tickfont=dict(size=15, color="#FFFFFF", family="Inter"),
                showgrid=False
            ),
            yaxis=dict(
                title="<b>Severity</b>",
                title_font=dict(size=18, color="#FFFFFF"),
                tickfont=dict(size=15, color="#FFFFFF", family="Inter"),
                gridcolor="rgba(255,255,255,0.18)"
            ),
            legend=dict(
                title=dict(text="<b>Control Level</b>", font=dict(size=16, color="#FFFFFF")),
                font=dict(size=15, color="#FFFFFF"),
                bgcolor="rgba(20,20,20,0.85)",
                bordercolor="rgba(255,255,255,0.25)",
                borderwidth=1
            ),
            bargap=0.35
        )

        st.plotly_chart(fig_driver, use_container_width=True)
    else:
        st.write("No major watchlist drivers detected.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    section_header("Trend Analysis", "Current signal until historical trend fields are supplied")
    st.caption("Historical trend data is not available in the current input. The table below shows current trend signals based on PMI/EVM tolerance thresholds.")
    trend_df = build_trend_placeholder(result_row)
    st.dataframe(trend_df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    section_header("Key Reasons & Recovery Actions", "Why the project received this health status and what to do next")
    for reason in reasons:
        st.write(f"• {reason}")

    action_heading = "Recommended Actions" if final_status == "Green" else "Recommended Recovery Actions"
    st.markdown(f"#### {action_heading}")
    for action in actions:
        st.write(f"• {action}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    section_header("Export & Share", "Download the PDF report or share the executive summary")

    pdf_buffer = create_pdf_report(
        result_row["project_name"],
        final_status,
        priority,
        timeline,
        escalation,
        summary,
        dimensions,
        top_drivers,
        reasons,
        actions,
        result_row
    )

    st.download_button(
        label="Download PDF Report",
        data=pdf_buffer,
        file_name=f"{result_row['project_name'].replace(' ', '_')}_assessment_report.pdf",
        mime="application/pdf",
        key=f"download_pdf_{result_row['project_name']}_{final_status}_{result_row['pci_score']}"
    )

    reasons_text = "\n".join([f"- {r}" for r in reasons])
    actions_text = "\n".join([f"- {a}" for a in actions])
    action_heading = "Recommended Actions" if final_status == "Green" else "Recommended Recovery Actions"
    top_drivers_text = (
        "\n".join([
            f"- {item['Driver']}: {item['KPI Value']} ({item['Control Level']}) - {item['PMO Signal']}"
            for item in top_drivers
        ])
        if top_drivers else "No major watchlist drivers detected."
    )

    share_text = f"""
ProjectRescue AI Assessment Report

Project: {result_row['project_name']}
Project Type: {result_row['project_type']}
Health Status: {final_status}
BAC: {result_row['budget_at_completion']:,.0f}
EAC: {result_row['eac']:,.0f}
VAC: {result_row['vac']:,.0f} ({result_row['vac_percent']:.1f}%)
Project Control Index (PCI): {result_row['pci_score']}/100 - {result_row['pci_label']}
Recovery Priority: {priority}
Recovery Timeline: {timeline}
Executive Escalation: {escalation}

Executive Summary:
{summary}

Top KPI Watchlist Drivers:
{top_drivers_text}

Key Reasons:
{reasons_text}

{action_heading}:
{actions_text}

Note: The full PDF report includes visual charts. Download the PDF from ProjectRescue AI and attach it if required.

Generated by ProjectRescue AI | ThinkLab.pm
""".strip()

    encoded_text = urllib.parse.quote(share_text)
    encoded_subject = urllib.parse.quote(f"ProjectRescue AI Report - {result_row['project_name']}")
    whatsapp_url = f"https://wa.me/?text={encoded_text}"
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&su={encoded_subject}&body={encoded_text}"

    c1, c2 = st.columns(2)
    with c1:
        st.link_button("Share Summary on WhatsApp", whatsapp_url)
    with c2:
        st.link_button("Share Summary via Gmail", gmail_url)

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# PORTFOLIO EXECUTIVE INSIGHTS
# -----------------------------
def portfolio_dimension_dataframe(assessed_df):
    """Build dimension-level portfolio distribution from the same logic used in Single Project Assessment."""
    records = []
    for _, row in assessed_df.iterrows():
        dims = health_breakdown(row)
        for dimension, health in dims.items():
            records.append({
                "Dimension": dimension,
                "Health": status_label(health),
                "Raw Health": health,
                "Project": row.get("project_name", "Project")
            })
    return pd.DataFrame(records)


def portfolio_kpi_driver_summary(assessed_df):
    """Aggregate KPI risk signals across the full portfolio using actual KPI values."""
    rows = []

    def add(driver, value, critical_count, watchlist_count, pmo_signal):
        total = len(assessed_df)
        exposure_count = int(critical_count + watchlist_count)
        exposure_pct = round((exposure_count / total) * 100, 1) if total else 0
        rows.append({
            "Driver": driver,
            "Portfolio KPI": value,
            "Critical Projects": int(critical_count),
            "Watchlist Projects": int(watchlist_count),
            "Exposure %": f"{exposure_pct}%",
            "PMO Signal": pmo_signal
        })

    total = max(len(assessed_df), 1)
    spi_health = assessed_df["spi"].apply(evm_health)
    cpi_health = assessed_df["cpi"].apply(evm_health)
    cost_health = assessed_df["cost_variance_percent"].apply(lambda x: variance_health(float(x), 5, 15))
    schedule_health = assessed_df["schedule_delay_percent"].apply(lambda x: variance_health(float(x), 5, 15))
    risk_health = assessed_df["open_risks_count"].apply(lambda x: count_health(int(x), 4, 8))
    issue_health = assessed_df["open_issues_count"].apply(lambda x: count_health(int(x), 4, 8))
    scope_health = assessed_df["scope_changes_count"].apply(lambda x: count_health(int(x), 2, 5))
    stakeholder_health = assessed_df["stakeholder_sentiment_score"].apply(lambda x: sentiment_health(float(x)))
    pci_health_series = assessed_df.apply(lambda r: pci_health(r), axis=1)

    add("Cost Performance / CPI", f"Avg CPI {assessed_df['cpi'].mean():.2f}", (cpi_health == "Red").sum(), (cpi_health == "Amber").sum(), "Earned value cost efficiency")
    add("Schedule Performance / SPI", f"Avg SPI {assessed_df['spi'].mean():.2f}", (spi_health == "Red").sum(), (spi_health == "Amber").sum(), "Earned value schedule efficiency")
    add("Cost Variance", f"Avg {assessed_df['cost_variance_percent'].mean():.1f}%", (cost_health == "Red").sum(), (cost_health == "Amber").sum(), "Budget variance exposure")
    add("Schedule Delay", f"Avg {assessed_df['schedule_delay_percent'].mean():.1f}%", (schedule_health == "Red").sum(), (schedule_health == "Amber").sum(), "Time variance exposure")
    add("Open Risks", f"Avg {assessed_df['open_risks_count'].mean():.1f}", (risk_health == "Red").sum(), (risk_health == "Amber").sum(), "Open risk exposure")
    add("Open Issues", f"Avg {assessed_df['open_issues_count'].mean():.1f}", (issue_health == "Red").sum(), (issue_health == "Amber").sum(), "Execution blockers")
    add("Scope Changes", f"Avg {assessed_df['scope_changes_count'].mean():.1f}", (scope_health == "Red").sum(), (scope_health == "Amber").sum(), "Change control discipline")
    add("Stakeholder Sentiment", f"Avg {assessed_df['stakeholder_sentiment_score'].mean():.1f}/5", (stakeholder_health == "Red").sum(), (stakeholder_health == "Amber").sum(), "Stakeholder alignment")
    add("Project Control Index (PCI)", f"Avg {assessed_df['pci_score'].mean():.1f}/100", (pci_health_series == "Red").sum(), (pci_health_series == "Amber").sum(), "Project control maturity")

    out = pd.DataFrame(rows)
    out["Exposure Sort"] = out["Critical Projects"] * 3 + out["Watchlist Projects"]
    return out.sort_values("Exposure Sort", ascending=False).drop(columns=["Exposure Sort"])


def portfolio_health_matrix(assessed_df):
    """Create a practical PMO matrix: Schedule Performance vs Cost Performance.

    Rows = schedule health; columns = cost health. This shows where the portfolio
    needs governance focus: schedule-only, cost-only, or combined recovery.
    """
    records = []
    for _, row in assessed_df.iterrows():
        dims = health_breakdown(row)
        records.append({
            "Schedule Performance": status_label(dims["Schedule Performance"]),
            "Cost Performance": status_label(dims["Cost Performance"]),
            "Project": row.get("project_name", "Project")
        })

    matrix = pd.DataFrame(records)
    order = ["On Track", "Watchlist", "Critical"]
    matrix_counts = (
        matrix.groupby(["Schedule Performance", "Cost Performance"])
        .size()
        .reset_index(name="Project Count")
        .pivot(index="Schedule Performance", columns="Cost Performance", values="Project Count")
        .reindex(index=order, columns=order)
        .fillna(0)
        .astype(int)
    )
    return matrix_counts


def portfolio_priority_matrix(assessed_df):
    """Portfolio prioritization matrix: Health Status vs Project Control Index (PCI)."""
    def pci_band(score):
        score = float(score)
        if score >= 75:
            return "Excellent/Good"
        if score >= 60:
            return "Needs Attention"
        return "Weak Control"

    tmp = assessed_df.copy()
    tmp["Health Band"] = tmp["final_status"].apply(status_label)
    tmp["PCI Band"] = tmp["pci_score"].apply(pci_band)
    matrix = pd.crosstab(tmp["Health Band"], tmp["PCI Band"])
    desired_index = ["Critical", "Watchlist", "On Track"]
    desired_cols = ["Excellent/Good", "Needs Attention", "Weak Control"]
    matrix = matrix.reindex(index=desired_index, columns=desired_cols, fill_value=0)
    return matrix

def create_matrix_chart(matrix_df, title, x_label, y_label):
    # Color by severity position, not count volume.
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    severity = []
    for row_label in matrix_df.index:
        row_vals = []
        for col_label in matrix_df.columns:
            labels = [row_label, col_label]
            if "Critical" in labels or "High Risk" in labels or "Weak Control" in labels:
                row_vals.append(2)
            elif "Watchlist" in labels or "Medium Risk" in labels or "Needs Attention" in labels:
                row_vals.append(1)
            else:
                row_vals.append(0)
        severity.append(row_vals)
    cmap = plt.matplotlib.colors.ListedColormap([color_map["On Track"], color_map["Watchlist"], color_map["Critical"]])
    ax.imshow(severity, cmap=cmap, vmin=0, vmax=2)
    ax.set_xticks(range(len(matrix_df.columns)))
    ax.set_yticks(range(len(matrix_df.index)))
    ax.set_xticklabels(matrix_df.columns, rotation=20, ha="right")
    ax.set_yticklabels(matrix_df.index)
    ax.set_xlabel(x_label, fontweight="bold")
    ax.set_ylabel(y_label, fontweight="bold")
    ax.set_title(title, fontweight="bold")
    for i, row_label in enumerate(matrix_df.index):
        for j, col_label in enumerate(matrix_df.columns):
            ax.text(j, i, str(int(matrix_df.loc[row_label, col_label])), ha="center", va="center", color="white", fontweight="bold", fontsize=12)
    return matplotlib_buffer(fig)


def create_portfolio_pdf_report(assessed_df, portfolio_file_name=None):
    """Create an executive portfolio PDF report including summary, charts, matrices, actions, and watchlist."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=28, leftMargin=28, topMargin=28, bottomMargin=28)
    styles = getSampleStyleSheet()
    story = []

    total_projects = len(assessed_df)
    critical_projects = int((assessed_df["final_status"] == "Red").sum())
    watchlist_projects = int((assessed_df["final_status"] == "Amber").sum())
    ontrack_projects = int((assessed_df["final_status"] == "Green").sum())
    avg_pci = round(assessed_df["pci_score"].mean(), 1)
    total_bac = float(assessed_df["budget_at_completion"].sum()) if "budget_at_completion" in assessed_df else 0
    total_eac = float(assessed_df["eac"].sum()) if "eac" in assessed_df else 0
    total_vac = float(assessed_df["vac"].sum()) if "vac" in assessed_df else 0

    story.append(Paragraph("ProjectRescue AI - Portfolio Assessment Report", styles["Title"]))
    if portfolio_file_name:
        story.append(Paragraph(f"<b>Analyzed File:</b> {escape(str(portfolio_file_name))}", styles["Normal"]))
    story.append(Spacer(1, 10))

    summary_rows = [
        ["Total Projects", total_projects, "Critical Projects", critical_projects],
        ["Watchlist Projects", watchlist_projects, "On Track Projects", ontrack_projects],
        ["Average Project Control Index (PCI)", f"{avg_pci}/100", "Total Projects", len(assessed_df)],
        ["Total BAC", f"{total_bac:,.0f}", "Total EAC", f"{total_eac:,.0f}"],
        ["Total VAC", f"{total_vac:,.0f}", "", ""],
    ]
    story.append(Table(summary_rows, colWidths=[115, 100, 115, 100], style=TableStyle([
        ("GRID", (0,0), (-1,-1), 0.25, colors.HexColor("#CCCCCC")),
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F7F7F7")),
        ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8),
    ])))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Executive Summary", styles["Heading2"]))
    story.append(Paragraph(
        f"This portfolio contains {total_projects} projects: {ontrack_projects} On Track, "
        f"{watchlist_projects} Watchlist, and {critical_projects} Critical. "
        f"average Project Control Index (PCI) is {avg_pci}/100, and total forecast variance at completion is {total_vac:,.0f}.",
        styles["Normal"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Portfolio Charts", styles["Heading2"]))
    story.append(Image(create_portfolio_status_chart(assessed_df), width=470, height=260))
    story.append(Spacer(1, 8))
    story.append(Image(create_portfolio_dimension_chart(assessed_df), width=500, height=280))
    story.append(Spacer(1, 8))

    driver_summary = portfolio_kpi_driver_summary(assessed_df)
    story.append(Paragraph("Top Portfolio KPI Watchlist Drivers", styles["Heading2"]))
    story.append(dataframe_to_reportlab_table(driver_summary, max_rows=8, max_cols=4))
    story.append(Spacer(1, 8))
    story.append(Image(create_kpi_exposure_chart(driver_summary), width=500, height=280))
    story.append(Spacer(1, 8))

    schedule_cost_matrix = portfolio_health_matrix(assessed_df)
    priority_matrix = portfolio_priority_matrix(assessed_df)
    story.append(Paragraph("Portfolio Matrix View", styles["Heading2"]))
    story.append(Image(create_matrix_chart(schedule_cost_matrix, "Schedule-Cost Exposure Matrix", "Cost Performance", "Schedule Performance"), width=470, height=285))
    story.append(Spacer(1, 6))
    story.append(dataframe_to_reportlab_table(schedule_cost_matrix.reset_index(), max_rows=10, max_cols=5))
    story.append(Spacer(1, 10))
    story.append(Image(create_matrix_chart(priority_matrix, "Recovery Priority Matrix", "Project Control Index (PCI)", "Health Status"), width=470, height=285))
    story.append(Spacer(1, 6))
    story.append(dataframe_to_reportlab_table(priority_matrix.reset_index(), max_rows=10, max_cols=5))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Portfolio Recovery Actions", styles["Heading2"]))
    for action in portfolio_recovery_actions(assessed_df):
        story.append(Paragraph(f"- {escape(str(action))}", styles["Normal"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Critical Project Watchlist", styles["Heading2"]))
    watch_cols = [
        "project_name", "project_type", "portfolio_health", "recovery_priority",
        "executive_escalation", "spi", "cpi", "cost_variance_percent", "schedule_delay_percent",
        "eac", "vac", "pci_score", "open_risks_count", "open_issues_count"
    ]
    available_cols = [c for c in watch_cols if c in assessed_df.columns]
    priority_df = assessed_df.sort_values(["final_status", "pci_score"], ascending=[False, True])[available_cols]
    story.append(dataframe_to_reportlab_table(priority_df, max_rows=25, max_cols=8))

    doc.build(story)
    buffer.seek(0)
    return buffer



def render_dimension_distribution(assessed_df):
    """Portfolio dimension health section.

    Do not show raw "dimension signal" counts as headline KPIs because a portfolio has
    multiple dimension assessments per project. For example, 500 projects × 7 PMO
    dimensions = 3,500 assessments. Executives should see percentages and a dimension
    matrix, not misleading large raw signal totals.
    """
    dim_df = portfolio_dimension_dataframe(assessed_df)
    if dim_df.empty:
        st.warning("No dimension health records were generated. Please verify the portfolio input columns.")
        return

    dim_counts = dim_df.groupby(["Dimension", "Health"]).size().reset_index(name="Project Count")
    total_projects = len(assessed_df)
    total_assessments = len(dim_df)
    totals = dim_df.groupby("Health").size().to_dict()

    ontrack_count = int(totals.get("On Track", 0))
    watchlist_count = int(totals.get("Watchlist", 0))
    critical_count = int(totals.get("Critical", 0))

    ontrack_pct = (ontrack_count / total_assessments) * 100 if total_assessments else 0
    watchlist_pct = (watchlist_count / total_assessments) * 100 if total_assessments else 0
    critical_pct = (critical_count / total_assessments) * 100 if total_assessments else 0

    st.caption(
        f"Based on {total_assessments:,} PMO dimension assessments "
        f"({total_projects:,} projects × {int(total_assessments / total_projects) if total_projects else 0} dimensions)."
    )

    c0, c1, c2, c3 = st.columns(4)
    c0.metric("Dimension Assessments", f"{total_assessments:,}")
    c1.metric("On Track", f"{ontrack_pct:.1f}%", f"{ontrack_count:,} assessments")
    c2.metric("Watchlist", f"{watchlist_pct:.1f}%", f"{watchlist_count:,} assessments")
    c3.metric("Critical", f"{critical_pct:.1f}%", f"{critical_count:,} assessments")

    pivot = dim_counts.pivot_table(index="Dimension", columns="Health", values="Project Count", fill_value=0).reset_index()
    for col in ["On Track", "Watchlist", "Critical"]:
        if col not in pivot.columns:
            pivot[col] = 0
    pivot = pivot[["Dimension", "On Track", "Watchlist", "Critical"]]
    pivot["Total Projects"] = pivot[["On Track", "Watchlist", "Critical"]].sum(axis=1)
    pivot["Critical %"] = (pivot["Critical"] / pivot["Total Projects"] * 100).round(1)
    pivot["Watchlist %"] = (pivot["Watchlist"] / pivot["Total Projects"] * 100).round(1)
    pivot = pivot.sort_values(["Critical %", "Watchlist %"], ascending=False)

    st.markdown("#### Dimension Health Matrix")
    st.dataframe(styled_dataframe(pivot), use_container_width=True)

    fig_dim = px.bar(
        dim_counts,
        x="Dimension",
        y="Project Count",
        color="Health",
        title="<b>Portfolio Dimension Health Distribution</b>",
        category_orders={"Health": ["On Track", "Watchlist", "Critical"]},
        color_discrete_map=color_map,
        text="Project Count",
        barmode="group"
    )
    fig_dim.update_traces(
        textposition="outside",
        marker_line_color="rgba(255,255,255,0.85)",
        marker_line_width=1.2
    )
    fig_dim.update_layout(
        xaxis=dict(
            title="<b>PMO Control Area</b>",
            tickangle=-20,
            title_font=dict(size=17),
            tickfont=dict(size=14, color="#FFFFFF")
        ),
        yaxis=dict(
            title="<b>Number of Projects</b>",
            title_font=dict(size=17),
            tickfont=dict(size=14, color="#FFFFFF")
        ),
        legend=dict(
            title=dict(text="<b>Health</b>", font=dict(size=17, color="#FFFFFF")),
            font=dict(size=15, color="#FFFFFF"),
            bgcolor="rgba(20,20,20,0.88)",
            bordercolor="rgba(255,255,255,0.25)",
            borderwidth=1
        ),
        height=540,
        margin=dict(t=80, b=130)
    )
    st.plotly_chart(dark_plot(fig_dim), use_container_width=True)

def portfolio_share_links(assessed_df, portfolio_file_name, summary_text):
    total_projects = len(assessed_df)
    critical_projects = int((assessed_df["final_status"] == "Red").sum())
    watchlist_projects = int((assessed_df["final_status"] == "Amber").sum())
    ontrack_projects = int((assessed_df["final_status"] == "Green").sum())
    avg_pci = round(assessed_df["pci_score"].mean(), 1)
    total_bac = float(assessed_df["budget_at_completion"].sum()) if "budget_at_completion" in assessed_df else 0
    total_eac = float(assessed_df["eac"].sum()) if "eac" in assessed_df else 0
    total_vac = float(assessed_df["vac"].sum()) if "vac" in assessed_df else 0
    actions_text = "\n".join([f"- {a}" for a in portfolio_recovery_actions(assessed_df)])
    share_text = f"""
ProjectRescue AI Portfolio Assessment Report

File: {portfolio_file_name or 'Portfolio CSV'}
Projects Assessed: {total_projects}
On Track: {ontrack_projects}
Watchlist: {watchlist_projects}
Critical: {critical_projects}
Average Project Control Index (PCI): {avg_pci}/100
Total BAC: {total_bac:,.0f}
Total EAC: {total_eac:,.0f}
Total Forecast VAC: {total_vac:,.0f}

Executive Summary:
{summary_text}

Portfolio Recovery Actions:
{actions_text}

Note: The full PDF report includes health charts, KPI exposure, matrix views, bubble matrix, and critical project watchlist.

Generated by ProjectRescue AI | ThinkLab.pm
""".strip()
    encoded_text = urllib.parse.quote(share_text)
    encoded_subject = urllib.parse.quote("ProjectRescue AI Portfolio Report")
    return f"https://wa.me/?text={encoded_text}", f"https://mail.google.com/mail/?view=cm&fs=1&su={encoded_subject}&body={encoded_text}"


def render_portfolio_results(assessed_df, portfolio_file_name=None):
    """Detailed portfolio view with executive spacing, working dimension breakdown, and export/share options."""
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    header_col, clear_col = st.columns([4, 1])
    with header_col:
        st.subheader("Portfolio Results")
        if portfolio_file_name:
            st.caption(f"Analyzed file: {portfolio_file_name}")
    with clear_col:
        clear_portfolio = st.button("Clear Results", key="clear_portfolio_results")

    if clear_portfolio:
        st.session_state.portfolio_results = None
        st.session_state.portfolio_file_name = None
        st.rerun()

    total_projects = len(assessed_df)
    critical_projects = int((assessed_df["final_status"] == "Red").sum())
    watchlist_projects = int((assessed_df["final_status"] == "Amber").sum())
    ontrack_projects = int((assessed_df["final_status"] == "Green").sum())
    avg_pci = round(assessed_df["pci_score"].mean(), 1)
    total_bac = float(assessed_df["budget_at_completion"].sum()) if "budget_at_completion" in assessed_df else 0
    total_eac = float(assessed_df["eac"].sum()) if "eac" in assessed_df else 0
    total_vac = float(assessed_df["vac"].sum()) if "vac" in assessed_df else 0

    section_header("Executive Portfolio Command Center", "Portfolio-level KPIs for steering committee review")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Projects", total_projects)
    c2.metric("Critical Projects", critical_projects)
    c3.metric("Watchlist Projects", watchlist_projects)
    c4.metric("On Track Projects", ontrack_projects)

    c5, c6, c7 = st.columns(3)
    c5.metric("Average Project Control Index (PCI)", f"{avg_pci}/100")
    c6.metric("Total BAC", f"{total_bac:,.0f}")
    c7.metric("Total Forecast VAC", f"{total_vac:,.0f}")

    section_header("Portfolio Executive Summary", "Plain-language interpretation of portfolio health")
    summary_text = (
        f"This portfolio contains {total_projects} projects: {ontrack_projects} On Track, "
        f"{watchlist_projects} Watchlist, and {critical_projects} Critical. "
        f"Average Project Control Index (PCI) is {avg_pci}/100, "
        f"and total forecast variance at completion is {total_vac:,.0f}. "
        f"Executive attention should focus first on Critical projects and then on Watchlist projects with weak project control discipline or negative VAC."
    )
    st.markdown(f'<div class="portfolio-summary-card">{summary_text}</div>', unsafe_allow_html=True)

    section_header("Portfolio EVM Forecast & Project Control Index (PCI)", "PMBOK/EVM forecast aggregated at portfolio level")
    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Total BAC", f"{total_bac:,.0f}")
    e2.metric("Total EAC", f"{total_eac:,.0f}")
    e3.metric("Total VAC", f"{total_vac:,.0f}")
    e4.metric("Avg Project Control Index (PCI)", f"{avg_pci}/100")
    st.caption("EAC = BAC / CPI at project level. VAC = BAC - EAC. Negative VAC indicates forecast budget overrun.")

    section_header("Portfolio Health Charts", "Health distribution and 3D project control positioning")
    col1, col2 = st.columns(2)
    with col1:
        status_order = ["On Track", "Watchlist", "Critical"]
        fig1 = px.pie(
            assessed_df,
            names="portfolio_health",
            title="<b>Portfolio Health Distribution</b>",
            color="portfolio_health",
            category_orders={"portfolio_health": status_order},
            color_discrete_map=color_map,
            hole=0.45
        )
        fig1.update_traces(textinfo="percent+label", marker=dict(line=dict(color="#111111", width=2)))
        fig1.update_layout(height=520, margin=dict(t=70, b=50))
        st.plotly_chart(dark_plot(fig1), use_container_width=True)

    with col2:
        fig2 = px.scatter_3d(
            assessed_df,
            x="schedule_variance_days",
            y="cost_variance_percent",
            z="pci_score",
            color="portfolio_health",
            hover_name="project_name",
            title="<b>3D Portfolio Control View</b>",
            category_orders={"portfolio_health": status_order},
            color_discrete_map=color_map
        )
        fig2.update_layout(height=520, margin=dict(t=70, b=40))
        st.plotly_chart(polish_3d_portfolio_chart(dark_plot(fig2)), use_container_width=True)

    section_header("Health Breakdown by Dimension", "Cross-portfolio status of PMO control areas")
    render_dimension_distribution(assessed_df)

    section_header("Top Portfolio KPI Watchlist Drivers", "Critical and Watchlist exposure by KPI")
    driver_summary = portfolio_kpi_driver_summary(assessed_df)
    st.dataframe(styled_dataframe(driver_summary), use_container_width=True)

    fig_driver = px.bar(
        driver_summary.head(8),
        x="Driver",
        y=["Critical Projects", "Watchlist Projects"],
        title="<b>Critical & Watchlist Exposure by KPI</b>",
        barmode="group",
        text_auto=True,
        color_discrete_map={
            "Critical Projects": color_map["Critical Projects"],
            "Watchlist Projects": color_map["Watchlist Projects"]
        }
    )
    fig_driver.update_traces(marker_line_color="rgba(255,255,255,0.85)", marker_line_width=1.5)
    fig_driver.update_layout(
        xaxis=dict(title="<b>KPI Driver</b>", tickangle=-20, title_font=dict(size=17), tickfont=dict(size=14, color="#FFFFFF")),
        yaxis=dict(title="<b>Number of Projects</b>", title_font=dict(size=17), tickfont=dict(size=14, color="#FFFFFF")),
        legend=dict(title=dict(text="<b>Exposure Level</b>", font=dict(size=17, color="#FFFFFF")), font=dict(size=15, color="#FFFFFF")),
        height=560,
        margin=dict(t=80, b=120)
    )
    st.plotly_chart(dark_plot(fig_driver), use_container_width=True)

    section_header("Portfolio Matrix View", "Matrix colors show severity; cell numbers show project count")
    m1, m2 = st.columns(2)
    schedule_cost_matrix = portfolio_health_matrix(assessed_df)
    priority_matrix = portfolio_priority_matrix(assessed_df)
    matrix_colorscale = [
        [0.0, "#173D25"], [0.49, "#173D25"],
        [0.50, "#7A5200"], [0.74, "#7A5200"],
        [0.75, "#8B0000"], [1.0, "#8B0000"]
    ]

    with m1:
        st.markdown("#### Schedule vs Cost Performance Matrix")
        status_risk = {"On Track": 0, "Watchlist": 1, "Critical": 2}
        schedule_cost_severity = pd.DataFrame(
            [[max(status_risk.get(row_label, 0), status_risk.get(col_label, 0)) for col_label in schedule_cost_matrix.columns] for row_label in schedule_cost_matrix.index],
            index=schedule_cost_matrix.index,
            columns=schedule_cost_matrix.columns
        )
        fig_matrix = go.Figure(data=go.Heatmap(
            z=schedule_cost_severity.values,
            x=list(schedule_cost_matrix.columns),
            y=list(schedule_cost_matrix.index),
            zmin=0,
            zmax=2,
            colorscale=matrix_colorscale,
            showscale=False,
            text=schedule_cost_matrix.values,
            customdata=schedule_cost_matrix.values,
            texttemplate="<b>%{text}</b>",
            textfont={"size": 18, "color": "#FFFFFF"},
            hovertemplate="Schedule: %{y}<br>Cost: %{x}<br>Projects: %{customdata}<extra></extra>"
        ))
        fig_matrix.update_layout(
            title="<b>Schedule-Cost Exposure Matrix</b>",
            xaxis_title="<b>Cost Performance</b>",
            yaxis_title="<b>Schedule Performance</b>",
            paper_bgcolor="#0B0B0B",
            plot_bgcolor="#0B0B0B",
            font=dict(color="#FFFFFF", family="Inter"),
            height=450,
            margin=dict(t=80, b=70)
        )
        st.plotly_chart(fig_matrix, use_container_width=True)
        st.dataframe(styled_dataframe(schedule_cost_matrix.reset_index().rename(columns={"index": "Schedule Performance"})), use_container_width=True)

    with m2:
        st.markdown("#### Health Status vs Project Control Index (PCI) Matrix")
        health_band_score = {"On Track": 0, "Watchlist": 1, "Critical": 2}
        pci_band_score = {"Excellent/Good": 0, "Needs Attention": 1, "Weak Control": 2}
        priority_severity = pd.DataFrame(
            [[max(health_band_score.get(row_label, 0), pci_band_score.get(col_label, 0)) for col_label in priority_matrix.columns] for row_label in priority_matrix.index],
            index=priority_matrix.index,
            columns=priority_matrix.columns
        )
        fig_priority = go.Figure(data=go.Heatmap(
            z=priority_severity.values,
            x=list(priority_matrix.columns),
            y=list(priority_matrix.index),
            zmin=0,
            zmax=2,
            colorscale=matrix_colorscale,
            showscale=False,
            text=priority_matrix.values,
            customdata=priority_matrix.values,
            texttemplate="<b>%{text}</b>",
            textfont={"size": 18, "color": "#FFFFFF"},
            hovertemplate="Health Status: %{y}<br>PCI Band: %{x}<br>Projects: %{customdata}<extra></extra>"
        ))
        fig_priority.update_layout(
            title="<b>Recovery Priority Matrix</b>",
            xaxis_title="<b>Project Control Index (PCI)</b>",
            yaxis_title="<b>Health Status</b>",
            paper_bgcolor="#0B0B0B",
            plot_bgcolor="#0B0B0B",
            font=dict(color="#FFFFFF", family="Inter"),
            height=450,
            margin=dict(t=80, b=70)
        )
        st.plotly_chart(fig_priority, use_container_width=True)
        st.dataframe(styled_dataframe(priority_matrix.reset_index().rename(columns={"index": "Health Status"})), use_container_width=True)

    st.markdown('<div class="table-note">Matrix colors show severity: green = healthy/managed, amber = watchlist, red = critical. Cell numbers show project count.</div>', unsafe_allow_html=True)

    section_header("Portfolio Bubble Matrix", "Budget-weighted view of schedule delay vs cost variance")
    bubble_df = assessed_df.copy()
    bubble_df["Portfolio Health"] = bubble_df["final_status"].apply(status_label)
    bubble_df["Bubble Size"] = bubble_df.get("budget_at_completion", pd.Series([100000] * len(bubble_df))).astype(float).clip(lower=1)
    fig_bubble = px.scatter(
        bubble_df,
        x="schedule_delay_percent",
        y="cost_variance_percent",
        size="Bubble Size",
        color="Portfolio Health",
        hover_name="project_name",
        hover_data={
            "project_type": True,
            "spi": ":.2f",
            "cpi": ":.2f",
            "pci_score": ":.1f",
            "Bubble Size": False
        },
        title="<b>Schedule Delay vs Cost Variance Bubble Matrix</b>",
        category_orders={"Portfolio Health": ["On Track", "Watchlist", "Critical"]},
        color_discrete_map=color_map,
        size_max=30
    )
    fig_bubble.update_layout(
        xaxis=dict(title="<b>Schedule Delay %</b>", title_font=dict(size=17), tickfont=dict(size=14)),
        yaxis=dict(title="<b>Cost Variance %</b>", title_font=dict(size=17), tickfont=dict(size=14)),
        legend=dict(title=dict(text="<b>Project Health</b>", font=dict(size=17, color="#FFFFFF")), font=dict(size=15, color="#FFFFFF")),
        height=560,
        margin=dict(t=80, b=70)
    )
    fig_bubble.add_vline(x=5, line_dash="dash", line_color="rgba(255,255,255,0.35)")
    fig_bubble.add_vline(x=15, line_dash="dash", line_color="rgba(255,255,255,0.35)")
    fig_bubble.add_hline(y=5, line_dash="dash", line_color="rgba(255,255,255,0.35)")
    fig_bubble.add_hline(y=15, line_dash="dash", line_color="rgba(255,255,255,0.35)")
    st.plotly_chart(dark_plot(fig_bubble), use_container_width=True)

    section_header("Portfolio Recovery Actions", "Prioritized governance actions for the portfolio")
    for action in portfolio_recovery_actions(assessed_df):
        st.write(f"• {action}")

    section_header("Critical Project Watchlist", "Top projects requiring management attention")
    watch_cols = [
        "project_name", "project_type", "portfolio_health", "recovery_priority",
        "executive_escalation", "spi", "cpi", "cost_variance_percent", "schedule_delay_percent",
        "eac", "vac", "pci_score", "open_risks_count", "open_issues_count"
    ]
    available_cols = [c for c in watch_cols if c in assessed_df.columns]
    priority_source = assessed_df.copy()
    priority_source["_health_order"] = priority_source["final_status"].map({"Red": 3, "Amber": 2, "Green": 1}).fillna(0)
    priority_df = priority_source.sort_values(["_health_order", "pci_score"], ascending=[False, True])[available_cols]
    st.dataframe(styled_dataframe(priority_df.head(25)), use_container_width=True)

    section_header("Export & Share", "Download the full portfolio PDF report or share the executive summary")
    st.caption("The report includes executive summary, EVM forecast, Project Control Index (PCI), health charts, KPI exposure, matrix views, bubble matrix, recovery actions, and critical project watchlist.")
    portfolio_pdf_buffer = create_portfolio_pdf_report(assessed_df, portfolio_file_name)
    st.download_button(
        "Download PDF Report",
        data=portfolio_pdf_buffer,
        file_name="project_rescue_portfolio_assessment_report.pdf",
        mime="application/pdf",
        key="download_portfolio_pdf_report"
    )
    whatsapp_url, gmail_url = portfolio_share_links(assessed_df, portfolio_file_name, summary_text)
    s1, s2 = st.columns(2)
    with s1:
        st.link_button("Share Summary on WhatsApp", whatsapp_url)
    with s2:
        st.link_button("Share Summary via Gmail", gmail_url)

    st.markdown("</div>", unsafe_allow_html=True)




# -----------------------------
# CREATOR JOURNEY
# -----------------------------
def render_creator_journey():
    """Clean premium creator journey.

    Fixes:
    - no raw HTML leakage (uses textwrap.dedent + unsafe_allow_html)
    - no voice greeting
    - no repeated chips/strips/badges in Chapter 6 or Chapter 7
    - one focused chapter card at a time
    - correct LinkedIn and email links
    """
    publication_url = "https://ejtas.com/index.php/journal/article/view/94/68"

    chapters = [
        {
            "icon": "🎓",
            "nav": "Foundation",
            "sub": "Where the journey began",
            "kicker": "CHAPTER 1",
            "title": "Building the Foundation",
            "body": "Every project begins with learning. My journey began with Computer Science and grew into structured problem solving, technology, and delivery thinking.",
            "cards": [
                ("🎓", "B.E. Computer Science & Engineering", "Strong technical foundation"),
                ("📖", "M.S. Management of Technology", "Management, technology, and innovation"),
                ("💡", "Early Mindset", "Curiosity shaped the direction"),
            ],
            "takeaway": ("What it shaped", "A problem-solving mindset grounded in technology and execution."),
        },
        {
            "icon": "🌐",
            "nav": "Global Perspective",
            "sub": "Learning beyond borders",
            "kicker": "CHAPTER 2",
            "title": "Learning Beyond Borders",
            "body": "Global exposure shaped how I view leadership, communication, stakeholder trust, and disciplined execution across teams.",
            "cards": [
                ("🌎", "Global Exposure", "Broader view of people, process, and delivery"),
                ("🤝", "Stakeholder Communication", "Clarity, empathy, and alignment"),
                ("🧭", "Enterprise Mindset", "Connecting decisions to outcomes"),
            ],
            "takeaway": ("What it shaped", "A delivery mindset that values people, clarity, and accountable execution."),
        },
        {
            "icon": "💼",
            "nav": "Enterprise Delivery",
            "sub": "Turning strategy into delivery",
            "kicker": "CHAPTER 3",
            "title": "Turning Strategy into Delivery",
            "body": "Experience across public sector IT, higher education operations, enterprise software, and digital transformation shaped my delivery mindset: plan clearly, communicate early, and execute with ownership.",
            "cards": [
                ("🏛️", "Public Sector IT", "Enterprise software, renewals, governance, and stakeholders"),
                ("🎓", "Higher Education Operations", "Large-scale operations, compliance, and service delivery"),
                ("🧠", "Enterprise Software", "Requirements, data, delivery, quality, and client communication"),
            ],
            "takeaway": ("Professional signal", "Strategy becomes valuable only when teams can execute it with clarity."),
        },
        {
            "icon": "🏅",
            "nav": "Certifications",
            "sub": "Continuous learning",
            "kicker": "CHAPTER 4",
            "title": "Commitment to Professional Growth",
            "body": "Certifications strengthened the discipline behind planning, Agile delivery, risk management, governance, and recovery thinking.",
            "cards": [
                ("🏆", "PMP®", "Project leadership and governance"),
                ("📘", "CAPM®", "Project management fundamentals"),
                ("🧩", "CSM® / CSPO®", "Agile, Scrum, and product thinking"),
            ],
            "takeaway": ("Continuous learning", "The goal is not to collect credentials, but to keep improving how projects are led and delivered."),
        },
        {
            "icon": "📖",
            "nav": "Professional Contribution",
            "sub": "Research to practice",
            "kicker": "CHAPTER 5",
            "title": "Contributing to the Profession",
            "body": "My article, Project Management in the Era of Artificial Intelligence, explored how AI can support better project decision-making — the same idea that later shaped ProjectRescue AI.",
            "cards": [
                ("📖", "Published Article", "Project Management in the Era of Artificial Intelligence"),
                ("🤖", "AI for Project Management", "Decision support and project intelligence"),
                ("🔗", "Research → Practice → Product", "A professional idea turned into a working platform"),
            ],
            "publication": True,
            "takeaway": ("Research to product thinking", "A published idea became a practical product direction."),
        },
        {
            "icon": "🚀",
            "nav": "Why ProjectRescue AI",
            "sub": "Purpose behind building",
            "kicker": "CURRENT CHAPTER",
            "title": "Why ProjectRescue AI Exists",
            "body": "Across enterprise environments, I saw project risks often noticed too late. ProjectRescue AI helps project leaders assess health, forecast impact, prioritize recovery actions, and communicate with confidence.",
            "cards": [
                ("🧪", "Assess", "Health and risk signals"),
                ("📈", "Forecast", "EAC, VAC, recovery probability"),
                ("📝", "Report", "Executive-ready insights"),
            ],
            "takeaway": ("Product purpose", "Turning scattered project signals into clearer PMO decisions."),
        },
        {
            "icon": "🛣️",
            "nav": "Road Ahead",
            "sub": "The journey continues",
            "kicker": "THE ROAD CONTINUES",
            "title": "Driving Toward What Comes Next",
            "body": "The journey continues toward richer portfolio intelligence, configurable PMO thresholds, what-if recovery planning, assessment history, and executive-ready governance workflows.",
            "cards": [
                ("🧪", "What-if Analysis", "Test recovery options before decisions"),
                ("📚", "Assessment History", "Track project health over time"),
                ("🌐", "Portfolio Intelligence", "Governance at scale"),
            ],
            "takeaway": ("The road continues", "Every successful project is a journey of continuous learning, adaptation, and improvement. ProjectRescue AI is one milestone on that road — not the final destination."),
        },
    ]

    if "creator_journey_step" not in st.session_state:
        st.session_state.creator_journey_step = 0

    step = max(0, min(int(st.session_state.creator_journey_step), len(chapters) - 1))
    current = chapters[step]

    def esc(value):
        return escape(str(value))

    def route_html():
        output = []
        for i, ch in enumerate(chapters):
            active = " active" if i == step else ""
            output.append(
                f'<div class="cj-route-item{active}">'
                f'<div class="cj-num">{i + 1}</div>'
                f'<div class="cj-icon">{ch["icon"]}</div>'
                f'<div><div class="cj-route-title">{esc(ch["nav"])}</div>'
                f'<div class="cj-route-sub">{esc(ch["sub"])}</div></div>'
                f'</div>'
            )
        return "".join(output)

    def cards_html(items):
        output = []
        for icon, title, sub in items:
            output.append(
                f'<div class="cj-info-card">'
                f'<div class="cj-info-icon">{icon}</div>'
                f'<div><div class="cj-info-title">{esc(title)}</div>'
                f'<div class="cj-info-sub">{esc(sub)}</div></div>'
                f'</div>'
            )
        return "".join(output)

    publication_html = ""
    if current.get("publication"):
        publication_html = (
            f'<div class="cj-publication">'
            f'<div class="cj-publication-label">Featured Publication</div>'
            f'<a href="{publication_url}" target="_blank" rel="noopener noreferrer">'
            f'Project Management in the Era of Artificial Intelligence</a>'
            f'<div class="cj-publication-meta">European Journal of Theoretical and Applied Sciences, 2023</div>'
            f'<div class="cj-publication-tag">Research → Practice → Product Thinking</div>'
            f'</div>'
        )

    takeaway_title, takeaway_text = current.get("takeaway", ("", ""))
    takeaway_html = ""
    if takeaway_title or takeaway_text:
        takeaway_html = (
            f'<div class="cj-takeaway">'
            f'<div class="cj-takeaway-icon">✦</div>'
            f'<div><div class="cj-takeaway-title">{esc(takeaway_title)}</div>'
            f'<div class="cj-takeaway-sub">{esc(takeaway_text)}</div></div>'
            f'</div>'
        )

    dots = "".join([
        f'<span class="cj-dot {"active" if i == step else "done" if i < step else ""}"></span>'
        for i in range(len(chapters))
    ])

    html = f"""
    <div class="cj-wrap">
        <div class="cj-topbar">
            <div class="cj-headline">
                <h2>Creator Journey</h2>
                <p>Every milestone shaped the way I lead, build, and deliver.</p>
                <div class="cj-headline-line"></div>
            </div>
        </div>

        <div class="cj-grid">
            <div class="cj-left">
                <div class="cj-route">{route_html()}</div>
            </div>

            <div class="cj-main">
                <div class="cj-content">
                    <div class="cj-kicker">{esc(current['kicker'])}</div>
                    <div class="cj-title">{esc(current['title'])}</div>
                    <div class="cj-title-line"></div>
                    <div class="cj-body">{esc(current['body'])}</div>
                    <div class="cj-card-stack">{cards_html(current.get('cards', []))}</div>
                    {publication_html}
                    {takeaway_html}
                </div>
            </div>
        </div>

        <div class="cj-footer">
            <div>ProjectRescue AI © 2026 | Designed & Developed by Sivasubramaniyan Sahadevan</div>
            <div>
                <a href="https://www.linkedin.com/in/sivasubramaniyan-sahadevan" target="_blank" rel="noopener noreferrer">LinkedIn</a>
                <a href="mailto:sivasubramaniyansahadevan@gmail.com">Email</a>
            </div>
        </div>
    </div>
    """
    # IMPORTANT: Strip leading indentation before rendering.
    # Streamlit markdown treats 4-space-indented HTML as a code block,
    # which is why the raw <div> code was appearing in the app.
    html = "\n".join(line.strip() for line in html.splitlines() if line.strip())
    st.markdown(html, unsafe_allow_html=True)

    nav_left, nav_mid, nav_right = st.columns([1, 3, 1])
    with nav_left:
        if st.button("← Previous", key="creator_prev", disabled=(step == 0)):
            st.session_state.creator_journey_step = max(0, step - 1)
            st.rerun()
    with nav_mid:
        st.markdown(
            f'<div class="cj-dots">{dots}</div>'
            f'<div style="text-align:center;color:#C9D1D9;margin-top:10px;font-weight:800;">'
            f'Chapter {step + 1} of {len(chapters)}</div>',
            unsafe_allow_html=True
        )
    with nav_right:
        if st.button("Next →", key="creator_next", disabled=(step == len(chapters) - 1)):
            st.session_state.creator_journey_step = min(len(chapters) - 1, step + 1)
            st.rerun()




def render_global_footer():
    st.markdown("""
    <div class="footer">
        ProjectRescue AI © 2026 | Designed &amp; Developed by Sivasubramaniyan Sahadevan
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# MAIN UI
# -----------------------------

# Session-state containers keep Portfolio and Single Project workflows independent.
if "portfolio_results" not in st.session_state:
    st.session_state.portfolio_results = None

if "portfolio_file_name" not in st.session_state:
    st.session_state.portfolio_file_name = None

if "manual_result" not in st.session_state:
    st.session_state.manual_result = None


tab_csv, tab_manual, tab_creator = st.tabs([
    "📊Portfolio Assessment",
    "🎯Single Project Assessment",
    "🧭Creator Journey"
])


with tab_csv:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Portfolio Assessment")

    with st.form("portfolio_form"):
        uploaded_file = st.file_uploader(
            "Upload project portfolio CSV",
            type=["csv"],
            key="portfolio_csv_upload"
        )

        st.caption("Upload your CSV, then click Analyze Portfolio. The app will not analyze automatically.")

        analyze_portfolio = st.form_submit_button("Analyze Portfolio")

    st.markdown("</div>", unsafe_allow_html=True)

    # If the uploaded file is removed, clear only the portfolio result output area.
    # This prevents old portfolio results from remaining visible after file removal.
    if uploaded_file is None:
        st.session_state.portfolio_results = None
        st.session_state.portfolio_file_name = None

    if analyze_portfolio:
        if uploaded_file is None:
            st.warning("Please upload a CSV file first.")
        else:
            progress_placeholder = st.empty()
            with st.spinner("Generating portfolio assessment... Please wait while ProjectRescue AI analyzes the CSV, calculates EVM forecasts, PCI, matrices, and recovery actions."):
                df = pd.read_csv(uploaded_file)
                assessed_rows = []
                total_rows = len(df)
                progress_bar = progress_placeholder.progress(0, text="Starting portfolio assessment...")

                for idx, (_, r) in enumerate(df.iterrows(), start=1):
                    try:
                        result_row, prediction, final_status, severe, summary, priority, reasons, actions, timeline, escalation = assess_project(r)

                        assessed_rows.append({
                            **result_row,
                            "model_prediction": prediction,
                            "final_status": final_status,
                            "portfolio_health": status_label(final_status),
                            "recovery_priority": priority,
                            "recovery_timeline": timeline,
                            "executive_escalation": escalation
                        })

                    except Exception as e:
                        st.warning(f"Skipped one row due to invalid data: {e}")

                    if total_rows > 0:
                        progress_bar.progress(
                            min(idx / total_rows, 1.0),
                            text=f"Analyzing project {idx} of {total_rows}..."
                        )

                st.session_state.portfolio_results = pd.DataFrame(assessed_rows)
                st.session_state.portfolio_file_name = uploaded_file.name
                progress_placeholder.empty()

    if st.session_state.portfolio_results is not None:
        assessed_df = st.session_state.portfolio_results

        if not assessed_df.empty:
            render_portfolio_results(assessed_df, st.session_state.portfolio_file_name)

    else:
        st.info("Upload a CSV file and click Analyze Portfolio.")

    render_global_footer()


with tab_manual:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Single Project Assessment")

    with st.form("manual_project_form"):
        col_a, col_b = st.columns(2)

        with col_a:
            project_name = st.text_input(
                "Project Name",
                "Cloud Migration Program"
            )

            project_type = st.selectbox(
                "Project Type",
                [
                    "Cloud Migration",
                    "ERP Implementation",
                    "CRM Modernization",
                    "Data Warehouse Migration",
                    "Cybersecurity Program",
                    "ITSM Transformation",
                    "Procurement Automation",
                    "License Optimization",
                    "Infrastructure Refresh",
                    "Mobile App Development",
                    "AI Adoption Program",
                    "Other"
                ]
            )

            project_duration_days = st.number_input(
                "Planned Project Duration Days",
                min_value=1,
                value=180
            )

            budget_at_completion = st.number_input(
                "Budget at Completion / BAC",
                min_value=0.0,
                value=100000.0,
                step=1000.0
            )

            completed_tasks_percent = st.slider(
                "Completed Tasks %",
                0,
                100,
                65
            )

            cost_variance_percent = st.number_input(
                "Cost Variance %",
                value=8.0
            )

            schedule_variance_days = st.number_input(
                "Schedule Delay Days",
                value=10
            )

            spi = st.number_input(
                "SPI",
                value=0.95,
                step=0.01
            )

            cpi = st.number_input(
                "CPI",
                value=0.96,
                step=0.01
            )

        with col_b:
            open_risks_count = st.number_input(
                "Open Risks",
                min_value=0,
                value=4
            )

            open_issues_count = st.number_input(
                "Open Issues",
                min_value=0,
                value=3
            )

            scope_changes_count = st.number_input(
                "Scope Changes",
                min_value=0,
                value=2
            )

            resource_utilization_percent = st.slider(
                "Resource Utilization %",
                0,
                100,
                85
            )

            stakeholder_sentiment_score = st.slider(
                "Stakeholder Sentiment",
                1.0,
                5.0,
                3.5,
                step=0.1
            )

        analyze_manual = st.form_submit_button("Analyze Project")

    st.markdown("</div>", unsafe_allow_html=True)

    if analyze_manual:
        manual_row = {
            "project_name": project_name,
            "project_type": project_type,
            "project_duration_days": project_duration_days,
            "budget_at_completion": budget_at_completion,
            "completed_tasks_percent": completed_tasks_percent,
            "cost_variance_percent": cost_variance_percent,
            "schedule_variance_days": schedule_variance_days,
            "spi": spi,
            "cpi": cpi,
            "open_risks_count": open_risks_count,
            "open_issues_count": open_issues_count,
            "scope_changes_count": scope_changes_count,
            "resource_utilization_percent": resource_utilization_percent,
            "stakeholder_sentiment_score": stakeholder_sentiment_score
        }

        with st.spinner("Generating project assessment... Please wait while ProjectRescue AI calculates health, EVM forecast, PCI, KPI drivers, and recovery actions."):
            st.session_state.manual_result = assess_project(manual_row)

    if st.session_state.manual_result is not None:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        _, clear_col = st.columns([4, 1])
        with clear_col:
            clear_manual = st.button("Clear Result", key="clear_manual_result")

        if clear_manual:
            st.session_state.manual_result = None
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        render_result(*st.session_state.manual_result)

    render_global_footer()







with tab_creator:
    render_creator_journey()
