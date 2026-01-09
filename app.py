import streamlit as st
import pandas as pd

# 1. SAYFA AYARLARI VE KURUMSAL STİL
st.set_page_config(page_title="Bilirkişi Uzman Paneli v9.0", layout="wide")

st.markdown("""
    <style>
    .report-title { color: #002b45; border-bottom: 3px solid #002b45; font-weight: bold; margin-bottom: 20px; }
    .stButton>button { background-color: #002b45; color: white; border-radius: 4px; font-weight: bold; width: 100%; height: 3.5em; }
    .calc-box { background-color: #f8f9fa; padding: 20px; border-left: 6px solid #002b45; border-radius: 5px; }
    .hakkaniyet-box { background-color: #fff9f2; padding: 20px; border-left: 6px solid #fd7e14; border-radius: 5px; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- DİALOG KUTUSU (MODAL) ---
@st.dialog("⚠️ Veri Giriş Hatası")
def hata_penceresi(mesaj):
    st.write(f"### {mesaj}")
    st.write("Raporun hukuki denetlenebilirliği için tüm teknik alanlar doldurulmalıdır.")
    if st.button("Düzenlemek İçin Dön"):
        st.rerun()

# --- AKS BAZLI HİYERARŞİK VERİTABANI ---
# Kullanıcının ilettiği resmi sınıflara göre yapılandırılmıştır.
arac_db = {
    "1. Sınıf: 2 Aks / Aks Mesafesi < 3.20m (Otomobil, Hafif Ticari)": {
        "Togg": ["T10X V1", "T10X V2", "T10F"],
        "Volkswagen": ["Passat", "Golf", "Polo", "Tiguan"],
        "Renault": ["Clio", "Megane", "Austral", "Taliant"],
        "Fiat": ["Egea Sedan", "Egea Cross", "Fiorino", "Doblo (Kısa)"],
        "Chery": ["Omoda 5", "Tiggo 7 Pro", "Tiggo 8 Pro"],
        "Tesla": ["Model Y", "Model 3"],
        "Diğer": ["Manuel Giriş"]
    },
    "2. Sınıf: 2 Aks / Aks Mesafesi > 3.20m (Minibüs, Kamyonet, Otobüs)": {
        "Ford": ["Transit Panelvan", "Transit Kamyonet", "Ranger"],
        "Mercedes-Benz": ["Sprinter", "Vito", "Travego (2 Aks)", "Tourismo"],
        "Volkswagen": ["Crafter", "Transporter LWB"],
        "Fiat": ["Ducato Van", "Doblo Maxi"],
        "Diğer": ["Manuel Giriş"]
    },
    "3. Sınıf: 3 Akslı Araçlar (Otobüs, Kamyon, Çekici)": {
        "Mercedes-Benz": ["Actros 1845", "Axor 3240", "Travego 17 SHD"],
        "Volvo": ["FH 500 (6x2)", "FM 460"],
        "Scania": ["R 450 (6x2)", "G 400"],
        "Ford Trucks": ["F-MAX", "2533"],
        "Diğer": ["Manuel Giriş"]
    },
    "4. Sınıf: 4 ve 5 Akslı Araçlar (Tır, Ağır Vasıta)": {
        "Çekici + Yarırömork": ["5 Aks Toplam", "4 Aks Toplam"],
        "Kamyon + Römork": ["5 Aks Kombinasyon"],
        "Özel Amaçlı": ["Vinç / Mobil Platform"],
        "Diğer": ["Manuel Giriş"]
    },
    "5. Sınıf: 6 ve Üzeri Akslı Araçlar (Ağır Nakliye)": {
        "Lowbed": ["Ağır Nakliye Kombinasyonu"],
        "Özel Proje Tipi": ["Çok Akslı Modüler"],
        "Diğer": ["Manuel Giriş"]
    },
    "6. Sınıf: Motosikletler": {
        "Honda": ["Africa Twin", "PCX 125", "Forza 250"],
        "Yamaha": ["Tracer 9", "MT-07", "XMAX 250"],
        "BMW": ["R 1250 GS", "S 1000 RR"],
        "Diğer": ["Manuel Giriş"]
    }
}

st.markdown("<h2 class='report-title'>⚖️ Bilirkişi Aks Bazlı Araç Değerleme Paneli v9.0</h2>", unsafe_allow_html=True)

# --- BÖLÜM 1: PİYASA ARAŞTIRMASI ---
st.write("### 🔍 1. Piyasa Araştırması (3 Emsal)")
col_e1, col_e2, col_e3 = st.columns([2, 1, 3])
with col_e1:
    e1_f = st.number_input("Emsal 1 Fiyat (TL)", min_value=0, step=10000)
    e2_f = st.number_input("Emsal 2 Fiyat (TL)", min_value=0, step=10000)
    e3_f = st.number_input("Emsal 3 Fiyat (TL)", min_value=0, step=10000)
with col_e2:
    e1_k = st.number_input("Emsal 1 KM/Saat", min_value=0)
    e2_k = st.number_input("Emsal 2 KM/Saat", min_value=0)
    e3_k = st.number_input("Emsal 3 KM/Saat", min_value=0)
with col_e3:
    e1_n = st.text_input("Emsal 1 Kaynak", placeholder="İlan Linki / Kurum...")
    e2_n = st.text_input("Emsal 2 Kaynak", placeholder="İlan Linki / Kurum...")
    e3_n = st.text_input("Emsal 3 Kaynak", placeholder="İlan Linki / Kurum...")

fiyatlar = [f for f in [e1_f, e2_f, e3_f] if f > 0]
rayic_ort = sum(fiyatlar) / len(fiyatlar) if fiyatlar else 0

st.divider()

# --- BÖLÜM 2: AKS BAZLI ARAÇ KÜNYESİ ---
st.write("### 🚗 2. Aks Sınıfı ve Teknik Detaylar")
c1, c2, c3 = st.columns(3)

with c1:
    kat = st.selectbox("Resmi Araç Sınıfı (Aks/Dingil)", list(arac_db.keys()))
    marka_list = list(arac_db[kat].keys())
    marka = st.selectbox("Marka / Üretici", marka_list)
    
    if marka == "Diğer":
        manuel_m = st.text_input("Marka Giriniz")
        model = st.text_input("Model Giriniz")
    else:
        model = st.selectbox("Model / Seri", arac_db[kat][marka])
    
    yil = st.selectbox("Model Yılı", list(range(2026, 1929, -1)))

with c2:
    km = st.number_input("Mevcut Kilometre / Saat", min_value=0, value=50000)
    yakit = st.selectbox("Enerji Tipi", ["Dizel", "Benzin", "Elektrikli (BEV)", "Hibrit", "LPG", "Hidrojen"])
    vites = st.selectbox("Şanzıman", ["Otomatik", "Manuel", "Yarı Otomatik", "CVT", "E-Shift"])

with c3:
    beygir = st.number_input("Motor Gücü (HP)", min_value=0, value=150)
    hasar_derece = st.selectbox("Hasar Önem Derecesi", options=[1.0, 1.4, 1.9, 2.8], format_func=lambda x: "Düşük" if x==1.0 else ("Orta" if x==1.4 else ("Yüksek" if x==1.9 else "Ağır/Kritik")))
    hasar_alanlari = st.multiselect("Hasarlı Bölgeler", ["Ön", "Arka", "Yanlar", "Şasi/Dingil", "Kabin/Tavan", "Airbag", "Mekanik"])

st.divider()

# --- BÖLÜM 3: HESAPLAMA VE SONUÇ ---
if st.button("ANALİZİ TAMAMLA VE TEKNİK RAPORU HAZIRLA"):
    if len(fiyatlar) < 3:
        hata_penceresi("Piyasa tespiti için 3 adet emsal fiyat girişi zorunludur.")
    elif not hasar_alanlari:
        hata_penceresi("Lütfen hasarlı bölge seçimi yapınız.")
    else:
        # Teknik Hesaplama
        yas = 2026 - yil
        yas_k = 1.0 if yas <= 2 else (0.75 if yas <= 6 else 0.40)
        km_k = 1.0 if km <= 25000 else (0.65 if km <= 110000 else 0.30)
        
        # Ağır vasıta ve çok akslı araçlarda değer kaybı dinamiği farklıdır
        aks_carpan = 1.0
        if "3." in kat or "4." in kat or "5." in kat:
            aks_carpan = 1.2 # Ticari iş kaybı ve yapısal karmaşıklık bonusu
            
        teknik_zarar = rayic_ort * 0.15 * yas_k * km_k * hasar_derece * aks_carpan

        # SONUÇ GÖSTERİMİ
        st.markdown("<div class='calc-box'>", unsafe_allow_html=True)
        st.write(f"### 📊 Teknik Zarar Tespiti")
        st.write(f"**Sınıf:** {kat}")
        st.write(f"**Araç:** {yil} {marka if marka != 'Diğer' else manuel_m} {model}")
        st.write(f"## {teknik_zarar:,.2f} TL")
        st.latex(rf"DK = Rayiç \times 0.15 \times Y_k \times KM_k \times H_d \times Aks_c = {teknik_zarar:,.2f}")
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
        Dosya konusu {kat} sınıfına giren {yil} model {marka if marka != 'Diğer' else manuel_m} {model} 
        plakalı aracın yapılan piyasa araştırmasında; 3 adet emsal ortalaması olan {rayic_ort:,.2f} TL baz alınmıştır.
        
        TEKNİK ANALİZ:
        Aracın aks yapısı, kilometresi ({km:,}), hasar aldığı bölgeler ({', '.join(hasar_alanlari)}) 
        ve kullanım amacı birlikte değerlendirildiğinde; TEKNİK DEĞER KAYBININ {teknik_zarar:,.2f} TL 
        olduğu sonucuna varılmıştır.
        
        TBK 51-52 uyarınca hakkaniyet indirimi takdiri Sayın Mahkemenizdedir.
        """
        st.text_area("Metni Kopyala", rapor, height=200)
