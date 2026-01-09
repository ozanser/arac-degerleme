import streamlit as st
import pandas as pd

# 1. SAYFA AYARLARI VE KURUMSAL STİL
st.set_page_config(page_title="Bilirkişi Teknik Analiz v11.0", layout="wide")

st.markdown("""
    <style>
    .report-title { color: #002b45; border-bottom: 3px solid #002b45; font-weight: bold; margin-bottom: 20px; }
    .stButton>button { background-color: #002b45; color: white; border-radius: 4px; font-weight: bold; width: 100%; height: 3.5em; }
    .calc-box { background-color: #f8f9fa; padding: 25px; border-left: 6px solid #002b45; border-radius: 5px; }
    .tech-card { background-color: #eef2f7; padding: 15px; border-radius: 8px; border: 1px solid #002b45; }
    .hakkaniyet-box { background-color: #fff9f2; padding: 20px; border-left: 6px solid #fd7e14; border-radius: 5px; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- DİALOG KUTUSU (MODAL) ---
@st.dialog("⚠️ Teknik Veri Uyarısı")
def hata_penceresi(mesaj):
    st.write(f"### {mesaj}")
    st.write("Raporun denetlenebilirliği için tüm zorunlu alanlar doldurulmalıdır.")
    if st.button("Tamam, Düzenliyorum"):
        st.rerun()

# --- MEGA TEKNİK VERİTABANI (2026 GÜNCEL) ---
# Yapı: {Kategori: {Marka: {Model: {Motor_Paket: HP_Degeri}}}}
mega_db = {
    "1. Sınıf: 2 Aks / Aks Mesafesi < 3.20m": {
        "Togg": {
            "T10X": {"V1 RWD Standart": 218, "V2 RWD Uzun": 218, "AWD (4x4)": 435},
            "T10F": {"RWD Standart": 218, "AWD Premium": 435}
        },
        "Tesla": {
            "Model Y": {"Standard RWD": 299, "Long Range AWD": 514, "Performance": 534},
            "Model 3": {"Standard": 283, "Long Range": 498, "Performance": 510}
        },
        "Volkswagen": {
            "Passat": {"1.5 TSI 150HP": 150, "1.6 TDI 120HP": 120, "2.0 TDI 190HP": 190, "1.4 TSI GTE": 218},
            "Golf": {"1.0 TSI 110HP": 110, "1.5 eTSI 150HP": 150, "2.0 GTI": 245, "1.6 TDI 115HP": 115},
            "Tiguan": {"1.5 TSI 150HP": 150, "2.0 TDI 150HP": 150, "1.5 eHybrid": 204}
        },
        "Renault": {
            "Clio": {"1.0 SCe 65HP": 65, "1.0 TCe 90HP": 90, "1.5 dCi 85HP": 85, "1.6 Hybrid 145HP": 145},
            "Megane": {"1.3 TCe 140HP": 140, "1.5 dCi 115HP": 115, "E-Tech (Elektrik)": 220}
        },
        "Fiat": {
            "Egea": {"1.4 Fire 95HP": 95, "1.3 Mjet 95HP": 95, "1.6 Mjet 130HP": 130, "1.5 Hibrit 130HP": 130}
        },
        "Chery": {
            "Tiggo 8 Pro": {"1.6 TGDI 183HP": 183, "PHEV Hibrit": 320},
            "Omoda 5": {"1.6 TGDI 183HP": 183}
        },
        "BMW": {
            "3 Serisi": {"320i 170HP": 170, "330i 258HP": 258, "320d 190HP": 190},
            "5 Serisi": {"520i 170HP": 170, "520d 190HP": 190, "i5 (Elektrik)": 340}
        },
        "Diğer / Özel": {"Manuel Giriş": {"Liste Dışı Araç": 0}}
    },
    "2. Sınıf: 2 Aks / Aks Mesafesi > 3.20m": {
        "Mercedes-Benz": {
            "Sprinter": {"314 CDI": 143, "316 CDI": 163, "319 CDI": 190},
            "Vito": {"114 CDI": 136, "116 CDI": 163, "119 CDI": 190}
        },
        "Ford": {
            "Transit": {"2.0 EcoBlue 170HP": 170, "2.0 EcoBlue 130HP": 130, "E-Transit": 269}
        },
        "Diğer": {"Manuel Giriş": {"Liste Dışı Araç": 0}}
    },
    "3. Sınıf: 3 Akslı Araçlar": {
        "Mercedes-Benz": {
            "Actros": {"1845 LS": 449, "1848 LS": 476, "1851 LS": 510},
            "Axor": {"1840 LS": 401, "3240 Kamyon": 401}
        },
        "Volvo": {
            "FH": {"FH 460": 460, "FH 500": 500, "FH 540": 540}
        },
        "Diğer": {"Manuel Giriş": {"Liste Dışı Araç": 0}}
    },
    "6. Sınıf: Motosiklet": {
        "Honda": {"Africa Twin": {"1100L": 102}, "Forza": {"250": 23, "750": 58}},
        "Yamaha": {"MT-07": {"689cc": 73}, "Tracer 9": {"GT": 119}},
        "Diğer": {"Manuel Giriş": {"Liste Dışı Araç": 0}}
    }
}

st.markdown("<h2 class='report-title'>⚖️ Bilirkişi Değerleme ve Teknik Veri İstasyonu v11.0</h2>", unsafe_allow_html=True)

# --- BÖLÜM 1: PİYASA ARAŞTIRMASI ---
st.write("### 🔍 1. Piyasa Araştırması (3 Emsal)")
col_e1, col_e2, col_e3 = st.columns([2, 1, 3])
with col_e1:
    e1_f = st.number_input("Emsal 1 Fiyat (TL)", min_value=0, step=10000)
    e2_f = st.number_input("Emsal 2 Fiyat (TL)", min_value=0, step=10000)
    e3_f = st.number_input("Emsal 3 Fiyat (TL)", min_value=0, step=10000)
with col_e2:
    e1_k = st.number_input("Emsal 1 KM", min_value=0)
    e2_k = st.number_input("Emsal 2 KM", min_value=0)
    e3_k = st.number_input("Emsal 3 KM", min_value=0)
with col_e3:
    e1_n = st.text_input("Emsal 1 Not/Kaynak", placeholder="İlan Linki / Kurum...")
    e2_n = st.text_input("Emsal 2 Not/Kaynak", placeholder="İlan Linki / Kurum...")
    e3_n = st.text_input("Emsal 3 Not/Kaynak", placeholder="İlan Linki / Kurum...")

fiyatlar = [f for f in [e1_f, e2_f, e3_f] if f > 0]
rayic_ort = sum(fiyatlar) / len(fiyatlar) if fiyatlar else 0

st.divider()

# --- BÖLÜM 2: TEKNİK ARAÇ KÜNYESİ VE OTOMATİK HP ---
st.write("### 🚗 2. Araç Sınıfı ve Teknik Detaylar")
c1, c2, c3 = st.columns(3)

with c1:
    kat = st.selectbox("Aks / Dingil Sınıfı", list(mega_db.keys()))
    marka = st.selectbox("Marka", list(mega_db[kat].keys()))
    model = st.selectbox("Model / Seri", list(mega_db[kat][marka].keys()))
    motor_segment = st.selectbox("Motor / Alt Segment (Paket)", list(mega_db[kat][marka][model].keys()))
    
    # Otomatik HP Değerini Çekme
    otomatik_hp = mega_db[kat][marka][model][motor_segment]
    
    if motor_segment == "Liste Dışı Araç":
        manuel_marka = st.text_input("Marka/Model Yazınız")
        manuel_hp = st.number_input("Manuel Beygir Gücü (HP)", value=100)
    else:
        beygir = st.number_input("Motor Gücü (HP) - Otomatik Güncellenir", value=otomatik_hp)

with c2:
    yil = st.selectbox("Model Yılı", list(range(2026, 1929, -1)))
    km = st.number_input("Mevcut Kilometre / Saat", min_value=0, value=50000)
    yakit = st.selectbox("Enerji Tipi", ["Benzin", "Dizel", "Elektrikli (BEV)", "Hibrit", "LPG", "Hidrojen"])
    vites = st.selectbox("Şanzıman", ["Otomatik", "Manuel", "Yarı Otomatik", "CVT"])

with c3:
    st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
    h_derece = st.selectbox("Hasar Şiddeti", options=[1.0, 1.4, 1.9, 2.8], format_func=lambda x: "Hafif" if x==1.0 else ("Orta" if x==1.4 else ("Yüksek" if x==1.9 else "Ağır/Kritik")))
    h_alanlari = st.multiselect("Hasarlı Bölgeler", ["Ön", "Arka", "Yanlar", "Şasi/Dingil", "Tavan", "Direkler", "Hava Yastığı", "Mekanik"])
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- BÖLÜM 3: HESAPLAMA VE SONUÇ ---
if st.button("TEKNİK ANALİZİ TAMAMLA VE RAPORU HAZIRLA"):
    if len(fiyatlar) < 3:
        hata_penceresi("Piyasa tespiti için en az 3 emsal fiyat girişi şarttır.")
    elif not h_alanlari:
        hata_penceresi("Lütfen en az bir hasarlı bölge seçimi yapınız.")
    else:
        # Teknik Katsayı Hesaplama
        yas = 2026 - yil
        yas_k = 1.0 if yas <= 2 else (0.75 if yas <= 6 else (0.45 if yas <= 15 else 0.25))
        km_k = 1.0 if km <= 25000 else (0.65 if km <= 110000 else 0.35)
        
        # Kritik Hasar Çarpanı (Kritik bölgeler seçilirse)
        kritik_c = 1.35 if any(x in h_alanlari for x in ["Şasi/Dingil", "Direkler", "Tavan", "Hava Yastığı"]) else 1.0
        
        teknik_zarar = rayic_ort * 0.15 * yas_k * km_k * h_derece * kritik_c

        # SONUÇ EKRANI
        st.markdown("<div class='calc-box'>", unsafe_allow_html=True)
        st.write(f"### 📊 Teknik Zarar Tespiti")
        st.write(f"**Araç:** {yil} {marka if motor_segment != 'Liste Dışı Araç' else manuel_marka} {model} ({motor_segment})")
        st.write(f"## {teknik_zarar:,.2f} TL")
        st.latex(rf"DK = {rayic_ort:,.0f} \times 0.15 \times {yas_k} \times {km_k} \times {h_derece} \times {kritik_c} = {teknik_zarar:,.2f} \text{{ TL}}")
        st.markdown("</div>", unsafe_allow_html=True)

        # HAKKANİYET İNDİRİMİ
        st.markdown("<div class='hakkaniyet-box'>", unsafe_allow_html=True)
        st.write("### ⚖️ Mahkeme Hakkaniyet İndirimi (TBK 51/52)")
        res1, res2, res3 = st.columns(3)
        res1.metric("%10 İndirim", f"{teknik_zarar*0.9:,.2f} TL")
        res2.metric("%20 İndirim", f"{teknik_zarar*0.8:,.2f} TL")
        res3.metric("%30 İndirim", f"{teknik_zarar*0.7:,.2f} TL")
        st.markdown("</div>", unsafe_allow_html=True)

        # RAPOR TASLAĞI
        st.write("### 📝 Bilirkişi Rapor Metni")
        rapor = f"""
        Dosya konusu {kat} sınıfına giren {yil} model {marka} {model} ({motor_segment}) 
        plakalı aracın yapılan piyasa araştırmasında; 3 adet emsal ortalaması olan 
        {rayic_ort:,.2f} TL hasarsız rayiç değeri olarak kabul edilmiştir.
        
        TEKNİK ANALİZ:
        Aracın teknik özellikleri ({beygir if motor_segment != 'Liste Dışı Araç' else manuel_hp} HP), kilometresi ({km:,}), 
        hasar aldığı kritik bölgeler ({', '.join(h_alanlari)}) ve hasar şiddeti birlikte değerlendirildiğinde; 
        teknik yıpranma payları neticesinde TEKNİK DEĞER KAYBININ {teknik_zarar:,.2f} TL olduğu saptanmıştır.
        
        TBK 51-52 uyarınca hakkaniyet indirimi takdiri Sayın Mahkemenizdedir.
        """
        st.text_area("Metni Kopyala", rapor, height=250)
