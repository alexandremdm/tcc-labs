# Use uma imagem base Python oficial
FROM python:3.9-slim-buster

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instale o pacote paho-mqtt diretamente, sem requirements.txt
RUN pip install --no-cache-dir paho-mqtt

# Copie o script Python principal
COPY iot-producer.py .

# Comando para executar o script quando o contêiner iniciar
CMD ["python", "iot-producer.py"]
