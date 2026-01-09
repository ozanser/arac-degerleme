import streamlit as st
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="Bilirkişi Hesaplama Paneli", layout="wide")

# Kurumsal ve Sade Stil
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .report-box { padding: 20px; border: 1px solid #ccc; border-radius: 5px; background-color: #f9f9f9; }
    h1, h2, h3 { color: #1a1a1a; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Bilirkişi Araç Değer Kaybı Hesaplama")
st.caption("Not: Bu araç veri çekmez; sizin beyan ettiğiniz rayiç değerler üzerinden hesaplama yapar.")

# --- GİRİŞ ALANLARI ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Araç Bilgileri")
    arac_tanimi = st.text_input("Araç Marka / Model / Plaka", placeholder="Örn: 06 ABC 123 - VW Passat")
    yil = st.number_input("Model Yılı", 1990, 2026, 2020)
    km = st.number_input("Kilometre", 0, 1000000, 50000)
    hasar_yeri = st.multiselect("Hasarlı Parçalar", ["Tampon", "Kaput", "Çamurluk", "Şasi/Direk", "Mekanik"])

with col2:
    st.subheader("💰 Piyasa ve Maliyet")
    rayic_deger = st.number_input("Tespit Edilen Hasarsız Rayiç (TL)", min_value=0, value=1000000)
    onarim_bedeli = st.number_input("Onarım Bedeli (Parça+İşçilik) (TL)", min_value=0, value=50000)
    baz_kayip_orani = st.slider("Baz Kayıp Katsayısı (%)", 5, 25, 12) / 100

# --- HESAPLAMA MANTIĞI (Şeffaf Formül) ---
def hesapla():
    # Yaş Çarpanı
    yas = 2026 - yil
    if yas <= 1: yas_c = 1.0
    elif yas <= 4: yas_c = 0.8
    else: yas_c = 0.5
    
    # KM Çarpanı
    if km <= 20000: km_c = 1.0
    elif km <= 80000: km_c = 0.7
    else: km_c = 0.4
    
    # Kritik Parça Çarpanı
    kritik_c = 1.3 if "Şasi/Direk" in hasar_yeri else 1.0
    
    sonuc = rayic_deger * baz_kayip_orani * yas_c * km_c * kritik_c
    return sonuc, yas_c, km_c, kritik_c

# --- SONUÇ VE RAPOR ---
if st.button("📊 Analiz Raporu Oluştur"):
    dk, yc, kc, kr_c = hesapla()
    
    st.divider()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Hesaplanan Değer Kaybı", f"{dk:,.2f} TL")
    c2.metric("Yeni Piyasa Değeri", f"{rayic_deger - dk:,.2f} TL")
    c3.metric("Zarar / Rayiç Oranı", f"% {(dk/rayic_deger)*100:.2f}")

    st.markdown("### 📝 Bilirkişi Gerekçeli Karar Taslağı")
    rapor = f"""
    İnceleme konusu {arac_tanimi} marka/modelli aracın; {yil} model yılı ve {km} km'de olduğu görülmüştür. 
    
    Piyasa araştırmaları neticesinde aracın hasarsız rayicinin {rayic_deger:,.2f} TL olduğu kabul edilmiştir.
    Yapılan teknik hesaplamada; 
    - Yaş Katsayısı: {yc}
    - KM Katsayısı: {kc}
    - Hasar Bölgesi Katsayısı: {kr_c} 
    verileri baz alınarak, matematiksel olarak {dk:,.2f} TL değer kaybı oluştuğu tespit edilmiştir.
    
    Bu hesaplama denetime elverişli olup, genel kabul görmüş bilirkişi metodolojisine uygundur.
    """
    st.info(rapor)
