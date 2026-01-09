import streamlit as st
import pandas as pd

# 1. Sayfa Standartları
st.set_page_config(page_title="Bilirkişi Analiz Sistemi", layout="wide")

# Kurumsal ve Temiz Stil
st.markdown("""
    <style>
    .report-title { color: #002b45; border-bottom: 3px solid #002b45; font-weight: bold; margin-bottom: 20px; }
    .stButton>button { background-color: #002b45; color: white; border-radius: 4px; font-weight: bold; width: 100%; height: 3.5em; }
    .calc-box { background-color: #f8f9fa; padding: 20px; border-left: 6px solid #002b45; border-radius: 5px; }
    .hakkaniyet-box { background-color: #fff9f2; padding: 20px; border-left: 6px solid #fd7e14; border-radius: 5px; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİTABANI (Dinamik Menüler İçin) ---
# Not: Bu liste en yaygın araçları kapsar, manuel metin girişini engellemek için yapılandırılmıştır.
arac_yapisi = {
    "Otomobil": {
        "Volkswagen": ["Passat", "Golf", "Polo", "Tiguan", "Jetta"],
        "Renault": ["Clio", "Megane", "Symbol", "Fluence", "Austral"],
        "Fiat": ["Egea", "Linea", "Panda", "500"],
        "Toyota": ["Corolla", "Yaris", "Auris", "C-HR"],
        "Mercedes-Benz": ["C-Serisi", "E-Serisi", "A-Serisi", "CLA"],
        "BMW": ["3 Serisi", "5 Serisi", "1 Serisi", "X5"],
        "Hyundai": ["i20", "i30", "Accent Blue", "Tucson"]
    },
    "Hafif Ticari": {
        "Ford": ["Transit", "Transit Courier", "Connect"],
        "Fiat": ["Doblo", "Fiorino", "Ducato"],
        "Volkswagen": ["Caddy", "Transporter", "Crafter"]
    },
    "Ağır Vasıta (Tır/Kamyon)": {
        "Mercedes-Benz": ["Actros", "Axor", "Atego"],
        "Volvo": ["FH 16", "FH", "FM"],
        "Scania": ["R 450", "G 400", "S 500"],
        "Ford Trucks": ["F-MAX", "1848T"]
    }
}

st.markdown("<h2 class='report-title'>⚖️ Bilirkişi Araç Değer Kaybı Analiz Paneli</h2>", unsafe_allow_html=True)

# --- BÖLÜM 1: PİYASA ARAŞTIRMASI (3 EMSAL) ---
st.write("### 🔍 1. Piyasa Araştırması (Emsal Karşılaştırma)")
col_e1, col_e2, col_e3 = st.columns([2, 1, 3])

with col_e1:
    e1_f = st.number_input("Emsal 1 Fiyat (TL)", min_value=0, step=10000)
    e2_f = st.number_input("Emsal 2 Fiyat (TL)", min_value=0, step=10000)
    e3_f = st.number_input("Emsal 3 Fiyat (TL)", min_value=0, step=10000)
with col_e2:
    e1_k = st.number_input("Emsal 1 KM", min_value=0, step=1000)
    e2_k = st.number_input("Emsal 2 KM", min_value=0, step=1000)
    e3_k = st.number_input("Emsal 3 KM", min_value=0, step=1000)
with col_e3:
    e1_n = st.text_input("Emsal 1 Kaynak", placeholder="İlan Linki / Galeri...")
    e2_n = st.text_input("Emsal 2 Kaynak", placeholder="İlan Linki / Galeri...")
    e3_n = st.text_input("Emsal 3 Kaynak", placeholder="İlan Linki / Galeri...")

# Rayiç Hesaplama
fiyatlar = [f for f in [e1_f, e2_f, e3_f] if f > 0]
rayic_ort = sum(fiyatlar) / len(fiyatlar) if fiyatlar else 0
st.info(f"📍 **Tespit Edilen Ortalama Rayiç:** {rayic_ort:,.2f} TL")

st.divider()

# --- BÖLÜM 2: DAVA KONUSU ARAÇ ANALİZİ (MENÜLER) ---
st.write("### 🚗 2. Dava Konusu Araç ve Hasar Analizi")

c1, c2, c3 = st.columns(3)

with c1:
    # Hiyerarşik Seçim
    kat = st.selectbox("Araç Kategorisi", list(arac_yapisi.keys()))
    marka = st.selectbox("Marka", list(arac_yapisi[kat].keys()))
    model = st.selectbox("Model", arac_yapisi[kat][marka])

with c2:
    # Liste Halinde Yıl ve KM
    yil = st.selectbox("Model Yılı", list(range(2026, 1999, -1)))
    km = st.number_input("Aracın Kilometresi", min_value=0, value=50000)
    vites = st.selectbox("Şanzıman Tipi", ["Manuel", "Otomatik", "Yarı Otomatik"])

with c3:
    # Hasar Bölgesi ve Şiddeti
    hasar_bolgesi = st.multiselect("Hasar Alanları", ["Ön Kısım", "Arka Kısım", "Yan Paneller", "Tavan", "İç İskelet/Şasi"])
    hasar_siddeti = st.selectbox("Hasar Önem Derecesi", 
                                 options=[1.0, 1.3, 1.6], 
                                 format_func=lambda x: "Düşük (Plastik/Dış Parça)" if x==1.0 else ("Orta (Sac Aksam)" if x==1.3 else "Yüksek (Taşıyıcı İskelet)"))

st.divider()

# --- BÖLÜM 3: HESAPLAMA VE ÇIKTI ---
if st.button("ANALİZİ TAMAMLA VE TEKNİK RAPORU HAZIRLA"):
    if len(fiyatlar) < 3:
        st.error("Lütfen sağlıklı bir analiz için 3 emsal fiyatını da doldurunuz.")
    else:
        # Teknik Katsayılar (Matematiksel Model)
        yas_k = 1.0 if (2026-yil) <= 2 else (0.7 if (2026-yil) <= 6 else 0.4)
        km_k = 1.0 if km <= 25000 else (0.6 if km <= 110000 else 0.3)
        baz_oran = 0.15 # %15 Baz Değer Kaybı Oranı
        
        teknik_zarar = rayic_ort * baz_oran * yas_k * km_k * hasar_siddeti

        # Sonuç Ekranı
        st.markdown("<div class='calc-box'>", unsafe_allow_html=True)
        st.write("### 📊 Teknik Zarar Tespiti")
        st.write(f"İncelenen **{yil} {marka} {model}** marka araçta tespit edilen çıplak teknik zarar:")
        st.write(f"## {teknik_zarar:,.2f} TL")
        st.latex(rf"DK = {rayic_ort:,.0f} \times {baz_oran} \times {yas_k} \times {km_k} \times {hasar_siddeti} = {teknik_zarar:,.2f} \text{{ TL}}")
        st.markdown("</div>", unsafe_allow_html=True)

        # Hakkaniyet İndirimi Paneli
        st.markdown("<div class='hakkaniyet-box'>", unsafe_allow_html=True)
        st.write("### ⚖️ Mahkeme Hakkaniyet İndirimi (TBK 51/52)")
        st.caption("Hakimin takdir edebileceği olası indirimli sonuçlar:")
        h1, h2, h3 = st.columns(3)
        h1.metric("%10 İndirim", f"{teknik_zarar*0.9:,.2f} TL")
        h2.metric("%20 İndirim", f"{teknik_zarar*0.8:,.2f} TL")
        h3.metric("%30 İndirim", f"{teknik_zarar*0.7:,.2f} TL")
        st.markdown("</div>", unsafe_allow_html=True)

        # Rapor Metni
        st.write("### 📝 Bilirkişi Rapor Metni")
        rapor = f"""
        Dosya konusu {yil} model {marka} {model} ({km:,} KM) plakalı aracın yapılan piyasa araştırmasında; 
        ekte sunulan 3 adet emsal ilan ortalaması olan {rayic_ort:,.2f} TL baz alınmıştır.
        
        Aracın teknik özellikleri, yaşı, kilometresi ve hasar aldığı bölgeler ({', '.join(hasar_bolgesi)}) 
        birlikte değerlendirildiğinde; TEKNİK DEĞER KAYBININ {teknik_zarar:,.2f} TL OLDUĞU TESPİT EDİLMİŞTİR.
        
        Hakkaniyet indirimi takdiri Sayın Mahkemenizdedir.
        """
        st.text_area("Kopyala ve UYAP'a Yapıştır", rapor, height=200)
