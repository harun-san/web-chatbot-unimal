import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# 1. Inisialisasi Sastrawi Stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# 2. Data Pelatihan (Dataset NLP yang Diperluas)
data = [
    # --- Intent: Salam & Sapaan ---
    {"text": "halo", "intent": "salam_sapa"},
    {"text": "hai bot", "intent": "salam_sapa"},
    {"text": "selamat pagi", "intent": "salam_sapa"},
    {"text": "selamat siang", "intent": "salam_sapa"},
    {"text": "assalamualaikum", "intent": "salam_sapa"},
    {"text": "p", "intent": "salam_sapa"},
    {"text": "bot bisa bantu saya", "intent": "salam_sapa"},

    # --- Intent: Jadwal Kuliah ---
    {"text": "kapan jadwal kuliah rilis", "intent": "jadwal_kuliah"},
    {"text": "dimana saya bisa melihat jadwal semester ini", "intent": "jadwal_kuliah"},
    {"text": "jadwal kelas pengganti", "intent": "jadwal_kuliah"},
    {"text": "cara cek jadwal di siakad", "intent": "jadwal_kuliah"},
    {"text": "jadwal mata kuliah hari ini", "intent": "jadwal_kuliah"},
    {"text": "jadwal praktikum kapan keluar", "intent": "jadwal_kuliah"},
    {"text": "info jadwal kuliah", "intent": "jadwal_kuliah"},

    # --- Intent: Biaya UKT & Pembayaran ---
    {"text": "berapa biaya ukt semester ini", "intent": "biaya_ukt"},
    {"text": "bagaimana cara bayar ukt", "intent": "biaya_ukt"},
    {"text": "kapan batas akhir pembayaran ukt", "intent": "biaya_ukt"},
    {"text": "cara cicil ukt", "intent": "biaya_ukt"},
    {"text": "cara mendapatkan keringanan ukt", "intent": "biaya_ukt"},
    {"text": "bayar ukt bisa lewat bank apa saja", "intent": "biaya_ukt"},
    {"text": "kenapa tagihan ukt saya belum muncul", "intent": "biaya_ukt"},
    {"text": "cara bayar spp", "intent": "biaya_ukt"},

    # --- Intent: Informasi Beasiswa ---
    {"text": "ada info beasiswa terbaru tidak", "intent": "info_beasiswa"},
    {"text": "syarat daftar beasiswa kip kuliah", "intent": "info_beasiswa"},
    {"text": "cara mengajukan beasiswa bank indonesia", "intent": "info_beasiswa"},
    {"text": "syarat daftar beasiswa lpdp untuk lulusan s1", "intent": "info_beasiswa"},
    {"text": "info kuota dan persiapan beasiswa lpdp", "intent": "info_beasiswa"},
    {"text": "kapan pendaftaran beasiswa dibuka", "intent": "info_beasiswa"},
    {"text": "pengumuman lolos beasiswa dimana", "intent": "info_beasiswa"},

    # --- Intent: KRS & KHS (Kartu Rencana/Hasil Studi) ---
    {"text": "bagaimana cara isi krs", "intent": "pengisian_krs"},
    {"text": "kapan jadwal krs dibuka", "intent": "pengisian_krs"},
    {"text": "jadwal isi krs untuk mahasiswa semester 4", "intent": "pengisian_krs"},
    {"text": "cara konsultasi dengan dosen pembimbing akademik", "intent": "pengisian_krs"},
    {"text": "kenapa krs saya belum disetujui dpa", "intent": "pengisian_krs"},
    {"text": "cara melihat nilai khs", "intent": "pengisian_krs"},
    {"text": "cara ubah krs batal tambah mata kuliah", "intent": "pengisian_krs"},
    {"text": "cara perbaikan nilai", "intent": "pengisian_krs"},

    # --- Intent: Syarat Skripsi & Tugas Akhir ---
    {"text": "apa syarat pengajuan judul skripsi", "intent": "syarat_skripsi"},
    {"text": "berapa sks minimal untuk daftar skripsi", "intent": "syarat_skripsi"},
    {"text": "prosedur daftar seminar proposal", "intent": "syarat_skripsi"},
    {"text": "cara mengajukan dosen pembimbing skripsi", "intent": "syarat_skripsi"},
    {"text": "kapan jadwal sidang skripsi", "intent": "syarat_skripsi"},
    {"text": "syarat bebas pustaka dan lab untuk lulus", "intent": "syarat_skripsi"},

    # --- Intent: Info Program Studi / Fakultas ---
    {"text": "dimana letak lab teknik informatika", "intent": "info_prodi"},
    {"text": "jam kerja tata usaha fakultas teknik", "intent": "info_prodi"},
    {"text": "siapa kaprodi informatika sekarang", "intent": "info_prodi"},
    {"text": "lokasi ruang dekanat", "intent": "info_prodi"},
    {"text": "dimana gedung perkuliahan", "intent": "info_prodi"},

    # --- Intent: Cuti Akademik ---
    {"text": "bagaimana cara mengajukan cuti kuliah", "intent": "cuti_akademik"},
    {"text": "syarat cuti akademik", "intent": "cuti_akademik"},
    {"text": "batas waktu pengajuan cuti semester ini", "intent": "cuti_akademik"},
    {"text": "apakah cuti akademik harus bayar ukt", "intent": "cuti_akademik"}
]

# 3. Preprocessing (Stemming)
print(f"Memulai pelatihan NLP dengan {len(data)} data sampel...")
print("Melakukan stemming pada data teks (proses ini mungkin memakan waktu sebentar)...")
X_raw = [item["text"] for item in data]
y = [item["intent"] for item in data]
X_stemmed = [stemmer.stem(text) for text in X_raw]

# 4. Ekstraksi Fitur (TF-IDF)
print("Ekstraksi fitur TF-IDF...")
vectorizer = TfidfVectorizer(ngram_range=(1, 2)) # Menggunakan Unigram & Bigram agar lebih akurat
X_vectorized = vectorizer.fit_transform(X_stemmed)

# 5. Pelatihan Model (Naive Bayes)
print("Melatih model MultinomialNB...")
model = MultinomialNB(alpha=0.1) # Alpha disesuaikan agar smoothing lebih baik pada dataset kecil
model.fit(X_vectorized, y)

# 6. Simpan Model & Vectorizer
with open("chatbot_model.pkl", "wb") as f:
    pickle.dump(model, f)
    
with open("chatbot_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Pelatihan selesai! File 'chatbot_model.pkl' dan 'chatbot_vectorizer.pkl' berhasil diperbarui.")