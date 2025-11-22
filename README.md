# 📊 Student Performance Clustering

> **Data Mining project using K-Means Clustering to segment students based on Academic and Non-Academic achievements.**
> *Strategi personalisasi pendidikan berbasis data.*

![Cluster Visualization]

## 🚀 Overview
Proyek ini bertujuan untuk membantu pihak sekolah dalam memetakan profil siswa. Dengan menggunakan algoritma **K-Means Clustering**, sistem mengelompokkan siswa ke dalam beberapa segmen berdasarkan nilai rapor (Akademik) dan prestasi ekstrakurikuler (Non-Akademik).

Hasil klasterisasi ini digunakan untuk memberikan rekomendasi penanganan yang lebih personal (misal: siswa berprestasi akademik tapi kurang aktif, atau sebaliknya).

## 📂 Project Structure
Repository ini terdiri dari dua modul analisis terpisah:
1.  **Clusterisasi Siswa Akademik:** Fokus pada nilai mata pelajaran utama.
2.  **Clusterisasi Siswa Non-Akademik:** Fokus pada skor kegiatan ekstrakurikuler dan soft skills.

## ⚙️ Methodology
* **Data Preprocessing:** Cleaning data, handling missing values, dan normalisasi data (MinMax Scaling).
* **Elbow Method:** Digunakan untuk menentukan jumlah klaster (K) yang paling optimal.
* **K-Means Algorithm:** Mengelompokkan data siswa berdasarkan kedekatan karakteristik (Euclidean Distance).
* **Visualization:** Memvisualisasikan sebaran klaster menggunakan Scatter Plot 2D/3D.

## 🛠️ Tech Stack
* **Language:** Python
* **Libraries:** Pandas, NumPy, Scikit-Learn
* **Visualization:** Matplotlib, Seaborn
* **Tools:** Jupyter Notebook

## 📦 How to Run

1.  **Clone Repository**
    ```bash
    git clone [https://github.com/username-lu/student-performance-clustering.git](https://github.com/username-lu/student-performance-clustering.git)
    cd student-performance-clustering
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Notebook**
    Jalankan Jupyter Notebook untuk melihat proses analisis:
    ```bash
    jupyter notebook
    ```
    Buka file `.ipynb` di dalam folder masing-masing kategori.

## 🤝 Contact
Dibuat oleh **Kay** - *Data Scientist & AI Enthusiast*.
