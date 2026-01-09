import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları
st.set_page_config(page_title="Bilirkişi Teknik Analiz", layout="wide")

# Kurumsal ve Ciddi Stil
st.markdown("""
    <style>
    .report-title { color: #002b45; border-bottom: 2px solid #002b45; font-weight: bold; }
    .stButton>button { background-color: #002b45; color: white; border-radius: 0px; font-weight: bold; }
    .calc-box { background-color: #f1f3f5; padding: 15px; border-left: 5px solid #002b45; }
    .hakkaniyet-box { background-color: #fff4e6; padding: 15px; border-left: 5px solid #fd7e14; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 class='report-title'>⚖️ Teknik Araç Değer Kaybı Hesaplama Paneli</h2>", unsafe_allow_html=True)

# --- BÖLÜM 1: PİYASA ARAŞTIRMASI (EMSAL GİRİŞİ) ---
st.write("### 🔍 1. Piyasa Rayiç Tespiti (Emsal Metodu)")
col_e1, col_e2, col_e3 = st.columns([2, 1, 3])

with col_e1:
    e1_fiyat = st.number_input("Emsal 1 Fiyat (TL)", min_value=0, value=0)
    e2_fiyat = st.number_input("Emsal 2 Fiyat (TL)", min_value=0, value=0)
with col_e2:
    e1_km = st.number_input("Emsal 1 KM", min_value=0, value=0)
    e2_km = st.number_input("Emsal 2 KM", min_value=0, value=0)
with col_e3:
    e1_not = st.text_input("Emsal 1 Kaynak", placeholder="İlan linki veya galeri adı...")
    e2_not = st.text_input("Emsal 2 Kaynak", placeholder="İlan linki veya galeri adı...")

# Ortalama Hesaplama
fiyatlar = [f for f in [e1_fiyat, e2_fiyat] if f > 0]
rayic_ortalamasi = sum(fiyatlar) / len(fiyatlar) if fiyatlar else 0

st.divider()

# --- BÖLÜM 2: TEKNİK VERİLER ---
st.write("### 🚗 2. Dava Konusu Araç Teknik Detayları")
c1, c2, c3 = st.columns(3)

with c1:
    arac_tanim = st.text_input("Plaka / Marka / Model", "06 ABC 123 - VW Passat")
    yil = st.number_input("Model Yılı", 1990, 2026, 2021)
with c2:
    km = st.number_input("Aracın Kilometresi", 0, 1000000, 50000)
    onarim = st.number_input("Onarım Bedeli (TL)", 0, 5000000, 75000)
with c3:
    hasar_segmenti = st.selectbox("Hasar Bölgesi Önem Derecesi", 
                                  options=[1.0, 1.2, 1.4], 
                                  format_func=lambda x: "Hafif (Tampon vb.)" if x==1.0 else ("Orta (Kaporta)" if x==1.2 else "Ağır (Şasi/Direk)"))

st.divider()

# --- BÖLÜM 3: HESAPLAMA VE HUKUKİ SONUÇ ---
if st.button("TEKNİK ANALİZ RAPORUNU OLUŞTUR"):
    if rayic_ortalamasi == 0:
        st.error("Liyet analizi için en az bir emsal fiyat girmelisiniz.")
    else:
        # Teknik Değer Kaybı Hesaplama (Bilirkişinin Tespit Ettiği Çıplak Zarar)
        yas_k = 1.0 if (2026-yil) <= 2 else (0.7 if (2026-yil) <= 6 else 0.4)
        km_k = 1.0 if km <= 30000 else (0.6 if km <= 120000 else 0.3)
        
        # Formül: Teknik Zarar
        teknik_deger_kaybi = rayic_ortalamasi * 0.15 * yas_k * km_k * hasar_segmenti

        # Analiz Sonuç Paneli
        st.markdown("<div class='calc-box'>", unsafe_allow_html=True)
        st.write("### 📊 Teknik Zarar Tespiti")
        st.write(f"**Hesaplanan Çıplak Değer Kaybı:** :blue[**{teknik_deger_kaybi:,.2f} TL**]")
        st.caption("Bu tutar, aracın piyasa rayici ve teknik özellikleri baz alınarak hesaplanan net zarardır.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("") # Boşluk

        # Mahkeme Hakkaniyet İndirimi Simülasyonu (Bilgi Amaçlı)
        st.markdown("<div class='hakkaniyet-box'>", unsafe_allow_html=True)
        st.write("### ⚖️ Mahkeme Takdiri (Hakkaniyet İndirimi Simülasyonu)")
        st.write("TBK m. 51/52 uyarınca mahkemenin uygulayabileceği olası indirimli tutarlar:")
        
        h_indirim_10 = teknik_deger_kaybi * 0.90
        h_indirim_20 = teknik_deger_kaybi * 0.80
        h_indirim_30 = teknik_deger_kaybi * 0.70
        
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.write(f"**%10 İndirimli:**\n{h_indirim_10:,.2f} TL")
        res_col2.write(f"**%20 İndirimli:**\n{h_indirim_20:,.2f} TL")
        res_col3.write(f"**%30 İndirimli:**\n{h_indirim_30:,.2f} TL")
        st.markdown("</div>", unsafe_allow_html=True)

        # Rapor Taslağı
        st.write("### 📝 Rapor Gerekçe Metni")
        rapor = f"""
        Sayın Hakimliğine,
        
        {arac_tanim} plakalı aracın model yılı, kilometresi ve hasar bölgeleri üzerinde yapılan teknik incelemede; 
        emsal piyasa araştırması neticesinde hasarsız rayiç değerinin {rayic_ortalamasi:,.2f} TL olduğu saptanmıştır.
        
        TEKNİK ZARAR TESPİTİ: 
        Aracın teknik özellikleri ve yıpranma payları gözetilerek yapılan hesaplama neticesinde 
        teknik değer kaybının {teknik_deger_kaybi:,.2f} TL olduğu tespit edilmiştir. 
        
        HUKUKİ NOT: 
        İşbu tutar teknik zarar olup, TBK m. 51 ve 52 uyarınca yapılacak hakkaniyet indirimi takdiri Sayın Mahkemenize aittir.
        """
        st.text_area("Metni Kopyala", rapor, height=250)
