import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Sayfa Konfigürasyonu (Geniş ve Modern)
st.set_page_config(
    page_title="Bilirkişi Pro | Araç Değerleme",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Gelişmiş Kurumsal CSS Tasarımı
st.markdown("""
    <style>
    /* Ana Arkaplan */
    .stApp {
        background-color: #f4f7f9;
    }
    
    /* Sol Menü (Sidebar) Tasarımı */
    [data-testid="stSidebar"] {
        background-color: #002b45 !important;
        color: white;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: #d1dce5;
    }

    /* Başlık ve Kart Tasarımları */
    h1 {
        color: #002b45;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        border-bottom: 2px solid #002b45;
        padding-bottom: 10px;
    }

    .stMetric {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid #005a9c;
    }

    /* Tab Menü Tasarımı */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #ffffff;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        border: 1px solid #e1e4e8;
    }
    .stTabs [aria-selected="true"] {
        background-color: #005a9c !important;
        color: white !important;
        font-weight: bold;
    }

    /* Buton Tasarımı */
    div.stButton > button:first-child {
        background-color: #005a9c;
        color: white;
        border-radius: 8px;
        height: 3.5em;
        width: 100%;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #003d6b;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Input Alanları Gölgeleme */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VERİTABANI --- (Kısaltılmış örnek, önceki sürümdeki geniş listeyi buraya ekleyebilirsiniz)
arac_db = {
    "Otomobil": {
        "Volkswagen": ["Passat", "Golf", "Polo", "Tiguan"],
        "Mercedes-Benz": ["C-Serisi", "E-Serisi", "A-Serisi"],
        "Renault": ["Clio", "Megane", "Austral"],
        "Fiat": ["Egea", "Linea", "Doblo"]
    },
    "Tır / Çekici": {
        "Scania": ["R 450", "S 500"],
        "Volvo": ["FH 16", "FM"],
        "Mercedes-Benz": ["Actros"]
    }
}

# --- YAN PANEL ---
with st.sidebar:
    st.markdown("### 🏛️ Bilirkişi Paneli")
    st.divider()
    baz_oran = st.slider("Baz Değer Oranı (%)", 5, 25, 12) / 100
    k_yas = st.select_slider("Yaş Hassasiyeti", options=[0.8, 1.0, 1.2], value=1.0)
    k_km = st.select_slider("KM Hassasiyeti", options=[0.8, 1.0, 1.2], value=1.0)
    st.divider()
    st.caption("v2.1.0 - Kurumsal Bilirkişi Yazılımı")

# --- ANA EKRAN ---
st.title("⚖️ Araç Değer Kaybı Analiz Sistemi")

# Bölümleme: Üst kısımda özet bilgiler
tab_input, tab_analysis, tab_report = st.tabs(["📝 Veri Girişi", "📈 Teknik Analiz", "📄 Resmi Rapor"])

with tab_input:
    st.markdown("#### 1. Araç Künyesi ve Piyasa Verileri")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        tip = st.selectbox("Araç Kategorisi", list(arac_db.keys()))
        marka = st.selectbox("Marka", list(arac_db[tip].keys()))
        model = st.selectbox("Model", arac_db[tip][marka])
    with c2:
        yil = st.number_input("Model Yılı", 2000, 2026, 2021)
        km = st.number_input("Kilometre", 0, 1000000, 45000)
        renk = st.text_input("Araç Rengi", "Beyaz")
    with c3:
        rayic = st.number_input("Piyasa Rayiç Değeri (TL)", 0, 50000000, 1250000)
        hasar_bedeli = st.number_input("İncelenen Onarım Bedeli (TL)", 0, 5000000, 85000)
        hasar_bolgesi = st.multiselect("Hasarlı Bölgeler", ["Ön Panel", "Kaput", "Şasiler", "Tavan", "Arka Panel"])

    st.divider()
    calculate = st.button("📊 HESAPLAMAYI GERÇEKLEŞTİR")

if calculate:
    # --- MATEMATİKSEL MOTOR ---
    yas = 2026 - yil
    yas_puan = 1.2 if yas <= 1 else (1.0 if yas <= 4 else 0.7)
    km_puan = 1.1 if km <= 20000 else (1.0 if km <= 60000 else 0.5)
    
    # Şasi/Tavan gibi kritik yerlerde katsayı artar
    hasar_katsayi = 1.4 if any(x in hasar_bolgesi for x in ["Şasiler", "Tavan"]) else 1.0
    
    deger_kaybi = rayic * baz_oran * yas_puan * km_puan * hasar_katsayi * k_yas * k_km

    with tab_analysis:
        st.markdown("#### 2. Matematiksel Değerlendirme")
        
        # Sonuç Kartları
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Tespit Edilen Değer Kaybı", f"{deger_kaybi:,.2f} TL")
        with m2:
            st.metric("Hasar Sonrası Yeni Rayiç", f"{rayic - deger_kaybi:,.2f} TL")
        with m3:
            st.metric("Zarar Oranı / Rayiç", f"% {(deger_kaybi/rayic)*100:.1f}")
        
        st.divider()
        
        # Grafik
        st.write("**Değer Değişim Grafiği**")
        chart_data = pd.DataFrame({
            "Kategori": ["Hasarsız", "Hasarlı"],
            "Değer (TL)": [rayic, rayic - deger_kaybi]
        })
        st.bar_chart(chart_data.set_index("Kategori"))

    with tab_report:
        st.markdown("#### 3. Bilirkişi Rapor Taslağı")
        st.info("Aşağıdaki metin UYAP ve Mahkeme formatına uygun şekilde oluşturulmuştur.")
        
        rapor = f"""
        DOSYA NO: [Dosya Numarası Giriniz]
        HUZURDAKİ ARAÇ: {yil} Model {marka} {model} ({km:,} KM)
        
        ANALİZ SONUCU:
        Yapılan teknik inceleme, kaza sonrası onarım boyutu ve piyasa rayiçleri (Emsal: {rayic:,} TL) 
        göz önüne alındığında, aracın kaza tarihindeki durumuna göre ikinci el satış değerinde 
        {deger_kaybi:,.2f} TL tutarında bir eksilme (değer kaybı) olduğu kanaatine varılmıştır.
        
        DAYANAK:
        Hesaplama; KM Katsayısı ({km_puan}), Yaş Katsayısı ({yas_puan}) ve Hasar Bölge Analizi 
        parametreleri kullanılarak, denetime elverişli matematiksel modelleme ile yapılmıştır.
        """
        st.text_area("Kopyalanabilir Rapor", rapor, height=250)
        st.button("🖨️ PDF Raporu Oluştur (Yakında)")
else:
    with tab_analysis:
        st.warning("Lütfen önce veri girişi yapıp hesapla butonuna basınız.")
