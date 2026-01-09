import streamlit as st
import pandas as pd

# 1. SAYFA AYARLARI VE KURUMSAL STİL
st.set_page_config(page_title="Bilirkişi Teknik Analiz v13.0", layout="wide")

st.markdown("""
    <style>
    .report-title { color: #002b45; border-bottom: 3px solid #002b45; font-weight: bold; margin-bottom: 20px; }
    .stButton>button { background-color: #002b45; color: white; border-radius: 4px; font-weight: bold; width: 100%; height: 3.5em; }
    .calc-box { background-color: #f8f9fa; padding: 25px; border-left: 6px solid #002b45; border-radius: 5px; }
    .method-box { background-color: #eef2f7; padding: 15px; border-radius: 8px; border: 1px solid #002b45; }
    </style>
    """, unsafe_allow_html=True)

# --- DİALOG KUTUSU (MODAL) ---
@st.dialog("⚠️ Veri Giriş Hatası")
def hata_penceresi(mesaj):
    st.write(f"### {mesaj}")
    st.write("Hesaplamanın ispatlanabilir olması için tüm alanlar doldurulmalıdır.")
    if st.button("Tamam, Düzenliyorum"):
        st.rerun()

# --- MEGA TEKNİK VERİTABANI (2026 GÜNCEL) ---
mega_db = {
    "1. Sınıf: 2 Aks / < 3.20m": {
        "Togg": {"T10X": {"V1 RWD": 218, "V2 RWD": 218, "AWD": 435}, "T10F": {"Standard": 218, "Premium": 435}},
        "Tesla": {"Model Y": {"RWD": 299, "Long Range": 514, "Performance": 534}, "Model 3": {"Standard": 283, "Performance": 510}},
        "Volkswagen": {"Passat": {"1.5 TSI": 150, "1.6 TDI": 120, "2.0 TDI": 190}, "Golf": {"1.0 TSI": 110, "1.5 eTSI": 150}},
        "Renault": {"Clio": {"1.0 TCe": 90, "1.5 dCi": 85}, "Megane": {"1.3 TCe": 140, "1.5 dCi": 115}},
        "Fiat": {"Egea": {"1.4 Fire": 95, "1.3 Mjet": 95, "1.6 Mjet": 130}},
        "Diğer": {"Manuel Giriş": {"Liste Dışı": 100}}
    },
    "2. Sınıf: 2 Aks / > 3.20m": {"Ford": {"Transit": {"2.0 EcoBlue": 170}}, "Mercedes-Benz": {"Sprinter": {"316 CDI": 163}}, "Diğer": {"Manuel": {"Liste Dışı": 0}}},
    "3. Sınıf: 3 Akslı Araçlar": {"Mercedes-Benz": {"Actros": {"1845 LS": 449}}, "Volvo": {"FH": {"FH 500": 500}}, "Diğer": {"Manuel": {"Liste Dışı": 0}}},
    "6. Sınıf: Motosiklet": {"Honda": {"Africa Twin": {"1100L": 102}}, "Yamaha": {"MT-07": {"689cc": 73}}, "Diğer": {"Manuel": {"Liste Dışı": 0}}}
}

st.markdown("<h2 class='report-title'>⚖️ Denetime Elverişli Bilirkişi Raporlama İstasyonu</h2>", unsafe_allow_html=True)

# --- BÖLÜM 1: PİYASA ARAŞTIRMASI ---
st.write("### 🔍 1. Piyasa Araştırması (Emsal Metodu)")
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
    e1_n = st.text_input("Emsal 1 Kaynak", "Sahibinden.com İlan No: ...")
    e2_n = st.text_input("Emsal 2 Kaynak", "Arabam.com İlan No: ...")
    e3_n = st.text_input("Emsal 3 Kaynak", "Piyasa Araştırması / Galeri")

fiyatlar = [f for f in [e1_f, e2_f, e3_f] if f > 0]
rayic_ort = sum(fiyatlar) / len(fiyatlar) if fiyatlar else 0

st.divider()

# --- BÖLÜM 2: TEKNİK ARAÇ KÜNYESİ ---
st.write("### 🚗 2. Araç ve Hasar Parametreleri")
c1, c2, c3 = st.columns(3)

with c1:
    kat = st.selectbox("Aks Sınıfı", list(mega_db.keys()))
    marka = st.selectbox("Marka", list(mega_db[kat].keys()))
    model = st.selectbox("Model", list(mega_db[kat][marka].keys()))
    motor_p = st.selectbox("Motor/Paket", list(mega_db[kat][marka][model].keys()))
    otomatik_hp = mega_db[kat][marka][model][motor_p]

with c2:
    yil = st.selectbox("Model Yılı", list(range(2026, 1929, -1)))
    km = st.number_input("Mevcut Kilometre", min_value=0, value=50000)
    yakit = st.selectbox("Yakıt", ["Benzin", "Dizel", "Elektrikli", "Hibrit", "LPG"])
    beygir = st.number_input("Motor Gücü (HP)", value=otomatik_hp)

with c3:
    h_derece = st.selectbox("Hasar Şiddeti", options=[1.0, 1.4, 1.9, 2.8], format_func=lambda x: "Hafif" if x==1.0 else ("Orta" if x==1.4 else ("Yüksek" if x==1.9 else "Ağır/Kritik")))
    h_alanlari = st.multiselect("Hasarlı Bölgeler", ["Ön", "Arka", "Yanlar", "Şasi", "Direkler", "Tavan", "Airbag", "Mekanik"])

st.divider()

# --- BÖLÜM 3: HESAPLAMA VE İSPATLI RAPOR ---
if st.button("ANALİZİ TAMAMLA VE İSPATLI RAPORU OLUŞTUR"):
    if len(fiyatlar) < 3:
        hata_penceresi("Rapor güvenliği için 3 adet emsal fiyat zorunludur.")
    elif not h_alanlari:
        hata_penceresi("Lütfen hasarlı bölge seçimi yapınız.")
    else:
        # Katsayı Belirleme
        yas = 2026 - yil
        yas_k = 1.0 if yas <= 2 else (0.75 if yas <= 6 else (0.45 if yas <= 15 else 0.25))
        km_k = 1.0 if km <= 25000 else (0.65 if km <= 110000 else 0.35)
        k_bonus = 1.35 if any(x in h_alanlari for x in ["Şasi", "Direkler", "Tavan", "Airbag"]) else 1.0
        baz_oran = 0.15 # Standart Değer Kaybı Oranı
        
        # Matematiksel Sonuç
        teknik_zarar = rayic_ort * baz_oran * yas_k * km_k * h_derece * k_bonus

        # 1. ANALİZ ÖZETİ (GEREKÇELENDİRME)
        st.markdown("<div class='calc-box'>", unsafe_allow_html=True)
        st.write("### 📊 Hesaplama Gerekçesi")
        st.write(f"- **Piyasa Rayiç Değeri:** {rayic_ort:,.2f} TL")
        st.write(f"- **Hesaplama Formülü:** $DK = Rayiç \times Oran \times Y_k \times KM_k \times H_d \times K_{{bonus}}$")
        st.write(f"- **Gerçek Rakamlarla İspat:** ${rayic_ort:,.0f} \\times {baz_oran} \\times {yas_k} \\times {km_k} \\times {h_derece} \\times {k_bonus} = {teknik_zarar:,.2f}$")
        st.markdown("</div>", unsafe_allow_html=True)

        st.divider()

        # 2. NİHAİ RAPOR (KOPYALANABİLİR)
        st.write("### 📝 Nihai Bilirkişi Raporu")
        st.caption("Aşağıdaki metni kopyalayarak UYAP veya Word dökümanınıza yapıştırabilirsiniz.")
        
        rapor_metni = f"""SAYIN HAKİMLİĞİNE

ARAÇ: {yil} Model {marka} {model} ({motor_p}, {beygir} HP)

PİYASA ARAŞTIRMASI:
Yapılan tetkiklerde, kaza tarihi itibarıyla benzer özelliklerdeki şu emsaller saptanmıştır:
1. {e1_f:,.0f} TL ({e1_n})
2. {e2_f:,.0f} TL ({e2_n})
3. {e3_f:,.0f} TL ({e3_n})
Emsallerin ortalaması olan {rayic_ort:,.2f} TL, hasarsız rayiç değeri olarak kabul edilmiştir.

MATEMATİKSEL HESAPLAMA VE İSPAT:
Hesaplama; denetime elverişli, bilimsel verilere dayanan şu formül ile gerçekleştirilmiştir:
Formül: DK = Rayiç x Baz Oran x Yaş Katsayısı x KM Katsayısı x Hasar Derecesi x Yapısal Bonus

Hesaplama Dökümü:
{rayic_ort:,.2f} (Rayiç) x {baz_oran} (Baz Oran) x {yas_k} (Yaş K.) x {km_k} (KM K.) x {h_derece} (Hasar D.) x {k_bonus} (Bonus)
= {teknik_zarar:,.2f} TL

TEKNİK SONUÇ:
Aracın yaşı, kilometresi, hasar alanları ({', '.join(h_alanlari)}) ve piyasa likiditesi birlikte değerlendirildiğinde; araçta {teknik_zarar:,.2f} TL tutarında bir değer kaybı oluştuğu mütaala edilmektedir.

HUKUKİ NOT: 
İşbu tutar teknik değer kaybı olup, TBK m. 51 ve 52 uyarınca yapılacak hakkaniyet indirimi takdiri Sayın Mahkemenizdedir.

Bilirkişi: [Adınız Soyadınız]
"""
        st.code(rapor_metni, language="text")
        st.text_area("Düzenlenebilir Rapor Alanı:", rapor_metni, height=350)
