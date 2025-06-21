import streamlit as st
import os
import json
import shutil
import matplotlib.pyplot as plt
from video_processor import VideoProcessor
from scipy.interpolate import make_interp_spline
import numpy as np

st.set_page_config(page_title="Contador de Pessoas", layout="centered")

st.title("Processo Seletivo Metta: Monitoramento de Pessoas")

video_path = "sample/people-walking.mp4"
output_path = "output_results"

if not os.path.exists(output_path):
    alert_threshold = st.slider(
        "Limiar de pessoas para gerar alerta (alerts.json)",
        min_value=1,
        max_value=10,
        value=3
    )

if not os.path.exists(output_path):
    if st.button("Processar vídeo"):
        with st.spinner("Processando vídeo..."):
            processor = VideoProcessor(video_path, output_path, alert_threshold)
            processor.process()
        st.success("Processamento concluído.")
        st.rerun()
else:
    if st.button("Processar Novamente"):
        with st.spinner("Deletando resultados..."):
            shutil.rmtree(output_path)
        st.success("Resultados Deletados.")
        st.rerun()

video_file = os.path.join(output_path, "processed_video.mp4")
if os.path.exists(video_file):
    st.subheader("Vídeo Processado")
    st.video(video_file)

if os.path.exists(output_path):
    plot_detail = st.slider(
            "Nível de Detalhe dos Gráficos",
            min_value=10,
            max_value=100,
            value=50,
            format="%i%%"
        )
    plot_detail /= 100

history_file = os.path.join(output_path, "history.json")
if os.path.exists(history_file):
    with open(history_file) as f:
        data = json.load(f)

    frame_ids = [entry["id"] for entry in data]
    counts = [entry["count"] for entry in data]
    
    frame_ids_spaced = np.linspace(min(frame_ids), max(frame_ids), int(max(frame_ids)*plot_detail))
    spl = make_interp_spline(frame_ids, counts, k=0)
    counts_smooth = spl(frame_ids_spaced)

    st.subheader("Gráfico de contagem de pessoas por frame")
    fig, ax = plt.subplots(figsize=(18,9))
    ax.plot(frame_ids_spaced, counts_smooth, label="Pessoas por frame")
    ax.set_xlabel("Frame")
    ax.set_ylabel("Número de pessoas")
    ax.grid(True)
    st.pyplot(fig)

alerts_file = os.path.join(output_path, "alerts.json")
if os.path.exists(alerts_file):
    with open(alerts_file) as f:
        data = json.load(f)

    threshold_used = data["threshold_used"]
    alerts = data["alerts"]

    frame_ids = [entry["id"] for entry in alerts]
    counts = [entry["count"] for entry in alerts]
    
    frame_ids_spaced = np.linspace(min(frame_ids), max(frame_ids), int(max(frame_ids)*plot_detail))
    spl = make_interp_spline(frame_ids, counts, k=0)
    counts_smooth = spl(frame_ids_spaced)

    st.subheader(f"Gráfico de contagem de pessoas por frame (com mais de {threshold_used} pessoas)")
    fig, ax = plt.subplots(figsize=(18,9))
    ax.plot(frame_ids_spaced, counts_smooth, label="Pessoas por frame")
    ax.set_xlabel("Frame")
    ax.set_ylabel("Número de pessoas")
    ax.grid(True)
    st.pyplot(fig)