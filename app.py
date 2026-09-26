# import streamlit as st
# import yfinance as yf
# import pandas as pd
# import numpy as np

# st.set_page_config(page_title="Max 1-Day Move Scanner", page_icon="📈", layout="wide")
# st.title("📈 Max 1-Day Move Scanner — Full History")
# st.caption("Fetches the maximum available Yahoo Finance history for each ticker and finds each stock's single largest 1-day % gain and % drop.")

# # ==============================================================================
# # KNOWN_STOCKS universe (same list as the reference dashboard)
# # ==============================================================================
# KNOWN_STOCKS = [
#     'PALL', 'PLTM', 'IHF', 'ESTC', 'PRU', 'RGEN', 'UBS', 'TRV', 'WEN', 'OKLO', 'IBB', 'Q', 'OUST', 'VPG', 'WOLF', 'NOK', 'HSBC', 'DLTR', 'SKHY', 'RDDT', 'RL', 'CROX', 'LEVI', 'FOTO', 'GNRC', 'KLIC', 'IWM', 'HBMX', 'PWR', 'EUV', 'GRID', 'MAGS', 'SPCX', 'IBM', 'ELV', 'OSCR', 'QNT', 'HYDR', 'ALGM', 'LGN', 'IESC', 'AEHR', 'ACLS', 'MKSI', 'SMTC', 'AMKR',
#     'LSCC', 'DIOD', 'POWI', 'AA', 'ABBV', 'ALAB', 'AMGN', 'APO', 'BOTZ', 'CRCL', 'CRWV', 'D', 'DRAM', 'DUK', 'EEM', 'EWJ', 'EWY', 'EXC', 'FIGR',
#     'GEV', 'GILD', 'GXC', 'JEF', 'KMI', 'KRMN', 'LIN', 'MNST', 'NASA', 'NEM', 'NTR', 'OR',
#     'OWL', 'Q', 'QQQ', 'RNG', 'RKT', 'SCCO', 'SHLD', 'SO', 'SOLS', 'SPMO', 'SPY', 'SPHB', 'TSEM', 'UNP', 'VTV',
#     'VUG', 'WGMI', 'WMB', 'XEL', 'XMAG', 'XYZ', 'ZIM', 'VICR', 'SLX', 'CBOE', 'SIMO', 'FLEX', 'POWL', 'VLO', 'DOCN',
#     'IYZ', 'LNG', 'AAOI', 'AXTI', 'TSEM', 'USO', 'JNJ',
#     'HP', 'GLD', 'ALB', 'BUG', 'BX', 'DOW', 'VZ', 'REMX', 'GDX', 'SIL', 'VEEV', 'SNDK', 'TLT', 'APH', 'ARM', 'FANG',
#     'NBIS', 'NVT', 'OXY', 'FORM', 'IBIT', 'QTUM', 'IAI', 'KWEB', 'IHI', 'UFO', 'ITA', 'IYT', 'CVS', 'HUM', 'NEE',
#     'HPE', 'PLAB', 'INOD', 'TTMI', 'CCJ', 'BE', 'SLV', 'PICK', 'COPX', 'MAR', 'XAR', 'VSXY', 'GLW', 'ANF', 'AEO',
#     'AEP', 'GH', 'SANM', 'ROK', 'PSN', 'IAT', 'HROW', 'PL', 'AVAV', 'CIEN', 'COHR', 'NU', 'WULF', 'IREN', 'CIFR',
#     'RDW', 'PH', 'LITE', 'ACHR', 'CACI', 'CRS', 'URA', 'NVO', 'NLR', 'ITB', 'EOSE', 'APP', 'RKLB', 'ASTS',
#     'IONQ', 'RMBS', 'RTX', 'NOC', 'LMT', 'HON', 'ONDS', 'CLS', 'LEU', 'VRT', 'VST', 'NRG', 'CEG', 'SMCI', 'CRDO',
#     'SOFI', 'XLP', 'XLE', 'HIMS', 'HOOD', 'GEV', 'XLV', 'HACK', 'XOP', 'CIBR', 'ICLN', 'XLB', 'XLU', 'XLRE', 'IGV',
#     'XLF', 'IPAY', 'XLC', 'XLI', 'KRE', 'XLK', 'CLOU', 'KBE', 'XME', 'XTL', 'JETS', 'SMH', 'XLY', 'XHB',
#     'XBI', 'XRT', 'MJ', 'META', 'MSFT', 'AAPL', 'AMZN', 'GOOGL', 'NVDA', 'TSLA', 'ARKX', 'ARKQ', 'ARKF',
#     'ARKW', 'ARKK', 'ARKG', 'CCL', 'RCL', 'UAL', 'BA', 'DAL', 'NCLH', 'AAL', 'LUV', 'PINS', 'SNAP',
#     'IBKR', 'SCHW', 'JPM', 'MS', 'GS', 'BAC', 'WFC', 'SPGI', 'BLK', 'NDAQ', 'C', 'LI', 'BIDU', 'NIO', 'XPEV',
#     'BABA', 'PDD', 'JD', 'DQ', 'JKS', 'ENPH', 'FSLR', 'TAN', 'SEDG', 'CSIQ', 'SPWR', 'RUN', 'PBW', 'CLX', 'PG',
#     'EL', 'LULU', 'SBUX', 'NKE', 'MELI', 'EBAY', 'FDX', 'UPS', 'SE', 'JMIA', 'ETSY', 'SHOP',
#     'Z', 'OPEN', 'CHWY', 'CVNA', 'BARK', 'GM', 'BLNK', 'QS', 'F', 'RIVN', 'FCEL', 'CHPT', 'LCID',
#     'UPST', 'PYPL', 'AFRM', 'V', 'MA', 'AXP', 'BITO', 'COIN', 'RIOT', 'MARA', 'MSTR',
#     'DKNG', 'PENN', 'BETZ', 'REGN', 'VRTX', 'MRK', 'UNH', 'TMO', 'ISRG', 'ABT', 'IDXX', 'TDOC', 'CRSP',
#     'BRK-B', 'ETN', 'CAT', 'U', 'RBLX', 'SKLZ', 'FSLY', 'TRIP', 'EXPE', 'BKNG', 'ABNB', 'DIS', 'WMT',
#     'COST', 'TGT', 'LOW', 'HD', 'DT', 'SNPS', 'CDNS', 'MDB', 'ORCL', 'NOW', 'ADP', 'SNOW', 'DDOG',
#     'FROG', 'ADSK', 'INTU', 'TEAM', 'WDAY', 'CRM', 'PAYC', 'ANET', 'ADBE', 'ACN', 'EPAM', 'ZM', 'TTD', 'TWLO',
#     'DASH', 'APPS', 'DOCU', 'AI', 'AKAM', 'QLYS', 'PANW', 'FTNT', 'CRWD', 'TENB', 'OKTA', 'ZS',
#     'NET', 'S', 'UMC', 'ASML', 'KEYS', 'CRUS', 'AMD', 'AVGO', 'MU', 'KLAC', 'TXN', 'QRVO', 'TSM', 'SWKS', 'AMBA',
#     'STM', 'MCHP', 'ON', 'QCOM', 'SOXX', 'MRVL', 'ADI', 'LRCX', 'AMAT', 'WDC', 'NXPI', 'TER', 'MPWR', 'INTC',
#     'GFS', 'STX', 'A', 'ZBRA', 'ENTG', 'ONTO', 'TRMB', 'BNTX', 'PFE', 'MRNA', 'NVAX', 'FCX', 'CF', 'DRI',
#     'PEP', 'XOM', 'LLY', 'CL', 'MCD', 'KO', 'GE', 'CVX', 'FISV', 'DE', 'WM', 'HLT', 'FUTU', 'UBER',
#     'TIGR', 'EQIX', 'DPZ', 'CSCO', 'COKE', 'SONY', 'FDS', 'MCO', 'GRAB', 'PTON', 'AMT', 'LIT', 'CMG', 'IPO',
#     'INMD', 'NNDM', 'MP', 'FUBO', 'SPOT', 'ALGN', 'PZZA', 'LOVE', 'LMND', 'POOL', 'PLTR', 'ROKU',
#     'CELH', 'NFLX', 'DHI', 'DELL'
# ]
# KNOWN_STOCKS = sorted(set(KNOWN_STOCKS))

# # ==============================================================================
# # Data fetch — chunked to stay well under Yahoo's rate limits
# # ==============================================================================
# @st.cache_data(ttl=86400, show_spinner=False)
# def download_max_history(tickers, chunk_size=40):
#     """
#     Downloads maximum available daily history for all tickers, in chunks,
#     and returns a dict of {ticker: DataFrame(Date, Close)}.
#     """
#     result = {}
#     chunks = [tickers[i:i + chunk_size] for i in range(0, len(tickers), chunk_size)]

#     progress = st.progress(0)
#     status = st.empty()

#     for idx, chunk in enumerate(chunks):
#         status.text(f"Downloading batch {idx + 1}/{len(chunks)} ({len(chunk)} tickers)...")
#         try:
#             raw = yf.download(
#                 chunk, period="max", interval="1d",
#                 progress=False, auto_adjust=True, group_by="ticker", threads=True
#             )
#         except Exception:
#             progress.progress((idx + 1) / len(chunks))
#             continue

#         for ticker in chunk:
#             try:
#                 if len(chunk) == 1:
#                     df = raw[['Close']].dropna()
#                 else:
#                     df = raw[ticker][['Close']].dropna()
#                 if not df.empty and len(df) > 1:
#                     result[ticker] = df
#             except Exception:
#                 continue

#         progress.progress((idx + 1) / len(chunks))

#     status.empty()
#     progress.empty()
#     return result


# @st.cache_data(ttl=86400, show_spinner=False)
# def compute_max_moves(ticker_data):
#     """
#     For each ticker, computes the single largest 1-day % gain and
#     single largest 1-day % drop across its full available history,
#     along with the date each occurred.
#     """
#     rows = []
#     for ticker, df in ticker_data.items():
#         try:
#             close = df['Close']
#             pct_chg = close.pct_change().dropna() * 100
#             if pct_chg.empty:
#                 continue

#             max_gain = pct_chg.max()
#             max_gain_date = pct_chg.idxmax()
#             max_drop = pct_chg.min()
#             max_drop_date = pct_chg.idxmin()

#             pct_chg_2d = (close / close.shift(2) - 1) * 100
#             pct_chg_2d = pct_chg_2d.dropna()

#             max_gain_2d = pct_chg_2d.max()
#             max_gain_2d_date = pct_chg_2d.idxmax()
#             max_drop_2d = pct_chg_2d.min()
#             max_drop_2d_date = pct_chg_2d.idxmin()

#             rows.append({
#                 "Ticker": ticker,
#                 "Max 1D Gain %": round(float(max_gain), 2),
#                 "Gain Date": max_gain_date.strftime("%Y-%m-%d"),
#                 "Max 1D Drop %": round(float(max_drop), 2),
#                 "Drop Date": max_drop_date.strftime("%Y-%m-%d"),
#                 "History Start": close.index[0].strftime("%Y-%m-%d"),
#                 "History Days": len(close),
#                 "Max 2D Gain %": round(float(max_gain_2d), 2),
#                 "2D Gain End Date": max_gain_2d_date.strftime("%Y-%m-%d"),
#                 "Max 2D Drop %": round(float(max_drop_2d), 2),
#                 "2D Drop End Date": max_drop_2d_date.strftime("%Y-%m-%d"),
#             })
#         except Exception:
#             continue

#     return pd.DataFrame(rows)


# # ==============================================================================
# # UI
# # ==============================================================================
# with st.sidebar:
#     st.header("Settings")
#     if st.button("🔄 Force Refresh Data", use_container_width=True):
#         download_max_history.clear()
#         compute_max_moves.clear()
#         st.rerun()
#     st.caption(f"Universe size: {len(KNOWN_STOCKS)} tickers")
#     st.caption("Data cached for 24h. Click Force Refresh to re-download.")

# with st.spinner("Fetching maximum available history from Yahoo Finance..."):
#     ticker_data = download_max_history(tuple(KNOWN_STOCKS))

# if not ticker_data:
#     st.error("No data could be downloaded. Try Force Refresh, or check your network/rate limits.")
#     st.stop()

# moves_df = compute_max_moves(ticker_data)

# if moves_df.empty:
#     st.warning("No moves could be computed from the downloaded data.")
#     st.stop()

# st.success(f"Loaded {len(moves_df)} / {len(KNOWN_STOCKS)} tickers successfully.")

# tab_gains, tab_drops, tab_gains2d, tab_drops2d, tab_all = st.tabs(
#     ["🚀 Biggest Gains", "📉 Biggest Drops", "🚀🚀 Biggest 2D Gains", "📉📉 Biggest 2D Drops", "📋 Full Table"]
# )

# with tab_gains:
#     st.subheader("Top 30 — Largest Single-Day % Gain (All-Time)")
#     top_gains = moves_df.sort_values("Max 1D Gain %", ascending=False).head(30).reset_index(drop=True)
#     st.dataframe(
#         top_gains[["Ticker", "Max 1D Gain %", "Gain Date", "History Start"]],
#         use_container_width=True, hide_index=True,
#         column_config={
#             "Max 1D Gain %": st.column_config.NumberColumn(format="%.2f%%"),
#         }
#     )

# with tab_drops:
#     st.subheader("Top 30 — Largest Single-Day % Drop (All-Time)")
#     top_drops = moves_df.sort_values("Max 1D Drop %", ascending=True).head(30).reset_index(drop=True)
#     st.dataframe(
#         top_drops[["Ticker", "Max 1D Drop %", "Drop Date", "History Start"]],
#         use_container_width=True, hide_index=True,
#         column_config={
#             "Max 1D Drop %": st.column_config.NumberColumn(format="%.2f%%"),
#         }
#     )

# with tab_gains2d:
#     st.subheader("Top 30 — Largest 2-Day Cumulative % Gain (All-Time)")
#     top_gains_2d = moves_df.sort_values("Max 2D Gain %", ascending=False).head(30).reset_index(drop=True)
#     st.dataframe(
#         top_gains_2d[["Ticker", "Max 2D Gain %", "2D Gain End Date", "History Start"]],
#         use_container_width=True, hide_index=True,
#         column_config={
#             "Max 2D Gain %": st.column_config.NumberColumn(format="%.2f%%"),
#         }
#     )

# with tab_drops2d:
#     st.subheader("Top 30 — Largest 2-Day Cumulative % Drop (All-Time)")
#     top_drops_2d = moves_df.sort_values("Max 2D Drop %", ascending=True).head(30).reset_index(drop=True)
#     st.dataframe(
#         top_drops_2d[["Ticker", "Max 2D Drop %", "2D Drop End Date", "History Start"]],
#         use_container_width=True, hide_index=True,
#         column_config={
#             "Max 2D Drop %": st.column_config.NumberColumn(format="%.2f%%"),
#         }
#     )

# with tab_all:
#     st.subheader("All Tickers")
#     sort_col = st.selectbox("Sort by", ["Max 1D Gain %", "Max 1D Drop %", "Max 2D Gain %", "Max 2D Drop %", "Ticker", "History Days"])
#     ascending = st.checkbox("Ascending", value=False)
#     display_df = moves_df.sort_values(sort_col, ascending=ascending).reset_index(drop=True)
#     st.dataframe(
#         display_df, use_container_width=True, hide_index=True,
#         column_config={
#             "Max 1D Gain %": st.column_config.NumberColumn(format="%.2f%%"),
#             "Max 1D Drop %": st.column_config.NumberColumn(format="%.2f%%"),
#             "Max 2D Gain %": st.column_config.NumberColumn(format="%.2f%%"),
#             "Max 2D Drop %": st.column_config.NumberColumn(format="%.2f%%"),
#         }
#     )
#     st.download_button(
#         "⬇️ Download CSV",
#         display_df.to_csv(index=False).encode(),
#         "max_1d_moves.csv",
#         "text/csv"
#     )

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time
import re
import plotly.graph_objects as go
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
import datetime
import base64
from zoneinfo import ZoneInfo
from plotly.subplots import make_subplots

GITHUB_API = "https://api.github.com"

def format_unavailable_reasons(failures):
    if not failures:
        return "previous provider unavailable"
    parts = []
    for provider, reason in failures.items():
        clue = (reason or "unknown reason").strip()
        if not clue:
            clue = "unknown reason"
        elif not clue.startswith("No "):
            clue = clue.split("\n", 1)[0].strip()
            if len(clue) > 60:
                clue = clue[:60].rstrip() + "..."
        parts.append(f"{provider} unavailable ({clue})")
    return "; ".join(parts)

_timing_log = {}  # module-level dict, accumulates across all call sites
_latest_bar_dropped = False
_latest_nan_report_log = {}
_latest_nan_tickers = set()   # 🔧 was: _latest_row_has_nan_reported = False
_benchmark_nan_seen = False

def timed(label, fn, *args, **kwargs):
    """Call fn(*args, **kwargs), record elapsed ms in _timing_log, return result."""
    t0 = time.perf_counter()
    result = fn(*args, **kwargs)
    elapsed = (time.perf_counter() - t0) * 1000
    _timing_log[label] = elapsed
    return result

def yf_download_batched(symbols, batch_size=25, **kwargs):
    """Drop-in replacement for yf.download() over a list of tickers.

    yf.download(list_of_N_tickers) with its default threads=True starts one
    OS thread PER TICKER essentially all at once — multitasking's thread pool
    only throttles how many run their WORK concurrently (a semaphore), it does
    NOT reduce how many Thread objects get created/started. On a small/shared
    cloud container that can exceed the process's thread ulimit and crash
    deep inside threading.Thread.start() with a RuntimeError Streamlit redacts
    (seen on a 34-ticker call — likely tipped over by OTHER concurrent
    yf.download() calls, same process, same or other user sessions, not that
    call's own ticker count alone).

    Splitting into batches and calling yf.download() once per batch bounds
    peak thread creation to batch_size instead of len(symbols) — each batch's
    threads fully finish (yf.download blocks until its own batch completes)
    before the next batch starts. Results are concatenated back into the same
    MultiIndex-columned shape (field -> ticker) a single unbatched call
    returns, so every existing raw_data['Open'][ticker]-style access pattern
    keeps working unchanged. Verified byte-for-byte identical output vs an
    unbatched call, and >2x lower peak thread count, before shipping this.
    """
    symbols = list(symbols)
    if len(symbols) <= batch_size:
        return yf.download(symbols, **kwargs)
    chunks = [symbols[i:i + batch_size] for i in range(0, len(symbols), batch_size)]
    frames = []
    for chunk in chunks:
        f = yf.download(chunk, **kwargs)
        if f is not None and not f.empty:
            frames.append(f)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, axis=1)

def render_copy_button(tickers):
    """Small copy-to-clipboard icon button for a ticker list. Must run inside
    st.components.v1.html — st.markdown(unsafe_allow_html=True) strips onXXX
    attributes via its sanitizer, so an inline onclick there silently no-ops.
    Some ticker lists (e.g. pt_list, vt_list) hold (ticker, atr_value) tuples
    instead of plain strings — normalize the same way the rest of the file
    already does (item[0] if isinstance(item, tuple) else item)."""
    tickers = [t[0] if isinstance(t, tuple) else t for t in tickers]
    csv = ", ".join(tickers)
    btn_html = f"""
<span id="copy-btn" title="Copy tickers" style="cursor:pointer;display:flex;align-items:center;color:#fafafa;">
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
  </svg>
</span>
<script>
(function() {{
  var btn = document.getElementById('copy-btn');
  var copyIcon = btn.innerHTML;
  var checkIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#3DD56D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
  btn.addEventListener('click', function() {{
    var text = `{csv}`;
    function fallbackCopy() {{
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.focus(); ta.select();
      try {{ document.execCommand('copy'); }} catch (e) {{}}
      document.body.removeChild(ta);
    }}
    if (navigator.clipboard && navigator.clipboard.writeText) {{
      navigator.clipboard.writeText(text).catch(fallbackCopy);
    }} else {{
      fallbackCopy();
    }}
    btn.innerHTML = checkIcon;
    setTimeout(function() {{ btn.innerHTML = copyIcon; }}, 1200);
  }});
}})();
</script>
"""
    st.components.v1.html(btn_html, height=38, scrolling=False)

def render_section_header_with_copy(render_title, tickers):
    """Render a section's existing title (render_title is a zero-arg callable
    wrapping its exact original st.markdown(...) call, unchanged) with a small
    ticker-copy button beside it. Falls back to the plain title when there are
    no tickers, so nothing changes on empty-result days."""
    if tickers:
        col_title, col_copy = st.columns([30, 1])
        with col_title:
            render_title()
        with col_copy:
            render_copy_button(tickers)
    else:
        render_title()

# 1. Setup Streamlit Page
st.set_page_config(page_title="Chrome Sector RS", page_icon="🐱", layout="wide")
#st.title("🐱 Theme Tracker")

# # ── AMD 1-Year OHLC Data Display ─────────────────────────────────────────────
# #@st.cache_data(ttl=3600)
# def load_amd_data():
#     df = yf.download("IHI", period="1y", interval="1d", auto_adjust=False, progress=False)
#     df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
#     df = df[["Open", "High", "Low", "Close", "Adj Close", "Volume"]].dropna()
#     df.index = df.index.strftime("%Y-%m-%d")
#     df = df.rename_axis("Date").reset_index()
#     for col in ["Open", "High", "Low", "Close", "Adj Close"]:
#         df[col] = df[col].round(2)
#     return df

# amd_df = load_amd_data()

# st.markdown("### 📈 IHI — 1 Year Daily OHLC")
# st.dataframe(
#     amd_df,
#     use_container_width=True,
#     hide_index=True,
#     height=400,
#     column_config={
#         "Date":      st.column_config.TextColumn("Date"),
#         "Open":      st.column_config.NumberColumn("Open",      format="$%.2f"),
#         "High":      st.column_config.NumberColumn("High",      format="$%.2f"),
#         "Low":       st.column_config.NumberColumn("Low",       format="$%.2f"),
#         "Close":     st.column_config.NumberColumn("Close",     format="$%.2f"),
#         "Adj Close": st.column_config.NumberColumn("Adj Close", format="$%.2f"),
#         "Volume":    st.column_config.NumberColumn("Volume",    format="%,d"),
#     }
# )
# st.markdown("---")

st.markdown(
    """
    <style>
    /* Adjusts the sidebar drawer structural container width */
    [data-testid="stSidebar"] {
        min-width: 240px !important;
        max-width: 240px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. Cleaned Industry Database (Preserved as requested)
INDUSTRIES = {
    '3D Printing': ['XMTR', 'VELO', 'DDD', 'PRLB', 'MTLS', 'SSYS', 'NNDM'],
    'Crypto': ['BLOK', 'MSTR', 'CRCL', 'COIN', 'IBIT', 'RIOT'],
    'Nuclear': ['URA', 'NLR', 'CEG', 'CCJ', 'OKLO', 'UUUU', 'SMR', 'LEU'],
    'MAG7': ['MAGS', 'AAPL', 'GOOGL', 'NVDA', 'META', 'MSFT', 'AMZN', 'TSLA'],
    'ETF': ['XLK', 'XLF', 'XLV', 'XLE', 'XLU', 'XLP', 'XLY', 'XLC', 'XLI', 'XLB'],
    'SPACE': ['SPCX', 'UFO', 'VSAT', 'RKLB', 'SATL', 'RDW', 'LUNR', 'BKSY', 'PL', 'IRDM', 'GSAT', 'ASTS', 'NASA', 'FLY', 'SPCE', 'KRMN', 'SIDU'],
    'CATHIE WOOD': ['ARKG', 'ARKK', 'ARKQ', 'ARKW', 'ARKF', 'ARKX'],
    'CHINA': ['FUTU', 'LI', 'KWEB', 'XPEV', 'NIO', 'PDD', 'BIDU', 'JD', 'BABA'],
    'DATA CENTER': ['WGMI', 'CRWV', 'NBIS', 'IREN', 'WULF', 'CORZ', 'CIFR', 'HUT', 'BTDR', 'EQIX'],
    'SOLAR': ['TAN', 'SEDG', 'ENPH', 'FSLR', 'ARRY', 'SHLS', 'CSIQ', 'RUN', 'DQ'],
    'COML SVCS-ADVRTSNG': ['OMC', 'DJT', 'TTD', 'MGNI', 'PUBM'],
    'AEROSPACE/DEFENSE': ['SHLD', 'ITA', 'XAR', 'RTX', 'LMT', 'HON', 'BA', 'NOC'],
    #'AEROSPACE/DEFENSE': ['ITA', 'RTX', 'LMT', 'HON', 'BA', 'NOC', 'TDG', 'LHX', 'HWM', 'AXON', 'HEI', 'LDOS', 'TDY', 'TXT', 'FTAI', 'CW', 'BWXT', 'HII', 'CR', 'DRS', 'LOAR', 'AVAV', 'HXL', 'KTOS', 'MIR', 'OSIS', 'AIR', 'MRCY'],
    'AGRICULTURAL OPRTIONS': ['ADM', 'BG', 'PPC', 'CALM', 'SEB'],
    'TRNSPRT-AIR FREIGHT': ['UPS', 'FDX'],
    'TRANSPORTATION-SVCS': ['DASH', 'EXPD', 'CHRW', 'CART', 'GXO', 'HUBG', 'UBER', 'PFGC', 'SARO', 'VNT', 'VRRM', 'CAAP'],
    'TRNSPRTTIN-AIRLNE': ['JETS', 'DAL', 'UAL', 'LUV', 'AAL', 'ALK', 'CPA', 'SKYW'],
    'ENERGY-ALT/OTHER': ['BIP', 'TLN', 'CWEN', 'BEPC'],
    'MINING-METAL ORES': ['PICK', 'AA', 'CCJ', 'CRS', 'ATI', 'TECK', 'CENX', 'AG', 'HL', 'NEM', 'KALU', 'CSTM'],
    'COPPER': ['COPX', 'SCCO', 'FCX'],
    'APPAREL-SHOES & REL': ['NKE', 'DECK', 'ONON', 'RL', 'BIRK', 'CROX', 'LEVI', 'VFC', 'GIL', 'PVH', 'COLM', 'KTB', 'SHOO'],
    'RETAIL-APPRL/SHOES/ACC': ['TJX', 'ROST', 'BURL', 'TPR', 'GAP', 'ANF', 'BBWI', 'CPRI', 'BOOT', 'AEO', 'URBN', 'CRI', 'BKE', 'VSXY'],
    'AUTO/TRCK-ORGNL EQP': ['ITW', 'CMI', 'APTV', 'ITT', 'DCI', 'ALSN', 'ALV', 'GNTX', 'LEA', 'BC', 'ATMU', 'VC', 'BWA'],
    'AUTO/TRCK-RPLC PRTS': ['LKQ', 'DORM', 'AAP'],
    'BEVERAGES-ALCOHOLIC': ['STZ', 'TAP', 'SAM'],
    'BEV-NON-ALCOHOLIC': ['KO', 'MNST', 'CCEP', 'COKE', 'BRBR', 'CELH', 'FIZZ'],
    'MEDICAL-BIOMED/BTH': ['IBB', 'BNTX', 'AMGN', 'GILD', 'MRNA', 'ILMN', 'SMMT', 'PCVX', 'BMRN', 'TECH', 'ELAN', 'HALO', 'RNA', 'KRYS', 'ADMA', 'BBIO', 'IMVT', 'AXSM', 'CRSP', 'DNLI', 'ALVO', 'APGE', 'DYN', 'RYTM', 'KYMR', 'EWTX', 'PTGX', 'TWST', 'TXG', 'CGON', 'JANX', 'ARWR', 'VERA', 'NVAX', 'CLDX', 'Q'],
    'MEDIA-RADIO/TV': ['FOX', 'SIRI', 'NXST'],
    'TELCOM-SVC-CBL/SAT': ['CMCSA', 'CHTR'],
    'LEISRE-GAMNG/EQUIP': ['BETZ', 'FLUT', 'LVS', 'MGM', 'WYNN', 'CZR', 'BYD', 'RSI', 'DKNG', 'CHDN', 'PENN'],
    'CHEMICALS-FERTILIZERS': ['MOO', 'NTR', 'CTVA', 'CF', 'MOS', 'FMC', 'SMG'],
    'CHEMICALS-BASIC': ['DD', 'ESI', 'AVNT', 'HUN', 'IOSP', 'DOW', 'LYB', 'WLK', 'AVTR', 'CE', 'EMN', 'CC'],
    'CHEMICALS-SPECIALTY': ['LIN', 'ECL', 'APD', 'ALB', 'CBT', 'NEU', 'KWR', 'HWKN', 'MTX', 'TROX', 'OLN', 'FUL', 'WDFC', 'AZZ', 'UFPT'],
    'ENERGY COAL': ['HCC', 'BTU', 'ARLP', 'AMR'],
    'MEDIA-DIVERSIFIED': ['WMG', 'LYV', 'WBD'],
    'COMPTER-NETWRKING': ['ANET', 'CSCO', 'CALX'],
    'COMPTR-DATA STRGE': ['DRAM', 'EWY', 'WDC', 'STX', 'MU', 'SNDK', 'SKHY'],
    'CMP-HRDWRE/PERIP': ['DELL', 'HPQ', 'SMCI', 'HPE', 'ZBRA', 'NATL'],
    'CONTAINERS/PACKAGING': ['SW', 'BALL', 'PKG', 'AVY', 'AMCR', 'OC', 'CCK', 'ATR', 'GPK', 'SLGN', 'SON', 'GEF', 'OI'],
    'OIL&GAS-DRILLING': ['SLB', 'BKR', 'NE', 'VAL', 'HP', 'SDRL'],
    'BLDG-CMENT/CNCRT': ['CRH', 'MLM', 'VMC', 'EXP', 'KNF', 'USLM'],
    'CMPTER-TECH SRVCS': ['PAYX', 'MSCI', 'VRSK', 'TYL', 'GDDY', 'J', 'FDS', 'AKAM', 'DBX', 'EXLS', 'KD', 'MARA', 'EEFT', 'DXC', 'CORZ', 'AVPT', 'ACN', 'CTSH', 'CDW', 'CACI', 'PSN', 'EPAM', 'DOX', 'KBR', 'GLOB', 'NSIT', 'SAIC', 'INOD'],
    'RETAIL-DPRTMNT STRS': ['DDS', 'M', 'KSS'],
    'RETAIL-DISCNT&VARI': ['DG', 'DLTR', 'FIVE', 'OLLI'],
    'RETAIL-DRUG STORES': ['IHF', 'CVS', 'UNH', 'ELV', 'HUM'],
    'UTILITY-ELCTRIC PWR': ['NEE', 'SO', 'CEG', 'DUK', 'AEP', 'SRE', 'D', 'VST', 'PEG', 'PCG', 'EXC', 'XEL', 'ED', 'EIX', 'WEC', 'ETR', 'DTE', 'FE', 'PPL', 'AEE', 'ES', 'CMS', 'NRG', 'CNP', 'LNT', 'EVRG', 'AES', 'PNW', 'OGE', 'IDA', 'POR', 'ORA', 'BKH', 'TXNM', 'NWE', 'MGEE'],
    'ELEC-POWER/EQPMT': ['GRID', 'ETN', 'GEV', 'AME', 'ROK', 'HUBB', 'RRX', 'GNRC', 'AYI', 'BDC', 'ENS', 'FLNC', 'SMR', 'ATKR', 'PBW', 'POWL', 'VICR', 'BE', 'ENVX', 'QS'],
    'TELCOM-FIBR OPTCS': ['XTL', 'FOTO', 'AAOI', 'COHR', 'CIEN', 'FN', 'LITE', 'AXTI'],
    'ELEC-PARTS': ['APH', 'GLW', 'NVT', 'CAMT', 'TEL'],
    'ELEC-SCNTIFIC/MSRNG': ['PH', 'EMR', 'KEYS', 'FTV', 'CGNX', 'NOVT', 'ST', 'NXT', 'ITRI', 'ESE', 'SXI', 'MTRN', 'VPG'],
    'ELEC-SEMICNDCTR EQP': ['EUV', 'KLIC', 'ASML', 'KLAC', 'AMAT', 'LRCX', 'ONTO', 'NVMI', 'TER', 'AEIS', 'MKSI', 'ENTG', 'ACLS', 'AEHR', 'PLAB'],
    'ELEC-CONTRACT MFG': ['CLS', 'SOLS', 'VRT', 'FLEX', 'PLXS', 'JBL', 'SANM', 'TTMI'],
    'ELEC-MISC PRODUCTS': ['OLED', 'LFUS', 'VSH'],
    'WHOLESALE-ELECT': ['SNX', 'ARW', 'AVT', 'REZI', 'GWW', 'FAST', 'FERG', 'GPC', 'POOL', 'AIT', 'WCC', 'MSM', 'UGI'],
    'RETAIL-CNSMR ELEC': ['BBY', 'GME'],
    'CONSUMER PROD-ELEC': ['SN', 'ROKU', 'WHR', 'SPB', 'SONY'],
    'BLDG-HEAVY CONSTR': ['PWR', 'IESC', 'EME', 'FIX', 'ACM', 'TTEK', 'MTZ', 'APG', 'FLR', 'DY', 'STRL', 'ROAD', 'GVA', 'PRIM'],
    'BLDG-RSIDNT/COMML': ['ITB', 'IBP', 'EXPO', 'DHI', 'LEN', 'NVR', 'PHM', 'TOL', 'MTH', 'KBH', 'SKY', 'MHO', 'FTDR', 'GRBK', 'DFH', 'CCS', 'LGIH'],
    'BLDG-MBILE/MFG & RV': ['CVCO', 'PATK'],
    'POLLUTION CONTROL': ['WM', 'RSG', 'CLH', 'CWST'],
    'COMML SVCS-LEASING': ['URI', 'AER', 'UHAL', 'WSC', 'R', 'HRI', 'WD', 'CAR', 'MGRC', 'PRG'],
    'FINANCE-CARD/PMTPR': ['IPAY', 'XYZ', 'AXP', 'SYF', 'AFRM', 'FCFS', 'SLM', 'V', 'MA', 'PYPL', 'GPN', 'CPAY', 'FOUR', 'WEX', 'PAY', 'RELY', 'SOFI'],
    'FINANCE-CONS LOAN': ['RKT', 'OMF', 'ENVA', 'NNI'],
    'FINANCE-CMRCL LOAN': ['OBDC', 'PFSI', 'CACC'],
    'FINANCE-BLANK CHECK': ['BCSF', 'LOCL', 'MNTN', 'MSDL', 'NCDL', 'PSBD', 'RMI', 'SBXD'],
    'FINANCIAL SVC-SPEC': ['BLK', 'SPGI', 'MCO', 'EFX', 'TRU', 'ICLR', 'BAH', 'MEDP', 'CRL', 'FCN', 'MMS', 'CBZ', 'NSP', 'ICFI', 'EVH', 'FA'],
    'WHOLESALE-FOOD': ['SYY', 'USFD'],
    'RETAIL-SPR/MINI MKTS': ['KR', 'SFM', 'ACI', 'TBBB', 'CASY'],
    'FOOD-PACKAGED': ['KHC', 'GIS', 'CAG', 'SMPL', 'MDLZ', 'KDP', 'HSY', 'CPB', 'SJM', 'POST', 'FLO', 'NOMD', 'UTZ'],
    'FOOD-MEAT PRODUCTS': ['TSN', 'HRL'],
    'FOOD-MISC PREP': ['PEP', 'IFF', 'MKC', 'LW', 'INGR', 'DAR', 'BCPC', 'ASH', 'JJSF', 'SXT', 'TR'],
    'FOOD-CONFECTIONERY': ['FRPT', 'BROS'],
    'BLDG-WOOD PRDS': ['UFPI', 'LPX', 'TREX'],
    'UTILITY-GAS DSTRIBTN': ['TRGP', 'CQP', 'ATO', 'NI', 'MDU', 'BIPC', 'SWX', 'NJR', 'OGS', 'SR', 'CPK', 'EE'],
    'RTAIL-HME FRNSHNGS': ['MBC', 'WSM', 'W', 'RH', 'LOVE'],
    'RETL WHSLE BLDG PRDS': ['HD', 'LOW', 'BLDR', 'FND', 'CNM', 'BCC'],
    'MEDCAL-HOSPITALS': ['HCA', 'THC', 'UHS'],
    'MED-LONG-TRM CARE': ['CHE', 'PACS', 'SGRY', 'ARDT', 'ENSG', 'ADUS'],
    'MEDICAL-SERVICES': ['DVA', 'SOLV', 'EHC', 'ACHC', 'RDNT', 'OPCH', 'HIMS', 'GH', 'BTSG', 'CON', 'AZTA', 'TDOC'],
    'LEISURE-LODGING': ['PEJ', 'ABNB', 'EXPE', 'BKNG', 'MAR', 'HLT', 'RCL', 'CCL', 'VIK', 'H', 'NCLH', 'MTN', 'WH', 'CHH', 'RRR', 'TNL', 'VAC'],
    'COSMETICS/PERSNL CRE': ['PG', 'CL', 'KMB', 'KVUE', 'EL', 'CHD', 'CLX', 'ELF', 'IPAR'],
    'SOAP & CLNG PREPARAT': ['REYN', 'ENR'],
    'DVRSIFIED OPRTIONS': ['MMM', 'RLX', 'WMS', 'AWI', 'BRC', 'YETI', 'LCII'],
    'MCHNRY-GEN INDSTRL': ['GE', 'TT', 'CARR', 'JCI', 'IR', 'XYL', 'DOV', 'LII', 'PNR', 'IEX', 'GGG', 'NDSN', 'LECO', 'WWD', 'AAON', 'FLS', 'MIDD', 'MOD', 'WTS', 'BMI', 'ZWS', 'ESAB', 'TKR', 'GTES', 'FELE', 'KAI', 'MWA', 'NPO', 'CXT', 'OII', 'SYM'],
    'CHEMICALS-PAINTS': ['SHW', 'PPG', 'RPM', 'AXTA'],
    'COMPTER SFTWR-SCRITY': ['CIBR', 'FTNT', 'PANW', 'CRWD', 'CHKP', 'RBRK', 'RPD', 'OKTA', 'ZS', 'TENB', 'S', 'QLYS'],
    'COMPTER SFTWR-ENTR': ['IGV', 'FROG', 'TWLO', 'MSFT', 'ORCL', 'CRM', 'IBM', 'NOW', 'ADP', 'DOCN', 'PLTR', 'ADSK', 'ROP', 'TEAM', 'SNOW', 'VEEV', 'HUBS', 'PTC', 'MANH', 'TOST', 'MNDY', 'WDAY', 'SSNC', 'GWRE', 'BSY', 'PEGA', 'QTWO', 'APPF', 'BOX', 'WK', 'U', 'RNG'],
    'COMPTER SFTWR-DSGN': ['CLOU', 'ADBE', 'INTU', 'SNPS', 'CDNS', 'IOT', 'DT', 'TRMB', 'WIX'],
    'CMPTER SFTWR-FINCL': ['FICO', 'FIS', 'NU', 'SHOP'],
    'CMP SFTWR-GAMING': ['TTWO', 'RBLX'],
    'CMP SFTWR-DBASE': ['DDOG', 'MDB', 'ORCL', 'ESTC'],
    'COMPTER SFTWR-DSKTP': ['ZM', 'SNAP', 'Z'],
    'CMPTR SFTWR-MDCL': ['APP', 'HQY'],
    'INTERNET-CONTENT': ['NFLX', 'SPOT', 'PINS', 'RDDT', 'MMYT', 'MTCH', 'YELP', 'GRND'],
    'INTRNT-NETWK SLTNS': ['FSLY', 'IT', 'CSGP', 'VRSN', 'UPST', 'BRZE', 'CARG', 'NET', 'VLTO'],
    'INSURANCE-BROKERS': ['AON', 'AJG', 'WTW', 'BRO', 'RYAN', 'CRVL', 'GSHD'],
    'OIL&GAS INTEGRATED': ['USO', 'XOM', 'CVX', 'OXY'],
    'OIL&GAS-U S EXPL PRO': ['XOP', 'COP', 'EOG', 'FANG', 'DVN', 'EQT', 'EXE', 'PR', 'OVV', 'APA', 'CHRD', 'MTDR', 'NFG', 'CNX', 'CRC', 'CRGY', 'AR', 'RRC', 'MUR', 'MGY', 'SM', 'NOG', 'CRK', 'GPOR', 'XPRO'],
    'OIL&GAS-ROYALTY TRUST': ['VNOM', 'HESM', 'BSM'],
    'RETAIL-INTERNET': ['XRT', 'SE', 'AMZN', 'MELI', 'CPNG', 'LULU', 'EBAY', 'CHWY', 'GLBE', 'ETSY', 'ACVA'],
    'FIN-INVEST BNK/BKRS': ['IAI', 'GS', 'SCHW', 'ICE', 'CME', 'IBKR', 'NDAQ', 'TW', 'STT', 'CBOE', 'HOOD', 'LPLA', 'JEF', 'HLI', 'MKTX', 'XP', 'EVR', 'FRHC', 'PJT', 'MC', 'PIPR', 'VIRT', 'LAZ', 'SNEX'],
    'FNCE-INVSMNT MGT': ['BX', 'MS', 'KKR', 'BN', 'APO', 'ARES', 'OWL', 'RJF', 'TROW', 'TPG', 'PFG', 'BAM', 'NTRS', 'CRBG', 'CG', 'MORN', 'ARCC', 'BEN', 'SF', 'HLNE', 'SEIC', 'IVZ', 'STEP', 'FSK', 'AMG', 'CNS', 'MAIN', 'GBDC', 'AB', 'VCTR', 'APAM', 'HTGC', 'IFS', 'FHI', 'GCMG', 'AMP', 'OWL'],
    'FINANC-PBL INV FDEQT': ['TPL', 'BXSL'],
    'INSURANCE-LIFE': ['PRU', 'EQH', 'PRI', 'VOYA', 'JXN', 'LNC', 'BHF', 'PRVA'],
    'BANKS-MONEY CNTR': ['JPM', 'BAC', 'WFC', 'C', 'COF', 'HSBC'],
    'BANKS-FOREIGN': ['UBS', 'BAP'],
    'BANKS-SUPR RGIONAL': ['PNC', 'HBAN', 'RF', 'CFG', 'KEY', 'ZION', 'FITB', 'TFC', 'MTB', 'ALLY', 'WAL'],
    'BANKS-WST/STHWST': ['KBE', 'BOKF', 'ONB', 'TCBI', 'WAFD', 'PRK', 'BKU', 'IBOC', 'BANF', 'UCB', 'AUB', 'FIBK', 'CATY', 'FHB', 'BOH', 'CVBF'],
    'BANKS-SOUTHEAST': ['FNB', 'FBK', 'HOMB', 'OZK', 'ABCB'],
    'BANKS-MIDWEST': ['KRE', 'FFIN', 'UMBF', 'ASB', 'FULT', 'CBU', 'SFNC', 'FRME', 'NBTB', 'CBSH', 'COLB', 'GBCI', 'UBSI', 'HWC', 'TOWN'],
    'BANKS-NORTHEAST': ['IAT', 'FCNCA', 'EWBC', 'FHN', 'CFR', 'PNFP', 'SSB', 'WTFC', 'BPOP', 'PB', 'WU', 'EBC', 'FBP', 'TBBK'],
    'FINANC-SVINGS & LO': ['TFSL', 'WSFS', 'PFS'],
    'MED-MANAGED CARE': ['UNH', 'ELV', 'CI', 'CNC', 'HUM', 'MOH', 'OSCR', 'ALHC'],
    'TRANSPORTATION-SHIP': ['BOAT', 'KEX', 'FRO', 'MATX', 'GLNG', 'STNG', 'TDW', 'INSW', 'SBLK', 'ZIM', 'TNK'],
    'MDCAL-WHLSLE DRG': ['MCK', 'COR', 'CAH', 'HSIC'],
    'MEDICAL-PRODUCTS': ['TMO', 'ABT', 'DHR', 'A', 'IDXX', 'RMD', 'MTD', 'RVTY', 'BRKR', 'QGEN', 'BIO', 'LNTH', 'GKOS', 'BLCO', 'MMSI'],
    'MEDICAL-SYSTEMS/EQP': ['IHI', 'ISRG', 'SYK', 'BSX', 'MDT', 'BDX', 'GEHC', 'EW', 'DXCM', 'STE', 'WST', 'COO', 'ZBH', 'WAT', 'BAX', 'ALGN', 'PODD', 'NTRA', 'TFX', 'PEN', 'INSP', 'INMD'],
    'METAL PROC & FABRICA': ['RBC', 'MLI', 'VMI', 'ROCK'],
    'CMML SVCS-CNSLTNG': ['TNET', 'LOPE', 'CNXC', 'ABM', 'LAUR', 'QXO', 'G'],
    'AUTO MANUFACTURERS': ['TSLA', 'GM', 'F', 'RIVN'],
    'TRNSPRT-EQP MFG': ['OSK', 'HOG', 'WAB', 'TEX', 'TRN', 'ALG'],
    'LEISRE-MVIES & REL': ['DIS', 'LYV', 'FWONA', 'TKO', 'MSGS', 'FUN', 'CNK', 'PRKS', 'MANU', 'BATRA'],
    'INSRNCE-DIVRSIFIED': ['KIE', 'PGR', 'AFL', 'MET', 'ACGL', 'HIG', 'CINF', 'RGA', 'CNA', 'UNM', 'KNSL', 'GL', 'RLI', 'AXS', 'BWIN', 'ACT', 'FG', 'WTM', 'CNO', 'LMND'],
    'OFFICE SUPPLIES MFG': ['HNI', 'MLKN', 'ACCO'],
    'OIL&GAS-TRNSPRT/PIP': ['EPD', 'WMB', 'ET', 'OKE', 'KMI', 'MPLX', 'LNG', 'WES', 'PAA', 'DTM', 'KNTK', 'AM', 'SOBO', 'PAGP', 'DKL'],
    'OIL&GAS-RFING/MKT': ['PSX', 'MPC', 'VLO', 'DINO', 'IEP', 'PBF', 'CVI', 'SUN'],
    'OIL&GAS-FIELD SERVIC': ['HAL', 'WFRD', 'NOV', 'WHD', 'AROC', 'LBRT', 'USAC', 'KGS', 'AESI'],
    'LEISURE-SERVICES': ['CTAS', 'ROL', 'SCI', 'HRB', 'PLNT', 'LTH', 'VVV', 'GHC', 'UNF', 'LRN', 'DRVN', 'STRA'],
    'CONSUMR PROD-SPECI': ['MSA', 'HAS', 'AS', 'MAT', 'THO', 'PII', 'GOLF', 'HAYW', 'SIG'],
    #'CMP SFTWR-SPC-ENTR': ['TTD', 'MGNI', 'PUBM'],
    'MEDICAL-ETHICAL DRGS': ['XBI', 'NVO', 'LLY', 'JNJ', 'ABBV', 'MRK', 'PFE', 'VRTX', 'REGN', 'BMY', 'ZTS', 'ALNY', 'BIIB', 'RPRX', 'UTHR', 'VTRS', 'INCY', 'INSM', 'SRPT', 'NBIX', 'ROIV', 'RGEN', 'VKTX', 'EXEL', 'JAZZ', 'CYTK', 'IONS', 'BHVN', 'RARE', 'CORT', 'MDGL', 'OGN', 'ALKS', 'TGTX', 'PRGO', 'RVMD', 'HROW'],
    'MINING-GLD/SILVR/GMS': ['NEM', 'RGLD', 'AEM', 'AU', 'WPM', 'KGC', 'AGI', 'EGO', 'OR'],
    'INSRNCE-PRP/CAS/TITL': ['BRK-B','CB', 'TRV', 'ALL', 'AIG', 'ERIE', 'WRB', 'MKL', 'L', 'EG', 'RNR', 'AFG', 'AIZ', 'MTG', 'SIGI', 'THG', 'KMPR', 'HGTY', 'MCY', 'NMIH', 'PLMR', 'SPNT', 'FNF', 'ORI', 'ESNT', 'FAF', 'RDN', 'AGO'],
    'MEDIA-BOOKS': ['WLY', 'SCHL', 'NYT', 'NWS'],
    #'MEDIA-NEWSPAPERS': ['NWS', 'NYT'],
    'PAPER & PAPER PRODUC': ['IP', 'SLVM'],
    'TRANSPORTATION-RAIL': ['IYT', 'UNP', 'CSX', 'NSC', 'GATX'],
    'REAL STATE DVLPMT/OPS': ['CBRE', 'JLL', 'HHH', 'HGV', 'JOE', 'CWK', 'NMRK'],
    'FINANCE-REIT': ['HASI', 'ESBA'],
    'RETAIL-MJR DSC CHNS': ['WMT', 'COST', 'TGT', 'BJ', 'PSMT'],
    'RETAIL/WHLSLE-AUTO': ['CVNA', 'KMX', 'PAG', 'MUSA', 'LAD', 'AN', 'GPI', 'ABG', 'RUSHA'],
    'RETAIL/WSL-AUTO PRT': ['ORLY', 'AZO'],
    'RETAIL-SPECIALTY': ['MUSA', 'CASY', 'HZO', 'COST', 'BJ', 'ARKO', 'WMT', 'PSMT', 'TBBB', 'TGT', 'DKS', 'FIVE', 'BOBS', 'BBW', 'WINA', 'GME', 'MNSO', 'BBY', 'ULTA', 'EVGO', 'BWMX', 'OLLI', 'DLTR', 'RH', 'ASO', 'WSM', 'WOOF', 'DG', 'BBWI', 'SVV', 'SBH', 'BNED', 'ARHS', 'TSCO', 'EYE'],
    'RETAIL-RESTAURANTS': ['MCD', 'SBUX', 'CMG', 'YUM', 'QSR', 'DRI', 'YUMC', 'CAVA', 'DPZ', 'WING', 'TXRH', 'ARMK', 'SHAK', 'SG', 'EAT', 'WEN', 'CAKE', 'PZZA'],
    'TELECOM SVCS-FOREIGN': ['CCOI', 'LBTYA'],
    'TELCOM-INFRASTR': ['ASTS', 'IRDM', 'NOK', 'AMT'],
    'STEEL-PRODUCERS': ['XME', 'SLX', 'NWPX', 'PKX', 'NUE', 'STLD', 'WS', 'RS', 'ASTL', 'CLF', 'GGB', 'CMC', 'RIO', 'TX', 'MTUS', 'MT', 'HCC', 'MSB', 'VALE', 'SID'],
    'TELCOM-CONS PROD': ['MSI', 'GRMN', 'UI'],
    #'TEXTILES': ['AIN', 'CULP', 'UFI'],
    'TOBACCO': ['PM', 'MO'],
    'BLDG-HAND TOOLS': ['SWK', 'SNA'],
    'TRNSPORTATION-TRCK': ['XTN', 'ODFL', 'JBHT', 'XPO', 'SAIA', 'KNX', 'LSTR', 'SNDR', 'ARCB', 'WERN'],
    'MACHINERY-FARM': ['DE', 'CNH', 'TTC', 'AGCO', 'SITE', 'FSS', 'ACA'],
    'MCHNRY-CNSTR/MNG': ['CAT', 'PCAR', 'LGN', 'ICHR', 'UCTT'],
    'UTILITY-WATER SUPPLY': ['AWK', 'WTRG', 'AWR', 'CWT'],
    'TELCOM SVC-WIRLES': ['IYZ', 'TMUS', 'VZ', 'T', 'TIGO', 'TDS'],
    'ELEC-SEMICON FBLSS': ['SMH', 'SIMO', 'ARM', 'NVDA', 'AVGO', 'AMD', 'QCOM', 'ADI', 'MRVL', 'NXPI', 'MPWR', 'MCHP', 'ON', 'SWKS', 'QRVO', 'ALAB', 'CRDO', 'MTSI', 'LSCC', 'CRUS', 'PI', 'RMBS', 'SITM', 'ALGM', 'SLAB', 'POWI', 'IPGP', 'SMTC', 'DIOD', 'SYNA', 'AMBA', 'WOLF'],
    'ELEC-SEMICON FNDRY': ['SOXX', 'TSM', 'TXN', 'INTC', 'GFS', 'AMKR', 'TSEM', 'FORM', 'STM', 'UMC'],
    'ROBOTIC': ['BOTZ', 'AMBA', 'ARBE', 'MBLY', 'NOVT', 'JOBY', 'CGNX', 'ZBRA', 'CRNC', 'RR', 'PRCT', 'PTC', 'NDSN', 'HSAI', 'EMR', 'SERV', 'TER', 'IPGP', 'TRMB', 'SYM', 'OUST'],
    'RARE EARTH': ['REMX', 'USAR', 'METC', 'TMC', 'MP', 'MOS', 'CRML', 'NB', 'PPTA', 'UAMY'],
    'QUANTUM': ['WQTM', 'QNT', 'QMCO', 'IONQ', 'QUBT', 'QBTS', 'RGTI', 'BTQ', 'ARQQ', 'INFQ', 'XNDU'],
    'FUEL CELL': ['FCEL', 'BLDP', 'HYDR', 'BE', 'PLUG'],
    'LITHIUM': ['LIT', 'LAC', 'SLI', 'SQM', 'ALB', 'ATLX'],
    'EUROPE': ['ENOR', 'EFNL', 'EWN', 'EWI', 'EWL', 'EDEN', 'EWO', 'EIRL', 'EWK', 'EWG', 'IEUR', 'EPOL', 'IEV', 'EWU', 'EWP', 'EWQ', 'EWD'],
    'BRAZIL': ['GGB', 'ABEV', 'PBR', 'UGP', 'VALE', 'SID', 'SUZ', 'VIV', 'MELI', 'BSBR', 'CSAN', 'ITUB', 'CIG', 'BBD', 'TIMB', 'XP', 'PAGS', 'INTR', 'SBS'],
    'ARGENTINA': ['ARGT', 'YPF', 'PAM', 'TGS', 'TEO', 'LOMA', 'CRESY', 'CEPU', 'BBAR', 'BMA', 'EDN', 'GGAL', 'IRS', 'SUPV'],
    'CANNABIS': ['MJ', 'CNBS', 'GRWG', 'MSOS', 'IIPR', 'CRON', 'HITI', 'SNDL', 'ACB', 'VFF', 'CGC', 'TLRY', 'OGI'],
    'DRONES': ['RDW', 'JOBY', 'UMAC', 'GD', 'TXT', 'ONDS', 'ACHR', 'DPRO', 'LHX', 'ESLT', 'AVAV', 'EH', 'KTOS', 'PRZO', 'RCAT', 'ZENA'],
    'PRECIOUS METAL': ['GLD', 'SLV', 'PPLT', 'GDX', 'SIL', 'RGLD', 'PLTM', 'PALL'],
}

# Cleaned Known Stocks List Reference Array
KNOWN_STOCKS = [
    'NCLD', 'PALL', 'PLTM', 'IHF', 'ESTC', 'PRU', 'RGEN', 'UBS', 'TRV', 'WEN', 'OKLO', 'IBB', 'Q', 'OUST', 'VPG', 'WOLF', 'NOK', 'HSBC', 'DLTR', 'SKHY', 'RDDT', 'RL', 'CROX', 'LEVI', 'FOTO', 'GNRC', 'KLIC', 'IWM', 'HBMX', 'PWR', 'EUV', 'GRID', 'MAGS', 'SPCX', 'IBM', 'ELV', 'OSCR', 'QNT', 'HYDR', 'ALGM', 'LGN', 'IESC', 'AEHR', 'ACLS', 'MKSI', 'SMTC', 'AMKR', 
    'LSCC', 'DIOD', 'POWI', 'AA', 'ABBV', 'ALAB', 'AMGN', 'APO', 'BOTZ', 'CRCL', 'CRWV', 'D', 'DRAM', 'DUK', 'EEM', 'EWJ', 'EWY', 'EXC', 'FIGR', 
    'GEV', 'GILD', 'GXC', 'JEF', 'KMI', 'KRMN', 'LIN', 'MNST', 'NASA', 'NEM', 'NTR', 'OR', 
    'OWL', 'Q', 'QQQ', 'RNG', 'RKT', 'SCCO', 'SHLD', 'SO', 'SOLS', 'SPMO', 'SPY', 'SPHB', 'TSEM', 'UNP', 'VTV', 
    'VUG', 'WGMI', 'WMB', 'XEL', 'XMAG', 'XYZ', 'ZIM','VICR', 'SLX', 'CBOE', 'SIMO', 'FLEX', 'POWL', 'VLO', 'DOCN', 
    'IYZ', 'LNG', 'AAOI', 'AXTI', 'TSEM', 'USO', 'JNJ', 
    'HP', 'GLD', 'ALB', 'BUG', 'BX', 'DOW', 'VZ', 'REMX', 'GDX', 'SIL', 'VEEV', 'SNDK', 'TLT', 'APH', 'ARM', 'FANG', 
    'NBIS', 'NVT', 'OXY', 'FORM', 'IBIT', 'QTUM', 'IAI', 'KWEB', 'IHI', 'UFO', 'ITA', 'IYT', 'CVS', 'HUM', 'NEE', 
    'HPE', 'PLAB', 'INOD', 'TTMI', 'CCJ', 'BE', 'SLV', 'PICK', 'COPX', 'MAR', 'XAR', 'VSXY', 'GLW', 'ANF', 'AEO', 
    'AEP', 'GH', 'SANM', 'ROK', 'PSN', 'IAT', 'HROW', 'PL', 'AVAV', 'CIEN', 'COHR', 'NU', 'WULF', 'IREN', 'CIFR', 
    'RDW', 'PH', 'LITE', 'ACHR', 'CACI', 'CRS', 'URA', 'NVO', 'NLR', 'ITB', 'EOSE', 'APP', 'RKLB', 'ASTS', 
    'IONQ', 'RMBS', 'RTX', 'NOC', 'LMT', 'HON', 'ONDS', 'CLS', 'LEU', 'VRT', 'VST', 'NRG', 'CEG', 'SMCI', 'CRDO', 
    'SOFI', 'XLP', 'XLE', 'HIMS', 'HOOD', 'GEV', 'XLV', 'HACK', 'XOP', 'CIBR', 'ICLN', 'XLB', 'XLU', 'XLRE', 'IGV', 
    'XLF', 'IPAY', 'XLC', 'XLI', 'KRE', 'XLK', 'CLOU', 'KBE', 'XME', 'XTL', 'JETS', 'SMH', 'XLY', 'XHB', 
    'XBI', 'XRT', 'MJ', 'META', 'MSFT', 'AAPL', 'AMZN', 'GOOGL', 'NVDA', 'TSLA', 'ARKX', 'ARKQ', 'ARKF', 
    'ARKW', 'ARKK', 'ARKG', 'CCL', 'RCL', 'UAL', 'BA', 'DAL', 'NCLH', 'AAL', 'LUV', 'PINS', 'SNAP', 
    'IBKR', 'SCHW', 'JPM', 'MS', 'GS', 'BAC', 'WFC', 'SPGI', 'BLK', 'NDAQ', 'C', 'LI', 'BIDU', 'NIO', 'XPEV', 
    'BABA', 'PDD', 'JD', 'DQ', 'JKS', 'ENPH', 'FSLR', 'TAN', 'SEDG', 'CSIQ', 'RUN', 'PBW', 'CLX', 'PG', 
    'EL', 'LULU', 'SBUX', 'NKE', 'MELI', 'EBAY', 'FDX', 'UPS', 'SE', 'JMIA', 'ETSY', 'SHOP', 
    'Z', 'OPEN', 'CHWY', 'CVNA', 'BARK', 'GM', 'BLNK', 'QS', 'F', 'RIVN', 'FCEL', 'CHPT', 'LCID', 
    'UPST', 'PYPL', 'AFRM', 'V', 'MA', 'AXP', 'BITO', 'COIN', 'RIOT', 'MARA', 'MSTR',
    'DKNG', 'PENN', 'BETZ', 'REGN', 'VRTX', 'MRK', 'UNH', 'TMO', 'ISRG', 'ABT', 'IDXX', 'TDOC', 'CRSP', 
    'BRK-B', 'ETN', 'CAT', 'U', 'RBLX', 'FSLY', 'TRIP', 'EXPE', 'BKNG', 'ABNB', 'DIS', 'WMT', 
    'COST', 'TGT', 'LOW', 'HD', 'DT', 'SNPS', 'CDNS', 'MDB', 'ORCL', 'NOW', 'ADP', 'SNOW', 'DDOG', 
    'FROG', 'ADSK', 'INTU', 'TEAM', 'WDAY', 'CRM', 'PAYC', 'ANET', 'ADBE', 'ACN', 'EPAM', 'ZM', 'TTD', 'TWLO', 
    'DASH', 'APPS', 'DOCU', 'AI', 'AKAM', 'QLYS', 'PANW', 'FTNT', 'CRWD', 'TENB', 'OKTA', 'ZS', 
    'NET', 'S', 'UMC', 'ASML', 'KEYS', 'CRUS', 'AMD', 'AVGO', 'MU', 'KLAC', 'TXN', 'QRVO', 'TSM', 'SWKS', 'AMBA', 
    'STM', 'MCHP', 'ON', 'QCOM', 'SOXX', 'MRVL', 'ADI', 'LRCX', 'AMAT', 'WDC', 'NXPI', 'TER', 'MPWR', 'INTC', 
    'GFS', 'STX', 'A', 'ZBRA', 'ENTG', 'ONTO', 'TRMB', 'BNTX', 'PFE', 'MRNA', 'NVAX', 'FCX', 'CF', 'DRI', 
    'PEP', 'XOM', 'LLY', 'CL', 'MCD', 'KO', 'GE', 'CVX', 'FISV', 'DE', 'WM', 'HLT', 'FUTU', 'UBER', 
    'TIGR', 'EQIX', 'DPZ', 'CSCO', 'COKE', 'SONY', 'FDS', 'MCO', 'GRAB', 'PTON', 'AMT', 'LIT', 'CMG', 'IPO', 
    'INMD', 'NNDM', 'MP', 'FUBO', 'SPOT', 'ALGN', 'PZZA', 'LOVE', 'LMND', 'POOL', 'PLTR', 'ROKU', 
    'CELH', 'NFLX', 'DHI', 'DELL'
]
# Ensure uniqueness
KNOWN_STOCKS = list(set(KNOWN_STOCKS))

#Solely for Deepvue
LIME_STOCKS = [
    'CIBR', 'COPX', 'DRAM', 'GDX', 'IBIT', 'IGV', 'IHI',
    'IPAY', 'ITB', 'JETS', 'KRE', 'KWEB', 'LIT', 'MAGS',
    'PBW', 'REMX', 'SHLD', 'SIL', 'SLX', 'SMH', 'TAN',
    'UFO', 'URA', 'USO', 'VTV', 'VUG', 'WGMI', 'XBI',
    'XME', 'XRT', 'FOTO', 'SPY', 'QQQ', 'RSP'
]#NCLD

LIME_STOCKS1 = [
    'IHF', 'CIBR', 'COPX', 'DRAM', 'GDX', 'IBIT', 'IGV', 'IHI', 'EWY',
    'IPAY', 'ITB', 'JETS', 'KRE', 'KWEB', 'LIT', 'MAGS',
    'PBW', 'REMX', 'SHLD', 'SIL', 'SLX', 'SMH', 'TAN',
    'UFO', 'URA', 'USO', 'VTV', 'VUG', 'WGMI', 'XBI',
    'XME', 'XRT', 'XTL', 'SPY', 'QQQ', 'RSP', 'FOTO', 'KBE', 'NLR', 
    'CLOU', 'XHB', 'BUG', 'HACK', 'ITA', 'IAT', 'XOP', 'NASA', 
    'XTN', 'IYT', 'BOAT', 'MOO', 'BLOK', 'PICK', 'BOTZ', 'MJ', 'WQTM', 'IBB', 'KIE', 'IAI', 'SOXX'
]#NCLD

RRG_STOCKS = [
    'CIBR', 'COPX', 'DRAM', 'GDX', 'IBIT', 'IGV', 'IHI',
    'IPAY', 'ITB', 'JETS', 'KRE', 'KWEB', 'LIT', 'MAGS',
    'PBW', 'REMX', 'SHLD', 'SIL', 'SLX', 'SMH', 'TAN',
    'UFO', 'URA', 'USO', 'WGMI', 'XBI',
    'XME', 'XRT', 'FOTO'
]

STAGE_PCT_WATCHLIST = [
    'CIBR', 'DRAM', 'FOTO', 'IBIT', 'IGV', 'IHF', 'IHI',
    'IPAY', 'ITB', 'JETS', 'KRE', 'KWEB', 'LIT', 'MAGS',
    'PBW', 'REMX', 'SHLD', 'SMH', 'TAN',
    'UFO', 'URA', 'USO', 'WGMI', 'XBI',
    'XME', 'XRT', 'XOP', 'XTN', 'IYT', 'BOAT', 'MOO', 'PICK', 'BOTZ', 'MJ', 'WQTM', 'IBB', 'KIE', 'IAI', 'SOXX', 'PEJ'
]

TICKER_ALIASES = {
    "GOOG": "GOOGL",
}

def normalize_ticker(sym):
    """Map alias tickers (e.g. GOOG) to their canonical KNOWN_STOCKS symbol (GOOGL)."""
    if not sym:
        return sym
    sym = sym.strip().upper()
    return TICKER_ALIASES.get(sym, sym)

def _avg_pct_change(tickers, _ticker_dfs):
    """Average latest daily % change across tickers — reuses already-loaded data, no new fetch."""
    vals = []
    for t in tickers:
        df = _ticker_dfs.get(t)
        if df is None or len(df) < 2:
            continue
        c0, c1 = df['Close'].iloc[-1], df['Close'].iloc[-2]
        if pd.isna(c0) or pd.isna(c1) or c1 == 0:
            continue
        vals.append((c0 - c1) / c1 * 100)
    return sum(vals) / len(vals) if vals else None

# ============================================================
# SHARED DOWNLOAD: runs once, feeds all history compute fns
# ============================================================
@st.cache_data(ttl=3600)
def download_known_stocks_data(stocks_tuple):
    benchmark_symbol = "^GSPC"
    all_symbols = list(stocks_tuple) + [benchmark_symbol]
    raw_data = yf_download_batched(all_symbols, period="2y", interval="1d", progress=False, auto_adjust=True)

    ticker_dfs = {}
    nan_tickers_known = []
    for ticker in stocks_tuple:
        try:
            df = pd.DataFrame({
                'Open':   raw_data['Open'][ticker],
                'High':   raw_data['High'][ticker],
                'Low':    raw_data['Low'][ticker],
                'Close':  raw_data['Close'][ticker],
                'Volume': raw_data['Volume'][ticker]
            }).dropna()
            if not df.empty:
                ticker_dfs[ticker] = df
            else:
                nan_tickers_known.append(ticker)  # NEW
        except Exception:
            nan_tickers_known.append(ticker)  # NEW
            continue

    benchmark_df = pd.DataFrame({
        'Close': raw_data['Close'][benchmark_symbol]
    })#.ffill().dropna()   # <-- was: .dropna()

    st.session_state["nan_tickers_known"] = nan_tickers_known  # NEW

    return ticker_dfs, benchmark_df

@st.cache_data(ttl=3600)
def download_lime_stocks_data(stocks_tuple):
    raw_data = yf_download_batched(list(stocks_tuple), period="2mo", interval="1d", progress=False, auto_adjust=True)
    ticker_dfs = {}
    nan_tickers_lime = []  # NEW: tickers that came back empty/NaN from this download
    for ticker in stocks_tuple:
        try:
            df = pd.DataFrame({
                'Open':   raw_data['Open'][ticker],
                'High':   raw_data['High'][ticker],
                'Low':    raw_data['Low'][ticker],
                'Close':  raw_data['Close'][ticker],
                'Volume': raw_data['Volume'][ticker]
            }).dropna()
            if not df.empty:
                ticker_dfs[ticker] = df
            else:
                nan_tickers_lime.append(ticker)  # NEW
        except Exception:
            nan_tickers_lime.append(ticker)  # NEW
            continue
    st.session_state["nan_tickers_lime"] = nan_tickers_lime  # NEW
    return ticker_dfs

@st.cache_data(ttl=3600)
def fetch_etf_daily_direction(etf_symbols):
    if not etf_symbols:
        return {}, {}, None, {}

    finnhub_key = st.secrets.get("FINNHUB_API_KEY")
    if not finnhub_key:
        st.warning("FINNHUB_API_KEY missing from secrets.")
        return {}, {}, None, {}

    changes      = {}
    pct_changes  = {}
    latest_date  = None
    market_caps  = {
        'XLK': 125.3, 'XLF': 51.2, 'XLV': 39.4, 'XLE': 39.1, 'XLI': 31.1,
        'XLC': 23.8, 'XLU': 22.7, 'XLY': 22.4, 'XLP': 14.7, 'XLB': 8.0
    }

    for sym in etf_symbols:
        try:
            resp = requests.get(
                "https://finnhub.io/api/v1/quote",
                params={"symbol": sym, "token": finnhub_key},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()

            if data.get("c") is None:
                continue

            changes[sym]     = float(data.get("d") or 0.0)
            pct_changes[sym] = float(data.get("dp") or 0.0)

            ts = data.get("t")
            if ts:
                latest_date = datetime.datetime.fromtimestamp(ts)

        except Exception as e:
            st.warning(f"Finnhub fetch error for {sym}: {e}")
            continue

    return changes, pct_changes, latest_date, market_caps

@st.cache_data(ttl=3600)
def fetch_ratio_chart_data(ratio_pairs, period="1y"):
    symbols = sorted({sym for pair in ratio_pairs for sym in pair})
    if not symbols:
        return pd.DataFrame()

    td_keys = [k for k in [st.secrets.get("TWELVEDATA_API_KEY"), st.secrets.get("TWELVEDATA_API_KEY_2")] if k]
    if not td_keys:
        st.warning("TWELVEDATA_API_KEY missing from secrets.")
        return pd.DataFrame()

    CHUNK_SIZE = 7  # stay under the 8-credits/minute free-tier ceiling per key
    chunks = [symbols[i:i + CHUNK_SIZE] for i in range(0, len(symbols), CHUNK_SIZE)]
    all_data = {}

    for i, chunk in enumerate(chunks):
        td_key = td_keys[i % len(td_keys)]  # alternate keys per chunk
        try:
            resp = requests.get(
                "https://api.twelvedata.com/time_series",
                params={
                    "symbol": ",".join(chunk),
                    "interval": "1day",
                    "outputsize": 260,
                    "apikey": td_key,
                },
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            if len(chunk) == 1:
                data = {chunk[0]: data}
            all_data.update(data)
        except Exception as e:
            st.warning(f"Twelve Data fetch error (chunk {i+1}): {e}")

        # Only wait if the NEXT chunk would reuse a key that was just used
        if i < len(chunks) - 1 and len(td_keys) < 2:
            time.sleep(61)  # wait for credit quota to reset before next chunk

    close_series_map = {}
    for sym in symbols:
        sym_data = all_data.get(sym)
        if not sym_data or sym_data.get("status") != "ok" or "values" not in sym_data:
            continue
        rows = sym_data["values"]
        s = pd.Series({row["datetime"]: float(row["close"]) for row in rows})
        s.index = pd.to_datetime(s.index)
        close_series_map[sym] = s.sort_index()

    if not close_series_map:
        return pd.DataFrame()

    close_df = pd.DataFrame(close_series_map).dropna(how="all")
    ratio_df = pd.DataFrame(index=close_df.index)
    for numerator, denominator in ratio_pairs:
        if numerator not in close_df.columns or denominator not in close_df.columns:
            continue
        ratio = close_df[numerator].div(close_df[denominator]).replace([np.inf, -np.inf], np.nan).dropna()
        if ratio.empty:
            continue
        ratio_df[f"{numerator}/{denominator}"] = ratio

    return ratio_df.dropna(how="all").tail(60)

# ==============================================================================

@st.cache_data(ttl=3600)
def compute_breadth_and_stage(stocks_list, ticker_dfs, benchmark_df_input):
    """
    Computes IBD-style market breadth stats and stage analysis
    for the given stock list, mirroring the original Python screener logic.
    """
    try:
        breadth_stats = {
            'new_high': 0, 'new_low': 0,
            'advance': 0, 'decline': 0,
            'up_from_open': 0, 'down_from_open': 0,
            'up_volume': 0, 'down_volume': 0,
            'up_4pct': 0, 'down_4pct': 0
        }
        new_high_tickers = []
        new_low_tickers = []
        stage_counts = {1: 0, 2: 0, 3: 0, 4: 0, 0: 0}
        total_processed = 0

        for ticker in stocks_list:
            try:
                df = ticker_dfs.get(ticker)
                if df is None or len(df) < 5:
                    continue

                currentClose = df['Close'].iloc[-1]
                prevClose    = df['Close'].iloc[-2]
                currentOpen  = df['Open'].iloc[-1]
                currentVol   = df['Volume'].iloc[-1]
                prevVol      = df['Volume'].iloc[-2]

                # 52-week high/low (exclude today for high, mirror original logic)
                low_of_52week  = float(df['Low'].values[-261:-1].min()) if len(df) >= 261 else float(df['Low'].values[:-1].min())
                high_of_52week = float(df['High'].values[-260:-1].max()) if len(df) >= 260 else float(df['High'].values[:-1].max())

                pct_change = (currentClose - prevClose) / prevClose if prevClose != 0 else 0

                total_processed += 1

                # 1. New High / New Low (only include stocks trading above $20)
                if currentClose >= 20 and currentClose >= high_of_52week:
                    breadth_stats['new_high'] += 1
                    new_high_tickers.append(ticker)
                if currentClose >= 20 and currentClose <= low_of_52week:
                    breadth_stats['new_low'] += 1
                    new_low_tickers.append(ticker)

                # 2. Advance / Decline
                if currentClose > prevClose:
                    breadth_stats['advance'] += 1
                elif currentClose < prevClose:
                    breadth_stats['decline'] += 1

                # 3. Up from Open / Down from Open
                if currentClose > currentOpen:
                    breadth_stats['up_from_open'] += 1
                elif currentClose < currentOpen:
                    breadth_stats['down_from_open'] += 1

                # 4. Up on Volume / Down on Volume
                if currentClose > prevClose and currentVol > prevVol:
                    breadth_stats['up_volume'] += 1
                elif currentClose < prevClose and currentVol > prevVol:
                    breadth_stats['down_volume'] += 1

                # 5. Up 4% / Down 4%
                if pct_change >= 0.04:
                    breadth_stats['up_4pct'] += 1
                elif pct_change <= -0.04:
                    breadth_stats['down_4pct'] += 1

                # ── Stage Analysis ──────────────────────────────────────────────
                # Requires benchmark alignment and at least 260 bars
                if len(df) < 260 or benchmark_df_input is None or benchmark_df_input.empty:
                    stage_counts[0] += 1
                    continue

                df_idx = df.index.tz_localize(None) if df.index.tz is not None else df.index
                bm_idx = benchmark_df_input.index.tz_localize(None) if benchmark_df_input.index.tz is not None else benchmark_df_input.index

                df_aligned = df.copy()
                df_aligned.index = df_idx
                bm_aligned = benchmark_df_input.copy()
                bm_aligned.index = bm_idx

                combined = pd.merge(
                    df_aligned[['Close', 'Open']],
                    bm_aligned[['Close']].rename(columns={'Close': 'Close_bench'}),
                    left_index=True, right_index=True, how='inner'
                )

                if combined.empty:
                    stage_counts[0] += 1
                    continue

                # EMA 126 of stock close (for price vs trend line check)
                ema126 = df_aligned['Close'].ewm(span=126, adjust=False).mean()

                # RS Ratio
                rs = combined['Close'] / combined['Close_bench']

                # 8 EMAs of RS ratio (matches original screener)
                ema_spans = [21, 42, 63, 72, 84, 126, 147, 168]
                rs_emas = {span: rs.ewm(span=span, adjust=False).mean() for span in ema_spans}

                last = combined.index[-1]
                rsme  = rs.loc[last]
                c     = combined['Close'].loc[last]
                o     = combined['Open'].loc[last]

                # Align ema126 to combined index
                ema126_val = ema126.reindex(combined.index, method='ffill').loc[last]

                r21  = rs_emas[21].loc[last]
                r42  = rs_emas[42].loc[last]
                r63  = rs_emas[63].loc[last]
                r72  = rs_emas[72].loc[last]
                r84  = rs_emas[84].loc[last]
                r126 = rs_emas[126].loc[last]
                r147 = rs_emas[147].loc[last]
                r168 = rs_emas[168].loc[last]

                # Stage logic (exact mirror of original screener, checked in order)
                if rsme >= r84 and rsme < r126:
                    stage = 1
                elif (rsme < r42 and rsme >= r72 and rsme >= r84 and rsme >= r126
                      and (r42 > r63 or rsme < r63) and r63 > r126 and c >= ema126_val):
                    stage = 3
                elif (rsme >= r168 and rsme >= r147 and rsme >= r126
                      and c >= ema126_val and (r21 >= r42 or r42 >= r63)):
                    stage = 2
                elif rsme >= r126 and c >= ema126_val and (r21 >= r42 or r42 >= r63):
                    stage = 2
                elif (rsme < r63 and rsme < r126) or (r63 < r126 and rsme < r126):
                    stage = 4
                elif (o >= ema126_val or c >= ema126_val) and rsme >= r72 and rsme < r126:
                    stage = 1
                elif rsme >= r84 and rsme >= r72 and (o >= ema126_val or c >= ema126_val):
                    stage = 1
                else:
                    stage = 0

                stage_counts[stage] += 1

            except Exception:
                stage_counts[0] += 1
                continue

        return breadth_stats, stage_counts, total_processed, new_high_tickers, new_low_tickers

    except Exception as e:
        return {}, {1: 0, 2: 0, 3: 0, 4: 0, 0: 0}, 0, []

# ============================================================
# PINE SCRIPT "Relative Strength Table" — 39-ticker RS panel
# Methodology ported from the TradingView Pine indicator:
# percentrank(price_ratio, length) for periods 5/21/63/126,
# sorted by the 21-period RS (Pine default sort_key_options='P2').
# ============================================================
PINE_RS_TICKERS = [
    'QQQ', 'QQQE', 'RSP', 'ITB', 'IWM', 'XLV', 'XLE', 'XLF', 'PBW', 'XLB',
    'XLP', 'XLU', 'XLY', 'XLK', 'XLC', 'XLI', 'FOTO', 'SMH', 'SLV', 'NLR',
    'TAN', 'IBIT', 'JETS', 'GLD', 'COPX', 'UFO', 'KWEB', 'CIBR', 'IGV', 'USO',
    'MAGS', 'ITA', 'IYT', 'IHI', 'XBI', 'LIT', 'WGMI', 'DRAM', 'REMX'
]

@st.cache_data(ttl=3600)
def download_pine_rs_data(tickers_tuple, benchmark_symbol="SPY"):
    all_symbols = list(tickers_tuple) + [benchmark_symbol]
    raw = yf_download_batched(all_symbols, period="9mo", interval="1d", progress=False, auto_adjust=True)
    return raw['Close']


def _percentrank_last(series, length):
    """Pine ta.percentrank(source, length) for the latest bar only."""
    if series is None or len(series) < length + 1:
        return np.nan
    window = series.iloc[-(length + 1):-1].values
    current = series.iloc[-1]
    if len(window) < length:
        return np.nan
    return round(float(np.sum(window < current)) / length * 100, 2)


def _is_latest_close_above_52w_close(close_series):
    """True only when the latest close exceeds the prior 52-week close."""
    if close_series is None:
        return False
    close = pd.Series(close_series).dropna()
    if close.empty or len(close) < 2:
        return False
    latest_close = float(close.iloc[-1])
    prior_closes = close.iloc[-253:-1] if len(close) > 253 else close.iloc[:-1]
    if prior_closes.empty:
        return False
    previous_52w_close = float(prior_closes.max())
    return latest_close > previous_52w_close


@st.cache_data(ttl=3600)
def compute_pine_rs_table(tickers_tuple, benchmark_symbol="SPY"):
    close_data = download_pine_rs_data(tickers_tuple, benchmark_symbol)
    if benchmark_symbol not in close_data.columns:
        return []
    bench_close = close_data[benchmark_symbol].dropna()

    rows = []
    for t in tickers_tuple:
        if t not in close_data.columns:
            continue
        close = close_data[t].dropna()
        aligned_close, aligned_bench = close.align(bench_close, join='inner')
        if aligned_close.empty:
            continue
        ratio = aligned_close / aligned_bench
        rs5   = _percentrank_last(ratio, 5)
        rs21  = _percentrank_last(ratio, 21)
        rs63  = _percentrank_last(ratio, 63)
        rs126 = _percentrank_last(ratio, 126)
        rows.append({
            "Ticker": t,
            "RS5": rs5,
            "RS21": rs21,
            "RS63": rs63,
            "RS126": rs126,
            "Is52WHigh": _is_latest_close_above_52w_close(close),
        })

    # Sort descending by RS(21), tie-broken by RS63 -> RS126 -> RS5
    # (fixes ties like SLV/NLR/GLD/COPX/IGV all at 100% RS21 — the one with
    # stronger RS63/RS126/RS5 should rank higher, matching TradingView)
    def _sort_key(r):
        return (
            r["RS21"]  if not pd.isna(r["RS21"])  else -1,
            r["RS5"]   if not pd.isna(r["RS5"])   else -1,            
            r["RS63"]  if not pd.isna(r["RS63"])  else -1,
            r["RS126"] if not pd.isna(r["RS126"]) else -1,
        )

    rows.sort(key=_sort_key, reverse=True)
    return rows

def render_pine_rs_table_html(rows, max_height):
    if not rows:
        return "<div style='color:#888;font-size:11px;'>No RS data available.</div>"

    sector_etfs = {"XLE", "XLK", "XLY", "XLB", "XLF", "XLI", "XLC", "XLU", "XLV", "XLP"}
    index_etfs  = {"QQQE", "QQQ", "RSP", "IWM", "SMH", "MAGS"}

    def fmt(v):
        return "-" if v is None or pd.isna(v) else f"{v:.2f}%"

    def rs_cell_style(v):
        base = "padding:1px 5px;text-align:right;font-size:9px;border:1px solid #ccc;white-space:nowrap;"
        if v is not None and not pd.isna(v) and v >= 80:
            return base + "background:rgba(255, 183, 197, 0.8);color:#000000;"
        return base + "background:#ffffff;color:#000000;"

    header_html = (
        "<tr>"
        "<th style='padding:1px 5px;background:#ffffff;color:#000000;text-align:left;font-size:9px;border:1px solid #ccc;white-space:nowrap;'></th>"
        "<th style='padding:1px 5px;background:#ffffff;color:#000000;text-align:center;font-size:9px;border:1px solid #ccc;white-space:nowrap;'>RS (5)</th>"
        "<th style='padding:1px 5px;background:#0000ff;color:#ffffff;text-align:center;font-size:9px;border:1px solid #ccc;white-space:nowrap;'>RS (21)*</th>"
        "<th style='padding:1px 5px;background:#ffffff;color:#000000;text-align:center;font-size:9px;border:1px solid #ccc;white-space:nowrap;'>RS (63)</th>"
        "<th style='padding:1px 5px;background:#ffffff;color:#000000;text-align:center;font-size:9px;border:1px solid #ccc;white-space:nowrap;'>RS (126)</th>"
        "</tr>"
    )

    body_html = ""
    n = len(rows)
    for i, r in enumerate(rows):
        sym = r["Ticker"]
        ticker_label = f"{sym}**" if r.get("Is52WHigh", False) else sym
        name_bg, name_color = "#ffffff", "#000000"
        if i == n - 1:
            name_bg, name_color = "#ff0000", "#ffffff"
        if sym in sector_etfs:
            name_bg, name_color = "#00ffff", "#000000"
        if sym in index_etfs:
            name_bg, name_color = "#FFD700", "#ff0000"

        body_html += (
            f"<tr>"
            f"<td style='padding:1px 5px;background:{name_bg};color:{name_color};text-align:left;font-size:9px;border:1px solid #ccc;font-weight:bold;white-space:nowrap;'>{ticker_label}</td>"
            f"<td style='{rs_cell_style(r['RS5'])}'>{fmt(r['RS5'])}</td>"
            f"<td style='{rs_cell_style(r['RS21'])}'>{fmt(r['RS21'])}</td>"
            f"<td style='{rs_cell_style(r['RS63'])}'>{fmt(r['RS63'])}</td>"
            f"<td style='{rs_cell_style(r['RS126'])}'>{fmt(r['RS126'])}</td>"
            f"</tr>"
        )

    return (
        f"<div style='overflow:visible; border:1px solid #333; border-radius:4px; "
        f"width:max-content; margin-left:-25px;'>"
        f"<table style='border-collapse:collapse; background:#ffffff;'>"
        f"<thead>{header_html}</thead><tbody>{body_html}</tbody></table></div>"
    )

# 3. Sidebar Inputs
with st.sidebar:
    st.header("Settings")
    benchmark = "^GSPC" #benchmark = st.selectbox("Benchmark", ["^GSPC", "^IXIC"], index=0)
    rs_length = st.number_input("RS Lookback Length", value=90, min_value=10)
    top_n = st.number_input("Top N for Group Avg", value=5, min_value=1)
    show_all_rs = st.toggle("Show RS < 80", value=False)
    show_ppp_charts = st.toggle("Show PPP Charts", value=False)
    show_gap_charts = st.toggle("Show Gap Charts", value=False)
    show_all_setups = st.toggle("Show All Setups (top-5)", value=True)
    new_style_industry_table = st.toggle("Old/New Style", value=True)  # NEW: True = new style (KNOWN_STOCKS only), False = old style (all tickers, unchanged)
    traffic_light_mode = st.toggle("Traffic Light", value=True)  # NEW
    
    if st.button("Refresh Deepvue Theme", use_container_width=True):
        # Clear the caches for BOTH functions so fresh data is requested
        download_lime_stocks_data.clear()
        st.toast("Cache cleared! Fetching real-time market data...", icon="🔄")

    if st.button("Refresh Deepvue Breadth", use_container_width=True):
        # Clear the caches for BOTH functions so fresh data is requested
        compute_breadth_and_stage.clear()
        st.toast("Cache cleared! Fetching real-time market data...", icon="🔄")

    if st.button("Clear Cache"):
        st.cache_data.clear()
    _nan_known = st.session_state.get("nan_tickers_known", [])
    _nan_lime  = st.session_state.get("nan_tickers_lime", [])
    _nan_total = len(_nan_known) + len(_nan_lime)
    st.caption(f"⚠️ NaN tickers: {_nan_total} total ({len(_nan_known)} known / {len(_nan_lime)} lime)")
    if _nan_total:
        with st.expander("NaN ticker list"):
            if _nan_known:
                st.write("Known:", ", ".join(_nan_known))
            if _nan_lime:
                st.write("Lime:", ", ".join(_nan_lime))

# st.markdown("---")
#st.markdown(f"#### 📊 Market Breadth")

lime_ticker_dfs = timed(
    "download_lime_stocks_data",
    download_lime_stocks_data,
    tuple(LIME_STOCKS)
)

lime_perf_rows = []
for sym in LIME_STOCKS:
    df_sym = lime_ticker_dfs.get(sym)
    if df_sym is None or len(df_sym) < 2:
        continue
    c_today = df_sym['Close'].iloc[-1]
    c_prev  = df_sym['Close'].iloc[-2]
    if pd.isna(c_today) or pd.isna(c_prev) or c_prev == 0:
        continue
    pct_1d = round((c_today - c_prev) / c_prev * 100, 2)

    c_1w = df_sym['Close'].iloc[-6] if len(df_sym) >= 6 else None
    pct_1w = round((c_today - c_1w) / c_1w * 100, 2) if (c_1w is not None and not pd.isna(c_1w) and c_1w != 0) else None

    c_1m = df_sym['Close'].iloc[-22] if len(df_sym) >= 22 else None
    pct_1m = round((c_today - c_1m) / c_1m * 100, 2) if (c_1m is not None and not pd.isna(c_1m) and c_1m != 0) else None

    lime_perf_rows.append({
        "sym": sym, "pct": pct_1d, "pct_1w": pct_1w, "pct_1m": pct_1m,
        "is_2m_high": bool(c_today >= df_sym['Close'].max())   # NEW
    })

if lime_perf_rows:

    two_month_high_syms = {r["sym"] for r in lime_perf_rows if r.get("is_2m_high")}

    pattern_defs = """
    <defs>
    <pattern id="stripe-blue" width="6" height="6" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
        <rect width="6" height="6" fill="#9CC4EA"/>
        <line x1="0" y1="0" x2="0" y2="6" stroke="#378ADD" stroke-width="3"/>
    </pattern>
    <pattern id="stripe-pink" width="6" height="6" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
        <rect width="6" height="6" fill="#FFC2DE"/>
        <line x1="0" y1="0" x2="0" y2="6" stroke="#FF69B4" stroke-width="3"/>
    </pattern>
    </defs>
    """

    BAR_MAX_PX = 175  # was 200

    rows_1d = sorted(lime_perf_rows, key=lambda x: -x["pct"])
    rows_1w = sorted([r for r in lime_perf_rows if r["pct_1w"] is not None], key=lambda x: -x["pct_1w"])
    rows_1m = sorted([r for r in lime_perf_rows if r["pct_1m"] is not None], key=lambda x: -x["pct_1m"])

    max_abs_1d = max(abs(r["pct"])     for r in rows_1d) or 1
    max_abs_1w = max(abs(r["pct_1w"])  for r in rows_1w) or 1
    max_abs_1m = max(abs(r["pct_1m"])  for r in rows_1m) or 1

    ROW_H   = 21   # was 18
    LABEL_W = 120   # was 110
    COL_W   = LABEL_W + BAR_MAX_PX
    GAP     = 55   # was 60
    PADDING = 13    # was 12
    FS      = 13    # font size

    N      = max(len(rows_1d), len(rows_1w), len(rows_1m))
    SVG_H  = N * ROW_H + PADDING * 2
    SVG_W  = COL_W * 3 + GAP * 2 + PADDING * 2

    X0_1d = PADDING
    X0_1w = PADDING + COL_W + GAP
    X0_1m = PADDING + (COL_W + GAP) * 2

    HEADER_H = 20  # height reserved for header row
    SVG_H    = N * ROW_H + PADDING * 2 + HEADER_H  # add header height to SVG

    def col_header(col_x, label):
        center_x = col_x + LABEL_W // 2 + BAR_MAX_PX // 2
        return (
            f'<text x="{center_x}" y="{PADDING + 12}" '
            f'font-size="10" font-family="Source Sans Pro,sans-serif" '
            f'font-weight="700" fill="#888888" text-anchor="middle" '
            f'letter-spacing="1">{label}</text>'
        )

    sgt_now_str = datetime.datetime.now(ZoneInfo("Asia/Singapore")).strftime("%Y-%m-%d %H:%M")

    headers_html = (
        col_header(X0_1d, f"DAILY ({sgt_now_str})") +
        col_header(X0_1w, "1 WEEK (Developing)") +
        col_header(X0_1m, "1 MONTH (Leading Theme)")
    )

    def row_y(i):
        return PADDING + HEADER_H + i * ROW_H + ROW_H

    def bar_end_x(col_x, pct, max_abs):
        return col_x + LABEL_W + int(abs(pct) / max_abs * BAR_MAX_PX)

    def color(pct):
        return "#378ADD" if pct >= 0 else "#FF69B4"

    def sign(pct):
        return f"+{pct:.2f}%" if pct >= 0 else f"{pct:.2f}%"

    def build_index(rows, pct_key, max_abs, col_x):
        return {
            r["sym"]: (i, bar_end_x(col_x, r[pct_key], max_abs))
            for i, r in enumerate(rows)
        }

    idx_1d = build_index(rows_1d, "pct",    max_abs_1d, X0_1d)
    idx_1w = build_index(rows_1w, "pct_1w", max_abs_1w, X0_1w)
    idx_1m = build_index(rows_1m, "pct_1m", max_abs_1m, X0_1m)

    lines_html = ""

    for sym, (i_1d, ex_1d) in idx_1d.items():
        if sym not in idx_1w:
            continue
        i_1w, ex_1w = idx_1w[sym]
        y1 = row_y(i_1d); y2 = row_y(i_1w)
        c  = color(rows_1d[i_1d]["pct"])
        lines_html += (
            f'<line class="mesh mesh-{sym}" '
            f'x1="{ex_1d}" y1="{y1}" x2="{ex_1w}" y2="{y2}" '
            f'stroke="{c}" stroke-width="1.2" stroke-opacity="0" '
            f'style="transition:stroke-opacity 0.2s;pointer-events:none;"/>'
        )

    for sym, (i_1w, ex_1w) in idx_1w.items():
        if sym not in idx_1m:
            continue
        i_1m, ex_1m = idx_1m[sym]
        y1 = row_y(i_1w); y2 = row_y(i_1m)
        c  = color(rows_1w[i_1w]["pct_1w"])
        lines_html += (
            f'<line class="mesh mesh-{sym}" '
            f'x1="{ex_1w}" y1="{y1}" x2="{ex_1m}" y2="{y2}" '
            f'stroke="{c}" stroke-width="1.2" stroke-opacity="0" '
            f'style="transition:stroke-opacity 0.2s;pointer-events:none;"/>'
        )

    def draw_col(rows, pct_key, max_abs, col_x, stripe_syms=None):
        html = ""
        for i, r in enumerate(rows):
            pct   = r[pct_key]
            sym   = r["sym"]
            bw    = max(int(abs(pct) / max_abs * BAR_MAX_PX), 2)
            c     = color(pct)
            y     = row_y(i)
            label = sign(pct)
            html += (
                f'<rect class="hitbar" data-sym="{sym}" '
                f'x="{col_x}" y="{y - 7}" '
                f'width="{LABEL_W + bw}" height="19" '
                f'fill="transparent" style="cursor:pointer;"/>'
            )
            bar_fill = c
            if stripe_syms and sym in stripe_syms:
                bar_fill = "url(#stripe-blue)" if c == "#378ADD" else "url(#stripe-pink)"
            html += (
                f'<rect class="bar bar-{sym}" data-sym="{sym}" '
                f'x="{col_x + LABEL_W}" y="{y - 4}" '
                f'width="{bw}" height="11" rx="2" fill="{bar_fill}" '
                f'style="cursor:pointer;"/>'
            )
            # label x positions scaled to new LABEL_W=100:
            html += (
                f'<text class="lbl lbl-{sym}" data-sym="{sym}" '
                f'x="{col_x + 58}" y="{y + 4}" '  # ~52% of LABEL_W
                f'font-size="{FS}" font-family="Source Sans Pro,sans-serif" '
                f'font-weight="600" fill="{c}" '
                f'text-anchor="end" style="cursor:pointer;">{label}</text>'
            )
            ticker_color = (
                "#FFD700" if sym == "SPY"
                else "#ADFF2F" if sym == "QQQ"
                else "#FFD700" if sym == "RSP"
                else "#cccccc"
            )
            html += (
                f'<text class="lbl lbl-{sym}" data-sym="{sym}" '
                f'x="{col_x + 62}" y="{y + 4}" '  # 4px gap after %
                f'font-size="{FS}" font-family="Source Sans Pro,sans-serif" '
                f'font-weight="600" fill="{ticker_color}" '
                f'text-anchor="start" style="cursor:pointer;">{sym}</text>'
            )
        return html

    cols_html  = draw_col(rows_1d, "pct",    max_abs_1d, X0_1d, stripe_syms=two_month_high_syms)
    cols_html += draw_col(rows_1w, "pct_1w", max_abs_1w, X0_1w, stripe_syms=two_month_high_syms)
    cols_html += draw_col(rows_1m, "pct_1m", max_abs_1m, X0_1m, stripe_syms=two_month_high_syms)

    js = """
    <script>
    (function() {
      let selected = null;

      function reset() {
        document.querySelectorAll('.mesh').forEach(function(el) {
          el.style.strokeOpacity = '0';
        });
        document.querySelectorAll('.bar, .lbl').forEach(function(el) {
          el.style.opacity = '1';
        });
        selected = null;
      }

      function select(sym) {
        document.querySelectorAll('.bar, .lbl').forEach(function(el) {
          el.style.opacity = '0.15';
        });
        document.querySelectorAll('.mesh').forEach(function(el) {
          el.style.strokeOpacity = '0';
        });
        document.querySelectorAll('.bar-' + sym + ', .lbl-' + sym).forEach(function(el) {
          el.style.opacity = '1';
        });
        document.querySelectorAll('.mesh-' + sym).forEach(function(el) {
          el.style.strokeOpacity = '0.9';
        });
        selected = sym;
      }

      document.addEventListener('click', function(e) {
        var el = e.target.closest('[data-sym]');
        if (!el) { reset(); return; }
        var sym = el.getAttribute('data-sym');
        if (sym === selected) { reset(); }
        else { select(sym); }
      });
    })();
    </script>
    """

    html_out = f"""
    <div style="background:#0e1117; border-radius:6px;">
    <svg xmlns="http://www.w3.org/2000/svg"
        width="{SVG_W}" height="{SVG_H}"
        style="display:block;">
        {pattern_defs}
        {headers_html}
        {lines_html}
        {cols_html}
    </svg>
    </div>
    {js}
    """

    # col_lime_chart, col_pine_rs = st.columns([4, 1])  # NEW: right-side column for RS table
    # with col_lime_chart:
    #     st.components.v1.html(html_out, height=SVG_H + 24, scrolling=False)
    # with col_pine_rs:  # NEW
    #     pine_rs_rows = timed("compute_pine_rs_table", compute_pine_rs_table, tuple(PINE_RS_TICKERS))
    #     st.markdown(render_pine_rs_table_html(pine_rs_rows, SVG_H), unsafe_allow_html=True)

    # ============================================================
    # ADDITIVE: Single-column chart — % Change Since Today's Open
    # (Close vs TODAY'S OPEN, distinct from existing 'pct' which is
    # today's Close vs yesterday's Close)
    # ============================================================
    open_pct_rows = []
    for sym in LIME_STOCKS:
        df_sym = lime_ticker_dfs.get(sym)
        if df_sym is None or len(df_sym) < 1:
            continue
        o_today = df_sym['Open'].iloc[-1]
        c_today = df_sym['Close'].iloc[-1]
        if pd.isna(o_today) or pd.isna(c_today) or o_today == 0:
            continue
        pct_open = round((c_today - o_today) / o_today * 100, 2)
        open_pct_rows.append({"sym": sym, "pct_open": pct_open})

    if open_pct_rows:
        OPEN_ROW_H      = 21
        OPEN_LABEL_W    = 120
        OPEN_BAR_MAX_PX = 175
        OPEN_COL_W      = OPEN_LABEL_W + OPEN_BAR_MAX_PX
        OPEN_PADDING    = 13
        OPEN_FS         = 13
        OPEN_HEADER_H   = 20

        open_rows_sorted = sorted(open_pct_rows, key=lambda x: -x["pct_open"])
        max_abs_open = max(abs(r["pct_open"]) for r in open_rows_sorted) or 1

        N_open     = len(open_rows_sorted)
        OPEN_SVG_W = OPEN_COL_W + OPEN_PADDING * 2
        OPEN_SVG_H = N_open * OPEN_ROW_H + OPEN_PADDING * 2 + OPEN_HEADER_H

        #open_sgt_now_str = datetime.datetime.now(ZoneInfo("Asia/Singapore")).strftime("%Y-%m-%d %H:%M")

        _nan_total_open = len(st.session_state.get("nan_tickers_known", [])) + len(st.session_state.get("nan_tickers_lime", []))

        open_header_html = (
            f'<text x="{OPEN_PADDING + OPEN_LABEL_W // 2 + OPEN_BAR_MAX_PX // 2}" '
            f'y="{OPEN_PADDING + 12}" font-size="10" font-family="Source Sans Pro,sans-serif" '
            f'font-weight="700" fill="#888888" text-anchor="middle" letter-spacing="1">'
            f'SINCE OPEN (NaN: {_nan_total_open})</text>'
        )

        def open_row_y(i):
            return OPEN_PADDING + OPEN_HEADER_H + i * OPEN_ROW_H + OPEN_ROW_H

        open_cols_html = ""
        for i, r in enumerate(open_rows_sorted):
            pct = r["pct_open"]
            sym = r["sym"]
            bw  = max(int(abs(pct) / max_abs_open * OPEN_BAR_MAX_PX), 2)
            c   = "#378ADD" if pct >= 0 else "#FF69B4"   # blue = up, pink/red = down
            y   = open_row_y(i)
            label = f"+{pct:.2f}%" if pct >= 0 else f"{pct:.2f}%"

            open_cols_html += (
                f'<rect x="{OPEN_PADDING}" y="{y - 7}" '
                f'width="{OPEN_LABEL_W + bw}" height="19" fill="transparent" style="cursor:pointer;"/>'
            )
            open_cols_html += (
                f'<rect x="{OPEN_PADDING + OPEN_LABEL_W}" y="{y - 4}" '
                f'width="{bw}" height="11" rx="2" fill="{c}"/>'
            )
            open_cols_html += (
                f'<text x="{OPEN_PADDING + 58}" y="{y + 4}" '
                f'font-size="{OPEN_FS}" font-family="Source Sans Pro,sans-serif" '
                f'font-weight="600" fill="{c}" text-anchor="end">{label}</text>'
            )
            ticker_color = (
                "#FFD700" if sym == "SPY"
                else "#ADFF2F" if sym == "QQQ"
                else "#FFD700" if sym == "RSP"
                else "#cccccc"
            )
            open_cols_html += (
                f'<text x="{OPEN_PADDING + 62}" y="{y + 4}" '
                f'font-size="{OPEN_FS}" font-family="Source Sans Pro,sans-serif" '
                f'font-weight="600" fill="{ticker_color}" text-anchor="start">{sym}</text>'
            )

        open_html_out = f"""
        <div style="background:#0e1117; border-radius:6px;">
        <svg xmlns="http://www.w3.org/2000/svg"
            width="{OPEN_SVG_W}" height="{OPEN_SVG_H}"
            style="display:block;">
            {open_header_html}
            {open_cols_html}
        </svg>
        </div>
        """

        st.components.v1.html(open_html_out, height=OPEN_SVG_H + 24, scrolling=False)
else:
    st.info("No Lime Stocks performance data available.")
