# E-Commerce Data Analysis Dashboard

## Setup Environment

### Cara Menjalankan

1. **Instalasi dependency**
   - Menggunakan `pip`:

     ```bash
     pip install -r requirements.txt
     ```

   - Atau dengan pipenv (lihat `Pipfile`):
     ```bash
     pipenv install --dev
     pipenv shell
     ```

2. **Jalankan dashboard Streamlit** di terminal:

   ```bash
   streamlit run dashboard/dashboard.py
   ```

   Atau masuk ke direktori `dashboard` dulu:

   ```bash
   cd dashboard
   streamlit run dashboard.py
   ```

## Deskripsi Tugas

Dashboard ini dibuat sebagai bagian akhir proyek analisa E-Commerce Public Dataset.

### Pertanyaan Bisnis yang Dijawab

- Pertanyaan 1: Kategori produk mana yang memiliki jumlah penjualan tertinggi? Bagaimana distribusi pendapatan berdasarkan harga?
- Pertanyaan 2: Berapa rata-rata pengeluaran pelanggan?
- Pertanyaan 3: State mana yang memiliki jumlah pembeli terbanyak?

## Folder Structure

- `dashboard/` : File dashboard Streamlit dan dataset ekspor (`main_data.csv`)
- `data/` : Sumber kumpulan data mentah
- `notebook.ipynb` : Notebook proses eksplorasi dan analisis
- `requirements.txt` : File berisi semua library yang diperlukan
