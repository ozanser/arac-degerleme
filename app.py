import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bilirkişi Uzman Analiz", layout="wide")

# --- VERİ SÖZLÜĞÜ (Geliştirilebilir) ---
# Burada araç türü -> marka -> model hiyerarşisi kurulmuştur.
veritabani = {
    "Otomobil": {
        "Volkswagen": ["Passat", "Golf", "Polo", "Tiguan"],
        "Renault": ["Clio", "Megane", "Symbol", "Austral"],
        "Fiat": ["Egea", "Linea", "Panda"],
        "Mercedes-Benz": ["C-Serisi", "E-Serisi", "A-Serisi"],
        "BMW": ["3 Serisi", "5 Serisi", "X5"]
    },
    "Tır / Çekici": {
        "Mercedes-Benz": ["Actros", "Arocs", "Axor"],
        "Volvo": ["FH16", "FH", "FMX"],
        "Scania": ["R Serisi", "S Serisi", "G Serisi"],
        "Ford Trucks": ["F-MAX", "1848T"]
    },
    "Kamyon": {
        "Ford": ["Cargo", "Transit (Kamyonet)"],
        "Isuzu": ["NPR", "NQR"],
        "Iveco": ["Daily", "Eurocargo"]
    }
}

# --- YAN PANEL: KATSAYI AYARLARI ---
st.sidebar.header("⚙️ Bilirkişi Parametreleri")
baz_oran = st.sidebar.slider("Baz Değer Oranı (%)", 1, 50, 15) / 100
k_km = st.sidebar.slider("KM Hassasiyet Katsayısı", 0.5, 1.5, 1.0)
k_yas = st.sidebar.slider("Yaş Hassasiyet Katsayısı", 0.5, 1.5, 1.0)

# --- ANA PANEL: AYRI MENÜLER ---
st.title("⚖️ Profesyonel Bilirkişi Araç Değerleme")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Araç Tanımı")
    
    # 1. Menü: Araç Türü
    secilen_tur = st.selectbox("1. Araç Türünü Seçiniz", list(veritabani.keys()))
    
    # 2. Menü: Marka (Seçilen türe göre filtrelenir)
    markalar = list(veritabani[secilen_tur].keys())
    secilen_marka = st.selectbox("2. Markayı Seçiniz", markalar)
    
    # 3. Menü: Model (Seçilen markaya göre filtrelenir)
    modeller = veritabani[secilen_tur][secilen_marka]
    secilen_model = st.selectbox("3. Modeli Seçiniz", modeller)

with col2:
    st.subheader("📊 Teknik ve Mali Veriler")
    yil = st.number_input("Model Yılı", 1990, 2026, 2020)
    km = st.number_input("Kilometre", 0, 2000000, 75000)
    rayic_bedel = st.number_input("Piyasa Rayiç Değeri (TL)", min_value=0, value=1500000)
    onarim_bedeli = st.number_input("İncelenen Onarım Bedeli (TL)", min_value=0, value=200000)

# --- MATEMATİKSEL HESAPLAMA ---
if st.button("⚖️ Bilirkişi Raporunu Hesapla"):
    # Dinamik Katsayı Analizi
    yas = 2026 - yil
    yas_puan = 1.0 if yas <= 2 else (0.7 if yas <= 6 else 0.4)
    km_puan = 1.0 if km <= 30000 else (0.6 if km <= 120000 else 0.3)
    
    # Gelişmiş Formül Uygulaması
    # DK = Rayiç * BazOran * YasPuan * KMPuan * KullanıcıKatsayıları
    deger_kaybi = rayic_bedel * baz_oran * yas_puan * km_puan * k_km * k_yas
    
    st.divider()
    
    # Rapor Sunumu
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric("Hesaplanan Değer Kaybı", f"{deger_kaybi:,.2f} TL")
    with res_col2:
        st.metric("Nihai Araç Değeri", f"{rayic_bedel - deger_kaybi:,.2f} TL")
    
    st.subheader("📝 Hesaplama Metot Notu")
    st.latex(r"DK = Rayiç \times Oran_{baz} \times P_{yaş} \times P_{km} \times K_{ayar}")
    st.write(f"""
    Yapılan inceleme neticesinde; **{secilen_marka} {secilen_model}** model aracın, 
    {yil} model yılı ve {km} km verileri ışığında, piyasa rayiçleri ve teknik katsayılar 
    kullanılarak yukarıdaki sonuca ulaşılmıştır.
    """)
    st.success("Bu rapor denetime elverişli ve matematiksel olarak gerekçelendirilmiştir.")
