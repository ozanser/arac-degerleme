import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları
st.set_page_config(page_title="Bilirkişi Uzman Paneli v3.0", layout="wide")

# Kurumsal Stil
st.markdown("""
    <style>
    .report-title { color: #002b45; border-bottom: 3px solid #002b45; font-weight: bold; margin-bottom: 20px; }
    .stButton>button { background-color: #002b45; color: white; border-radius: 4px; font-weight: bold; width: 100%; height: 3.5em; }
    .calc-box { background-color: #f8f9fa; padding: 20px; border-left: 6px solid #002b45; border-radius: 5px; }
    .hakkaniyet-box { background-color: #fff9f2; padding: 20px; border-left: 6px solid #fd7e14; border-radius: 5px; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

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

# --- BÖLÜM 1: PİYASA ARAŞTIRMASI (3 EMSAL) ---
st.write("### 🔍 1. Piyasa Araştırması (Emsal Karşılaştırma)")
col_e1, col_e2, col_e3 = st.columns([2, 1, 3])

with col_e1:
    e1_f = st.number_input("Emsal 1 Fiyat (TL)", min_value=0, step=10000)
    e2_f = st.number_input("Emsal 2 Fiyat (TL)", min_value=0, step=10000)
    e3_f = st.number_input("Emsal 3 Fiyat (TL)", min_value=0, step=10000)
with col_e2:
    e1_k = st.number_input("Emsal 1 KM/Saat", min_value=0, step=1000)
    e2_k = st.number_input("Emsal 2 KM/Saat", min_value=0, step=1000)
    e3_k = st.number_input("Emsal 3 KM/Saat", min_value=0, step=1000)
with col_e3:
    e1_n = st.text_input("Emsal 1 Kaynak", placeholder="İlan No / Link / Kurum...")
    e2_n = st.text_input("Emsal 2 Kaynak", placeholder="İlan No / Link / Kurum...")
    e3_n = st.text_input("Emsal 3 Kaynak", placeholder="İlan No / Link / Kurum...")

# Rayiç Hesaplama
fiyatlar = [f for f in [e1_f, e2_f, e3_f] if f > 0]
rayic_ort = sum(fiyatlar) / len(fiyatlar) if fiyatlar else 0
st.info(f"📍 **Tespit Edilen Ortalama Rayiç:** {rayic_ort:,.2f} TL")

st.divider()

# --- BÖLÜM 2: GENİŞLETİLMİŞ ARAÇ ANALİZİ ---
st.write("### 🚗 2. Dava Konusu Araç Teknik Detayları")

c1, c2, c3 = st.columns(3)

with c1:
    kat = st.selectbox("Araç Kategorisi", list(arac_yapisi.keys()))
    marka = st.selectbox("Marka", list(arac_yapisi[kat].keys()))
    model = st.selectbox("Model", arac_yapisi[kat][marka])
    # Model yılı 1930'a kadar genişletildi
    yil = st.selectbox("Model Yılı", list(range(2026, 1929, -1)))

with c2:
    km = st.number_input("Kilometre / Çalışma Saati", min_value=0, value=50000)
    # Yakıt Tipi Genişletildi
    yakit = st.selectbox("Yakıt / Enerji Tipi", ["Benzin", "Dizel", "LPG + Benzin", "Hibrit (HEV)", "Plug-in Hibrit (PHEV)", "Tam Elektrikli (BEV)", "Hidrojen", "Elektrik / Dizel"])
    vites = st.selectbox("Şanzıman / Şanzıman Tipi", ["Manuel", "Tam Otomatik", "Yarı Otomatik (DSG/EDC vb.)", "CVT", "4 İleri Otomatik", "9 İleri Otomatik"])

with c3:
    hasar_bolgesi = st.multiselect("Hasar Alanları", ["Ön Kısım", "Arka Kısım", "Yan Paneller", "Tavan", "İç İskelet/Şasi", "Mekanik/Motor", "Elektronik/Sensör"])
    hasar_siddeti = st.selectbox("Hasar Önem Derecesi", 
                                 options=[1.0, 1.3, 1.6, 2.0], 
                                 format_func=lambda x: "Düşük (Plastik/Dış)" if x==1.0 else ("Orta (Sac Aksam)" if x==1.3 else ("Yüksek (İskelet/Şasi)" if x==1.6 else "Ağır/Pert Kayıtlı")))

st.divider()

# --- BÖLÜM 3: HESAPLAMA VE ÇIKTI ---
if st.button("HUKUKİ VE TEKNİK ANALİZİ TAMAMLA"):
    if len(fiyatlar) < 3:
        st.error("Hatalı Rapor Riski: Lütfen en az 3 emsal fiyatını doldurunuz.")
    else:
        # Teknik Katsayılar (Genişletilmiş model)
        current_year = 2026
        yas = current_year - yil
        
        # Yaş Katsayısı (Klasik araçlar için özel düzenleme eklenebilir, şu an standart aşınma)
        yas_k = 1.0 if yas <= 2 else (0.8 if yas <= 5 else (0.5 if yas <= 15 else 0.3))
        
        # KM Katsayısı
        km_k = 1.0 if km <= 20000 else (0.7 if km <= 100000 else (0.4 if km <= 250000 else 0.2))
        
        baz_oran = 0.15 
        teknik_zarar = rayic_ort * baz_oran * yas_k * km_k * hasar_siddeti

        # Sonuç Ekranı
        st.markdown("<div class='calc-box'>", unsafe_allow_html=True)
        st.write("### 📊 Teknik Zarar Tespiti")
        st.write(f"**{yil} {marka} {model}** ({yakit}) için hesaplanan teknik zarar:")
        st.write(f"## {teknik_zarar:,.2f} TL")
        st.latex(rf"DK = {rayic_ort:,.0f} \times {baz_oran} \times {yas_k} \times {km_k} \times {hasar_siddeti} = {teknik_zarar:,.2f} \text{{ TL}}")
        st.markdown("</div>", unsafe_allow_html=True)

        # Hakkaniyet İndirimi
        st.markdown("<div class='hakkaniyet-box'>", unsafe_allow_html=True)
        st.write("### ⚖️ Mahkeme Hakkaniyet İndirimi (TBK 51/52)")
        h1, h2, h3 = st.columns(3)
        h1.metric("%10 İndirim", f"{teknik_zarar*0.9:,.2f} TL")
        h2.metric("%20 İndirim", f"{teknik_zarar*0.8:,.2f} TL")
        h3.metric("%30 İndirim", f"{teknik_zarar*0.7:,.2f} TL")
        st.markdown("</div>", unsafe_allow_html=True)

        # Rapor Metni
        st.write("### 📝 Bilirkişi Rapor Metni")
        rapor = f"""
        İnceleme konusu {yil} model {marka} {model} ({yakit}) plakalı aracın yapılan piyasa araştırmasında; 
        ekte sunulan 3 adet emsal ortalaması olan {rayic_ort:,.2f} TL baz alınmıştır.
        
        Aracın teknik özellikleri, yaşı ({yas}), katettiği mesafe ({km:,} KM/Saat), yakıt tipi ({yakit}) ve 
        hasar aldığı bölgeler ({', '.join(hasar_bolgesi)}) birlikte değerlendirildiğinde; 
        TEKNİK DEĞER KAYBININ {teknik_zarar:,.2f} TL OLDUĞU TESPİT EDİLMİŞTİR.
        
        Hakkaniyet indirimi takdiri Sayın Mahkemenizdedir.
        """
        st.text_area("Kopyala ve UYAP'a Yapıştır", rapor, height=200)
