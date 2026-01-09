import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları
st.set_page_config(page_title="Profesyonel Bilirkişi Paneli", layout="wide")

# Kurumsal Stil
st.markdown("""
    <style>
    .report-title { color: #002b45; border-bottom: 2px solid #002b45; font-weight: bold; }
    .stButton>button { background-color: #002b45; color: white; border-radius: 0px; font-weight: bold; }
    .calc-box { background-color: #f1f3f5; padding: 15px; border-radius: 5px; border-left: 5px solid #002b45; }
    .hakkaniyet-box { background-color: #fff4e6; padding: 15px; border-radius: 5px; border-left: 5px solid #fd7e14; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 class='report-title'>⚖️ Bilirkişi Araç Değerleme Sistemi (3 Emsal Metodu)</h2>", unsafe_allow_html=True)

# --- BÖLÜM 1: 3'LÜ PİYASA ARAŞTIRMASI ---
st.write("### 🔍 1. Piyasa Rayiç Tespiti (En Az 3 Emsal)")
col_e1, col_e2, col_e3 = st.columns([2, 1, 3])

with col_e1:
    e1_f = st.number_input("Emsal 1 Fiyat (TL)", min_value=0, value=0)
    e2_f = st.number_input("Emsal 2 Fiyat (TL)", min_value=0, value=0)
    e3_f = st.number_input("Emsal 3 Fiyat (TL)", min_value=0, value=0)
with col_e2:
    e1_k = st.number_input("Emsal 1 KM", min_value=0, value=0)
    e2_k = st.number_input("Emsal 2 KM", min_value=0, value=0)
    e3_k = st.number_input("Emsal 3 KM", min_value=0, value=0)
with col_e3:
    e1_n = st.text_input("Emsal 1 Kaynak/Not", placeholder="Link veya Galeri...")
    e2_n = st.text_input("Emsal 2 Kaynak/Not", placeholder="Link veya Galeri...")
    e3_n = st.text_input("Emsal 3 Kaynak/Not", placeholder="Link veya Galeri...")

# Dinamik Ortalama (Sadece girilen değerleri alır)
fiyat_listesi = [f for f in [e1_f, e2_f, e3_f] if f > 0]
rayic_ort = sum(fiyat_listesi) / len(fiyat_listesi) if fiyat_listesi else 0

if rayic_ort > 0:
    st.info(f"📊 **Tespit Edilen Ortalama Rayiç:** {rayic_ort:,.2f} TL (İncelenen Emsal Sayısı: {len(fiyat_listesi)})")

st.divider()

# --- BÖLÜM 2: TEKNİK VERİLER VE ANALİZ ---
st.write("### 🚗 2. Dava Konusu Araç ve Hasar Analizi")
c1, c2, c3 = st.columns(3)

with c1:
    arac_bilgi = st.text_input("Araç Tanımı", "2021 VW Passat")
    yil = st.number_input("Model Yılı", 1990, 2026, 2021)
with c2:
    km = st.number_input("Aracın Kilometresi", 0, 1000000, 50000)
    hasar_tipi = st.selectbox("Hasar Bölgesi Şiddeti", 
                               options=[1.0, 1.25, 1.5], 
                               format_func=lambda x: "Hafif (Plastik/Tampon)" if x==1.0 else ("Orta (Kaporta/Panel)" if x==1.25 else "Ağır (Şasi/İskelet)"))
with c3:
    # Bilirkişi tarafından belirlenen temel kayıp oranı (Piyasa şartlarına göre)
    baz_oran = st.number_input("Baz Kayıp Oranı (%)", 1, 50, 15) / 100

# --- BÖLÜM 3: HESAPLAMA VE İSPAT ---
if st.button("ANALİZ RAPORUNU VE MATEMATİKSEL İSPATI OLUŞTUR"):
    if len(fiyat_listesi) < 2:
        st.error("Lütfen sağlıklı bir analiz için en az 2, tercihen 3 emsal fiyat giriniz.")
    else:
        # Teknik Katsayılar
        yas_k = 1.0 if (2026-yil) <= 2 else (0.75 if (2026-yil) <= 6 else 0.45)
        km_k = 1.0 if km <= 25000 else (0.65 if km <= 110000 else 0.35)
        
        # Teknik Zarar Formülü
        t_zarar = rayic_ort * baz_oran * yas_k * km_k * hasar_tipi

        # Analiz Sonuçları
        st.markdown("<div class='calc-box'>", unsafe_allow_html=True)
        st.write("### 📈 Teknik Değer Kaybı Tespiti")
        st.write(f"**Net Teknik Zarar:** {t_zarar:,.2f} TL")
        st.caption("Bu rakam mahkemenin takdirinden önceki çıplak teknik zararı ifade eder.")
        st.markdown("</div>", unsafe_allow_html=True)

        # Matematiksel İspat Bölümü (Denetime Elverişlilik İçin)
        st.write("#### 🔍 Matematiksel Formül Dökümü")
        st.latex(rf"DK = {rayic_ort:,.0f} \times {baz_oran} \times {yas_k} \times {km_k} \times {hasar_tipi} = {t_zarar:,.2f} \text{{ TL}}")

        # Mahkeme Hakkaniyet İndirimi Paneli
        st.markdown("<div class='hakkaniyet-box'>", unsafe_allow_html=True)
        st.write("### ⚖️ Olası Hakkaniyet İndirimleri (TBK 51/52)")
        col_h1, col_h2, col_h3 = st.columns(3)
        col_h1.metric("%10 İndirimli", f"{t_zarar*0.9:,.2f} TL")
        col_h2.metric("%20 İndirimli", f"{t_zarar*0.8:,.2f} TL")
        col_h3.metric("%30 İndirimli", f"{t_zarar*0.7:,.2f} TL")
        st.markdown("</div>", unsafe_allow_html=True)

        # Hazır Rapor Metni
        st.write("### 📝 Bilirkişi Sonuç Metni")
        rapor = f"""
        Dosya konusu {arac_bilgi} plakalı aracın piyasa rayiç araştırmasında, ekte sunulan 3 adet emsalin ortalaması olan {rayic_ort:,.2f} TL baz alınmıştır.
        
        Aracın yaşı, kilometresi ve hasar şiddeti ({hasar_tipi}) katsayıları ile yapılan matematiksel modelleme neticesinde; 
        araçtaki TEKNİK DEĞER KAYBININ {t_zarar:,.2f} TL OLDUĞU TESPİT EDİLMİŞTİR.
        
        TBK m.51-52 uyarınca yapılacak takdiri indirimler Sayın Mahkemenin yetkisindedir.
        """
        st.text_area("Raporu Kopyala", rapor, height=200)
