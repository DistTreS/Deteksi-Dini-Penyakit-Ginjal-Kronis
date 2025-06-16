# ❤️ Chronic Kidney Disease Risk Detection System

Sistem deteksi dini risiko penyakit ginjal kronis menggunakan Random Forest Algorithm.

## 🚀 Features

- **Manual Input**: Input data pasien satu per satu
- **Batch Processing**: Upload file Excel untuk analisis massal
- **Risk Categorization**: 4 level risiko (Minimal, Rendah, Sedang, Tinggi)
- **Interactive Visualization**: Gauge chart dan distribusi risiko
- **Export Results**: Download hasil dalam format Excel/CSV

## 📊 Model Performance

- **Algorithm**: Random Forest Classifier
- **Accuracy**: 92%
- **Recall for High Risk**: 99% (excellent for medical screening)

## 🏥 Medical Features Used

1. Age (Usia)
2. Gender (Jenis Kelamin)
3. BMI (Body Mass Index)
4. Systolic Blood Pressure (Tekanan Darah Sistolik)
5. Diastolic Blood Pressure (Tekanan Darah Diastolik)
6. HbA1c (Hemoglobin A1c)
7. Serum Creatinine
8. GFR (Glomerular Filtration Rate)
9. Hemoglobin Levels
10. Total Cholesterol

## 🎯 Risk Categories

- **🔴 RISIKO TINGGI** (≥80%): Segera konsultasi dokter spesialis
- **🟡 RISIKO SEDANG** (60-79%): Pemeriksaan lanjutan dalam 1-2 minggu
- **🟢 RISIKO RENDAH** (40-59%): Pantau kondisi kesehatan rutin
- **🟢 RISIKO MINIMAL** (<40%): Pertahankan gaya hidup sehat

## ⚠️ Medical Disclaimer

**PENTING**: Hasil prediksi ini hanya untuk screening awal dan TIDAK menggantikan diagnosa medis profesional. Selalu konsultasikan dengan dokter spesialis untuk diagnosa dan perawatan yang tepat.

## 🛠️ Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📋 Usage

### Manual Input
1. Pilih "Input Manual (Satu Pasien)"
2. Isi semua parameter medis
3. Klik "Analisis Risiko"
4. Lihat hasil dan rekomendasi

### Batch Processing
1. Pilih "Upload File Excel (Batch)"
2. Download template Excel
3. Isi data pasien sesuai template
4. Upload file dan analisis
5. Download hasil dalam Excel/CSV

## 🏗️ Technical Details

- **Framework**: Streamlit
- **ML Library**: Scikit-learn
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy

---
*Developed for early detection of chronic Chronic Kidney Disease risk*
