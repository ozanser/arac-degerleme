import streamlit as st
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="Bilirkişi Araç Değerleme", layout="wide")

st.title("⚖️ Profesyonel Bilirkişi Araç Analiz Sistemi")

# --- VERİ SETİ (Örnek listeleri genişletebilirsiniz) ---
arac_tipleri = ["Otomobil", "Kamyonet", "Kamyon", "Çekici (Tır)", "Otobüs", "Motosiklet"]
renkler = ["Beyaz", "Siyah", "Gri (Gümüş)", "Gri (Füme)", "Kırmızı", "Mavi", "Diğer"]

# Marka ve Model İlişkisi
marka_model_verisi = {
    "Volkswagen": ["Passat", "Golf", "Polo", "Tiguan", "Transporter"],
    "Renault": ["Clio", "Megane", "Symbol", "Fluence", "Master"],
    "Fiat": ["Egea", "Linea", "Doblo", "Fiorino", "Ducato"],
    "Ford": ["Focus", "Fiesta", "Transit", "Courier", "F-Max (Tır)"],
    "Mercedes-Benz": ["C-Serisi", "E-Serisi", "Actros (Tır)", "Vito", "Sprinter"],
    "Toyota": ["Corolla", "Yaris", "Hilux", "Auris"],
    "BMW": ["3 Serisi", "5 Serisi", "1 Serisi", "X5"]
}

# --- ARAYÜZ TASARIMI ---
st.sidebar.header("📋 Araç Tanımlama")

# 1. Araç Cinsi ve Rengi
cins = st.sidebar.selectbox("Araç Cinsi", arac_tipleri)
renk = st.sidebar.selectbox("Renk", renkler)

# 2. Dinamik Marka/Model Seçimi
marka = st.sidebar.selectbox("Marka", list(marka_model_verisi.keys()))
model = st.sidebar.selectbox("Model", marka_model_verisi[marka])

# 3. Teknik Detaylar
yil = st.sidebar.number_input("Model Yılı", 1990, 2026, 2020)
km = st.sidebar.number_input("Kilometre", 0, 2000000, 50000)
vites = st.sidebar.selectbox("Vites/Şanzıman", ["Manuel", "Yarı Otomatik", "Tam Otomatik"])

st.sidebar.divider()

# 4. Hasar ve Kaza Bilgileri
st.sidebar.header("💥 Hasar Durumu")
tramer = st.sidebar.number_input("Toplam Tramer Kaydı (TL)", 0, 5000000, 0)
kaza_bedeli = st.sidebar.number_input("İncelenen Kaza Onarım Bedeli (TL)", 0, 1000000, 0)

# --- HESAPLAMA VE ANALİZ ---
if st.sidebar.button("Analiz Raporu Oluştur"):
    st.subheader(f"🔍 Araç Analiz Özeti: {marka} {model}")
    
    # Bilirkişi hesaplama simülasyonu
    # (Bu değerler internetteki ortalama verileri temsil eder)
    taban_fiyat = 1000000  # Örnek taban fiyat
    km_etkisi = (km / 10000) * 5000  # Her 10bin km için 5bin TL düşüş (örnektir)
    
    # Tahmini Rayiç Değer
    tahmini_rayic = taban_fiyat - km_etkisi
    
    # Değer Kaybı Hesaplama (Yargıtay/Sigorta Mevzuatı Taslağı)
    # Değer kaybı genellikle onarım bedelinin %15-45'i arası değişir (KM ve yaşa göre)
    km_katsayisi = 1.0 if km < 50000 else (0.7 if km < 150000 else 0.3)
    hesaplanan_deger_kaybi = kaza_bedeli * 0.5 * km_katsayisi

    # Sonuç Paneli
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Piyasa Rayiç (Hasarsız)", f"{tahmini_rayic:,.0f} TL")
    with col2:
        st.metric("Hesaplanan Değer Kaybı", f"{hesaplanan_deger_kaybi:,.0f} TL", delta="-Zarar")
    with col3:
        st.metric("Nihai Değer (Hasarlı)", f"{tahmini_rayic - hesaplanan_deger_kaybi:,.0f} TL")

    st.divider()

    # Bilirkişi Rapor Tablosu
    rapor_data = {
        "Kalem": ["Araç Cinsi", "Marka / Model", "Model Yılı / Renk", "Kilometre", "Vites Tipi", "Toplam Tramer"],
        "Detay": [cins, f"{marka} {model}", f"{yil} / {renk}", f"{km:,.0f} KM", vites, f"{tramer:,.0f} TL"]
    }
    st.table(pd.DataFrame(rapor_data))
    
    st.warning(f"**Bilirkişi Notu:** Bu rapor, {marka} markasının {model} modeli için girilen {km} km ve {kaza_bedeli} TL'lik onarım verileri doğrultusunda oluşturulmuştur.")

else:
    st.info("Lütfen sol paneldeki bilgileri eksiksiz doldurarak 'Analiz Raporu Oluştur' butonuna basınız.")
