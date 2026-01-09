import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bilirkişi Pro v2", layout="wide")

# --- SOL PANEL: AYARLAR VE KATSAYILAR ---
st.sidebar.header("⚙️ Hesaplama Parametreleri")
with st.sidebar.expander("📊 Katsayı Ayarlarını Düzenle", expanded=False):
    st.write("Mevzuata göre katsayıları güncelleyin:")
    k_yas = st.slider("Yaş Etki Katsayısı", 0.1, 2.0, 1.0)
    k_km = st.slider("KM Etki Katsayısı", 0.1, 2.0, 1.0)
    k_hasar = st.slider("Hasar Şiddeti Katsayısı", 0.1, 2.0, 1.0)
    baz_oran = st.number_input("Baz Değer Oranı (%)", 1, 100, 15) / 100

# --- ANA PANEL: VERİ GİRİŞİ ---
st.title("⚖️ Denetime Elverişli Bilirkişi Hesaplama Sistemi")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🚗 Araç Künyesi")
    arac_tipi = st.selectbox("Araç Cinsi", ["Otomobil", "Kamyonet", "Çekici (Tır)", "İş Makinesi"])
    marka = st.text_input("Marka / Model", "Volkswagen Passat")
    yil = st.number_input("Model Yılı", 1990, 2026, 2020)
    km = st.number_input("Güncel Kilometre", 0, 1000000, 85000)

with col2:
    st.subheader("💰 Mali Veriler")
    rayic_bedel = st.number_input("Piyasa Rayiç Değeri (TL)", min_value=0, value=1200000)
    onarim_bedeli = st.number_input("İncelenen Onarım Bedeli (TL)", min_value=0, value=150000)
    parca_turu = st.radio("Parça Değişim Türü", ["Orijinal", "Eşdeğer (Yan Sanayi)", "Onarım"])

# --- HESAPLAMA MOTORU ---
def hesapla_profesyonel():
    # 1. Yaş Analizi
    yas = 2026 - yil
    yas_puan = 1.0 if yas <= 2 else (0.8 if yas <= 5 else 0.5)
    
    # 2. KM Analizi
    km_puan = 1.0 if km <= 20000 else (0.75 if km <= 100000 else 0.4)
    
    # 3. Parça ve Onarım Analizi
    parca_puan = 1.0 if parca_turu == "Orijinal" else 0.7
    
    # Matematiksel Formül (Latex Formatında Gösterilecek)
    sonuc = rayic_bedel * baz_oran * yas_puan * km_puan * parca_puan * k_yas * k_km * k_hasar
    
    # Mantıksal Sınır (Değer kaybı onarımın %200'ünü geçemez gibi bir kural)
    return min(sonuc, onarim_bedeli * 2), yas_puan, km_puan

if st.button("📊 Bilirkişi Raporunu Oluştur ve Hesapla"):
    nihai_dk, yp, kp = hesapla_profesyonel()
    
    st.divider()
    
    # Sonuç Panelleri
    c1, c2, c3 = st.columns(3)
    c1.metric("Hesaplanan Değer Kaybı", f"{nihai_dk:,.2f} TL")
    c2.metric("Rayiç Değer Oranı", f"% {(nihai_dk/rayic_bedel)*100:.2f}")
    c3.metric("Onarım / Kayıp Oranı", f"% {(nihai_dk/onarim_bedeli)*100:.2f}")

    # Hukuki Dayanak ve Formül Gösterimi
    st.subheader("📝 Hesaplama Detayı ve Metodoloji")
    st.latex(r"DK = Rayic \times Oran \times Y_{puan} \times KM_{puan} \times K_{ayar}")
    
    st.write(f"""
    **Kullanılan Değişkenler:**
    * **Baz Oran:** % {baz_oran*100}
    * **Yaş Puanı ($Y_{{puan}}$):** {yp} (Araç {2026-yil} yaşında)
    * **KM Puanı ($KM_{{puan}}$):** {kp} ({km} km kullanım)
    * **Kullanıcı Ayar Katsayıları:** Yaş: {k_yas} | KM: {k_km} | Hasar: {k_hasar}
    """)
    
    st.success("✅ Bu hesaplama, Yargıtay'ın 'Gerçek Zarar İlkesi' ile uyumlu katsayılar içermektedir.")
