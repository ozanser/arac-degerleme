import streamlit as st
import pandas as pd

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Bilirkişi Uzman Paneli v12.0", layout="wide")

st.markdown("""
    <style>
    .report-title { color: #002b45; border-bottom: 3px solid #002b45; font-weight: bold; margin-bottom: 20px; }
    .stButton>button { background-color: #002b45; color: white; border-radius: 4px; font-weight: bold; width: 100%; height: 3.5em; }
    .calc-box { background-color: #f8f9fa; padding: 25px; border-left: 6px solid #002b45; border-radius: 5px; }
    .method-box { background-color: #eef2f7; padding: 15px; border-radius: 8px; border: 1px solid #002b45; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# --- DİALOG KUTUSU ---
@st.dialog("⚠️ Veri Giriş Hatası")
def hata_penceresi(mesaj):
    st.write(f"### {mesaj}")
    if st.button("Tamam, Düzenliyorum"):
        st.rerun()

# --- MEGA TEKNİK VERİTABANI (Sadeleştirilmiş Örnek - Önceki sürümdeki geniş liste buraya dahildir) ---
mega_db = {
    "1. Sınıf: 2 Aks / < 3.20m": {
        "Togg": {"T10X": {"V1 RWD": 218, "V2 RWD": 218, "AWD": 435}},
        "Volkswagen": {"Passat": {"1.5 TSI": 150, "1.6 TDI": 120}, "Golf": {"1.0 TSI": 110, "1.5 eTSI": 150}},
        "Tesla": {"Model Y": {"Standard": 299, "Long Range": 514}},
        "Renault": {"Clio": {"1.0 TCe": 90, "1.5 dCi": 85}, "Megane": {"1.3 TCe": 140, "1.5 dCi": 115}},
        "Fiat": {"Egea": {"1.4 Fire": 95, "1.3 Mjet": 95, "1.6 Mjet": 130}},
        "Diğer / Özel": {"Manuel Giriş": {"Liste Dışı": 100}}
    },
    "2. Sınıf: 2 Aks / > 3.20m": {"Mercedes-Benz": {"Sprinter": {"316 CDI": 163}}, "Ford": {"Transit": {"2.0 EcoBlue": 170}}, "Diğer": {"Manuel": {"Liste Dışı": 0}}},
    "3. Sınıf: 3 Akslı": {"Mercedes-Benz": {"Actros": {"1845 LS": 449}}, "Volvo": {"FH": {"FH 500": 500}}, "Diğer": {"Manuel": {"Liste Dışı": 0}}},
    "6. Sınıf: Motosiklet": {"Honda": {"Forza": {"250": 23}}, "Yamaha": {"MT-07": {"689cc": 73}}, "Diğer": {"Manuel": {"Liste Dışı": 0}}}
}

st.markdown("<h2 class='report-title'>⚖️ Gerekçeli Bilirkişi Raporlama Sistemi</h2>", unsafe_allow_html=True)

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
    e1_n = st.text_input("Emsal 1 Kaynak", "Sahibinden.com İlan No: ...")
    e2_n = st.text_input("Emsal 2 Kaynak", "Arabam.com İlan No: ...")
    e3_n = st.text_input("Emsal 3 Kaynak", "Yerel Galeri Beyanı")

fiyatlar = [f for f in [e1_f, e2_f, e3_f] if f > 0]
rayic_ort = sum(fiyatlar) / len(fiyatlar) if fiyatlar else 0

st.divider()

# --- BÖLÜM 2: TEKNİK ARAÇ KÜNYESİ ---
st.write("### 🚗 2. Araç ve Hasar Teknik Analizi")
c1, c2, c3 = st.columns(3)

with c1:
    kat = st.selectbox("Aks / Dingil Sınıfı", list(mega_db.keys()))
    marka = st.selectbox("Marka", list(mega_db[kat].keys()))
    model = st.selectbox("Model", list(mega_db[kat][marka].keys()))
    motor_segment = st.selectbox("Motor / Paket", list(mega_db[kat][marka][model].keys()))
    otomatik_hp = mega_db[kat][marka][model][motor_segment]

with c2:
    yil = st.selectbox("Model Yılı", list(range(2026, 1929, -1)))
    km = st.number_input("Mevcut Kilometre", min_value=0, value=50000)
    yakit = st.selectbox("Yakıt Tipi", ["Benzin", "Dizel", "Elektrikli", "Hibrit", "LPG"])
    beygir = st.number_input("Motor Gücü (HP)", value=otomatik_hp)

with c3:
    h_derece = st.selectbox("Hasar Şiddeti", options=[1.0, 1.4, 1.9, 2.8], format_func=lambda x: "Hafif" if x==1.0 else ("Orta" if x==1.4 else ("Yüksek" if x==1.9 else "Ağır/Kritik")))
    h_alanlari = st.multiselect("Hasarlı Bölgeler", ["Ön", "Arka", "Yanlar", "Şasi", "Direkler", "Tavan", "Airbag", "Mekanik"])

st.divider()

# --- BÖLÜM 3: HESAPLAMA VE GEREKÇELİ RAPOR ---
if st.button("ANALİZİ TAMAMLA VE GEREKÇELİ RAPORU OLUŞTUR"):
    if len(fiyatlar) < 3:
        hata_penceresi("Rapor ispatı için en az 3 emsal girilmelidir.")
    elif not h_alanlari:
        hata_penceresi("Lütfen hasarlı bölge seçimi yapınız.")
    else:
        # Teknik Katsayı Belirleme (Gerekçelendirme için)
        yas = 2026 - yil
        yas_k = 1.0 if yas <= 2 else (0.75 if yas <= 6 else (0.45 if yas <= 15 else 0.25))
        km_k = 1.0 if km <= 25000 else (0.65 if km <= 110000 else 0.35)
        kritik_c = 1.35 if any(x in h_alanlari for x in ["Şasi", "Direkler", "Tavan", "Airbag"]) else 1.0
        
        # Formül
        teknik_zarar = rayic_ort * 0.15 * yas_k * km_k * h_derece * kritik_c

        # 1. HESAPLAMA DÖKÜMÜ (AÇIKLAMA METNİ)
        st.markdown("<div class='calc-box'>", unsafe_allow_html=True)
        st.write("### 📊 Hesaplama Metodolojisi ve Gerekçe")
        st.write(f"""
        İşbu hesaplama, Yargıtay ve SBM standartlarına paralel olarak aşağıdaki parametrelerle yapılmıştır:
        - **Baz Rayiç Değer:** {rayic_ort:,.2f} TL (3 adet emsal ilan ortalamasıdır).
        - **Yaş Katsayısı ({yas_k}):** Araç {yas} yaşında olduğu için piyasadaki yıpranma payı katsayısıdır.
        - **KM Katsayısı ({km_k}):** Aracın {km:,} km mesafesi üzerinden ekonomik ömür kaybı çarpanıdır.
        - **Hasar Şiddeti ({h_derece}):** Onarımın niteliğine göre belirlenen hasar derinlik katsayısıdır.
        - **Yapısal Bonus ({kritik_c}):** {'Şasi/Airbag gibi kritik bölgeler hasarlı olduğu için %35 artırılmıştır.' if kritik_c > 1 else 'Yapısal bir hasar tespit edilmemiştir.'}
        """)
        st.markdown("</div>", unsafe_allow_html=True)

        st.divider()

        # 2. KOPYALANABİLİR NİHAİ RAPOR
        st.write("### 📝 Nihai Bilirkişi Raporu")
        st.caption("Aşağıdaki metnin sağ üstündeki butona basarak tek tıkla kopyalayabilirsiniz.")
        
        rapor_metni = f"""SAYIN HAKİMLİĞİNE

DOSYA NO: [Dosya No Giriniz]
ARAÇ: {yil} Model {marka} {model} ({motor_segment}, {beygir} HP)

PİYASA ARAŞTIRMASI:
Tarafımızca yapılan teknik incelemede, kaza tarihi itibarıyla benzer özelliklerdeki şu emsaller tespit edilmiştir:
1. {e1_f:,.0f} TL ({e1_n})
2. {e2_f:,.0f} TL ({e2_n})
3. {e3_f:,.0f} TL ({e3_n})
Emsallerin aritmetik ortalaması olan {rayic_ort:,.2f} TL, aracın hasarsız rayiç değeri olarak kabul edilmiştir.

TEKNİK ANALİZ VE HESAPLAMA GEREKÇESİ:
Hesaplamada; aracın yaşı ({yas}), kilometresi ({km:,} KM), hasar aldığı bölgeler ({', '.join(h_alanlari)}) ve hasar şiddeti baz alınmıştır. Denetime elverişli matematiksel modelleme sonucunda; aracın ikinci el piyasasındaki arz-talep dengesi ve teknik yıpranma katsayıları neticesinde araçta {teknik_zarar:,.2f} TL tutarında bir eksilme (değer kaybı) olduğu saptanmıştır.

HUKUKİ SONUÇ:
Tespit edilen {teknik_zarar:,.2f} TL teknik değer kaybı olup, TBK 51-52 uyarınca yapılacak takdiri indirimler Sayın Mahkemenizdedir.

Bilirkişi: [Adınız Soyadınız]
"""
        # st.code bileşeni kopyalama butonu içerir
        st.code(rapor_metni, language="text")
        
        # Düzenleme alanı (Opsiyonel)
        st.text_area("Rapor üzerinde manuel düzenleme yapabilirsiniz:", rapor_metni, height=300)
