import streamlit as st
import os
import json
import matplotlib.pyplot as plt
from video_processor import VideoProcessor

st.set_page_config(page_title="Contador de Pessoas", layout="centered")

st.title("Processo Seletivo Metta: Monitoramento de Pessoas")

video_path = "sample/people-walking.mp4"
output_path = "output_results"

alert_threshold = st.slider(
    "Limiar de pessoas para gerar alerta (alerts.json)",
    min_value=1,
    max_value=10,
    value=3
)

if st.button("Processar vídeo"):
    with st.spinner("Processando vídeo..."):
        processor = VideoProcessor(video_path, output_path, alert_threshold)
        processor.process()
    st.success("Processamento concluído!")

video_file = os.path.join(output_path, "processed_video.mp4")
if os.path.exists(video_file):
    st.subheader("Vídeo Processado")
    st.video(video_file)

history_file = os.path.join(output_path, "history.json")
if os.path.exists(history_file):
    with open(history_file) as f:
        data = json.load(f)

    frame_ids = [entry["id"] for entry in data]
    counts = [entry["count"] for entry in data]

    st.subheader("Gráfico de contagem de pessoas por frame")
    fig, ax = plt.subplots()
    ax.plot(frame_ids, counts, label="Pessoas por frame")
    ax.set_xlabel("Frame")
    ax.set_ylabel("Número de pessoas")
    ax.grid(True)
    st.pyplot(fig)

alerts_file = os.path.join(output_path, "alerts.json")
if os.path.exists(alerts_file):
    with open(alerts_file) as f:
        data = json.load(f)

    frame_ids = [entry["id"] for entry in data]
    counts = [entry["count"] for entry in data]

    st.subheader(f"Gráfico de contagem de pessoas por frame (com mais de {alert_threshold} pessoas)")
    fig, ax = plt.subplots()
    ax.plot(frame_ids, counts, label="Pessoas por frame")
    ax.set_xlabel("Frame")
    ax.set_ylabel("Número de pessoas")
    ax.grid(True)
    st.pyplot(fig)