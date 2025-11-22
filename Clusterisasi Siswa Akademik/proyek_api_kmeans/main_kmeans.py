import joblib
import pandas as pd
from fastapi import FastAPI, UploadFile, File
import uvicorn
import io
from fastapi.middleware.cors import CORSMiddleware

print("Mencoba memuat model...")
# 1. Load Model & Scaler (SAMA)
try:
    model = joblib.load("model_kmeans_siswa.pkl")
    scaler = joblib.load("scaler_siswa.pkl")
    print("Model K-Means dan Scaler berhasil di-load.")
except Exception as e:
    print(f"Error pas load model/scaler: {e}")
    model = None
    scaler = None

# Mapping klaster (SAMA)
cluster_mapping = {
    0: "Cluster A (Si Kutu Buku)",
    1: "Cluster B (Si Aktivis Lomba)",
    2: "Cluster C (Si Rata-Rata)"
}

app = FastAPI(title="API Klasterisasi Siswa (Versi Upload)")

# (PENTING) Tambah CORS (SAMA)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. (PENTING) Tentukan Kolom yang Dibutuhin Model
# Ini harus SAMA PERSIS dengan yang lu pake di notebook training
# (Urutannya juga harus SAMA PERSIS kayak pas 'scaler.fit_transform')
FITUR_MODEL = [
    'Nilai_MTK', 'Nilai_Fisika', 'Nilai_Kimia', 
    'Nilai_Indo', 'Absensi', 'Keikutsertaan_Lomba'
]

# (PENTING) Tentukan nama kolom identitas siswa
KOLOM_NAMA_SISWA = "Nama_Siswa" # Nanti di CSV-nya harus ada kolom ini

# 3. Bikin 'Endpoint' BARU: /upload_dan_klasterisasi
@app.post("/upload_dan_klasterisasi")
async def upload_dan_klasterisasi(file_csv: UploadFile = File(...)):
    
    if model is None or scaler is None:
        return {"error": "Model/Scaler tidak siap."}

    # 4. Baca file CSV yang di-upload
    try:
        # Baca file dari 'upload'
        contents = await file_csv.read()
        # Ubah jadi format yang bisa dibaca pandas
        df = pd.read_csv(io.BytesIO(contents))
        print(f"Menerima file {file_csv.filename}, {len(df)} baris data.")
    except Exception as e:
        return {"error": f"Gagal membaca file CSV: {e}"}

    # 5. Cek Kolom Wajib
    # Cek dulu apakah kolom nama dan semua kolom fitur ada di file
    kolom_wajib = [KOLOM_NAMA_SISWA] + FITUR_MODEL
    kolom_yg_hilang = [kol for kol in kolom_wajib if kol not in df.columns]
    
    if kolom_yg_hilang:
        return {"error": f"File CSV lu kurang kolom ini: {kolom_yg_hilang}"}

    # 6. Preprocessing & Prediksi (SAMA, tapi versi 'batch')
    try:
        # Ambil cuma data fitur yang mau di-scale
        data_fitur = df[FITUR_MODEL]
        
        # (WAJIB) Scale data
        data_input_scaled = scaler.transform(data_fitur)
        
        # Prediksi semua data sekaligus
        prediksi_klaster_ids = model.predict(data_input_scaled)
        
        # Tambahin hasil prediksi ke DataFrame
        df['Cluster_ID'] = prediksi_klaster_ids
        df['Deskripsi_Cluster'] = df['Cluster_ID'].map(cluster_mapping)
        
        print("Prediksi selesai. Mengelompokkan hasil...")

        # 7. (BARU) Kelompokkan nama siswa
        hasil_akhir = {}
        # 'groupby' berdasarkan 'Deskripsi_Cluster' yang udah kita map
        for nama_klaster, group in df.groupby('Deskripsi_Cluster'):
            # Ambil semua nama siswa di grup itu
            nama_siswa_di_klaster = group[KOLOM_NAMA_SISWA].tolist()
            # Masukin ke JSON
            hasil_akhir[nama_klaster] = nama_siswa_di_klaster
            
        # 8. Kirim balik JSON berisi grup
        return hasil_akhir
        
    except Exception as e:
        return {"error": f"Error pas prediksi: {e}"}

@app.get("/")
def read_root():
    return {"message": "API Klasterisasi K-Means v2.0 (Upload)"}