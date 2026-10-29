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

# Kunci API Router9 (diambil dari Secrets Streamlit Cloud atau .env lokal)
ROUTER9_API_KEY = os.getenv("ROUTER9_API_KEY", "").strip()
ROUTER9_URL = "https://api.router9.com/v1/chat/completions"

# Definisi 5 Divisi Lengkap dari Katalog Router9 Free Tier
DIVISI = {
    "Lead Software Architect": {
        "nama": "DeepSeek V4 Pro",
        "model": "deepseek/deepseek-v4-pro",
        "icon": "🧠",
        "deskripsi": "Arsitektur data kompleks, logika bisnis tingkat lanjut, dan optimasi performa sistem.",
        "system": (
            "Anda adalah Principal Software Architect spesialis sistem absensi dan kinerja kantor. "
            "Fokus tugas: merancang arsitektur sistem yang skalabel, relasi database, kalkulasi keterlambatan/lembur "
            "yang kompleks, serta algoritma pemrosesan data presensi."
        )
    },
    "Fast Backend Developer": {
        "nama": "DeepSeek V4 Flash",
        "model": "deepseek/deepseek-v4-flash",
        "icon": "⚙️",
        "deskripsi": "Eksekusi cepat endpoint API, fungsi validasi GPS/geofencing, dan skrip CRUD harian.",
        "system": (
            "Anda adalah Senior Backend Developer yang fokus pada efisiensi dan kecepatan. "
            "Tugas: membuat fungsi backend ringkas, validasi koordinat GPS radius kantor, "
            "pengecekan toleransi jam masuk/pulang, dan integrasi API form absensi."
        )
    },
    "Frontend & CSS Architect": {
        "nama": "Qwen3 235B",
        "model": "qwen/qwen3-235b-a22b-2507",
        "icon": "🎨",
        "deskripsi": "Tata letak dashboard responsif (HP & Desktop), Tailwind CSS, Flexbox, dan Grid modern.",
        "system": (
            "Anda adalah Frontend Architect ahli CSS modern, Tailwind CSS, Flexbox, dan Grid. "
            "Tugas: membangun antarmuka web absensi yang rapi, modern, responsif untuk layar smartphone staf, "
            "serta komponen interaktif seperti kartu profil, tabel absensi, dan tombol presensi presisi."
        )
    },
    "UI/UX Inspector": {
        "nama": "MiniMax M3",
        "model": "minimax/minimax-m3",
        "icon": "👁️",
        "deskripsi": "Audit visual, hierarki tipografi, standar kontras WCAG, dan kemudahan navigasi pengguna.",
        "system": (
            "Anda adalah Lead UI/UX Designer. "
            "Tugas: mengevaluasi kenyamanan alur pengguna pada web absensi kantor, memeriksa kontras warna, "
            "memastikan ukuran tombol nyaman disentuh jari pada smartphone, serta memberikan saran micro-interaction."
        )
    },
    "QA & Security Auditor": {
        "nama": "GLM 5.2",
        "model": "z-ai/glm-5.2",
        "icon": "🛡️",
        "deskripsi": "Audit celah keamanan, mitigasi manipulasi lokasi/fake GPS, dan uji skenario eror formulir.",
        "system": (
            "Anda adalah Lead QA & Cyber Security Auditor sistem aplikasi web kantor. "
            "Tugas: memeriksa kerentanan kode backend/frontend, memastikan form aman dari manipulasi fake GPS, "
            "mencegah kebocoran data presensi staf, dan menguji skenario input yang rusak (edge-cases)."
        )
    }
}

def panggil_karyawan(model_id: str, system_prompt: str, pesan_user: str) -> str:
    if not ROUTER9_API_KEY:
        return "⚠️ Galat: Kunci API Router9 belum terdeteksi. Masukkan API Key di bilah samping atau Secrets."

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

# --- SIDEBAR: STATUS TIM KANTOR ---
with st.sidebar:
    st.title("🏢 Divisi Kantor AI")
    st.caption("5 Karyawan Pengembang Web Absensi & Kinerja")
    st.markdown("---")
    
    for jabatan, info in DIVISI.items():
        st.markdown(f"**{info['icon']} {jabatan}**")
        st.caption(f"Model: `{info['nama']}`\n\n{info['deskripsi']}")
        st.markdown("---")
        
    api_input = st.text_input("Ganti API Key Router9 (Opsional):", value=ROUTER9_API_KEY, type="password")
    if api_input and api_input != ROUTER9_API_KEY:
        ROUTER9_API_KEY = api_input

# --- AREA UTAMA ---
st.title("💼 Ruang Manajer: Rapat Tim Pengembang AI")
st.markdown("Instruksikan 5 model AI sekaligus untuk merancang, mengode, dan mengaudit sistem absensi Anda.")

mode_kerja = st.radio(
    "Pilih Format Kerja:",
    ["Meja Spesifik (Konsultasi 1 Karyawan)", "Rapat Tim Penuh (5 Karyawan Menjawab Serentak)"],
    horizontal=True
)

instruksi = st.text_area(
    "Instruksi Pekerjaan / Fitur yang Ingin Dibuat:",
    height=140,
    placeholder="Misal: Buatkan modul verifikasi lokasi radius 50 meter dari kantor beserta kartu status absensi mobile-friendly..."
)

tombol_kirim = st.button("🚀 Kirim Instruksi ke Meja Kerja", type="primary", use_container_width=True)

# 1. MODE MEJA SPESIFIK
if mode_kerja == "Meja Spesifik (Konsultasi 1 Karyawan)":
    pilihan_divisi = st.selectbox("Pilih Karyawan yang Bertugas:", list(DIVISI.keys()))
    
    if tombol_kirim and instruksi.strip():
        karyawan = DIVISI[pilihan_divisi]
        with st.spinner(f"Sedang dikerjakan oleh {karyawan['nama']} ({pilihan_divisi})..."):
            jawaban = panggil_karyawan(karyawan["model"], karyawan["system"], instruksi)
            
        st.markdown(f"### 📋 Hasil Kerja: {karyawan['icon']} {pilihan_divisi} (`{karyawan['nama']}`)")
        st.markdown(jawaban)

# 2. MODE RAPAT TIM PENUH (5 KOLOM PARALEL)
else:
    if tombol_kirim and instruksi.strip():
        st.markdown("### 📊 Hasil Rapat Lengkap 5 Divisi")
        kolom_tim = st.columns(len(DIVISI))
        
        for idx, (jabatan, info) in enumerate(DIVISI.items()):
            with kolom_tim[idx]:
                st.markdown(f"#### {info['icon']} {info['nama']}")
                st.caption(f"**{jabatan}**")
                with st.spinner(f"Menyusun respons..."):
                    hasil = panggil_karyawan(info["model"], info["system"], instruksi)
                st.markdown(hasil)
