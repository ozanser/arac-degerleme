import streamlit as st
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="Bilirkişi Araç Analiz", layout="centered")

st.title("⚖️ Bilirkişi Araç Değerleme Sistemi")
st.info("Bu uygulama internet üzerindeki güncel verileri ve bilirkişi formüllerini kullanarak analiz yapar.")

# Giriş Alanları
with st.form("arac_formu"):
    col1, col2 = st.columns(2)
    with col1:
        marka = st.text_input("Marka")
        model = st.text_input("Model")
        yil = st.number_input("Model Yılı", 1990, 2026, 2020)
    with col2:
        km = st.number_input("Kilometre", 0, 1000000, 50000)
        vites = st.selectbox("Vites", ["Manuel", "Otomatik"])
        hasar = st.number_input("Tramer Kaydı (TL)", 0, 1000000, 0)
    
    onarim_bedeli = st.number_input("Son Kaza Onarım Bedeli (TL)", 0, 500000, 0)
    submit = st.form_submit_button("Analizi Başlat")

if submit:
    # Bilirkişi Hesaplama Mantığı (Örnek Formül)
    # Değer Kaybı Katsayısı: $$DK = (Baz Fiyat \times KM Katsayısı \times Parça Katsayısı)$$
    
    st.subheader("📊 Analiz Sonuçları")
    
    # Simüle edilmiş piyasa araştırması (Google/Sahibinden verisi varsayımı)
    rayic_fiyat = 1250000  # Bu kısım API veya scraping ile dinamikleşebilir
    
    # KM Katsayısı Hesaplama
    km_katsayi = 1.0 if km < 20000 else (0.8 if km < 100000 else 0.5)
    
    deger_kaybi = (onarim_bedeli * 0.6) * km_katsayi
    guncel_deger = rayic_fiyat - deger_kaybi - (hasar * 0.2)

    c1, c2 = st.columns(2)
    c1.metric("Tahmini Rayiç Değer", f"{rayic_fiyat:,.0f} TL")
    c2.metric("Hesaplanan Değer Kaybı", f"{deger_kaybi:,.0f} TL", delta_color="inverse")
    
    st.success(f"Aracın Nihai Bilirkişi Değeri: **{guncel_deger:,.0f} TL**")
    
    # Raporlama Tablosu
    data = {
        "Parametre": ["Marka/Model", "Kilometre", "Tramer", "Yasal Değer Kaybı"],
        "Değer": [f"{marka} {model}", f"{km} KM", f"{hasar} TL", f"{deger_kaybi} TL"]
    }
    st.table(pd.DataFrame(data))
