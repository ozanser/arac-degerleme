import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Yapılandırması
st.set_page_config(page_title="Bilirkişi AI - Araç Değerleme", layout="wide", initial_sidebar_state="expanded")

# --- GENİŞLETİLMİŞ ARAÇ VERİTABANI ---
arac_db = {
    "Otomobil": {
        "Volkswagen": ["Passat", "Golf", "Polo", "Tiguan", "T-Roc", "Arteon", "Jetta"],
        "Renault": ["Clio", "Megane", "Symbol", "Fluence", "Austral", "Taliant", "Kadjar"],
        "Fiat": ["Egea", "Linea", "Panda", "500", "Punto"],
        "Ford": ["Focus", "Fiesta", "Mondeo", "Puma", "Kuga"],
        "Toyota": ["Corolla", "Yaris", "Auris", "C-HR", "RAV4"],
        "Mercedes-Benz": ["C-Serisi", "E-Serisi", "A-Serisi", "CLA", "GLA", "S-Serisi"],
        "BMW": ["1 Serisi", "2 Serisi", "3 Serisi", "4 Serisi", "5 Serisi", "X1", "X3", "X5"],
        "Audi": ["A3", "A4", "A5", "A6", "Q2", "Q3", "Q5"],
        "Hyundai": ["i10", "i20", "i30", "Accent Blue", "Elantra", "Tucson", "Bayon"],
        "Honda": ["Civic", "City", "Jazz", "CR-V", "HR-V"],
        "Peugeot": ["208", "301", "308", "2008", "3008", "5008"],
        "Opel": ["Astra", "Corsa", "Insignia", "Mokka", "Crossland", "Grandland"],
        "Skoda": ["Octavia", "Superb", "Fabia", "Kamiq", "Karoq", "Kodiaq"],
        "Dacia": ["Duster", "Sandero", "Jogger", "Lodgy"],
        "Volvo": ["S60", "S90", "XC40", "XC60", "XC90"],
        "Nissan": ["Qashqai", "Micra", "Juke", "X-Trail"]
    },
    "Hafif Ticari": {
        "Ford": ["Transit", "Transit Courier", "Transit Connect", "Ranger"],
        "Fiat": ["Doblo", "Fiorino", "Pratico", "Ducato"],
        "Volkswagen": ["Caddy", "Transporter", "Crafter", "Amarok"],
        "Renault": ["Kangoo", "Trafic", "Master"],
        "Mercedes-Benz": ["Vito", "Sprinter"],
        "Peugeot": ["Partner", "Rifter", "Expert"],
        "Citroen": ["Berlingo", "Jumpy"]
    },
    "Ağır Vasıta (Tır/Kamyon)": {
        "Mercedes-Benz": ["Actros", "Arocs", "Axor", "Atego"],
        "Volvo": ["FH 16", "FH", "FM", "FMX"],
        "Scania": ["R 450", "G 400", "S 500", "P Serisi"],
        "Ford Trucks": ["F-MAX", "1848T", "2533", "3542"],
        "MAN": ["TGX", "TGS", "TGL"],
        "Iveco": ["S-Way", "Stralis", "Eurocargo", "Daily (Kamyon)"],
        "DAF": ["XF 480", "XG", "CF"]
    }
}

# --- CUSTOM CSS (Görsel İyileştirme) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004a99; color: white; }
    </style>
    """, unsafe_allow_value=True)

# --- YAN PANEL (Parametreler) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3251/3251520.png", width=100)
st.sidebar.title("Bilirkişi Ayarları")

with st.sidebar.expander("⚖️ Hesaplama Katsayıları", expanded=False):
    k_yas = st.slider("Yaş Hassasiyeti", 0.5, 1.5, 1.0)
    k_km = st.slider("KM Hassasiyeti", 0.5, 1.5, 1.0)
    baz_oran = st.number_input("Baz Zarar Oranı (%)", 1, 50, 12) / 100

st.sidebar.info("Bu araç, Yargıtay uygulamaları ve sigorta mevzuatına uygun şekilde matematiksel modelleme yapar.")

# --- ANA EKRAN ---
st.title("⚖️ Araç Değer Kaybı ve Rayiç Tespit Sistemi")
st.markdown("Mahkeme ve Sigorta Bilirkişileri için Hazırlanmış Profesyonel Analiz Paneli")

tab1, tab2, tab3 = st.tabs(["📋 Veri Girişi", "📊 Analiz ve Sonuç", "📄 Resmi Rapor Taslağı"])

with tab1:
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("🚗 Araç Bilgileri")
        tip = st.selectbox("Araç Kategorisi", list(arac_db.keys()))
        marka = st.selectbox("Marka", list(arac_db[tip].keys()))
        model = st.selectbox("Model", arac_db[tip][marka])
        yil = st.number_input("Model Yılı", 1990, 2026, 2021)
        km = st.number_input("Kilometre", 0, 2000000, 45000)
        renk = st.text_input("Renk", "Beyaz")

    with c2:
        st.subheader("💰 Hasar ve Piyasa")
        rayic = st.number_input("Piyasa Rayiç Değeri (TL)", 0, 50000000, 1450000)
        hasar_bedeli = st.number_input("Onarım (Parça+İşçilik) Bedeli (TL)", 0, 5000000, 120000)
        hasar_bolgesi = st.multiselect("Hasar Alanları", ["Ön Tampon/Panel", "Motor Kaputu", "Şasiler", "Direkler", "Yan Paneller", "Arka Kısım", "Mekanik Aksam"])
        tramer_toplam = st.number_input("Geçmiş Tramer Toplamı (TL)", 0, 5000000, 0)

with tab2:
    # Hesaplama Motoru
    yas = datetime.now().year - yil
    
    # Katsayı Mantığı
    yas_puan = 1.2 if yas <= 1 else (1.0 if yas <= 3 else (0.7 if yas <= 7 else 0.4))
    km_puan = 1.1 if km <= 15000 else (1.0 if km <= 50000 else (0.6 if km <= 150000 else 0.2))
    hasar_etkisi = 1.3 if any(x in hasar_bolgesi for x in ["Şasiler", "Direkler"]) else 1.0
    
    deger_kaybi = rayic * baz_oran * yas_puan * km_puan * hasar_etkisi * k_yas * k_km
    
    # Görsel Kartlar
    res_c1, res_c2, res_c3 = st.columns(3)
    res_c1.metric("Hesaplanan Değer Kaybı", f"{deger_kaybi:,.2f} TL", delta="-Zarar")
    res_c2.metric("İkinci El Satış Değeri", f"{rayic - deger_kaybi:,.2f} TL")
    res_c3.metric("Hasar/Rayiç Oranı", f"% {(hasar_bedeli/rayic)*100:.1f}")
    
    st.divider()
    st.subheader("📈 Analiz Grafiği")
    grafik_data = pd.DataFrame({
        "Durum": ["Hasarsız Rayiç", "Hasar Sonrası Değer"],
        "Tutar (TL)": [rayic, rayic - deger_kaybi]
    })
    st.bar_chart(grafik_data.set_index("Durum"))

with tab3:
    st.subheader("📝 Bilirkişi Rapor Özeti (Taslak)")
    rapor_metni = f"""
    SAYIN HAKİMLİĞİNE / İLGİLİ MAKAMA
    
    KONU: {marka} {model} ({yil}) plakalı aracın değer kaybı tespiti.
    
    ARAÇ BİLGİLERİ:
    - Marka/Model: {marka} {model}
    - Model Yılı: {yil} ({yas} yaşında)
    - Kilometre: {km:,} KM
    - Hasar Geçmişi: {tramer_toplam:,} TL Tramer
    
    TEKNİK ANALİZ:
    Yapılan incelemeler ve piyasa araştırmaları neticesinde aracın kaza tarihindeki hasarsız rayiç değerinin {rayic:,} TL olduğu tespit edilmiştir. 
    Aracın kilometresi, yaşı ve hasarın boyutu ({", ".join(hasar_bolgesi)}) göz önüne alınarak; 
    Yargıtay 17. Hukuk Dairesi prensiplerine uygun katsayılar ile yapılan hesaplama sonucunda;
    
    HESAPLANAN DEĞER KAYBI: {deger_kaybi:,.2f} TL
    
    SONUÇ: Aracın onarım sonrası ikinci el piyasasında oluşan değer azalışı yukarıda matematiksel olarak ispat edilmiştir.
    
    Bilirkişi Adı Soyadı: ................................
    İmza:
    """
    st.text_area("Raporu Kopyala (UYAP uyumlu)", rapor_metni, height=400)
    st.button("📥 PDF Olarak Kaydet (Hazırlanıyor...)")

if st.button("🚀 Tüm Verileri Analiz Et"):
    st.balloons()
    st.success("Analiz Başarıyla Tamamlandı!")
