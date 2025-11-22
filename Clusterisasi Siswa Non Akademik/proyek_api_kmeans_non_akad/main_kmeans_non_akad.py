import joblib
import pandas as pd
from fastapi import FastAPI, UploadFile, File
import uvicorn
import io
from fastapi.middleware.cors import CORSMiddleware

print("Mencoba memuat model NON-AKADEMIK...")
# 1. Load Model & Scaler
try:
    model = joblib.load("model_kmeans_non_akad.pkl")
    scaler = joblib.load("scaler_non_akad.pkl")
    print("Model K-Means dan Scaler NON-AKADEMIK berhasil di-load.")
except Exception as e:
    print(f"Error pas load model/scaler: {e}")
    model = None
    scaler = None

# Mapping klaster (Tebakan, nanti bisa dicek)
cluster_mapping = {
    0: "Cluster A (Si Organisator)",
    1: "Cluster B (Si Atlet/Seniman)",
    2: "Cluster C (Si Pasif)"
}

app = FastAPI(title="API Klasterisasi Siswa NON-AKADEMIK")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# 2. Tentukan Kolom yang Dibutuhin Model
FITUR_MODEL = [
    'Kehadiran_Ekskul', 'Jumlah_Sertifikat', 
    'Tingkat_Prestasi', 'Jabatan_Organisasi'
]
KOLOM_NAMA_SISWA = "Nama_Siswa" # Wajib ada di CSV yg di-upload

# 3. Bikin 'Endpoint' BARU: /upload_klasterisasi_non_akad
@app.post("/upload_klasterisasi_non_akad")
async def upload_klasterisasi_non_akad(file_csv: UploadFile = File(...)):
    
    if model is None or scaler is None:
        return {"error": "Model/Scaler tidak siap."}

    # 4. Baca file CSV
    try:
        contents = await file_csv.read()
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        return {"error": f"Gagal membaca file CSV: {e}"}

    # 5. Cek Kolom Wajib
    kolom_wajib = [KOLOM_NAMA_SISWA] + FITUR_MODEL
    kolom_yg_hilang = [kol for kol in kolom_wajib if kol not in df.columns]
    
    if kolom_yg_hilang:
        return {"error": f"File CSV lu kurang kolom ini: {kolom_yg_hilang}"}

    # 6. Preprocessing & Prediksi
    try:
        data_fitur = df[FITUR_MODEL]
        data_input_scaled = scaler.transform(data_fitur)
        prediksi_klaster_ids = model.predict(data_input_scaled)
        
        df['Cluster_ID'] = prediksi_klaster_ids
        df['Deskripsi_Cluster'] = df['Cluster_ID'].map(cluster_mapping)
        
        # 7. Kelompokkan nama siswa
        hasil_akhir = {}
        for nama_klaster, group in df.groupby('Deskripsi_Cluster'):
            nama_siswa_di_klaster = group[KOLOM_NAMA_SISWA].tolist()
            hasil_akhir[nama_klaster] = nama_siswa_di_klaster
            
        # 8. Kirim balik JSON berisi grup
        return hasil_akhir
        
    except Exception as e:
        return {"error": f"Error pas prediksi: {e}"}

@app.get("/")
def read_root():
    return {"message": "API Klasterisasi K-Means v2.0 NON-AKADEMIK"}