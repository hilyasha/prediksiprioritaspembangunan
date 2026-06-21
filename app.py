import streamlit as st
import joblib
from pathlib import Path

st.set_page_config(layout="wide", page_title="Analisis Prioritas Pembangunan", page_icon="📍")

# ----------------------------------------------------------------------------
# DESIGN TOKENS
# Palet dipertahankan dari versi awal (cream + maroon + terracotta), diperluas
# dengan warna status untuk 3 klaster dan tinta hangat untuk teks (bukan hitam pekat).
# ----------------------------------------------------------------------------
CREAM = "#FBF9D1"
INK = "#3D2C2C"
MAROON = "#9A3F3F"
TERRACOTTA = "#C1856D"
SAGE = "#6B8F71"      # klaster tinggi
OCHRE = "#D9A441"      # klaster sedang
BRICK = "#B0413E"      # klaster rendah
CARD_BORDER = "rgba(154, 63, 63, 0.14)"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Lora:wght@500;600;700&display=swap');

    html, body, [class*="css"]  {{ font-family: 'Inter', sans-serif; }}
    h1, h2, h3, .display-font {{ font-family: 'Lora', serif !important; letter-spacing: -0.01em; }}

    .stApp {{ background-color: {CREAM}; color: {INK}; }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {MAROON} 0%, #7A2F2F 100%);
    }}
    section[data-testid="stSidebar"] * {{ color: #F6E9E2 !important; }}
    .sidebar-profile {{
        padding: 22px 18px 18px 18px;
        border-bottom: 1px solid rgba(255,255,255,0.15);
        margin-bottom: 14px;
    }}
    .sidebar-avatar {{
        width: 42px; height: 42px; border-radius: 50%;
        background: {TERRACOTTA};
        display: flex; align-items: center; justify-content: center;
        font-family: 'Lora', serif; font-weight: 600; font-size: 1.1rem;
        color: #fff; margin-bottom: 10px;
    }}
    .sidebar-name {{ font-size: 1.05rem; font-weight: 600; }}
    .sidebar-role {{ font-size: 0.8rem; opacity: 0.75; }}

    section[data-testid="stSidebar"] div[data-testid="stButton"] button {{
        width: 100%;
        text-align: left;
        justify-content: flex-start;
        background: transparent;
        border: 1px solid transparent;
        color: #F6E9E2 !important;
        font-weight: 500;
        font-size: 0.95rem;
        padding: 10px 14px;
        border-radius: 10px;
        margin-bottom: 4px;
        box-shadow: none;
        transition: background 0.15s ease;
    }}
    section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {{
        background: rgba(255,255,255,0.10);
        color: #fff !important;
        border-color: transparent;
    }}
    section[data-testid="stSidebar"] div[data-testid="stButton"] button:focus:not(:active) {{
        box-shadow: none;
    }}
    section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"] {{
        background: rgba(255,255,255,0.16);
        color: #fff !important;
        border-left: 3px solid {TERRACOTTA};
        font-weight: 600;
    }}


    .stNumberInput input, .stTextInput input, .stTextArea textarea {{
        background-color: #FFFFFF !important;
        border: 1px solid {CARD_BORDER} !important;
        border-radius: 8px !important;
        color: {INK} !important;
    }}
    .stNumberInput button {{
        background-color: #FFFFFF !important;
        border: 1px solid {CARD_BORDER} !important;
        color: {MAROON} !important;
    }}
    div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
        border: 1px solid {CARD_BORDER} !important;
        border-radius: 8px !important;
    }}


    .hero-banner {{
        background: linear-gradient(135deg, {MAROON} 0%, {TERRACOTTA} 100%);
        padding: 42px 40px;
        border-radius: 16px;
        color: #fff;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }}
    .hero-banner::after {{
        content: "";
        position: absolute; top: -60px; right: -60px;
        width: 220px; height: 220px; border-radius: 50%;
        background: rgba(255,255,255,0.08);
    }}
    .hero-eyebrow {{
        text-transform: uppercase; letter-spacing: 0.12em; font-size: 0.72rem;
        font-weight: 600; opacity: 0.85; margin-bottom: 8px;
    }}
    .hero-banner h1 {{ margin: 0 0 8px 0; font-size: 2.1rem; color: #fff; }}
    .hero-banner p {{ margin: 0; opacity: 0.9; font-size: 1rem; max-width: 560px; }}

    .card-white {{
        background-color: #FFFFFF;
        padding: 26px 28px;
        border-radius: 14px;
        border: 1px solid {CARD_BORDER};
        box-shadow: 0 4px 14px -6px rgba(154,63,63,0.10);
        margin-bottom: 18px;
    }}
    .dim-card {{
        background-color: #FFFFFF;
        border: 1px solid {CARD_BORDER};
        border-radius: 14px;
        padding: 18px 18px 16px 18px;
        height: 100%;
    }}
    .dim-card .dim-label {{
        text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.68rem;
        font-weight: 600; color: {MAROON}; margin-bottom: 6px;
    }}
    .dim-card .dim-title {{ font-family: 'Lora', serif; font-weight: 600; font-size: 1rem; margin-bottom: 4px; }}
    .dim-card .dim-desc {{ font-size: 0.85rem; color: #6b5a5a; line-height: 1.5; }}


    .result-card {{
        background: #FFFFFF;
        border-radius: 14px;
        padding: 26px 28px;
        border-left: 6px solid var(--accent);
        box-shadow: 0 4px 14px -6px rgba(154,63,63,0.12);
        margin-top: 6px;
    }}
    .result-eyebrow {{
        font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em;
        font-weight: 600; color: var(--accent); margin-bottom: 6px;
    }}
    .result-title {{ font-family: 'Lora', serif; font-size: 1.4rem; font-weight: 600; margin: 0 0 10px 0; color: {INK}; }}
    .result-desc {{ font-size: 0.95rem; line-height: 1.6; color: #4a3a3a; }}

    .gauge-track {{
        position: relative;
        height: 10px; border-radius: 6px; margin: 26px 0 10px 0;
        background: linear-gradient(90deg, {BRICK} 0%, {OCHRE} 50%, {SAGE} 100%);
    }}
    .gauge-marker {{
        position: absolute; top: -7px;
        width: 24px; height: 24px; border-radius: 50%;
        background: #fff; border: 4px solid var(--accent);
        transform: translateX(-50%);
        box-shadow: 0 2px 6px rgba(0,0,0,0.18);
    }}
    .gauge-labels {{ display: flex; justify-content: space-between; font-size: 0.72rem; color: #8a7a7a; }}


    div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stVerticalBlock"]) {{
        background-color: #FFFFFF;
        border: 1px solid {CARD_BORDER} !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 14px -6px rgba(154,63,63,0.10);
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] {{ margin-bottom: 18px; }}

    .form-title {{ font-family: 'Lora', serif; font-weight: 600; font-size: 1.15rem; color: {INK}; margin-bottom: 2px; }}
    .form-subtitle {{ font-size: 0.85rem; color: #8a7270; margin-bottom: 18px; }}
    .stTextInput label p {{ color: {MAROON} !important; font-size: 0.82rem !important; font-weight: 600 !important; }}

    div[data-testid="stFormSubmitButton"] button {{
        background-color: {MAROON} !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 0 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-top: 6px;
    }}
    div[data-testid="stFormSubmitButton"] button:hover {{ background-color: #7A2F2F !important; }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)


MODEL_PATH = Path(__file__).parent / "model_ipm_lr.pkl"


@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        st.error(
            f"File model tidak ditemukan di `{MODEL_PATH.name}`. "
            "Pastikan file model sudah di-commit ke repo (cek juga .gitignore "
            "dan ukuran file jika lebih dari 100MB, perlu Git LFS)."
        )
        st.stop()
    return joblib.load(MODEL_PATH)


model = load_model()

CLUSTER_INFO = {
    0: {
        "label": "Kesejahteraan Rendah",
        "color": BRICK,
        "position": 12,
        "desc": (
            "Prioritaskan akselerasi akses kesehatan dasar (Puskesmas, gizi, sanitasi) dan "
            "pendidikan dasar secara simultan, dipadukan dengan program pengentasan kemiskinan "
            "langsung (bantuan sosial, padat karya) agar peningkatan layanan dasar berdampak "
            "pada penurunan kemiskinan, bukan berjalan terpisah."
        ),
    },
    1: {
        "label": "Kesejahteraan Sedang",
        "color": OCHRE,
        "position": 50,
        "desc": (
            "Arahkan kebijakan pada penciptaan lapangan kerja dan peningkatan upah minimum, "
            "diiringi peningkatan mutu pendidikan menengah ke atas (vokasi/keterampilan kerja) "
            "agar daerah naik kelas dari kategori sedang ke tinggi secara berkelanjutan."
        ),
    },
    2: {
        "label": "Kesejahteraan Tinggi",
        "color": SAGE,
        "position": 88,
        "desc": (
            "Capaian komponen makro daerah sudah prima dan di atas ambang batas rata-rata. "
            "Fokus kebijakan bergeser ke menjaga kualitas layanan publik serta pemerataan "
            "distribusi hasil pembangunan antarwilayah, agar capaian tinggi tidak menimbulkan "
            "ketimpangan baru di internal daerah."
        ),
    },
}


st.sidebar.markdown("""
    <div class="sidebar-profile">
        <div class="sidebar-avatar">E</div>
        <div class="sidebar-name">Halo, Elena!</div>
        <div class="sidebar-role">Analis Kebijakan Wilayah</div>
    </div>
""", unsafe_allow_html=True)
menu_options = [("Beranda", "🏠"), ("Prediksi", "📊")]
if "page" not in st.session_state:
    st.session_state.page = "Beranda"

for label, icon in menu_options:
    is_active = st.session_state.page == label
    if st.sidebar.button(
        f"{icon}   {label}",
        key=f"nav_{label}",
        type="primary" if is_active else "secondary",
        use_container_width=True,
    ):
        st.session_state.page = label
        st.rerun()

menu = st.session_state.page


if menu == "Beranda":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-eyebrow">Sistem Pemetaan Kesejahteraan Wilayah</div>
        <h1>Analisis Makro Klaster IPM</h1>
        <p>Mengelompokkan wilayah berdasarkan Indeks Pembangunan Manusia menggunakan
        algoritma machine learning, sebagai dasar penyusunan rekomendasi kebijakan yang tepat sasaran.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<h3 class="display-font">Apa itu Indeks Pembangunan Manusia?</h3>', unsafe_allow_html=True)
        st.write(
            "Indeks Pembangunan Manusia (IPM) adalah ukuran standar statistik untuk menilai "
            "keberhasilan pembangunan kualitas hidup manusia, disusun dari tiga dimensi dasar: "
            "umur panjang dan hidup sehat, pengetahuan, serta standar hidup layak."
        )

    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    dims = [
        ("Kesehatan", "Angka Harapan Hidup (AHH)", "Lama hidup rata-rata penduduk sejak lahir."),
        ("Pendidikan", "Rata-rata Lama Sekolah (RLS)", "Jenjang pendidikan yang ditempuh penduduk usia 25+."),
        ("Pendidikan", "Harapan Lama Sekolah (HLS)", "Lama sekolah yang diharapkan dapat ditempuh anak usia 7+."),
        ("Ekonomi", "Pengeluaran per Kapita", "Standar hidup layak dari sisi daya beli masyarakat."),
    ]
    for col, (eyebrow, title, desc) in zip([col1, col2, col3, col4], dims):
        with col:
            st.markdown(f"""
                <div class="dim-card">
                    <div class="dim-label">{eyebrow}</div>
                    <div class="dim-title">{title}</div>
                    <div class="dim-desc">{desc}</div>
                </div>
            """, unsafe_allow_html=True)


    st.markdown('<h2 class="display-font">Sistem Klasifikasi</h2>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("""
            <div class="form-title">Parameter Indikator Wilayah</div>
            <div class="form-subtitle">Masukkan nilai capaian indikator makro untuk menguji klaster prediksi</div>
        """, unsafe_allow_html=True)

        with st.form("ipm_form"):
            col1, col2 = st.columns(2)
            with col1:
                ahh_raw = st.text_input("Angka Harapan Hidup (AHH) - Tahun", placeholder="Contoh: 71.5")
                hls_raw = st.text_input("Harapan Lama Sekolah (HLS) - Tahun", placeholder="Contoh: 13.0")
            with col2:
                rls_raw = st.text_input("Rata-rata Lama Sekolah (RLS) - Tahun", placeholder="Contoh: 8.5")
                peng_raw = st.text_input("Rata-rata Pengeluaran per Tahun (Ribu Rp/Tahun)", placeholder="Contoh: 11000")

            submitted = st.form_submit_button("Jalankan Analisis Klasifikasi", use_container_width=True, type="primary")

    if submitted:
        try:
            ahh, rls, hls, pengeluaran = (
                float(ahh_raw.replace(",", ".")),
                float(rls_raw.replace(",", ".")),
                float(hls_raw.replace(",", ".")),
                float(peng_raw.replace(",", ".")),
            )
        except ValueError:
            st.error("Semua kolom wajib diisi dengan angka yang valid, mengikuti contoh pada setiap field.")
            st.stop()

        input_data = [[ahh, rls, hls, pengeluaran]]
        hasil = int(model.predict(input_data)[0])
        info = CLUSTER_INFO[hasil]

        st.markdown(f"""
            <div class="result-card" style="--accent: {info['color']};">
                <div class="result-eyebrow">Hasil Klasifikasi</div>
                <h3 class="result-title">Cluster {hasil} — {info['label']}</h3>
                <div class="result-desc">{info['desc']}</div>
                <div class="gauge-track">
                    <div class="gauge-marker" style="left: {info['position']}%;"></div>
                </div>
                <div class="gauge-labels">
                    <span>Rendah</span><span>Sedang</span><span>Tinggi</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
