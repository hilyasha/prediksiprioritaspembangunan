import streamlit as st
import joblib

st.set_page_config(layout="wide", page_title="Analisis Prioritas Pembangunan", page_icon="📍")

CREAM = "#FBF9D1"
INK = "#3D2C2C"
MAROON = "#9A3F3F"
TERRACOTTA = "#C1856D"
SAGE = "#6B8F71"
OCHRE = "#D9A441"
BRICK = "#B0413E"
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

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    return joblib.load("model_ipm_lr.pkl")


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
menu = st.sidebar.radio("Navigasi", ["Beranda", "Prediksi"], label_visibility="collapsed")


if menu == "Beranda":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-eyebrow">Sistem Pemetaan Kesejahteraan Wilayah</div>
        <h1>Analisis Makro Klaster IPM</h1>
        <p>Mengelompokkan wilayah berdasarkan Indeks Pembangunan Manusia menggunakan
        algoritma machine learning, sebagai dasar penyusunan rekomendasi kebijakan yang tepat sasaran.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card-white">', unsafe_allow_html=True)
    st.markdown('<h3 class="display-font">Apa itu Indeks Pembangunan Manusia?</h3>', unsafe_allow_html=True)
    st.write(
        "Indeks Pembangunan Manusia (IPM) adalah ukuran standar statistik untuk menilai "
        "keberhasilan pembangunan kualitas hidup manusia, disusun dari tiga dimensi dasar: "
        "umur panjang dan hidup sehat, pengetahuan, serta standar hidup layak."
    )
    st.markdown('</div>', unsafe_allow_html=True)

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


elif menu == "Prediksi":
    st.markdown('<h2 class="display-font">Sistem Klasifikasi Wilayah</h2>', unsafe_allow_html=True)
    st.caption("Masukkan nilai keempat indikator untuk menentukan klaster kesejahteraan suatu wilayah.")

    with st.container():
        st.markdown('<div class="card-white">', unsafe_allow_html=True)
        with st.form("ipm_form"):
            col1, col2 = st.columns(2)
            with col1:
                ahh = st.number_input("Angka Harapan Hidup (AHH) — tahun", min_value=50.0, max_value=90.0, step=0.1)
                rls = st.number_input("Rata-rata Lama Sekolah (RLS) — tahun", min_value=1.0, max_value=20.0, step=0.1)
            with col2:
                hls = st.number_input("Harapan Lama Sekolah (HLS) — tahun", min_value=5.0, max_value=20.0, step=0.1)
                pengeluaran = st.number_input("Pengeluaran per Kapita per Tahun (ribu Rp)", min_value=1000, max_value=30000, step=100)

            submitted = st.form_submit_button("Jalankan Analisis Klasifikasi")
        st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
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