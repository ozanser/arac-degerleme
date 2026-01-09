import streamlit as st
import pandas as pd

# 1. SAYFA AYARLARI VE KURUMSAL STİL
st.set_page_config(page_title="Bilirkişi Uzman Paneli v3.0", layout="wide")

st.markdown("""
    <style>
    .report-title { color: #002b45; border-bottom: 3px solid #002b45; font-weight: bold; margin-bottom: 20px; }
    .stButton>button { background-color: #002b45; color: white; border-radius: 4px; font-weight: bold; width: 100%; height: 3.5em; }
    .calc-box { background-color: #f8f9fa; padding: 20px; border-left: 6px solid #002b45; border-radius: 5px; }
    .hakkaniyet-box { background-color: #fff9f2; padding: 20px; border-left: 6px solid #fd7e14; border-radius: 5px; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- DİALOG KUTUSU (MODAL) FONKSİYONU ---
@st.dialog("⚠️ Eksik veya Hatalı Bilgi")
def hata_penceresi(mesaj):
    st.write(f"### {mesaj}")
    st.write("Raporun hukuki geçerliliği ve denetlenebilirliği için bu alanların eksiksiz doldurulması zorunludur.")
    if st.button("Tamam, Anladım"):
        st.rerun()

# --- DEV ARAÇ VERİTABANI ---
arac_yapisi = {
    "Otomobil": {
        "Volkswagen": ["Passat", "Golf", "Polo", "Tiguan", "T-Roc", "Arteon", "Jetta", "Scirocco", "Beetle", "Touareg"],
        "Renault": ["Clio", "Megane", "Austral", "Taliant", "Zoe", "Captur", "Kadjar", "Fluence", "Symbol", "Koleos"],
        "Fiat": ["Egea", "Linea", "500", "500X", "Panda", "Punto", "Bravo", "Albea", "Palio", "Uno"],
        "Toyota": ["Corolla", "Yaris", "C-HR", "RAV4", "Hilux", "Auris", "Avensis", "Camry", "Land Cruiser", "Supra"],
        "Mercedes-Benz": ["C-Serisi", "E-Serisi", "A-Serisi", "S-Serisi", "CLA", "CLS", "GLA", "GLC", "GLE", "EQS"],
        "BMW": ["1 Serisi", "2 Serisi", "3 Serisi", "4 Serisi", "5 Serisi", "7 Serisi", "X1", "X3", "X5", "X7", "i4", "iX"],
        "Audi": ["A1", "A3", "A4", "A5", "A6", "A8", "Q2", "Q3", "Q5", "Q7", "e-tron"],
        "Hyundai": ["i10", "i20", "i30", "Elantra", "Accent Blue", "Tucson", "Santa Fe", "Bayon", "Kona", "IONIQ 5"],
        "Honda": ["Civic", "City", "Jazz", "CR-V", "HR-V", "Accord", "NSX"],
        "Peugeot": ["208", "308", "408", "508", "2008", "3008", "5008", "301", "206", "407"],
        "Opel": ["Corsa", "Astra", "Insignia", "Mokka", "Crossland", "Grandland", "Combo", "Adam"],
        "Skoda": ["Fabia", "Scala", "Octavia", "Superb", "Kamiq", "Karoq", "Kodiaq"],
        "Ford": ["Fiesta", "Focus", "Mondeo", "Puma", "Kuga", "Mustang", "Mustang Mach-E"],
        "Dacia": ["Sandero", "Duster", "Jogger", "Lodgy", "Logan", "Spring"]
    },
    "Hafif Ticari": {
        "Ford": ["Transit Courier", "Transit Connect", "Transit Custom", "Transit Van", "Ranger"],
        "Fiat": ["Doblo", "Fiorino", "Pratico", "Ducato", "Scudo"],
        "Volkswagen": ["Caddy", "Transporter", "Caravelle", "Crafter", "Amarok"],
        "Mercedes-Benz": ["Vito", "Sprinter", "X-Class", "Citan"],
        "Renault": ["Kangoo", "Express", "Trafic", "Master"],
        "Peugeot": ["Partner", "Rifter", "Expert", "Boxer"],
        "Citroen": ["Berlingo", "Jumpy", "Jumper"]
    },
    "Ağır Vasıta (Tır/Kamyon)": {
        "Mercedes-Benz": ["Actros", "Arocs", "Axor", "Atego"],
        "Volvo": ["FH 16", "FH", "FM", "FMX", "FE", "FL"],
        "Scania": ["R Serisi", "S Serisi", "G Serisi", "P Serisi", "L Serisi"],
        "Ford Trucks": ["F-MAX", "Çekici Serisi", "Yol Serisi", "İnşaat Serisi"],
        "MAN": ["TGX", "TGS", "TGM", "TGL"],
        "Iveco": ["S-Way", "Stralis", "Eurocargo", "Trakker", "Daily (Kamyon)"],
        "DAF": ["XF", "XG", "XG+", "CF", "LF"]
    },
    "Motosiklet": {
        "Honda": ["Africa Twin", "Gold Wing", "CB500F", "Forza 250", "PCX 125", "CBR650R"],
        "Yamaha": ["MT-07", "MT-09", "Tracer 9", "R25", "XMAX 250", "NMAX 125"],
        "BMW": ["R 1250 GS", "S 1000 RR", "F 850 GS", "G 310 R", "C 400 GT"],
        "Kawasaki": ["Ninja H2", "Z900", "Versys 650", "Vulcan S"],
        "Harley-Davidson": ["Fat Boy", "Iron 883", "Pan America", "Street Glide"]
    },
    "İş Makinesi / Tarım": {
        "Hidromek": ["HMK 102 B", "HMK 230 LC", "HMK 600 MG"],
        "JCB": ["3CX", "4CX", "531-70", "JS220"],
        "Caterpillar": ["428F2", "320 GC", "950 GC", "D6"],
        "New Holland": ["TD5.110", "TR6.120", "TT4.75"],
        "John Deere": ["5075E", "6120M", "8R 410"]
    }
}

st.markdown("<h2 class='report-title'>⚖️ Bilirkişi Araç Değer Kaybı Analiz Paneli v3.0</h2>", unsafe_allow_html=True)

# --- BÖLÜM 1: PİYASA ARAŞTIRMASI ---
st.write("### 🔍 1. Piyasa Araştırması (Emsal Karşılaştırma)")
col_e1, col_e2, col_e3 = st.columns([2, 1, 3])

with col_e1:
    e1_f = st.number_input("Emsal 1 Fiyat (TL)", min_value=0, step=5000)
    e2_f = st.number_input("Emsal 2 Fiyat (TL)", min_value=0, step=5000)
    e3_f = st.number_input("Emsal 3 Fiyat (TL)", min_value=0, step=5000)
with col_e2:
    e1_k = st.number_input("Emsal 1 KM/Saat", min_value=0)
    e2_k = st.number_input("Emsal 2 KM/Saat", min_value=0)
    e3_k = st.number_input("Emsal 3 KM/Saat", min_value=0)
with col_e3:
    e1_n = st.text_input("Emsal 1 Not/Link", placeholder="İlan No / Link / Kurum...")
    e2_n = st.text_input("Emsal 2 Not/Link", placeholder="İlan No / Link / Kurum...")
    e3_n = st.text_input("Emsal 3 Not/Link", placeholder="İlan No / Link / Kurum...")

fiyatlar = [f for f in [e1_f, e2_f, e3_f] if f > 0]
rayic_ort = sum(fiyatlar) / len(fiyatlar) if fiyatlar else 0

st.divider()

# --- BÖLÜM 2: DAVA KONUSU ARAÇ ANALİZİ ---
st.write("### 🚗 2. Dava Konusu Araç Teknik Detayları")
c1, c2, c3 = st.columns(3)

with c1:
    kat = st.selectbox("Araç Kategorisi", list(arac_yapisi.keys()))
    marka = st.selectbox("Marka", list(arac_yapisi[kat].keys()))
    model = st.selectbox("Model", arac_yapisi[kat][marka])
    yil = st.selectbox("Model Yılı", list(range(2026, 1929, -1)))

with c2:
    km = st.number_input("Kilometre / Çalışma Saati", min_value=0, value=50000)
    yakit = st.selectbox("Yakıt / Enerji Tipi", ["Benzin", "Dizel", "LPG + Benzin", "Tam Elektrikli (BEV)", "Hibrit", "Diğer"])
    vites = st.selectbox("Şanzıman Tipi", ["Manuel", "Tam Otomatik", "Yarı Otomatik", "CVT"])

with c3:
    hasar_bolgesi = st.multiselect("Hasar Alanları", ["Ön Kısım", "Arka Kısım", "Yan Paneller", "Tavan", "Şasi/İskelet", "Mekanik"])
    hasar_siddeti = st.selectbox("Hasar Önem Derecesi", options=[1.0, 1.3, 1.6], format_func=lambda x: "Düşük (Plastik)" if x==1.0 else ("Orta (Sac)" if x==1.3 else "Yüksek (İskelet)"))

st.divider()

# --- BÖLÜM 3: HESAPLAMA VE DİALOG KONTROLÜ ---
if st.button("HUKUKİ VE TEKNİK ANALİZİ TAMAMLA"):
    # HATA KONTROLLERİ (Ekranın ortasında açılır)
    if len(fiyatlar) < 3:
        hata_penceresi("Piyasa rayiç tespiti için en az 3 adet emsal fiyat girişi yapılması zorunludur.")
    elif not hasar_bolgesi:
        hata_penceresi("Hesaplama yapılabilmesi için en az bir hasarlı bölge seçilmelidir.")
    elif rayic_ort == 0:
        hata_penceresi("Emsal fiyatların ortalaması 0 olamaz. Lütfen geçerli tutarlar giriniz.")
    else:
        # TEKNİK HESAPLAMA MANTIĞI
        yas_k = 1.0 if (2026-yil) <= 2 else (0.7 if (2026-yil) <= 7 else 0.4)
        km_k = 1.0 if km <= 25000 else (0.6 if km <= 120000 else 0.3)
        teknik_zarar = rayic_ort * 0.15 * yas_k * km_k * hasar_siddeti

        # SONUÇ GÖSTERİMİ
        st.markdown("<div class='calc-box'>", unsafe_allow_html=True)
        st.write(f"### 📊 Teknik Zarar: {teknik_zarar:,.2f} TL")
        st.latex(rf"DK = {rayic_ort:,.0f} \times 0.15 \times {yas_k} \times {km_k} \times {hasar_siddeti} = {teknik_zarar:,.2f} \text{{ TL}}")
        st.markdown("</div>", unsafe_allow_html=True)

        # HAKKANİYET İNDİRİMİ
        st.markdown("<div class='hakkaniyet-box'>", unsafe_allow_html=True)
        st.write("### ⚖️ Olası Hakkaniyet İndirimleri (TBK 51/52)")
        h1, h2, h3 = st.columns(3)
        h1.metric("%10 İndirim", f"{teknik_zarar*0.9:,.2f} TL")
        h2.metric("%20 İndirim", f"{teknik_zarar*0.8:,.2f} TL")
        h3.metric("%30 İndirim", f"{teknik_zarar*0.7:,.2f} TL")
        st.markdown("</div>", unsafe_allow_html=True)

        # RAPOR TASLAĞI
        st.write("### 📝 Bilirkişi Rapor Metni")
        rapor = f"""
        Dosya konusu {yil} model {marka} {model} ({yakit}) plakalı aracın piyasa araştırmasında; 
        ekte sunulan 3 adet emsal ortalaması olan {rayic_ort:,.2f} TL baz alınmıştır.
        
        Aracın teknik özellikleri, yaşı, kilometresi ve hasar aldığı bölgeler ({', '.join(hasar_bolgesi)}) 
        birlikte değerlendirildiğinde; TEKNİK DEĞER KAYBININ {teknik_zarar:,.2f} TL OLDUĞU TESPİT EDİLMİŞTİR.
        
        TBK 51-52 uyarınca hakkaniyet indirimi takdiri Sayın Mahkemenizdedir.
        """
        st.text_area("Metni Kopyala", rapor, height=200)
