# Processo Seletivo Metta | Detector de Pessoas

## Como instalar e executar

### 1. Clone o repositório
```bash
git clone https://github.com/henriqfranco/metta-video-detector.git
cd metta-video-detector
```

### 2. Crie e ative um ambiente virtual
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# Windows:
.venv\Scripts\activate

# Linux/MacOS:
source .venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação
```bash
streamlit run src/gui.py
```

### 5. Acesse a aplicação
Abra seu navegador em: `http://localhost:8501`

## Desativar ambiente virtual
```bash
deactivate
```

## Estrutura do projeto
```
metta-video-detector/
├── src/
│   ├── detector.py
│   ├── video_processor.py
│   └── gui.py
├── sample/
├── output_results/
├── requirements.txt
└── README.md
```

## Funcionalidades
- Detecção de pessoas em vídeos usando YOLOv11
- Interface web com Streamlit
- Geração de alertas configuráveis
- Gráficos de análise temporal
- Vídeo processado com bounding boxes