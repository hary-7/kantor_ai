import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Kantor AI — Ruang Kerja Tim Pengembang",
    page_icon="🏢",
    layout="wide"
)

# Kunci API Router9
ROUTER9_API_KEY = os.getenv("ROUTER9_API_KEY", "").strip()
ROUTER9_URL = "https://api.router9.com/v1/chat/completions"

# Definisi Meja Divisi & Persona Karyawan AI
DIVISI = {
    "Backend Engineer": {
        "nama": "DeepSeek V4 Flash",
        "model": "deepseek/deepseek-v4-flash",
        "icon": "⚙️",
        "deskripsi": "Logika absensi, validasi GPS/geofencing, database, dan security.",
        "system": (
            "Anda adalah Senior Backend Developer spesialis sistem absensi kantor. "
            "Fokus tugas Anda: merancang skema data, API endpoints, validasi jam masuk/pulang, "
            "perhitungan keterlambatan/lembur, dan validasi radius GPS (geofencing). "
            "Berikan kode yang aman, efisien, dan bersih."
        )
    },
    "Frontend & CSS Architect": {
        "nama": "Qwen3 235B",
        "model": "qwen/qwen3-235b-a22b-2507",
        "icon": "🎨",
        "deskripsi": "Tata letak dashboard, Tailwind/CSS responsif, dan interaktivitas komponen.",
        "system": (
            "Anda adalah Frontend Architect ahli CSS modern, Tailwind CSS, Flexbox, dan Grid. "
            "Tugas Anda: membangun antarmuka web absensi yang bersih, rapi, responsif "
            "(sempurna di HP dan monitor desktop), serta komponen interaktif (kartu profil, tabel absensi, tombol presensi)."
        )
    },
    "UI/UX Inspector": {
        "nama": "MiniMax M3",
        "model": "minimax/minimax-m3",
        "icon": "👁️",
        "deskripsi": "Audit visual, hierarki tipografi, kontras warna, dan pengalaman pengguna.",
        "system": (
            "Anda adalah Lead UI/UX Designer. Tugas Anda: mengevaluasi kenyamanan alur pengguna "
            "pada web absensi kantor, memeriksa kontras warna (WCAG), memastikan tombol mudah ditekan di layar sentuh, "
            "dan memberikan saran perbaikan visual micro-interaction."
        )
    }
}

def panggil_karyawan(model_id: str, system_prompt: str, pesan_user: str) -> str:
    if not ROUTER9_API_KEY:
        return "⚠️ Galat: Kunci API Router9 belum diatur di .env atau pengaturan."

    headers = {
        "Authorization": f"Bearer {ROUTER9_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pesan_user}
        ],
        "temperature": 0.4
    }

    try:
        res = requests.post(ROUTER9_URL, headers=headers, json=payload, timeout=60)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"]
        return f"Galat Router9 ({res.status_code}): {res.text}"
    except Exception as e:
        return f"Koneksi gagal: {str(e)}"

# --- SIDEBAR: STATUS TIM ---
with st.sidebar:
    st.title("🏢 Divisi Kantor AI")
    st.caption("Tim Pengembang Web Absensi Kantor")
    
    st.markdown("---")
    for jabatan, info in DIVISI.items():
        st.markdown(f"**{info['icon']} {jabatan}**")
        st.caption(f"Model: `{info['nama']}`\n\n{info['deskripsi']}")
        st.markdown("---")
        
    api_input = st.text_input("Ganti API Key Router9:", value=ROUTER9_API_KEY, type="password")
    if api_input != ROUTER9_API_KEY:
        ROUTER9_API_KEY = api_input

# --- AREA UTAMA ---
st.title("💼 Ruang Manajer: Instruksikan Karyawan AI")
st.markdown("Ruang kerja portabel untuk membangun, menata CSS, dan memecahkan masalah website absensi kantor.")

mode_kerja = st.radio(
    "Pilih Format Kerja:",
    ["Meja Spesifik (Konsultasi 1 Karyawan)", "Rapat Tim Penuh (3 Karyawan Menjawab Serentak)"],
    horizontal=True
)

instruksi = st.text_area(
    "Instruksi Pekerjaan:",
    height=140,
    placeholder="Misal: Buatkan komponen kartu absensi mobile-friendly dengan tombol 'Absen Masuk' yang menyala hijau saat di dalam radius kantor..."
)

tombol_kirim = st.button("🚀 Kirim Instruksi ke Meja Kerja", type="primary", use_container_width=True)

# 1. MODE MEJA SPESIFIK
if mode_kerja == "Meja Spesifik (Konsultasi 1 Karyawan)":
    pilihan_divisi = st.selectbox("Pilih Karyawan yang Bertugas:", list(DIVISI.keys()))
    
    if tombol_kirim and instruksi.strip():
        karyawan = DIVISI[pilihan_divisi]
        with st.spinner(f"Sedang dikerjakan oleh {karyawan['nama']} ({pilihan_divisi})..."):
            jawaban = panggil_karyawan(karyawan["model"], karyawan["system"], instruksi)
            
        st.markdown(f"### 📋 Hasil Kerja: {karyawan['icon']} {pilihan_divisi}")
        st.markdown(jawaban)

# 2. MODE RAPAT TIM PENUH (MULTI-AGENT DASHBOARD)
else:
    if tombol_kirim and instruksi.strip():
        st.markdown("### 📊 Hasil Rapat Tim Pengembang")
        kol_backend, kol_frontend, kol_uiux = st.columns(3)
        
        with kol_backend:
            st.markdown(f"#### ⚙️ Backend (DeepSeek)")
            with st.spinner("Merancang arsitektur & logika..."):
                hasil_be = panggil_karyawan(
                    DIVISI["Backend Engineer"]["model"],
                    DIVISI["Backend Engineer"]["system"],
                    instruksi
                )
            st.markdown(hasil_be)
            
        with kol_frontend:
            st.markdown(f"#### 🎨 Frontend (Qwen3)")
            with st.spinner("Menyusun HTML & Tailwind CSS..."):
                hasil_fe = panggil_karyawan(
                    DIVISI["Frontend & CSS Architect"]["model"],
                    DIVISI["Frontend & CSS Architect"]["system"],
                    instruksi
                )
            st.markdown(hasil_fe)
            
        with kol_uiux:
            st.markdown(f"#### 👁️ UI/UX (MiniMax)")
            with st.spinner("Mengaudit visual & kenyamanan alur..."):
                hasil_ux = panggil_karyawan(
                    DIVISI["UI/UX Inspector"]["model"],
                    DIVISI["UI/UX Inspector"]["system"],
                    instruksi
                )
            st.markdown(hasil_ux)