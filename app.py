import os
import requests
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

load_dotenv(override=True)

st.set_page_config(
    page_title="Kantor AI — Ruang Kerja Tim Pengembang",
    page_icon="🏢",
    layout="wide"
)

# Kunci API Router9
API_KEY_AWAL = st.secrets.get("ROUTER9_API_KEY", os.getenv("ROUTER9_API_KEY", "")).strip()
ROUTER9_URL = "https://api.router9.com/v1/chat/completions"

if "router9_api_key" not in st.session_state:
    st.session_state["router9_api_key"] = API_KEY_AWAL

# Definisi 5 Divisi AI
DIVISI = {
    "Lead Software Architect": {
        "id": "ds_pro",
        "nama": "DeepSeek V4 Pro",
        "model": "deepseek/deepseek-v4-pro",
        "icon": "🧠",
        "santai_icon": "📖",
        "santai_text": "Membaca Buku",
        "deskripsi": "Arsitektur data kompleks, logika bisnis tingkat lanjut, dan optimasi performa sistem.",
        "system": (
            "Anda adalah Principal Software Architect spesialis sistem absensi dan kinerja kantor. "
            "Fokus tugas: merancang arsitektur sistem yang skalabel, relasi database, kalkulasi keterlambatan/lembur "
            "yang kompleks, serta algoritma pemrosesan data presensi."
        )
    },
    "Fast Backend Developer": {
        "id": "ds_flash",
        "nama": "DeepSeek V4 Flash",
        "model": "deepseek/deepseek-v4-flash",
        "icon": "⚙️",
        "santai_icon": "☕",
        "santai_text": "Menyeruput Kopi",
        "deskripsi": "Eksekusi cepat endpoint API, fungsi validasi GPS/geofencing, dan skrip CRUD harian.",
        "system": (
            "Anda adalah Senior Backend Developer yang fokus pada efisiensi dan kecepatan. "
            "Tugas: membuat fungsi backend ringkas, validasi koordinat GPS radius kantor, "
            "pengecekan toleransi jam masuk/pulang, dan integrasi API form absensi."
        )
    },
    "Frontend & CSS Architect": {
        "id": "qwen3",
        "nama": "Qwen3 235B",
        "model": "qwen/qwen3-235b-a22b-2507",
        "icon": "🎨",
        "santai_icon": "🪑",
        "santai_text": "Putar Kursi",
        "deskripsi": "Tata letak dashboard responsif (HP & Desktop), Tailwind CSS, Flexbox, dan Grid modern.",
        "system": (
            "Anda adalah Frontend Architect ahli CSS modern, Tailwind CSS, Flexbox, dan Grid. "
            "Tugas: membangun antarmuka web absensi yang rapi, modern, responsif untuk layar smartphone staf, "
            "serta komponen interaktif seperti kartu profil, tabel absensi, dan tombol presensi presisi."
        )
    },
    "UI/UX Inspector": {
        "id": "minimax",
        "nama": "MiniMax M3",
        "model": "minimax/minimax-m3",
        "icon": "👁️",
        "santai_icon": "🍩",
        "santai_text": "Ngemil Donat",
        "deskripsi": "Audit visual, hierarki tipografi, standar kontras WCAG, dan kemudahan navigasi pengguna.",
        "system": (
            "Anda adalah Lead UI/UX Designer. "
            "Tugas: mengevaluasi kenyamanan alur pengguna pada web absensi kantor, memeriksa kontras warna, "
            "memastikan ukuran tombol nyaman disentuh jari pada smartphone, serta memberikan saran micro-interaction."
        )
    },
    "QA & Security Auditor": {
        "id": "glm",
        "nama": "GLM 5.2",
        "model": "z-ai/glm-5.2",
        "icon": "🛡️",
        "santai_icon": "🎮",
        "santai_text": "Bermain PS",
        "deskripsi": "Audit celah keamanan, mitigasi manipulasi lokasi/fake GPS, dan uji skenario eror formulir.",
        "system": (
            "Anda adalah Lead QA & Cyber Security Auditor sistem aplikasi web kantor. "
            "Tugas: memeriksa kerentanan kode backend/frontend, memastikan form aman dari manipulasi fake GPS, "
            "mencegah kebocoran data presensi staf, dan menguji skenario input yang rusak (edge-cases)."
        )
    }
}

# --- KOMPONEN ANIMASI KANTOR VIRTUAL ---
def render_kantor_animasi(karyawan_sedang_kerja=None):
    mode_kerja = karyawan_sedang_kerja is not None
    is_semua = (karyawan_sedang_kerja == "SEMUA")

    kartu_karakter_html = ""
    for jabatan, info in DIVISI.items():
        is_worker = is_semua or (karyawan_sedang_kerja == jabatan)

        if not mode_kerja:
            css_state = "idle"
            avatar_content = info["santai_icon"]
            status_text = info["santai_text"]
        elif is_worker:
            css_state = "working"
            avatar_content = "💻"
            status_text = "⚡ Mengode..."
        else:
            css_state = "watching"
            avatar_content = "👀"
            status_text = "Nonton"

        kartu_karakter_html += f"""
        <div class="station {css_state}">
          <div class="avatar-wrap">
            <span class="avatar-icon">{avatar_content}</span>
            <span class="job-badge">{info['icon']}</span>
          </div>
          <div class="desk">
            <div class="monitor"></div>
          </div>
          <div class="status-bubble">{status_text}</div>
          <div class="char-name">{info['nama'].split()[0]}</div>
          <div class="char-role">{jabatan}</div>
        </div>
        """

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        background: transparent;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #e6edf3;
        overflow: hidden;
      }}
      .office-stage {{
        position: relative;
        width: 100%;
        height: 230px;
        background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        display: flex;
        justify-content: space-around;
        align-items: flex-end;
        padding-bottom: 20px;
      }}
      .lantai {{
        position: absolute;
        bottom: 0;
        width: 100%;
        height: 24px;
        background: repeating-linear-gradient(90deg, #21262d, #21262d 48px, #1c2128 48px, #1c2128 96px);
        border-top: 2px solid #30363d;
        z-index: 1;
      }}
      .decor-plant {{
        position: absolute;
        bottom: 24px;
        left: 14px;
        font-size: 24px;
        z-index: 2;
      }}
      .station {{
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        z-index: 2;
        width: 18%;
      }}
      .avatar-wrap {{
        position: relative;
        width: 54px;
        height: 54px;
        border-radius: 50%;
        background: #21262d;
        border: 2px solid #388bfd;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
      }}
      .job-badge {{
        position: absolute;
        bottom: -2px;
        right: -2px;
        font-size: 12px;
        background: #161b22;
        border-radius: 50%;
        border: 1px solid #30363d;
        width: 18px;
        height: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
      }}
      .desk {{
        width: 76px;
        height: 10px;
        background: #30363d;
        border-radius: 3px;
        margin-top: 4px;
        position: relative;
      }}
      .monitor {{
        position: absolute;
        top: -14px;
        left: 27px;
        width: 22px;
        height: 14px;
        background: #0d1117;
        border: 1px solid #484f58;
        border-radius: 2px;
      }}
      .status-bubble {{
        font-size: 10px;
        margin-top: 4px;
        background: #21262d;
        border: 1px solid #30363d;
        padding: 2px 6px;
        border-radius: 8px;
        color: #8b949e;
        white-space: nowrap;
      }}
      .char-name {{
        font-size: 11px;
        font-weight: 700;
        margin-top: 3px;
        color: #f0f6fc;
      }}
      .char-role {{
        font-size: 9px;
        color: #8b949e;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 85px;
      }}

      /* ANIMASI SANTAI */
      .idle .avatar-wrap {{
        animation: nafas 3s infinite ease-in-out;
      }}
      @keyframes nafas {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-4px); }}
      }}

      /* ANIMASI BEKERJA */
      .working .avatar-wrap {{
        border-color: #3fb950 !important;
        box-shadow: 0 0 14px rgba(63, 185, 80, 0.7);
        animation: mengetik 0.2s infinite alternate !important;
      }}
      .working .monitor {{
        background: #3fb950;
        box-shadow: 0 0 10px #3fb950;
      }}
      .working .status-bubble {{
        background: rgba(63, 185, 80, 0.2);
        color: #3fb950;
        font-weight: bold;
        border-color: #3fb950;
      }}
      @keyframes mengetik {{
        0% {{ transform: translateY(0) rotate(-1deg); }}
        100% {{ transform: translateY(-3px) rotate(1deg); }}
      }}

      /* ANIMASI MENONTON */
      .watching .avatar-wrap {{
        filter: grayscale(0.2);
        animation: intip 2s infinite ease-in-out !important;
      }}
      .watching .status-bubble {{
        color: #58a6ff;
        border-color: #388bfd;
      }}
      @keyframes intip {{
        0%, 100% {{ transform: scale(0.96); }}
        50% {{ transform: scale(1.02) translateX(2px); }}
      }}
    </style>
    </head>
    <body>
      <div class="office-stage">
        <div class="decor-plant">🪴</div>
        <div class="lantai"></div>
        {kartu_karakter_html}
      </div>
    </body>
    </html>
    """
    components.html(html_code, height=245)

def panggil_karyawan(model_id: str, system_prompt: str, pesan_user: str) -> str:
    api_key = st.session_state.get("router9_api_key", "").strip() or API_KEY_AWAL
    if not api_key:
        return "⚠️ Galat: Kunci API Router9 belum terdeteksi. Masukkan API Key di bilah samping atau Secrets."

    headers = {
        "Authorization": f"Bearer {api_key}",
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
        elif res.status_code == 429:
            return "⏳ Galat 429: Batas frekuensi panggilan tercapai. Tunggu sejenak hingga reset kuota."
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
        st.caption(f"Model: `{info['nama']}`\nAktivitas: *{info['santai_text']}*\n\n{info['deskripsi']}")
        st.markdown("---")
        
    api_input = st.text_input(
        "Ganti API Key Router9 (Opsional):",
        value=st.session_state["router9_api_key"],
        type="password"
    )
    if api_input and api_input != st.session_state["router9_api_key"]:
        st.session_state["router9_api_key"] = api_input.strip()

# --- AREA UTAMA ---
st.title("💼 Ruang Manajer: Rapat Tim Pengembang AI")
st.markdown("Instruksikan 5 model AI sekaligus untuk merancang, mengode, dan mengaudit sistem absensi Anda.")

# Panggung Animasi Kantor Virtual
wadah_animasi = st.empty()
with wadah_animasi:
    render_kantor_animasi(None)

mode_kerja = st.radio(
    "Pilih Format Kerja:",
    ["Meja Spesifik (Konsultasi 1 Karyawan)", "Rapat Tim Penuh (5 Karyawan Menjawab Serentak)"],
    horizontal=True
)

# Tampilkan pilihan karyawan tepat di bawah radio button jika mode Meja Spesifik
pilihan_divisi = None
if mode_kerja == "Meja Spesifik (Konsultasi 1 Karyawan)":
    pilihan_divisi = st.selectbox("Pilih Karyawan yang Bertugas:", list(DIVISI.keys()))

instruksi = st.text_area(
    "Instruksi Pekerjaan / Fitur yang Ingin Dibuat:",
    height=140,
    placeholder="Ketik instruksi pekerjaan Anda di sini..."
)

tombol_kirim = st.button("🚀 Kirim Instruksi ke Meja Kerja", type="primary", use_container_width=True)

# 1. EKSEKUSI MODE MEJA SPESIFIK
if mode_kerja == "Meja Spesifik (Konsultasi 1 Karyawan)":
    if tombol_kirim and instruksi.strip():
        karyawan = DIVISI[pilihan_divisi]
        
        with wadah_animasi:
            render_kantor_animasi(pilihan_divisi)
            
        with st.spinner(f"Sedang dikerjakan oleh {karyawan['nama']} ({pilihan_divisi})..."):
            jawaban = panggil_karyawan(karyawan["model"], karyawan["system"], instruksi)
            
        with wadah_animasi:
            render_kantor_animasi(None)
            
        st.markdown(f"### 📋 Hasil Kerja: {karyawan['icon']} {pilihan_divisi} (`{karyawan['nama']}`)")
        st.markdown(jawaban)

# 2. EKSEKUSI MODE RAPAT TIM PENUH
else:
    if tombol_kirim and instruksi.strip():
        with wadah_animasi:
            render_kantor_animasi("SEMUA")
            
        st.markdown("### 📊 Hasil Rapat Lengkap 5 Divisi")
        kolom_tim = st.columns(len(DIVISI))
        
        for idx, (jabatan, info) in enumerate(DIVISI.items()):
            with kolom_tim[idx]:
                st.markdown(f"#### {info['icon']} {info['nama']}")
                st.caption(f"**{jabatan}**")
                with st.spinner("Menyusun respons..."):
                    hasil = panggil_karyawan(info["model"], info["system"], instruksi)
                st.markdown(hasil)
                
        with wadah_animasi:
            render_kantor_animasi(None)
