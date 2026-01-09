import streamlit as st
import pandas as pd

# 1. Sayfa Standartları
st.set_page_config(page_title="Bilirkişi Uzman Paneli", layout="wide")

# Kurumsal Stil Uygulaması
st.markdown("""
    <style>
    .report-title { color: #002b45; border-bottom: 3px solid #002b45; padding-bottom: 10px; font-weight: bold; margin-bottom: 25px; }
    .emsal-box { background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; border-radius: 4px; margin-bottom: 10px; }
    .stButton>button { background-color: #002b45; color: white; border-radius: 2px; width: 100%; font-weight: bold; }
    .result-section { background-color: #e9ecef; padding: 20px; border-radius: 4px; border-left: 6px solid #002b45; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 class='report-title'>⚖️ Araç Değerleme ve Değer Kaybı Analiz Sistemi</h2>", unsafe_allow_html=True)

# --- BÖLÜM 1: MANUEL EMSAL ARAŞTIRMASI ---
st.write("### 🔍 Adım 1: Piyasa Araştırması (Emsal İlanlar)")
st.caption("İncelediğiniz en az 3 benzer ilanın bilgilerini giriniz. Sistem rayiç ortalamayı bu verilerden kuracaktır.")

emsal_verileri = []
col_e1, col_e2, col_e3 = st.columns([2, 1, 3])

with col_e1:
    e1_fiyat = st.number_input("Emsal 1 Fiyat (TL)", min_value=0, value=0, step=10000)
    e2_fiyat = st.number_input("Emsal 2 Fiyat (TL)", min_value=0, value=0, step=10000)
    e3_fiyat = st.number_input("Emsal 3 Fiyat (TL)", min_value=0, value=0, step=10000)

with col_e2:
    e1_km = st.number_input("Emsal 1 KM", min_value=0, value=0)
    e2_km = st.number_input("Emsal 2 KM", min_value=0, value=0)
    e3_km = st.number_input("Emsal 3 KM", min_value=0, value=0)

with col_e3:
    e1_not = st.text_input("Emsal 1 Kaynak/Not", placeholder="Örn: Sahibinden İlan No: 123...")
    e2_not = st.text_input("Emsal 2 Kaynak/Not", placeholder="Örn: X Galeri Sözlü Beyan...")
    e3_not = st.text_input("Emsal 3 Kaynak/Not", placeholder="Örn: Gazete İlanı / Emsal İlan...")

# Ortalama Rayiç Hesaplama
fiyat_listesi = [f for f in [e1_fiyat, e2_fiyat, e3_fiyat] if f > 0]
hesaplanan_rayic = sum(fiyat_listesi) / len(fiyat_listesi) if fiyat_listesi else 0

if hesaplanan_rayic > 0:
    st.info(f"📌 **Emsal Ortalamasına Göre Belirlenen Rayiç Değer:** {hesaplanan_rayic:,.2f} TL")
st.divider()

# --- BÖLÜM 2: ANALİZİ YAPILAN ARAÇ BİLGİLERİ ---
st.write("### 🚗 Adım 2: Dava Konusu Araç ve Hasar Detayları")
c1, c2 = st.columns(2)

with c1:
    arac_tanimi = st.text_input("Araç Marka/Model/Plaka", placeholder="Örn: 06 ABC 123 - VW Passat")
    yil = st.number_input("Model Yılı", 1990, 2026, 2021)
    km = st.number_input("Aracın Kilometresi", 0, 1000000, 50000)

with c2:
    onarim_bedeli = st.number_input("Onarım Bedeli (Parça+İşçilik) (TL)", 0, 5000000, 50000)
    hasar_yeri = st.multiselect("Hasar Alanları", ["Ön Kısım", "Arka Kısım", "Yan Paneller", "Şasi/Direk/Tavan (Ağır)", "Mekanik"])
    k_hassasiyet = st.slider("Bilirkişi İnisiyatif Katsayısı", 0.8, 1.2, 1.0, help="Piyasa hareketliliğine göre %20 esneme payı.")

# --- BÖLÜM 3: HESAPLAMA VE RAPORLAMA ---
if st.button("ANALİZİ TAMAMLA VE RAPORU OLUŞTUR"):
    if hesaplanan_rayic == 0:
        st.error("Lütfen hesaplama için en az bir emsal fiyatı giriniz.")
    else:
        # Matematiksel Modelleme
        yas_c = 1.0 if (2026-yil) <= 2 else (0.75 if (2026-yil) <= 6 else 0.5)
        km_c = 1.0 if km <= 30000 else (0.7 if km <= 100000 else 0.4)
        hasar_c = 1.35 if "Şasi/Direk/Tavan (Ağır)" in hasar_yeri else 1.0
        
        # Formül: DK = Rayic * BazOran(%15) * YasC * KMC * HasarC * Hassasiyet
        deger_kaybi = hesaplanan_rayic * 0.15 * yas_c * km_c * hasar_c * k_hassasiyet

        st.markdown("<div class='result-section'>", unsafe_allow_html=True)
        st.write("### 📊 Teknik Analiz Sonucu")
        st.write(f"**Tespit Edilen Değer Kaybı:** {deger_kaybi:,.2f} TL")
        st.write(f"**Kaza Tarihi Rayiç Değeri:** {hesaplanan_rayic:,.2f} TL")
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("### 📝 Gerekçeli Rapor Taslağı")
        rapor = f"""
        SAYIN HAKİMLİĞİNE
        
        İnceleme konusu {arac_tanimi} plakalı aracın yapılan teknik tetkikinde; {yil} model olduğu ve {km:,} km mesafede bulunduğu tespit edilmiştir.
        
        PİYASA ARAŞTIRMASI:
        Tarafımızca yapılan manuel piyasa araştırmasında benzer özelliklerdeki şu emsaller baz alınmıştır:
        1. {e1_fiyat:,.0f} TL ({e1_not})
        2. {e2_fiyat:,.0f} TL ({e2_not})
        3. {e3_fiyat:,.0f} TL ({e3_not})
        Emsal verilerin ortalaması neticesinde aracın hasarsız rayiç değerinin {hesaplanan_rayic:,.2f} TL olduğu sonucuna varılmıştır.
        
        DEĞER KAYBI TESPİTİ:
        Aracın {", ".join(hasar_yeri)} bölgelerinden aldığı hasar, model yılı ve kilometresi baz alınarak yapılan matematiksel modelleme sonucunda; 
        ikinci el piyasa değerinde {deger_kaybi:,.2f} TL tutarında bir eksilme (değer kaybı) olduğu kanaati hasıl olmuştur.
        
        Arz olunur.
        """
        st.text_area("Rapor Metni (Kopyalamak için tıklayın)", rapor, height=350)
