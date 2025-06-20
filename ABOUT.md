# Explicações/Justificativas Técnicas

## Justificativa de Tecnologias Utilizadas

- Python: Diversas bibliotecas e módulos em alto nível para trabalhar com visão computacional e  inteligência artificial.
- YOLO da Ultralytics: Precisão alta em objetos comuns, rápida velocidade de processamento e facilidade de uso e implementação.
- OpenCV (cv2): Biblioteca muito utilizada para processamento de imagens e vídeos por ser rápida e eficiente.
- Streamlit: Framework leve e eficiente para construção de GUIs em Python, ideal para visualização de vídeos e gráficos e interação do usuário. Possui integração simples com OpenCV e matplotlib.
- Matplotlib: Possui integração direta com o Streamlit, permitindo exibição de gráficos diretamente dentro da interface da aplicação.

## Solução Desenvolvida

### detector.py

<p>O código desenvolvido para detecção de pessoas por imagem/frame foi estruturado de forma que, ao receber uma imagem, processe-a e extraia apenas as coordenadas <code>xyxy</code> da bounding box a ser desenhada ao redor da pessoa. Ele funciona executando a função <code>predict</code> do modelo neural YOLO na imagem passada e retorna os <code>resultados</code> em uma lista (mesmo quando apenas uma imagem é fornecida).

Como garantimos que apenas uma imagem será passada por vez, a lista de resultados terá apenas um resultado, evitando a necessidade de iterar por todos os resultados e permitindo o acesso direto ao primeiro (e único) elemento da lista. Com esse elemento <code>resultado</code>, podemos acessar os elementos que foram encontrados na imagem pela função <code>predict</code>. Destes elementos, nos concentramos no objeto <code>boxes</code>, que possui informações de todas as bounding boxes encontradas na tela.

Passando por cada <code>box</code> dentro de boxes, verificamos se o seu <code>cls</code> (classe de identificação) é igual a 0 (código para identificação de humanos). Se o cls for 0, armazenamos as coordenadas (que são retornadas em um tensor com 4 valores, referentes ao ponto superior esquerdo e ao ponto inferior direito) em variaveis <code>x1</code>, <code>y1</code>, <code>x2</code> e <code>y2</code>, juntamos as variaveis em uma tupla e adicionamos a mesma em uma lista com todas as bounding boxes encontradas naquela imagem/frame.</p>

![Diagrama de Funcionamento do Detector](about_images\detector.png)

### video_processor.py

<p>O código responsável pelo processamento do vídeo foi estruturado de forma que, ao receber o caminho do vídeo de entrada, o diretório de saída e o limite de pessoas para alerta, execute a leitura e o processamento frame a frame do vídeo original. Inicialmente, são coletadas informações do vídeo como largura, altura, taxa de quadros por segundo (FPS) e número total de frames, que são utilizadas para configurar corretamente o vídeo de saída. Um objeto do tipo <code>PeopleDetector</code> é instanciado para realizar a detecção de pessoas em cada frame analisado.

O loop principal do método <code>process</code> percorre todos os frames do vídeo utilizando a função <code>read()</code> da biblioteca OpenCV. Para cada frame lido com sucesso, o mesmo é enviado ao <code>detector</code>, que retorna uma lista de caixas delimitadoras (bounding boxes) das pessoas detectadas. Essas caixas são desenhadas sobre o frame por meio da função <code>cv2.rectangle</code>, utilizando as coordenadas retornadas.

A cada iteração, a contagem de pessoas detectadas no frame atual é calculada com base no número de boxes retornadas, e um registro com o identificador do frame (<code>frame_id</code>) e a contagem é adicionado a uma lista chamada <code>history</code>, que será salva no arquivo <code>history.json</code>. Se a quantidade de pessoas detectadas for maior ou igual ao valor do limite (<code>alert_threshold</code>), um registro adicional é adicionado à lista <code>alerts</code>, contendo também o identificador do frame e a contagem de pessoas.

Ao final do processamento, todos os frames com as caixas desenhadas são salvos em um novo vídeo chamado <code>processed_video.mp4</code>, e as listas <code>history</code> e <code>alerts</code> são gravadas em arquivos .json no diretório de saída definido. O arquivo <code>alerts.json</code> inclui também o valor do limiar utilizado, como metadado. Por fim, os recursos utilizados, como o leitor e o gravador de vídeo, são liberados corretamente com os métodos <code>release()</code>.</p>

![Frame do vídeo com bounding boxes ao redor das pessoas](about_images\detected_people.png)

### gui.py

<p>O código responsável por exibir os resultados do processamento foi desenvolvido utilizando a biblioteca <code>Streamlit</code>, que permite a criação de interfaces gráficas interativas com foco em aplicações de ciência de dados e visão computacional. A aplicação inicia configurando o título e o layout da página, além de definir os caminhos para o vídeo de entrada, o diretório de saída dos resultados e os arquivos gerados pelo processamento.

O primeiro bloco de interação verifica se os resultados já existem. Caso não existam, o usuário pode definir o limiar de alerta através de um controle deslizante (<code>slider</code>) e iniciar o processamento ao clicar no botão <code>Processar vídeo</code>. Ao fazer isso, o código cria uma instância da classe <code>VideoProcessor</code>, que executa a análise do vídeo, gera os arquivos de saída e reinicia automaticamente a interface com <code>st.rerun()</code> após a conclusão.

Se os resultados já existirem, o usuário poderá optar por apagar os arquivos de saída e processar novamente, através do botão Processar Novamente, que remove o diretório <code>output_results</code> usando <code>shutil.rmtree()</code> e reinicia a interface.

Na sequência, o aplicativo verifica a existência do arquivo <code>processed_video.mp4</code> e, se encontrado, exibe o vídeo processado diretamente na interface usando o método <code>st.video()</code>. Após isso, os dados de <code>history.json</code> e <code>alerts.json</code> são carregados e transformados em listas com os identificadores de frames e a contagem de pessoas detectadas.

Para visualizar esses dados, são gerados dois gráficos utilizando a biblioteca <code>matplotlib</code>: o primeiro mostra a contagem de pessoas em cada frame ao longo do vídeo; o segundo, mais específico, exibe apenas os frames em que o número de pessoas foi igual ou superior ao limiar definido. Esses gráficos são integrados ao Streamlit com <code>st.pyplot()</code>, permitindo análise visual direta a partir da interface.</p>

![Vídeo sendo mostrado na interface](about_images\gui_video.png)