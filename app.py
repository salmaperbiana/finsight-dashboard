import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
import os
from pathlib import Path
from PIL import Image

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Finsight EDA Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background: #F0F6FF; color: #1A2E4A; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #DAEEFF 0%, #C5E3FF 100%);
    border-right: 2px solid #90CAF9;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #1565C0 !important; }

[data-testid="metric-container"] {
    background: #FFFFFF;
    border: 1.5px solid #90CAF9;
    border-top: 4px solid #1E88E5;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 20px rgba(30,136,229,0.10);
}
[data-testid="metric-container"] label {
    color: #1565C0 !important; font-size: 0.78rem !important;
    font-weight: 700 !important; letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #0D47A1 !important; font-size: 1.6rem !important; font-weight: 800 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #1976D2 !important; font-size: 0.8rem !important; font-weight: 600 !important;
}

h1 { color: #0D47A1 !important; font-weight: 800 !important; }
h2 { color: #1565C0 !important; font-weight: 700 !important; }
h3 { color: #1976D2 !important; font-weight: 600 !important; }
p  { color: #1A2E4A !important; }
hr { border-color: #BBDEFB !important; }

.stTabs [data-baseweb="tab-list"] {
    background: #DAEEFF; border-radius: 12px; padding: 4px; gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; color: #1565C0 !important;
    border-radius: 8px; font-weight: 600; font-size: 0.88rem; padding: 8px 18px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1E88E5, #1565C0) !important;
    color: #FFFFFF !important; box-shadow: 0 2px 8px rgba(30,136,229,0.3);
}

[data-testid="stDataFrame"] {
    border: 1.5px solid #90CAF9; border-radius: 12px; overflow: hidden; background: #FFFFFF;
}
.stAlert { border-radius: 12px !important; }
[data-testid="stExpander"] {
    background: #FFFFFF !important; border: 1.5px solid #90CAF9 !important; border-radius: 12px !important;
}

.insight-card {
    background: linear-gradient(135deg, #E3F2FD 0%, #EEF6FF 100%);
    border: 1.5px solid #90CAF9; border-left: 5px solid #1E88E5;
    border-radius: 12px; padding: 18px 22px; margin: 10px 0;
    box-shadow: 0 2px 12px rgba(30,136,229,0.08);
}
.insight-card h4 {
    color: #1565C0 !important; margin: 0 0 8px 0; font-size: 0.9rem;
    font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em;
}
.insight-card p { color: #1A2E4A !important; margin: 0; font-size: 0.92rem; line-height: 1.7; }

.dataset-badge {
    display: inline-block; background: #E3F2FD; color: #1565C0;
    border: 1.5px solid #90CAF9; border-radius: 20px; padding: 4px 16px;
    font-size: 0.82rem; font-weight: 700; margin-bottom: 16px; letter-spacing: 0.04em;
}
.dataset-badge-green {
    display: inline-block; background: #E8F5E9; color: #2E7D32;
    border: 1.5px solid #66BB6A; border-radius: 20px; padding: 4px 16px;
    font-size: 0.82rem; font-weight: 700; margin-bottom: 16px; letter-spacing: 0.04em;
}
.dataset-badge-orange {
    display: inline-block; background: #FFF8E1; color: #F57F17;
    border: 1.5px solid #FFB300; border-radius: 20px; padding: 4px 16px;
    font-size: 0.82rem; font-weight: 700; margin-bottom: 16px; letter-spacing: 0.04em;
}

.badge-safe {
    background: #E8F5E9; color: #2E7D32; border: 1.5px solid #66BB6A;
    border-radius: 20px; padding: 3px 14px; font-size: 0.8rem; font-weight: 700;
}
.badge-over {
    background: #FFEBEE; color: #C62828; border: 1.5px solid #EF5350;
    border-radius: 20px; padding: 3px 14px; font-size: 0.8rem; font-weight: 700;
}

.hero-header {
    background: linear-gradient(135deg, #1565C0 0%, #1E88E5 55%, #42A5F5 100%);
    border-radius: 20px; padding: 36px 40px; margin-bottom: 30px;
    position: relative; overflow: hidden;
    box-shadow: 0 8px 32px rgba(30,136,229,0.25);
}
.hero-header::before {
    content: ''; position: absolute; top: -40%; right: -10%;
    width: 380px; height: 380px; background: rgba(255,255,255,0.08); border-radius: 50%;
}
.hero-header::after {
    content: ''; position: absolute; bottom: -30%; left: 30%;
    width: 200px; height: 200px; background: rgba(255,255,255,0.05); border-radius: 50%;
}
.hero-header h1 { color: #FFFFFF !important; font-size: 2.2rem; margin: 0 0 8px 0; }
.hero-header p  { color: rgba(255,255,255,0.90) !important; font-size: 1rem; margin: 0; }

.budget-bar-container {
    background: #BBDEFB; border-radius: 8px; height: 12px; margin: 6px 0; overflow: hidden;
}
.budget-bar-fill-safe {
    height: 100%; border-radius: 8px; background: linear-gradient(90deg, #43A047, #66BB6A);
}
.budget-bar-fill-over {
    height: 100%; border-radius: 8px; background: linear-gradient(90deg, #E53935, #EF5350);
}
</style>
""", unsafe_allow_html=True)

BLUE       = ["#1565C0", "#1E88E5", "#42A5F5", "#90CAF9", "#BBDEFB", "#E3F2FD"]
BG_COLOR   = "#FFFFFF"
CARD_COLOR = "#F0F6FF"
TEXT_COLOR = "#1A2E4A"
GRID_COLOR = "#BBDEFB"

def set_mpl_theme():
    plt.rcParams.update({
        "figure.facecolor": BG_COLOR,
        "axes.facecolor":   CARD_COLOR,
        "axes.edgecolor":   "#90CAF9",
        "axes.labelcolor":  TEXT_COLOR,
        "axes.titlecolor":  "#0D47A1",
        "axes.titlesize":   13,
        "axes.titleweight": "bold",
        "xtick.color":      TEXT_COLOR,
        "ytick.color":      TEXT_COLOR,
        "grid.color":       GRID_COLOR,
        "grid.alpha":       0.7,
        "text.color":       TEXT_COLOR,
        "font.family":      "DejaVu Sans",
        "legend.facecolor": "#FFFFFF",
        "legend.edgecolor": "#90CAF9",
        "legend.labelcolor": TEXT_COLOR,
    })

set_mpl_theme()

@st.cache_data
def load_transaksi(path):
    df = pd.read_csv(path)
    df = df.dropna()
    df = df[~df.duplicated()]
    df["tanggal"]            = pd.to_datetime(df["tanggal"])
    df["category_clean"]     = df["category"].str.lower().str.strip()
    df["tahun"]              = df["tanggal"].dt.year
    df["bulan"]              = df["tanggal"].dt.month
    df["hari"]               = df["tanggal"].dt.day
    df["hari_dalam_minggu"]  = df["tanggal"].dt.day_name()
    df["minggu"]             = df["tanggal"].dt.isocalendar().week.astype(int)
    df["year_month"]         = df["tanggal"].dt.to_period("M")
    stats = df.groupby("category_clean")["nominal"].agg(["mean","std"]).reset_index()
    stats.columns = ["category_clean","mean_nominal","std_nominal"]
    df = df.merge(stats, on="category_clean", how="left")
    df["z_score"]    = np.where(df["std_nominal"]>0, (df["nominal"]-df["mean_nominal"])/df["std_nominal"], 0)
    df["is_anomaly"] = df["z_score"].abs() > 2.5
    Q1 = df["nominal"].quantile(0.25)
    Q3 = df["nominal"].quantile(0.75)
    upper_bound = Q3 + 1.5*(Q3-Q1)
    df["anomaly_status"] = df["nominal"].apply(lambda x: "Anomaly" if x > upper_bound else "Normal")
    return df, Q1, Q3, upper_bound

@st.cache_data
def load_kategori(path):
    dk = pd.read_csv(path, usecols=["deskripsi","category"])
    dk = dk.dropna()
    dk = dk[~dk.duplicated()]
    dk["category_clean"]   = dk["category"].str.lower().str.strip()
    dk["deskripsi_clean"]  = dk["deskripsi"].str.strip()
    dk["panjang_deskripsi"]= dk["deskripsi_clean"].str.len()
    dk["jumlah_kata"]      = dk["deskripsi_clean"].str.split().str.len()
    return dk

@st.cache_data
def scan_images(folder_str):
    folder = Path(folder_str)
    exts   = {".jpg",".jpeg",".png",".webp",".bmp",".tiff",".tif"}
    if not folder.exists():
        return []
    return sorted([
        {"path": str(f), "name": f.name, "ext": f.suffix.lower(),
         "size_kb": round(f.stat().st_size/1024, 1)}
        for f in folder.iterdir() if f.suffix.lower() in exts
    ], key=lambda x: x["name"])

@st.cache_data
def get_resolutions(path_name_pairs):
    res = []
    for path_str, name in path_name_pairs:
        try:
            with Image.open(path_str) as im:
                w, h = im.size
                res.append({"name": name, "width": w, "height": h,
                            "megapixel": round(w*h/1_000_000, 2), "mode": im.mode})
        except Exception:
            pass
    return res

try:
    df, Q1, Q3, upper_bound = load_transaksi("dataset_transaksi_sintetik.csv")
except FileNotFoundError:
    st.error("❌ File `dataset_transaksi_sintetik.csv` tidak ditemukan.")
    st.stop()

dk = None
dk_error = None
try:
    dk = load_kategori("dataset_kategori.csv")
except FileNotFoundError:
    dk_error = "❌ File `dataset_kategori.csv` tidak ditemukan."

BUDGET_THRESHOLDS = {
    "tagihan": 2_500_000, "belanja": 2_000_000, "pendidikan": 1_800_000,
    "kesehatan dan perawatan diri": 1_500_000, "sosial": 1_200_000,
    "makanan": 1_000_000, "transportasi": 1_500_000, "hiburan": 1_200_000,
    "travel": 1_800_000, "lainnya": 800_000,
}

with st.sidebar:
    st.markdown("## 💰 Finsight EDA")
    st.markdown("**Platform Literasi Keuangan**")
    st.markdown("---")
    st.markdown("### 🔍 Filter Transaksi")

    all_cats = sorted(df["category"].unique())
    selected_cats = st.multiselect("Pilih Kategori", options=all_cats, default=all_cats)

    month_names = {
        1:"Januari",2:"Februari",3:"Maret",4:"April",5:"Mei",6:"Juni",
        7:"Juli",8:"Agustus",9:"September",10:"Oktober",11:"November",12:"Desember"
    }
    available_months = sorted(df["bulan"].unique())
    selected_months  = st.multiselect(
        "Pilih Bulan", options=available_months, default=available_months,
        format_func=lambda x: month_names.get(x, str(x)),
    )

    zscore_threshold = st.slider("Z-Score Threshold (Anomaly)", 1.5, 3.5, 2.5, 0.1)

    st.markdown("---")
    st.markdown("### ⚙️ Budget Settings")
    budget_adjustment = st.slider(
        "Penyesuaian Budget (%)", 50, 200, 100, 5,
        help="Sesuaikan semua budget threshold secara proporsional"
    )

    st.markdown("---")
    tgl_min = df["tanggal"].min().strftime("%d %b %Y")
    tgl_max = df["tanggal"].max().strftime("%d %b %Y")
    st.markdown(f"""
        <small style='color:#1565C0'>
        📊 Transaksi: {len(df):,} baris<br>
        📅 Periode: {tgl_min} – {tgl_max}<br>
        🏷️ {df['category'].nunique()} kategori
        </small>
    """, unsafe_allow_html=True)

df_f = df[df["category"].isin(selected_cats) & df["bulan"].isin(selected_months)].copy()
df_f["is_anomaly"]     = df_f["z_score"].abs() > zscore_threshold
df_f["anomaly_status"] = df_f["nominal"].apply(lambda x: "Anomaly" if x > upper_bound else "Normal")
adj_budgets = {k: int(v * budget_adjustment / 100) for k, v in BUDGET_THRESHOLDS.items()}

st.markdown("""
<div class="hero-header">
    <h1>📊 Finsight Dashboard</h1>
    <p>Exploratory Data Analysis · Platform Literasi Keuangan</p>
</div>
""", unsafe_allow_html=True)

main_tab1, main_tab2, main_tab3 = st.tabs([
    "💳  Dataset Transaksi",
    "🏷️  Dataset Kategori",
    "🖼️  Dataset Gambar (OCR)",
])

# =============================================================
# TAB 1 — ANALISIS TRANSAKSI
# =============================================================
with main_tab1:

    st.markdown('<span class="dataset-badge">📂 Sumber: dataset_transaksi_sintetik.csv</span>', unsafe_allow_html=True)
    st.markdown("Dataset transaksi keuangan pengguna selama periode 90 hari, berisi nominal, kategori, dan tanggal pengeluaran.")

    total_transaksi   = len(df_f)
    total_pengeluaran = df_f["nominal"].sum()
    rata_rata         = df_f["nominal"].mean()
    total_anomali     = df_f["is_anomaly"].sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📦 Total Transaksi",       f"{total_transaksi:,}",                  f"{total_transaksi} records")
    c2.metric("💵 Total Pengeluaran",     f"Rp {total_pengeluaran/1_000_000:.1f}M","seluruh kategori")
    c3.metric("📈 Rata-rata / Transaksi", f"Rp {rata_rata:,.0f}",                  "per transaksi")
    c4.metric("⚠️ Anomali Terdeteksi",   f"{total_anomali}",                       f"{total_anomali/total_transaksi*100:.2f}%")
    c5.metric("🗂️ Kategori Aktif",       f"{df_f['category'].nunique()}",           "kategori unik")

    st.markdown("<br>", unsafe_allow_html=True)

    sub1, sub2, sub3, sub4 = st.tabs([
        "🔎 Overview EDA",
        "📊 Top Kategori",
        "🔔 Budget Alert",
        "🚨 Anomaly Detection",
    ])

    with sub1:
        st.markdown("### Overview Distribusi & Pola Transaksi")
        col_a, col_b = st.columns(2)

        with col_a:
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.hist(df_f["nominal"], bins=40, color="#1E88E5", alpha=0.80, edgecolor="#1565C0", lw=0.5)
            ax.axvline(df_f["nominal"].mean(),   color="#E53935", lw=2, ls="--", label=f"Mean: Rp {df_f['nominal'].mean():,.0f}")
            ax.axvline(df_f["nominal"].median(), color="#43A047", lw=2, ls=":",  label=f"Median: Rp {df_f['nominal'].median():,.0f}")
            ax.set_title("Distribusi Nominal Transaksi")
            ax.set_xlabel("Nominal (Rp)"); ax.set_ylabel("Frekuensi")
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"Rp{x/1000:.0f}K"))
            ax.legend(fontsize=8); ax.grid(True, alpha=0.4)
            fig.tight_layout(); st.pyplot(fig); plt.close(fig)

        with col_b:
            daily = df_f.groupby(df_f["tanggal"].dt.date).size().reset_index()
            daily.columns = ["tanggal","count"]
            daily["tanggal"] = pd.to_datetime(daily["tanggal"])
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(daily["tanggal"], daily["count"], color="#1E88E5", lw=2, marker="o", markersize=3)
            ax.fill_between(daily["tanggal"], daily["count"], alpha=0.15, color="#42A5F5")
            ax.set_title("Tren Jumlah Transaksi Harian")
            ax.set_xlabel("Tanggal"); ax.set_ylabel("Jumlah Transaksi")
            ax.tick_params(axis="x", rotation=30); ax.grid(True, alpha=0.4)
            fig.tight_layout(); st.pyplot(fig); plt.close(fig)

        col_c, col_d = st.columns(2)

        with col_c:
            top_cats = df_f["category_clean"].value_counts().head(10).reset_index()
            top_cats.columns = ["kategori","jumlah"]
            fig, ax = plt.subplots(figsize=(7, 4))
            bars = ax.barh(top_cats["kategori"][::-1], top_cats["jumlah"][::-1], color=BLUE[:len(top_cats)])
            for bar in bars:
                w = bar.get_width()
                ax.text(w+0.3, bar.get_y()+bar.get_height()/2, str(int(w)), va="center", fontsize=9)
            ax.set_title("Top 10 Kategori (Frekuensi)")
            ax.set_xlabel("Jumlah Transaksi"); ax.grid(True, alpha=0.4, axis="x")
            fig.tight_layout(); st.pyplot(fig); plt.close(fig)

        with col_d:
            top8    = df_f["category_clean"].value_counts().head(8).index
            df_top8 = df_f[df_f["category_clean"].isin(top8)]
            fig, ax = plt.subplots(figsize=(7, 4))
            sns.boxplot(data=df_top8, y="category_clean", x="nominal", palette=BLUE[:8], ax=ax,
                        flierprops=dict(marker="o", color="#1E88E5", alpha=0.5, markersize=4))
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"Rp{x/1000:.0f}K"))
            ax.set_title("Distribusi Nominal per Kategori (Top 8)")
            ax.set_xlabel("Nominal (Rp)"); ax.set_ylabel("Kategori"); ax.grid(True, alpha=0.4, axis="x")
            fig.tight_layout(); st.pyplot(fig); plt.close(fig)

        st.markdown("### 📋 Statistik Deskriptif")
        desc = df_f["nominal"].describe().rename({
            "count":"Jumlah","mean":"Mean","std":"Std Dev",
            "min":"Min","25%":"Q1 (25%)","50%":"Median","75%":"Q3 (75%)","max":"Max"
        })
        st.dataframe(pd.DataFrame({"Nilai (Rp)": desc}).map(lambda x: f"Rp {x:,.0f}"), use_container_width=True)

        st.markdown("""
        <div class="insight-card"><h4>💡 Insight Overview</h4><p>
        • Distribusi nominal cenderung <b>right-skewed</b> — pengguna lebih sering bertransaksi kecil-menengah.<br>
        • Median mendekati mean → distribusi relatif simetris dengan beberapa outlier di sisi kanan.<br>
        • Tren harian stabil dengan fluktuasi normal, tidak ada lonjakan ekstrem.<br>
        • Kategori dengan frekuensi tertinggi belum tentu yang paling besar nominalnya.
        </p></div>
        """, unsafe_allow_html=True)

    with sub2:
        st.markdown("### BQ1 · Distribusi Kontribusi & Top 3 Kategori")
        st.markdown("Mengidentifikasi 3 kategori pengeluaran terbesar berdasarkan total nominal dan persentase kontribusi.")

        cat_contrib = df_f.groupby("category_clean")["nominal"].agg(["sum","count","mean"]).round(0).reset_index()
        cat_contrib.columns = ["Kategori","Total_Nominal","Jumlah_Transaksi","Rata_rata"]
        total_spend = cat_contrib["Total_Nominal"].sum()
        cat_contrib["Persentase"] = (cat_contrib["Total_Nominal"]/total_spend*100).round(2)
        cat_contrib = cat_contrib.sort_values("Total_Nominal", ascending=False).reset_index(drop=True)
        top3 = cat_contrib.head(3)

        medals = ["🥇","🥈","🥉"]
        cc1, cc2, cc3 = st.columns(3)
        for i, (col, (_, row)) in enumerate(zip([cc1,cc2,cc3], top3.iterrows())):
            with col:
                st.markdown(f"""
                <div class="insight-card" style="text-align:center">
                    <h4>{medals[i]} #{i+1} · {row['Kategori'].title()}</h4>
                    <p>
                        <b style="color:#1565C0;font-size:1.3rem">Rp {row['Total_Nominal']/1_000_000:.2f}M</b><br>
                        Kontribusi: <b>{row['Persentase']:.1f}%</b><br>
                        {int(row['Jumlah_Transaksi'])} transaksi · Avg Rp {row['Rata_rata']/1000:.0f}K
                    </p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_e, col_f = st.columns(2)

        with col_e:
            top10      = cat_contrib.head(10)
            colors_bar = BLUE[0:3] + ["#42A5F5"]*(len(top10)-3)
            fig, ax = plt.subplots(figsize=(7, 5))
            bars = ax.barh(top10["Kategori"][::-1], top10["Total_Nominal"][::-1]/1_000_000, color=colors_bar[::-1])
            for bar in bars:
                w = bar.get_width()
                ax.text(w+0.05, bar.get_y()+bar.get_height()/2, f"Rp{w:.1f}M", va="center", fontsize=9)
            ax.set_title("Top 10 Kategori · Total Nominal")
            ax.set_xlabel("Total Nominal (Rp Juta)"); ax.grid(True, alpha=0.4, axis="x")
            fig.tight_layout(); st.pyplot(fig); plt.close(fig)

        with col_f:
            others_sum = cat_contrib.iloc[3:]["Total_Nominal"].sum()
            pie_vals   = list(top3["Total_Nominal"]) + [others_sum]
            pie_labels = [f"{r['Kategori'].title()}\n({r['Persentase']:.1f}%)" for _,r in top3.iterrows()] + [f"Lainnya\n({others_sum/total_spend*100:.1f}%)"]
            fig, ax = plt.subplots(figsize=(6, 5))
            wedges, texts = ax.pie(pie_vals, labels=pie_labels, colors=BLUE[:4],
                                   startangle=140, wedgeprops=dict(edgecolor="#FFFFFF", linewidth=2))
            for t in texts: t.set_fontsize(9); t.set_color(TEXT_COLOR)
            ax.set_title("Distribusi: Top 3 vs Lainnya")
            fig.tight_layout(); st.pyplot(fig); plt.close(fig)

        st.markdown("### 📋 Detail Semua Kategori")
        disp = cat_contrib.copy()
        disp["Total_Nominal"] = disp["Total_Nominal"].apply(lambda x: f"Rp {x:,.0f}")
        disp["Rata_rata"]     = disp["Rata_rata"].apply(lambda x: f"Rp {x:,.0f}")
        disp["Persentase"]    = disp["Persentase"].apply(lambda x: f"{x:.2f}%")
        disp.index = range(1, len(disp)+1)
        st.dataframe(disp, use_container_width=True)

        st.markdown(f"""
        <div class="insight-card"><h4>💡 Insight BQ1</h4><p>
        • <b>{top3['Persentase'].sum():.1f}% pengeluaran</b> terkonsentrasi di Top 3 kategori.<br>
        • Keseimbangan Konsumsi–Investasi: Belanja (konsumtif) vs Pendidikan & Kesehatan (investasi diri).<br>
        • Frekuensi ketiga kategori hampir setara → pola pengeluaran yang terstruktur.<br>
        • Rekomendasi: Fokuskan monitoring dan budget alert pada Top 3 kategori ini.
        </p></div>
        """, unsafe_allow_html=True)

    with sub3:
        st.markdown("### BQ2 · Simulasi Budget Alert System")
        st.markdown("Deteksi kategori yang melebihi batas anggaran bulanan dengan threshold yang dapat disesuaikan.")

        budget_df = df_f.groupby("category_clean")["nominal"].sum().reset_index()
        budget_df.columns = ["Kategori","Total_Pengeluaran"]
        budget_df["Budget"]      = budget_df["Kategori"].map(adj_budgets)
        budget_df = budget_df.dropna(subset=["Budget"])
        budget_df["Selisih"]     = budget_df["Total_Pengeluaran"] - budget_df["Budget"]
        budget_df["Utilisasi_%"] = (budget_df["Total_Pengeluaran"]/budget_df["Budget"]*100).round(1)
        budget_df["Status"]      = budget_df["Selisih"].apply(lambda x: "Over Budget" if x>0 else "Aman")
        budget_df = budget_df.sort_values("Utilisasi_%", ascending=False).reset_index(drop=True)

        over_count    = (budget_df["Status"]=="Over Budget").sum()
        safe_count    = (budget_df["Status"]=="Aman").sum()
        effectiveness = safe_count/len(budget_df)*100 if len(budget_df)>0 else 100

        k1, k2, k3 = st.columns(3)
        k1.metric("✅ Kategori Aman",     f"{safe_count}",         f"{safe_count}/{len(budget_df)} kategori")
        k2.metric("🚨 Over Budget",       f"{over_count}",         f"{over_count} kategori melebihi")
        k3.metric("🎯 Efektivitas Alert", f"{effectiveness:.1f}%", "compliance rate")

        st.markdown("<br>", unsafe_allow_html=True)
        col_g, col_h = st.columns([1, 1.2])

        with col_g:
            st.markdown("#### Status Budget per Kategori")
            for _, row in budget_df.iterrows():
                util    = min(row["Utilisasi_%"], 200)
                is_over = row["Status"] == "Over Budget"
                badge   = '<span class="badge-over">Over Budget</span>' if is_over else '<span class="badge-safe">Aman</span>'
                bar_cls = "budget-bar-fill-over" if is_over else "budget-bar-fill-safe"
                st.markdown(f"""
                <div style="margin:12px 0">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
                        <span style="color:#1565C0;font-weight:600;font-size:0.88rem">{row['Kategori'].title()}</span>
                        {badge}
                    </div>
                    <div class="budget-bar-container">
                        <div class="{bar_cls}" style="width:{min(util,100)}%"></div>
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:0.78rem;color:#1976D2;margin-top:2px">
                        <span>Rp {row['Total_Pengeluaran']/1000:.0f}K / Rp {row['Budget']/1000:.0f}K</span>
                        <span><b>{row['Utilisasi_%']:.1f}%</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col_h:
            colors_budget = ["#EF5350" if s>0 else "#43A047" for s in budget_df["Selisih"]]
            fig, ax = plt.subplots(figsize=(7, 6))
            ax.barh(budget_df["Kategori"][::-1], budget_df["Selisih"][::-1]/1000, color=colors_budget[::-1])
            ax.axvline(0, color="#1A2E4A", lw=1.5, ls="--")
            ax.set_title("Selisih Budget per Kategori (Rp Ribu)")
            ax.set_xlabel("Selisih — Merah: Over, Hijau: Aman")
            ax.grid(True, alpha=0.4, axis="x")
            ax.legend(handles=[mpatches.Patch(color="#EF5350", label="Over Budget"),
                                mpatches.Patch(color="#43A047", label="Aman")], fontsize=9)
            fig.tight_layout(); st.pyplot(fig); plt.close(fig)

        st.markdown("### 📋 Detail Analisis Budget")
        tbl = budget_df.copy()
        tbl["Total_Pengeluaran"] = tbl["Total_Pengeluaran"].apply(lambda x: f"Rp {x:,.0f}")
        tbl["Budget"]            = tbl["Budget"].apply(lambda x: f"Rp {x:,.0f}")
        tbl["Selisih"]           = tbl["Selisih"].apply(lambda x: f"Rp {x:,.0f}")
        tbl["Utilisasi_%"]       = tbl["Utilisasi_%"].apply(lambda x: f"{x:.1f}%")
        tbl.index = range(1, len(tbl)+1)
        st.dataframe(tbl, use_container_width=True)

        st.markdown(f"""
        <div class="insight-card"><h4>💡 Insight BQ2</h4><p>
        • Sistem Budget Alert menunjukkan efektivitas <b>{effectiveness:.1f}%</b>.<br>
        • Threshold adaptif berbasis Q75 historis memberikan estimasi yang realistis.<br>
        • <b>Proactive Alert Strategy:</b> Kirim notifikasi saat pengeluaran mencapai 80% threshold.<br>
        • Gunakan slider penyesuaian budget di sidebar untuk simulasi skenario berbeda.
        </p></div>
        """, unsafe_allow_html=True)

    with sub4:
        st.markdown("### BQ3 · Anomaly Detection")
        st.markdown("Identifikasi transaksi anomali menggunakan **Z-Score per kategori** dan **IQR**.")

        anomaly_df   = df_f[df_f["is_anomaly"]]
        anomaly_rate = len(anomaly_df)/len(df_f)*100

        a1, a2, a3, a4 = st.columns(4)
        a1.metric("🔍 Z-Score Threshold", f"±{zscore_threshold}", "sidebar")
        a2.metric("⚠️ Anomali Z-Score",   f"{len(anomaly_df)}",   f"{anomaly_rate:.2f}%")
        a3.metric("📏 IQR Upper Bound",   f"Rp {upper_bound:,.0f}", "batas atas")
        a4.metric("✅ Transaksi Normal",  f"{len(df_f)-len(anomaly_df)}", "dalam batas")

        st.markdown("<br>", unsafe_allow_html=True)
        col_i, col_j = st.columns(2)

        with col_i:
            normal_d = df_f[~df_f["is_anomaly"]]
            anom_d   = df_f[df_f["is_anomaly"]]
            fig, ax = plt.subplots(figsize=(7, 4.5))
            ax.scatter(normal_d["tanggal"], normal_d["nominal"]/1000,
                       color="#42A5F5", alpha=0.6, s=25, label="Normal")
            if len(anom_d) > 0:
                ax.scatter(anom_d["tanggal"], anom_d["nominal"]/1000,
                           color="#E53935", alpha=0.9, s=70, zorder=5,
                           label=f"Anomali (Z>{zscore_threshold})", marker="^")
            ax.set_title("Deteksi Anomali: Transaksi vs Waktu")
            ax.set_xlabel("Tanggal"); ax.set_ylabel("Nominal (Rp Ribu)")
            ax.tick_params(axis="x", rotation=30); ax.legend(fontsize=9); ax.grid(True, alpha=0.4)
            fig.tight_layout(); st.pyplot(fig); plt.close(fig)

        with col_j:
            fig, ax = plt.subplots(figsize=(7, 4.5))
            ax.hist(df_f["z_score"], bins=40, color="#1E88E5", alpha=0.75, edgecolor="#1565C0", lw=0.4)
            ax.axvline( zscore_threshold, color="#E53935", lw=2, ls="--", label=f"+{zscore_threshold}")
            ax.axvline(-zscore_threshold, color="#E53935", lw=2, ls="--", label=f"-{zscore_threshold}")
            ax.set_title("Distribusi Z-Score Seluruh Transaksi")
            ax.set_xlabel("Z-Score"); ax.set_ylabel("Frekuensi")
            ax.legend(fontsize=9); ax.grid(True, alpha=0.4)
            fig.tight_layout(); st.pyplot(fig); plt.close(fig)

        col_k, col_l = st.columns(2)

        with col_k:
            if len(anomaly_df) > 0:
                anom_cat = anomaly_df["category_clean"].value_counts().reset_index()
                anom_cat.columns = ["kategori","jumlah"]
                fig, ax = plt.subplots(figsize=(7, 4))
                ax.barh(anom_cat["kategori"][::-1], anom_cat["jumlah"][::-1], color="#EF5350", alpha=0.85)
                ax.set_title("Jumlah Anomali Z-Score per Kategori")
                ax.set_xlabel("Jumlah Anomali"); ax.grid(True, alpha=0.4, axis="x")
                fig.tight_layout(); st.pyplot(fig); plt.close(fig)
            else:
                st.info("Tidak ada anomali Z-Score dengan threshold saat ini.")

        with col_l:
            weekly = df_f.groupby("minggu")["nominal"].sum().reset_index()
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(weekly["minggu"], weekly["nominal"]/1_000_000, color="#1E88E5", lw=2.5, marker="o", markersize=6)
            ax.fill_between(weekly["minggu"], weekly["nominal"]/1_000_000, alpha=0.15, color="#42A5F5")
            ax.set_title("Tren Pengeluaran Mingguan (Rp Juta)")
            ax.set_xlabel("Nomor Minggu"); ax.set_ylabel("Total (Rp Juta)"); ax.grid(True, alpha=0.4)
            fig.tight_layout(); st.pyplot(fig); plt.close(fig)

        if len(anomaly_df) > 0:
            st.markdown("### 🚨 Daftar Transaksi Anomali (Z-Score)")
            anom_display = anomaly_df[["tanggal","category","deskripsi","nominal","z_score"]].copy()
            anom_display["nominal"] = anom_display["nominal"].apply(lambda x: f"Rp {x:,.0f}")
            anom_display["z_score"] = anom_display["z_score"].apply(lambda x: f"{x:.3f}")
            anom_display = anom_display.sort_values("z_score", ascending=False)
            anom_display.index = range(1, len(anom_display)+1)
            st.dataframe(anom_display, use_container_width=True)

        if len(anomaly_df) > 0:
            top_anom = anomaly_df["category_clean"].value_counts().head(3)
            rec = " ".join([f"• Kategori <b>{c.title()}</b>: {n} anomali — monitoring direkomendasikan.<br>" for c,n in top_anom.items()])
        else:
            rec = "• Semua transaksi dalam batas normal. Pertahankan threshold saat ini."

        st.markdown(f"""
        <div class="insight-card"><h4>💡 Insight BQ3</h4><p>
        • Z-Score ±{zscore_threshold} memberikan deteksi akurat tanpa false positives berlebihan.<br>
        • Tingkat anomali <b>{anomaly_rate:.2f}%</b> — pola pengeluaran sehat dan konsisten.<br>
        {rec}
        • Update statistik kategori secara berkala (mingguan) untuk threshold yang adaptif.
        </p></div>
        """, unsafe_allow_html=True)


# =============================================================
# TAB 2 — DATASET KATEGORI
# =============================================================
with main_tab2:

    if dk_error:
        st.error(dk_error)
        st.stop()

    st.markdown('<span class="dataset-badge-green">📂 Sumber: dataset_kategori.csv</span>', unsafe_allow_html=True)
    st.markdown("Dataset pelatihan model klasifikasi otomatis kategori transaksi berdasarkan teks deskripsi pengeluaran.")

    cat_count_dk = dk["category_clean"].value_counts().reset_index()
    cat_count_dk.columns = ["kategori","jumlah"]

    dk1, dk2, dk3, dk4 = st.columns(4)
    dk1.metric("📦 Total Data",         f"{len(dk):,}",                     "baris unik")
    dk2.metric("🏷️ Jumlah Kategori",   f"{dk['category_clean'].nunique()}", "kategori unik")
    dk3.metric("✏️ Rata-rata Kata",     f"{dk['jumlah_kata'].mean():.1f}",  "kata/deskripsi")
    dk4.metric("📏 Rata-rata Karakter", f"{dk['panjang_deskripsi'].mean():.0f}", "karakter/deskripsi")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Distribusi Data per Kategori")
    r1a, r1b = st.columns(2)

    with r1a:
        fig, ax = plt.subplots(figsize=(7, 5))
        bars = ax.barh(cat_count_dk["kategori"][::-1], cat_count_dk["jumlah"][::-1], color=BLUE[:len(cat_count_dk)][::-1])
        for bar in bars:
            w = bar.get_width()
            ax.text(w+0.5, bar.get_y()+bar.get_height()/2, str(int(w)), va="center", fontsize=9)
        ax.set_title("Jumlah Data per Kategori")
        ax.set_xlabel("Jumlah Data"); ax.grid(True, alpha=0.4, axis="x")
        fig.tight_layout(); st.pyplot(fig); plt.close(fig)

    with r1b:
        fig, ax = plt.subplots(figsize=(6, 5))
        wedges, texts, autotexts = ax.pie(
            cat_count_dk["jumlah"], labels=cat_count_dk["kategori"],
            colors=BLUE[:len(cat_count_dk)], autopct="%1.1f%%", startangle=140,
            wedgeprops=dict(edgecolor="#FFFFFF", linewidth=1.5),
        )
        for t in texts: t.set_fontsize(8); t.set_color(TEXT_COLOR)
        for at in autotexts: at.set_fontsize(8); at.set_color("#FFFFFF"); at.set_fontweight("bold")
        ax.set_title("Proporsi Data per Kategori")
        fig.tight_layout(); st.pyplot(fig); plt.close(fig)

    st.markdown("### 📐 Analisis Panjang Deskripsi Teks")
    r2a, r2b = st.columns(2)

    with r2a:
        cats_ord = dk.groupby("category_clean")["jumlah_kata"].median().sort_values(ascending=False).index
        dk_ord   = dk.copy()
        dk_ord["category_clean"] = pd.Categorical(dk_ord["category_clean"], categories=cats_ord, ordered=True)
        fig, ax = plt.subplots(figsize=(7, 4.5))
        sns.boxplot(data=dk_ord.sort_values("category_clean"), y="category_clean", x="jumlah_kata",
                    palette=BLUE[:len(cats_ord)], ax=ax,
                    flierprops=dict(marker="o", color="#1E88E5", alpha=0.4, markersize=3))
        ax.set_title("Distribusi Jumlah Kata per Kategori")
        ax.set_xlabel("Jumlah Kata"); ax.set_ylabel("Kategori"); ax.grid(True, alpha=0.4, axis="x")
        fig.tight_layout(); st.pyplot(fig); plt.close(fig)

    with r2b:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.hist(dk["jumlah_kata"], bins=30, color="#1E88E5", alpha=0.78, edgecolor="#1565C0", lw=0.5)
        ax.axvline(dk["jumlah_kata"].mean(),   color="#E53935", lw=2, ls="--", label=f"Mean: {dk['jumlah_kata'].mean():.1f} kata")
        ax.axvline(dk["jumlah_kata"].median(), color="#43A047", lw=2, ls=":",  label=f"Median: {dk['jumlah_kata'].median():.0f} kata")
        ax.set_title("Distribusi Jumlah Kata Deskripsi")
        ax.set_xlabel("Jumlah Kata"); ax.set_ylabel("Frekuensi")
        ax.legend(fontsize=9); ax.grid(True, alpha=0.4)
        fig.tight_layout(); st.pyplot(fig); plt.close(fig)

    st.markdown("### ⚖️ Class Balance & Karakteristik Teks")
    r3a, r3b = st.columns(2)

    with r3a:
        avg_count  = len(dk)/dk["category_clean"].nunique()
        bar_colors = ["#EF5350" if v < avg_count*0.75 else "#43A047" if v >= avg_count else "#1E88E5"
                      for v in cat_count_dk["jumlah"]]
        fig, ax = plt.subplots(figsize=(7, 4.5))
        bars = ax.bar(cat_count_dk["kategori"], cat_count_dk["jumlah"], color=bar_colors, alpha=0.85)
        ax.axhline(avg_count, color="#E53935", lw=2, ls="--", label=f"Rata-rata: {avg_count:.0f}")
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x()+bar.get_width()/2, h+0.5, str(int(h)), ha="center", va="bottom", fontsize=9)
        ax.set_title("Class Balance Check")
        ax.set_xlabel("Kategori"); ax.set_ylabel("Jumlah Data")
        ax.tick_params(axis="x", rotation=35); ax.legend(fontsize=9); ax.grid(True, alpha=0.4, axis="y")
        fig.tight_layout(); st.pyplot(fig); plt.close(fig)

    with r3b:
        avg_words = dk.groupby("category_clean")["jumlah_kata"].mean().sort_values(ascending=False).reset_index()
        avg_words.columns = ["kategori","rata_kata"]
        fig, ax = plt.subplots(figsize=(7, 4.5))
        bars = ax.barh(avg_words["kategori"][::-1], avg_words["rata_kata"][::-1], color=BLUE[:len(avg_words)][::-1])
        for bar in bars:
            w = bar.get_width()
            ax.text(w+0.05, bar.get_y()+bar.get_height()/2, f"{w:.1f}", va="center", fontsize=9)
        ax.set_title("Rata-rata Jumlah Kata per Kategori")
        ax.set_xlabel("Rata-rata Kata"); ax.grid(True, alpha=0.4, axis="x")
        fig.tight_layout(); st.pyplot(fig); plt.close(fig)

    st.markdown("### 📋 Statistik Deskriptif Teks per Kategori")
    stat_teks = dk.groupby("category_clean").agg(
        Jumlah=("deskripsi","count"), Rata_Kata=("jumlah_kata","mean"),
        Min_Kata=("jumlah_kata","min"), Max_Kata=("jumlah_kata","max"),
        Rata_Karakter=("panjang_deskripsi","mean"),
    ).round(1).reset_index()
    stat_teks.columns = ["Kategori","Jumlah Data","Rata-rata Kata","Min Kata","Max Kata","Rata-rata Karakter"]
    stat_teks = stat_teks.sort_values("Jumlah Data", ascending=False).reset_index(drop=True)
    stat_teks.index = range(1, len(stat_teks)+1)
    st.dataframe(stat_teks, use_container_width=True)

    st.markdown("### 🔍 Sample Deskripsi per Kategori")
    selected_cat_dk = st.selectbox(
        "Pilih kategori untuk lihat contoh deskripsi:",
        options=sorted(dk["category_clean"].unique()), key="cat_dk_select"
    )
    sample_dk = dk[dk["category_clean"]==selected_cat_dk][["deskripsi","category"]].head(10).reset_index(drop=True)
    sample_dk.index = range(1, len(sample_dk)+1)
    st.dataframe(sample_dk, use_container_width=True)

    imbalance = cat_count_dk["jumlah"].max()/cat_count_dk["jumlah"].min()
    most_cat  = cat_count_dk.iloc[0]["kategori"]
    least_cat = cat_count_dk.iloc[-1]["kategori"]
    imb_text  = (
        "⚠️ <b>Class imbalance terdeteksi</b> (>2x) — pertimbangkan teknik oversampling/undersampling sebelum pelatihan."
        if imbalance > 2 else
        "✅ <b>Distribusi kelas cukup seimbang</b> — dataset siap untuk pelatihan langsung."
    )
    st.markdown(f"""
    <div class="insight-card"><h4>💡 Insight Dataset Kategori</h4><p>
    • Total <b>{len(dk):,} data</b> deskripsi transaksi untuk pelatihan model klasifikasi.<br>
    • Kategori terbanyak: <b>{most_cat.title()}</b> · Tersedikit: <b>{least_cat.title()}</b> · Rasio imbalance: <b>{imbalance:.1f}x</b>.<br>
    • {imb_text}<br>
    • Rata-rata <b>{dk['jumlah_kata'].mean():.1f} kata/deskripsi</b> — panjang teks ideal untuk model NLP berbasis token pendek.
    </p></div>
    """, unsafe_allow_html=True)


# =============================================================
# TAB 3 — DATASET GAMBAR OCR
# =============================================================
with main_tab3:

    st.markdown('<span class="dataset-badge-orange">📂 Sumber: folder /images (lokal)</span>', unsafe_allow_html=True)
    st.markdown("Dataset gambar struk/nota keuangan untuk pelatihan model **OCR (Optical Character Recognition)**. Gambar disimpan di folder `/images` — belum berlabel.")

    img_files  = scan_images("images")
    total_imgs = len(img_files)

    if total_imgs == 0:
        if not Path("images").exists():
            st.error("❌ Folder `/images` belum ada. Buat folder `images` di root project lalu masukkan gambar struk ke dalamnya.")
        else:
            st.warning("⚠️ Folder `/images` ditemukan tapi kosong. Masukkan file gambar (JPG, PNG, dll) ke dalamnya.")
    else:
        total_size = sum(f["size_kb"] for f in img_files)
        ext_count  = {}
        for f in img_files:
            ext_count[f["ext"]] = ext_count.get(f["ext"], 0) + 1

        g1, g2, g3, g4 = st.columns(4)
        g1.metric("🖼️ Total Gambar",    f"{total_imgs:,}",           "file gambar")
        g2.metric("💾 Total Ukuran",    f"{total_size/1024:.2f} MB", "di folder /images")
        g3.metric("🏷️ Status Label",   "Belum Berlabel",            "perlu anotasi")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📊 Statistik Dataset Gambar")
        s1, s2 = st.columns(2)

        with s1:
            exts   = list(ext_count.keys())
            counts = list(ext_count.values())
            fig, ax = plt.subplots(figsize=(6, 3.5))
            bars = ax.bar(exts, counts, color=BLUE[:len(exts)], alpha=0.85)
            for bar in bars:
                h = bar.get_height()
                ax.text(bar.get_x()+bar.get_width()/2, h+0.2, str(int(h)),
                        ha="center", va="bottom", fontsize=11, fontweight="bold")
            ax.set_title("Distribusi Format File Gambar")
            ax.set_xlabel("Format"); ax.set_ylabel("Jumlah File")
            ax.grid(True, alpha=0.4, axis="y")
            fig.tight_layout(); st.pyplot(fig); plt.close(fig)

        with s2:
            sizes = [f["size_kb"] for f in img_files]
            fig, ax = plt.subplots(figsize=(6, 3.5))
            ax.hist(sizes, bins=20, color="#1E88E5", alpha=0.8, edgecolor="#1565C0", lw=0.5)
            ax.axvline(np.mean(sizes),   color="#E53935", lw=2, ls="--", label=f"Mean: {np.mean(sizes):.0f} KB")
            ax.axvline(np.median(sizes), color="#43A047", lw=2, ls=":",  label=f"Median: {np.median(sizes):.0f} KB")
            ax.set_title("Distribusi Ukuran File (KB)")
            ax.set_xlabel("Ukuran (KB)"); ax.set_ylabel("Frekuensi")
            ax.legend(fontsize=9); ax.grid(True, alpha=0.4)
            fig.tight_layout(); st.pyplot(fig); plt.close(fig)

        st.markdown("### 📐 Analisis Resolusi Gambar")
        with st.spinner("Membaca resolusi gambar..."):
            resolutions = get_resolutions([(f["path"], f["name"]) for f in img_files])

        if resolutions:
            res_df = pd.DataFrame(resolutions)
            r1, r2, r3 = st.columns(3)
            r1.metric("↔️ Rata-rata Lebar",  f"{res_df['width'].mean():.0f} px")
            r2.metric("↕️ Rata-rata Tinggi", f"{res_df['height'].mean():.0f} px")
            r3.metric("🔲 Rata-rata MP",     f"{res_df['megapixel'].mean():.2f} MP")

            res_c1, res_c2 = st.columns(2)
            with res_c1:
                fig, ax = plt.subplots(figsize=(6, 3.5))
                ax.scatter(res_df["width"], res_df["height"],
                           color="#1E88E5", alpha=0.6, s=40, edgecolors="#1565C0", lw=0.5)
                ax.set_title("Scatter: Lebar vs Tinggi Gambar")
                ax.set_xlabel("Lebar (px)"); ax.set_ylabel("Tinggi (px)"); ax.grid(True, alpha=0.4)
                fig.tight_layout(); st.pyplot(fig); plt.close(fig)

            with res_c2:
                fig, ax = plt.subplots(figsize=(6, 3.5))
                ax.hist(res_df["megapixel"], bins=15, color="#42A5F5", alpha=0.8, edgecolor="#1565C0", lw=0.5)
                ax.set_title("Distribusi Megapixel")
                ax.set_xlabel("Megapixel"); ax.set_ylabel("Frekuensi"); ax.grid(True, alpha=0.4)
                fig.tight_layout(); st.pyplot(fig); plt.close(fig)

        st.markdown("### 🔍 Preview Sample Gambar")
        n_preview    = st.slider("Jumlah gambar yang ditampilkan", 4, min(24, total_imgs), min(8, total_imgs), 4)
        sample_files = img_files[:n_preview]
        for row_start in range(0, len(sample_files), 4):
            cols = st.columns(4)
            for col, img_info in zip(cols, sample_files[row_start:row_start+4]):
                try:
                    img = Image.open(img_info["path"])
                    col.image(img, caption=f"{img_info['name']}\n{img_info['size_kb']} KB · {img.size[0]}×{img.size[1]}px", use_container_width=True)
                except Exception:
                    col.warning(f"⚠️ {img_info['name']} — gagal dibuka")

        st.markdown("### 📋 Daftar Semua File Gambar")
        file_df = pd.DataFrame([{
            "No": i+1, "Nama File": f["name"], "Format": f["ext"], "Ukuran": f"{f['size_kb']} KB",
        } for i, f in enumerate(img_files)]).set_index("No")
        st.dataframe(file_df, use_container_width=True)

        st.markdown(f"""
        <div class="insight-card"><h4>💡 Insight Dataset Gambar OCR</h4><p>
        • Total <b>{total_imgs} gambar struk</b> tersimpan di folder <code>/images</code> dengan total ukuran <b>{total_size/1024:.2f} MB</b>.<br>
        • Variasi ukuran file (min {min(sizes):.0f} KB – maks {max(sizes):.0f} KB) menunjukkan perbedaan resolusi dan kualitas gambar antar struk.<br>
        • Seluruh gambar <b>belum berlabel</b> — proses anotasi perlu dilakukan sebelum dataset dapat digunakan untuk training model.
        </p></div>
        """, unsafe_allow_html=True)

st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#1565C0;font-size:0.82rem;padding:10px 0">
    💰 <b>Finsight</b> · Platform Literasi Keuangan · EDA Dashboard · Powered by Streamlit
</div>
""", unsafe_allow_html=True)
