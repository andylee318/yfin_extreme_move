import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Max 1-Day Move Scanner", page_icon="📈", layout="wide")
st.title("📈 Max 1-Day Move Scanner — Full History")
st.caption("Fetches the maximum available Yahoo Finance history for each ticker and finds each stock's single largest 1-day % gain and % drop.")

# ==============================================================================
# KNOWN_STOCKS universe (same list as the reference dashboard)
# ==============================================================================
KNOWN_STOCKS = [
    'PALL', 'PLTM', 'IHF', 'ESTC', 'PRU', 'RGEN', 'UBS', 'TRV', 'WEN', 'OKLO', 'IBB', 'Q', 'OUST', 'VPG', 'WOLF', 'NOK', 'HSBC', 'DLTR', 'SKHY', 'RDDT', 'RL', 'CROX', 'LEVI', 'FOTO', 'GNRC', 'KLIC', 'IWM', 'HBMX', 'PWR', 'EUV', 'GRID', 'MAGS', 'SPCX', 'IBM', 'ELV', 'OSCR', 'QNT', 'HYDR', 'ALGM', 'LGN', 'IESC', 'AEHR', 'ACLS', 'MKSI', 'SMTC', 'AMKR',
    'LSCC', 'DIOD', 'POWI', 'AA', 'ABBV', 'ALAB', 'AMGN', 'APO', 'BOTZ', 'CRCL', 'CRWV', 'D', 'DRAM', 'DUK', 'EEM', 'EWJ', 'EWY', 'EXC', 'FIGR',
    'GEV', 'GILD', 'GXC', 'JEF', 'KMI', 'KRMN', 'LIN', 'MNST', 'NASA', 'NEM', 'NTR', 'OR',
    'OWL', 'Q', 'QQQ', 'RNG', 'RKT', 'SCCO', 'SHLD', 'SO', 'SOLS', 'SPMO', 'SPY', 'SPHB', 'TSEM', 'UNP', 'VTV',
    'VUG', 'WGMI', 'WMB', 'XEL', 'XMAG', 'XYZ', 'ZIM', 'VICR', 'SLX', 'CBOE', 'SIMO', 'FLEX', 'POWL', 'VLO', 'DOCN',
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
    'BABA', 'PDD', 'JD', 'DQ', 'JKS', 'ENPH', 'FSLR', 'TAN', 'SEDG', 'CSIQ', 'SPWR', 'RUN', 'PBW', 'CLX', 'PG',
    'EL', 'LULU', 'SBUX', 'NKE', 'MELI', 'EBAY', 'FDX', 'UPS', 'SE', 'JMIA', 'ETSY', 'SHOP',
    'Z', 'OPEN', 'CHWY', 'CVNA', 'BARK', 'GM', 'BLNK', 'QS', 'F', 'RIVN', 'FCEL', 'CHPT', 'LCID',
    'UPST', 'PYPL', 'AFRM', 'V', 'MA', 'AXP', 'BITO', 'COIN', 'RIOT', 'MARA', 'MSTR',
    'DKNG', 'PENN', 'BETZ', 'REGN', 'VRTX', 'MRK', 'UNH', 'TMO', 'ISRG', 'ABT', 'IDXX', 'TDOC', 'CRSP',
    'BRK-B', 'ETN', 'CAT', 'U', 'RBLX', 'SKLZ', 'FSLY', 'TRIP', 'EXPE', 'BKNG', 'ABNB', 'DIS', 'WMT',
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
KNOWN_STOCKS = sorted(set(KNOWN_STOCKS))

# ==============================================================================
# Data fetch — chunked to stay well under Yahoo's rate limits
# ==============================================================================
@st.cache_data(ttl=86400, show_spinner=False)
def download_max_history(tickers, chunk_size=40):
    """
    Downloads maximum available daily history for all tickers, in chunks,
    and returns a dict of {ticker: DataFrame(Date, Close)}.
    """
    result = {}
    chunks = [tickers[i:i + chunk_size] for i in range(0, len(tickers), chunk_size)]

    progress = st.progress(0)
    status = st.empty()

    for idx, chunk in enumerate(chunks):
        status.text(f"Downloading batch {idx + 1}/{len(chunks)} ({len(chunk)} tickers)...")
        try:
            raw = yf.download(
                chunk, period="max", interval="1d",
                progress=False, auto_adjust=True, group_by="ticker", threads=True
            )
        except Exception:
            progress.progress((idx + 1) / len(chunks))
            continue

        for ticker in chunk:
            try:
                if len(chunk) == 1:
                    df = raw[['Close']].dropna()
                else:
                    df = raw[ticker][['Close']].dropna()
                if not df.empty and len(df) > 1:
                    result[ticker] = df
            except Exception:
                continue

        progress.progress((idx + 1) / len(chunks))

    status.empty()
    progress.empty()
    return result


@st.cache_data(ttl=86400, show_spinner=False)
def compute_max_moves(ticker_data):
    """
    For each ticker, computes the single largest 1-day % gain and
    single largest 1-day % drop across its full available history,
    along with the date each occurred.
    """
    rows = []
    for ticker, df in ticker_data.items():
        try:
            close = df['Close']
            pct_chg = close.pct_change().dropna() * 100
            if pct_chg.empty:
                continue

            max_gain = pct_chg.max()
            max_gain_date = pct_chg.idxmax()
            max_drop = pct_chg.min()
            max_drop_date = pct_chg.idxmin()

            rows.append({
                "Ticker": ticker,
                "Max 1D Gain %": round(float(max_gain), 2),
                "Gain Date": max_gain_date.strftime("%Y-%m-%d"),
                "Max 1D Drop %": round(float(max_drop), 2),
                "Drop Date": max_drop_date.strftime("%Y-%m-%d"),
                "History Start": close.index[0].strftime("%Y-%m-%d"),
                "History Days": len(close),
            })
        except Exception:
            continue

    return pd.DataFrame(rows)


# ==============================================================================
# UI
# ==============================================================================
with st.sidebar:
    st.header("Settings")
    if st.button("🔄 Force Refresh Data", use_container_width=True):
        download_max_history.clear()
        compute_max_moves.clear()
        st.rerun()
    st.caption(f"Universe size: {len(KNOWN_STOCKS)} tickers")
    st.caption("Data cached for 24h. Click Force Refresh to re-download.")

with st.spinner("Fetching maximum available history from Yahoo Finance..."):
    ticker_data = download_max_history(tuple(KNOWN_STOCKS))

if not ticker_data:
    st.error("No data could be downloaded. Try Force Refresh, or check your network/rate limits.")
    st.stop()

moves_df = compute_max_moves(ticker_data)

if moves_df.empty:
    st.warning("No moves could be computed from the downloaded data.")
    st.stop()

st.success(f"Loaded {len(moves_df)} / {len(KNOWN_STOCKS)} tickers successfully.")

tab_gains, tab_drops, tab_all = st.tabs(["🚀 Biggest Gains", "📉 Biggest Drops", "📋 Full Table"])

with tab_gains:
    st.subheader("Top 30 — Largest Single-Day % Gain (All-Time)")
    top_gains = moves_df.sort_values("Max 1D Gain %", ascending=False).head(30).reset_index(drop=True)
    st.dataframe(
        top_gains[["Ticker", "Max 1D Gain %", "Gain Date", "History Start"]],
        use_container_width=True, hide_index=True,
        column_config={
            "Max 1D Gain %": st.column_config.NumberColumn(format="%.2f%%"),
        }
    )

with tab_drops:
    st.subheader("Top 30 — Largest Single-Day % Drop (All-Time)")
    top_drops = moves_df.sort_values("Max 1D Drop %", ascending=True).head(30).reset_index(drop=True)
    st.dataframe(
        top_drops[["Ticker", "Max 1D Drop %", "Drop Date", "History Start"]],
        use_container_width=True, hide_index=True,
        column_config={
            "Max 1D Drop %": st.column_config.NumberColumn(format="%.2f%%"),
        }
    )

with tab_all:
    st.subheader("All Tickers")
    sort_col = st.selectbox("Sort by", ["Max 1D Gain %", "Max 1D Drop %", "Ticker", "History Days"])
    ascending = st.checkbox("Ascending", value=False)
    display_df = moves_df.sort_values(sort_col, ascending=ascending).reset_index(drop=True)
    st.dataframe(
        display_df, use_container_width=True, hide_index=True,
        column_config={
            "Max 1D Gain %": st.column_config.NumberColumn(format="%.2f%%"),
            "Max 1D Drop %": st.column_config.NumberColumn(format="%.2f%%"),
        }
    )
    st.download_button(
        "⬇️ Download CSV",
        display_df.to_csv(index=False).encode(),
        "max_1d_moves.csv",
        "text/csv"
    )