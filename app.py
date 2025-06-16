import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pickle
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Chronic Kidney Disease Risk Detector",
    page_icon="🫘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load model and features
@st.cache_resource
def load_model():
    try:
        model = joblib.load('heart_disease_model.joblib')
        features = joblib.load('selected_features.joblib')
        return model, features
    except:
        st.error("❌ Model files not found! Please ensure model files are in the same directory.")
        return None, None

def interpret_risk(probability):
    """Interpret risk level based on probability"""
    risk_prob = probability[1]  # Probabilitas berisiko
    
    if risk_prob >= 0.8:
        return "RISIKO TINGGI", "Segera konsultasi dokter spesialis Ginjal", "🔴", "#FF4B4B"
    elif risk_prob >= 0.6:
        return "RISIKO SEDANG", "Disarankan pemeriksaan lanjutan dalam 1-2 minggu", "🟡", "#FFB800"
    elif risk_prob >= 0.4:
        return "RISIKO RENDAH", "Pantau kondisi kesehatan secara rutin", "🟢", "#00D4AA"
    else:
        return "RISIKO MINIMAL", "Pertahankan gaya hidup sehat", "🟢", "#00D4AA"

def create_gauge_chart(probability):
    """Create gauge chart for risk visualization"""
    risk_percentage = probability[1] * 100
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risk Level (%)"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "#00D4AA"},
                {'range': [40, 60], 'color': "#FFB800"},
                {'range': [60, 80], 'color': "#FF8C00"},
                {'range': [80, 100], 'color': "#FF4B4B"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def validate_input_data(data):
    """Validate input data ranges"""
    validation_rules = {
        'Age': (0, 120, 'Usia harus antara 0-120 tahun'),
        'BMI': (10, 50, 'BMI harus antara 10-50'),
        'SystolicBP': (70, 250, 'Tekanan sistolik harus antara 70-250 mmHg'),
        'DiastolicBP': (40, 150, 'Tekanan diastolik harus antara 40-150 mmHg'),
        'HbA1c': (3, 15, 'HbA1c harus antara 3-15%'),
        'SerumCreatinine': (0.3, 10, 'Serum Creatinine harus antara 0.3-10 mg/dL'),
        'GFR': (5, 150, 'GFR harus antara 5-150 mL/min/1.73m²'),
        'HemoglobinLevels': (5, 20, 'Hemoglobin harus antara 5-20 g/dL'),
        'CholesterolTotal': (100, 500, 'Kolesterol total harus antara 100-500 mg/dL')
    }
    
    errors = []
    for col, (min_val, max_val, message) in validation_rules.items():
        if col in data.columns:
            invalid_rows = (data[col] < min_val) | (data[col] > max_val)
            if invalid_rows.any():
                errors.append(f"{message} (ditemukan {invalid_rows.sum()} data tidak valid)")
    
    return errors

# Load model
model, features = load_model()

if model is None or features is None:
    st.stop()

# Header
st.title("🫘 Chronic Kidney Disease Risk Detection System")
st.markdown("### Sistem Deteksi Dini Risiko Penyakit Ginjal Kronis")
st.markdown("---")

# Sidebar
st.sidebar.header("📊 Navigation")
mode = st.sidebar.selectbox(
    "Pilih Mode Input:",
    ["🏥 Input Manual (Satu Pasien)", "📋 Upload File Excel (Batch)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Informasi")
st.sidebar.info(
    """
    **Fitur yang Digunakan:**
    - Usia (Age)
    - Gender (Jenis Kelamin)
    - BMI (Body Mass Index)
    - Tekanan Darah Sistolik
    - Tekanan Darah Diastolik
    - HbA1c (Gula Darah)
    - Serum Creatinine
    - GFR (Fungsi Ginjal)
    - Hemoglobin
    - Kolesterol Total
    """
)

# Mode 1: Manual Input
if mode == "🏥 Input Manual (Satu Pasien)":
    st.header("🏥 Input Data Pasien Manual")
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Data Demografis")
        age = st.number_input("Usia (tahun)", min_value=0, max_value=120, value=50)
        gender = st.selectbox("Jenis Kelamin", ["Male", "Female"])
        bmi = st.number_input("BMI (Body Mass Index)", min_value=10.0, max_value=50.0, value=25.0, step=0.1)
        
        st.subheader("Tekanan Darah")
        systolic_bp = st.number_input("Tekanan Sistolik (mmHg)", min_value=70, max_value=250, value=120)
        diastolic_bp = st.number_input("Tekanan Diastolik (mmHg)", min_value=40, max_value=150, value=80)
    
    with col2:
        st.subheader("Parameter Lab")
        hba1c = st.number_input("HbA1c (%)", min_value=3.0, max_value=15.0, value=5.5, step=0.1)
        serum_creatinine = st.number_input("Serum Creatinine (mg/dL)", min_value=0.3, max_value=10.0, value=1.0, step=0.1)
        gfr = st.number_input("GFR (mL/min/1.73m²)", min_value=5, max_value=150, value=90)
        hemoglobin = st.number_input("Hemoglobin (g/dL)", min_value=5.0, max_value=20.0, value=13.0, step=0.1)
        cholesterol = st.number_input("Kolesterol Total (mg/dL)", min_value=100, max_value=500, value=200)
    
    # Convert gender to numeric
    gender_numeric = 1 if gender == "Male" else 0
    
    # Create input dataframe
    input_data = pd.DataFrame({
        'Age': [age],
        'Gender': [gender_numeric],
        'BMI': [bmi],
        'SystolicBP': [systolic_bp],
        'DiastolicBP': [diastolic_bp],
        'HbA1c': [hba1c],
        'SerumCreatinine': [serum_creatinine],
        'GFR': [gfr],
        'HemoglobinLevels': [hemoglobin],
        'CholesterolTotal': [cholesterol]
    })
    
    # Predict button
    if st.button("🔍 Analisis Risiko", type="primary", use_container_width=True):
        try:
            # Make prediction
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0]
            
            # Interpret results
            risk_level, recommendation, emoji, color = interpret_risk(probability)
            
            st.markdown("---")
            st.header("📋 Hasil Analisis")
            
            # Create three columns for results
            result_col1, result_col2, result_col3 = st.columns([1, 2, 1])
            
            with result_col1:
                st.metric(
                    label="Status Risiko",
                    value=f"{emoji} {risk_level}",
                    delta=f"{probability[1]*100:.1f}% Confidence"
                )
            
            with result_col2:
                # Gauge chart
                fig = create_gauge_chart(probability)
                st.plotly_chart(fig, use_container_width=True)
            
            with result_col3:
                st.metric(
                    label="Probabilitas Tidak Berisiko",
                    value=f"{probability[0]*100:.1f}%"
                )
                st.metric(
                    label="Probabilitas Berisiko",
                    value=f"{probability[1]*100:.1f}%"
                )
            
            # Recommendation
            st.markdown(f"### 💡 Rekomendasi")
            if probability[1] >= 0.8:
                st.error(f"🚨 **{risk_level}**: {recommendation}")
            elif probability[1] >= 0.6:
                st.warning(f"⚠️ **{risk_level}**: {recommendation}")
            else:
                st.success(f"✅ **{risk_level}**: {recommendation}")
            
            # Display input summary
            with st.expander("📊 Ringkasan Data Input"):
                display_data = input_data.copy()
                display_data['Gender'] = 'Laki-laki' if gender_numeric == 1 else 'Perempuan'
                st.dataframe(display_data.T, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error dalam prediksi: {str(e)}")

# Mode 2: Excel Upload
else:
    st.header("📋 Upload File Excel untuk Analisis Batch")
    
    # Download template
    st.subheader("📥 Download Template Excel")
    
    # Create template dataframe
    template_data = {
        'Age': [45, 55, 35],
        'Gender': [1, 0, 1],  # 1=Male, 0=Female
        'BMI': [25.5, 28.2, 22.1],
        'SystolicBP': [130, 140, 120],
        'DiastolicBP': [85, 90, 75],
        'HbA1c': [6.2, 7.1, 5.4],
        'SerumCreatinine': [1.1, 1.3, 0.9],
        'GFR': [85, 75, 95],
        'HemoglobinLevels': [13.5, 12.8, 14.2],
        'CholesterolTotal': [220, 250, 180]
    }
    
    template_df = pd.DataFrame(template_data)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.dataframe(template_df, use_container_width=True)
    with col2:
        # Convert to Excel bytes
        from io import BytesIO
        excel_buffer = BytesIO()
        template_df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        
        st.download_button(
            label="📥 Download Template",
            data=excel_buffer.getvalue(),
            file_name="heart_disease_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    st.info("💡 **Catatan**: Gender: 1 = Laki-laki, 0 = Perempuan")
    
    # File upload
    st.subheader("📤 Upload File Excel")
    uploaded_file = st.file_uploader(
        "Pilih file Excel (.xlsx atau .xls)",
        type=['xlsx', 'xls'],
        help="File harus mengandung semua kolom yang diperlukan sesuai template"
    )
    
    if uploaded_file is not None:
        try:
            # Read Excel file
            df = pd.read_excel(uploaded_file)
            
            st.subheader("👀 Preview Data")
            st.dataframe(df.head(), use_container_width=True)
            
            # Validate columns
            missing_cols = [col for col in features if col not in df.columns]
            if missing_cols:
                st.error(f"❌ Kolom yang hilang: {missing_cols}")
                st.stop()
            
            # Validate data ranges
            validation_errors = validate_input_data(df[features])
            if validation_errors:
                st.warning("⚠️ **Peringatan Validasi Data:**")
                for error in validation_errors:
                    st.write(f"- {error}")
                
                if not st.checkbox("Lanjutkan meskipun ada data yang tidak valid"):
                    st.stop()
            
            # Predict button
            if st.button("🔍 Analisis Semua Data", type="primary", use_container_width=True):
                # Make predictions
                predictions = model.predict(df[features])
                probabilities = model.predict_proba(df[features])
                
                # Create results dataframe
                results_df = df.copy()
                results_df['Prediction'] = predictions
                results_df['Risk_Probability'] = probabilities[:, 1]
                results_df['Risk_Level'] = [interpret_risk([1-p, p])[0] for p in probabilities[:, 1]]
                results_df['Recommendation'] = [interpret_risk([1-p, p])[1] for p in probabilities[:, 1]]
                
                # Display results
                st.header("📊 Hasil Analisis Batch")
                
                # Summary statistics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Pasien", len(results_df))
                
                with col2:
                    high_risk = sum(results_df['Risk_Probability'] >= 0.8)
                    st.metric("Risiko Tinggi", high_risk, f"{high_risk/len(results_df)*100:.1f}%")
                
                with col3:
                    medium_risk = sum((results_df['Risk_Probability'] >= 0.6) & (results_df['Risk_Probability'] < 0.8))
                    st.metric("Risiko Sedang", medium_risk, f"{medium_risk/len(results_df)*100:.1f}%")
                
                with col4:
                    low_risk = sum(results_df['Risk_Probability'] < 0.6)
                    st.metric("Risiko Rendah", low_risk, f"{low_risk/len(results_df)*100:.1f}%")
                
                # Risk distribution chart
                st.subheader("📈 Distribusi Tingkat Risiko")
                risk_counts = results_df['Risk_Level'].value_counts()
                fig_pie = px.pie(
                    values=risk_counts.values,
                    names=risk_counts.index,
                    title="Distribusi Tingkat Risiko",
                    color_discrete_map={
                        'RISIKO TINGGI': '#FF4B4B',
                        'RISIKO SEDANG': '#FFB800',
                        'RISIKO RENDAH': '#00D4AA',
                        'RISIKO MINIMAL': '#00D4AA'
                    }
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                
                # Detailed results table
                st.subheader("📋 Detail Hasil")
                
                # Filter options
                filter_risk = st.selectbox(
                    "Filter berdasarkan tingkat risiko:",
                    ["Semua", "RISIKO TINGGI", "RISIKO SEDANG", "RISIKO RENDAH", "RISIKO MINIMAL"]
                )
                
                if filter_risk != "Semua":
                    filtered_results = results_df[results_df['Risk_Level'] == filter_risk]
                else:
                    filtered_results = results_df
                
                # Display results with color coding
                def color_risk_level(val):
                    if val == "RISIKO TINGGI":
                        return 'background-color: #FF4B4B; color: white'
                    elif val == "RISIKO SEDANG":
                        return 'background-color: #FFB800; color: white'
                    else:
                        return 'background-color: #00D4AA; color: white'
                
                styled_df = filtered_results.style.applymap(color_risk_level, subset=['Risk_Level'])
                st.dataframe(styled_df, use_container_width=True)
                
                # Download results
                st.subheader("💾 Download Hasil")
                col1, col2 = st.columns(2)
                
                with col1:
                    # Excel download
                    from io import BytesIO
                    excel_buffer = BytesIO()
                    results_df.to_excel(excel_buffer, index=False, engine='openpyxl')
                    excel_buffer.seek(0)
                    
                    st.download_button(
                        label="📥 Download Hasil (Excel)",
                        data=excel_buffer.getvalue(),
                        file_name=f"heart_disease_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                with col2:
                    # CSV download
                    csv_buffer = results_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Hasil (CSV)",
                        data=csv_buffer,
                        file_name=f"heart_disease_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
        
        except Exception as e:
            st.error(f"❌ Error membaca file: {str(e)}")
            st.info("💡 Pastikan file Excel sesuai dengan template yang disediakan")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p><strong>⚠️ DISCLAIMER MEDIS</strong></p>
        <p>Hasil prediksi ini hanya untuk <strong>screening awal</strong> dan <strong>TIDAK menggantikan</strong> diagnosa medis profesional.</p>
        <p>Selalu konsultasikan dengan dokter spesialis untuk diagnosa dan perawatan yang tepat.</p>
        <p><em>Sistem ini menggunakan Random Forest Algorithm dengan akurasi 92%</em></p>
    </div>
    """,
    unsafe_allow_html=True
)
