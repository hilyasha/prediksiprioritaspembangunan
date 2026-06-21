import streamlit as st
import joblib
import pandas as pd

model = joblib.load('model_ipm_lr.pkl') 

st.title("Aplikasi Prediksi IPM")

pengeluaran = st.number_input("Masukkan Pengeluaran", min_value=0)
rls = st.number_input("Masukkan RLS", min_value=0.0)
hls = st.number_input("Masukkan HLS", min_value=0.0)
ahh = st.number_input("Masukkan AHH", min_value=0.0)

if st.button("Prediksi"):
    data_input = [[pengeluaran, rls, hls, ahh]]
    hasil = model.predict(data_input)
    st.write(f"Hasil Prediksi Klaster: {hasil[0]}")