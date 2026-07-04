import pickle
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import numpy as np

# Inisialisasi FastAPI
app = FastAPI(title="Akademik Chatbot API")

# Konfigurasi CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Muat Model dan Vectorizer
print("Memuat model NLP...")
with open("chatbot_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("chatbot_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Sastrawi Stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Respons Statis berdasarkan Intent
RESPONSES = {
    "salam_sapa": "Halo! Saya Asisten Akademik UNIMAL. Ada yang bisa saya bantu terkait jadwal, KRS, UKT, Beasiswa, atau info akademik lainnya?",
    
    "jadwal_kuliah": "Jadwal kuliah lengkap dapat Anda lihat melalui portal akademik (SIAKAD) di menu 'Jadwal Mahasiswa'. Pastikan Anda sudah memvalidasi KRS agar jadwal muncul.",
    
    "biaya_ukt": "Pembayaran UKT/SPP dapat dilakukan setiap awal semester via Bank BSI atau Bank Aceh. Tagihan, kode bayar, dan panduan keringanan UKT dapat diakses langsung melalui dashboard SIAKAD Anda.",
    
    "info_beasiswa": "UNIMAL mengelola berbagai beasiswa seperti KIP-Kuliah, Beasiswa BI, dan Beasiswa BSI. Selain itu, bagi mahasiswa yang ingin melanjutkan studi pascasarjana, sangat disarankan mulai mempersiapkan syarat beasiswa LPDP, seperti sertifikat bahasa asing. Info lengkap pantau terus di Mading Fakultas atau website kemahasiswaan.",
    
    "pengisian_krs": "Pengisian Kartu Rencana Studi (KRS) dilakukan melalui akun SIAKAD. Silakan pilih mata kuliah sesuai paket semester berjalan (misalnya semester 4) dan pastikan untuk menghubungi Dosen Pembimbing Akademik (DPA) Anda untuk meminta persetujuan validasi.",
    
    "syarat_skripsi": "Syarat umum pengajuan proposal Skripsi/Tugas Akhir: telah menyelesaikan minimal 120-138 SKS (tergantung prodi), lulus mata kuliah Metodologi Penelitian, IPK memenuhi syarat, dan tidak ada nilai E. Konsultasikan dengan Kaprodi untuk detail lebih lanjut.",
    
    "info_prodi": "Untuk informasi spesifik mengenai layanan fasilitas fakultas (seperti peminjaman lab Teknik Informatika atau jadwal tata usaha), Anda bisa mengunjungi ruang administrasi di masing-masing gedung fakultas pada hari kerja pukul 08.00 - 16.00 WIB.",
    
    "cuti_akademik": "Pengajuan cuti akademik dapat dilakukan paling lambat minggu kedua perkuliahan aktif. Anda harus mengisi form cuti di BAAK dan mendapat tanda tangan persetujuan dari Dosen Pembimbing Akademik dan Dekan."
}

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    # 1. Preprocessing Input
    clean_text = stemmer.stem(req.message.lower())
    
    # 2. Vektorisasi
    text_vec = vectorizer.transform([clean_text])
    
    # 3. Prediksi Intent & Probabilitas (Confidence Score)
    predicted_intent = model.predict(text_vec)[0]
    probabilities = model.predict_proba(text_vec)[0]
    confidence = np.max(probabilities)
    
    # 4. Thresholding (Jika bot tidak yakin dengan pertanyaan)
    # Jika tingkat keyakinan (confidence) di bawah 30%, berikan jawaban default
    if confidence < 0.30:
        bot_reply = "Maaf, pertanyaan Anda di luar cakupan informasi saya atau kurang spesifik. Silakan gunakan kata kunci lain seputar Jadwal Kuliah, KRS, UKT, Skripsi, atau Beasiswa."
        predicted_intent = "unknown"
    else:
        bot_reply = RESPONSES.get(predicted_intent, "Terjadi kesalahan dalam mengambil respons.")
    
    return {
        "intent": predicted_intent,
        "confidence": round(float(confidence), 2),
        "response": bot_reply
    }