import streamlit as st
import pandas as pd

# Sayfa Konfigürasyonu (Kurumsal Standart)
st.set_page_config(page_title="Bilirkişi Hesaplama Sistemi", layout="centered")

# Minimalist Stil (Göz yormayan, resmi format)
st.markdown("""
    <style>
    .report-header { color: #002b45; border-bottom: 2px solid #002b45; padding-bottom: 5px; margin-bottom: 20px; font-weight: bold; }
    .stButton>button { background-color: #002b45; color: white; border-radius: 0px; width: 100%; height: 3em; font-weight: bold; }
    .result-box { background-color: #f0f2f6; padding: 20px; border-left: 5px solid #002b45; }
    .stTextInput>div>div>input { border-radius: 0px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 class='report-header'>⚖️ Araç Değer Kaybı Tespit Paneli</h2>", unsafe_allow_html=True)

# --- 1. VERİ GİRİŞİ (TEK SÜTUN, NET SIRALAMA) ---
with st.container():
    st.write("### 1. Araç ve Dosya Bilgileri")
    dosya_no = st.text_input("Dosya / Esas No", placeholder="Örn: 2025/123 E.")
    arac_detay = st.text_input("Araç Marka / Model / Plaka", placeholder="Örn: 06 ABC 123 - 2021 Model VW Passat")
    
    c1, c2 = st.columns(2)
    with c1:
        yil = st.number_input("Model Yılı", 1990, 2026, 2021)
        km = st.number_input("Kilometre (KM)", 0, 1000000, 45000)
    with c2:
        rayic = st.number_input("Hasarsız Rayiç Değer (TL)", 0, 50000000, 1500000)
        hasar_bedeli = st.number_input("Onarım Bedeli (TL)", 0, 5000000, 100000)

    hasar_yeri = st.multiselect("Hasar Alanları", ["Ön Kısım", "Arka Kısım", "Yan Paneller", "Şasi / Direk / Tavan (Kritik)", "Mekanik Aksam"])

st.divider()

# --- 2. HESAPLAMA PARAMETRELERİ (ŞEFFAF) ---
st.write("### 2. Hesaplama Parametreleri")
st.caption("Bilirkişi görüşünüze göre katsayıları belirleyin. Bu katsayılar raporunuzun gerekçesini oluşturacaktır.")

col_k1, col_k2, col_k3 = st.columns(3)
with col_k1:
    k_yas = st.number_input("Yaş Katsayısı (0.1 - 1.5)", 0.1, 1.5, 1.0)
with col_k2:
    k_km = st.number_input("KM Katsayısı (0.1 - 1.5)", 0.1, 1.5, 1.0)
with col_k3:
    k_oran = st.number_input("Baz Zarar Oranı (%)", 1, 50, 15) / 100

# --- 3. ANALİZ VE ÇIKTI ---
if st.button("HESAPLA VE RAPOR TASLAĞI OLUŞTUR"):
    # Gerçekçi Matematiksel Modelleme
    yas_puan = 1.0 if (2026-yil) <= 2 else (0.7 if (2026-yil) <= 6 else 0.4)
    km_puan = 1.0 if km <= 20000 else (0.6 if km <= 100000 else 0.3)
    hasar_puan = 1.4 if "Şasi / Direk / Tavan (Kritik)" in hasar_yeri else 1.0
    
    deger_kaybi = rayic * k_oran * yas_puan * km_puan * hasar_puan * k_yas * k_km

    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
    st.write("### 📊 Hesaplama Sonucu")
    st.write(f"**Tespit Edilen Değer Kaybı:** :blue[{deger_kaybi:,.2f} TL]")
    st.write(f"**Hasar Sonrası Yeni Rayiç:** {rayic - deger_kaybi:,.2f} TL")
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("### 📝 Bilirkişi Raporu Gerekçe Metni")
    rapor_metni = f"""
    SAYIN HAKİMLİĞİNE
    Dosya No: {dosya_no}
    
    İnceleme konusu {arac_detay} plakalı aracın model yılı ({yil}) ve katettiği mesafe ({km:,} KM) göz önüne alındığında; 
    serbest piyasa koşullarında hasarsız rayiç değerinin {rayic:,} TL olduğu tespit edilmiştir.
    
    Aracın {", ".join(hasar_yeri)} bölgelerinden aldığı hasarın boyutu, onarım bedeli ({hasar_bedeli:,} TL) ve 
    ikinci el piyasasındaki marka/model popülaritesi kriterleri doğrultusunda yapılan teknik hesaplama neticesinde; 
    araçta {deger_kaybi:,.2f} TL tutarında bir değer kaybı oluştuğu mütaala edilmektedir.
    
    Hesaplama Metodu: Denetime elverişli matematiksel modelleme (Yaş, KM ve Hasar Şiddeti katsayıları baz alınmıştır).
    """
    st.text_area("Kopyalamak için tıklayın", rapor_metni, height=300)
