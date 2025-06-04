import paho.mqtt.client as mqtt
import json
import uuid
import random
import time # Ainda necessário para time.sleep(5) em caso de erro, mas não para o intervalo de publicação
# import os # Removido
from datetime import datetime

# Configurações do Broker - Fixas no código
BROKER = '192.168.122.81' # IP fixo do seu broker MQTT
PORT = 1883              # Porta fixa do broker
TOPIC = 'iot-events'     # Tópico fixo
ANOMALY_CHANCE = 0.05    # Chance de anomalia fixa (5%)
# PUBLISH_INTERVAL_SEC = 0.5 # Removido, pois não haverá atraso artificial

def generate_payload(anomaly_chance):
    """
    Gera um payload de dados de saúde simulando variações e anomalias.
    """
    is_anomaly = random.random() < anomaly_chance

    if is_anomaly:
        heart_rate = random.choice([random.randint(130, 180), random.randint(30, 50)])
        temperature = round(random.uniform(38.5, 41.0), 1)
        blood_pressure = f"{random.randint(150, 180)}/{random.randint(95, 120)}"
    else:
        heart_rate = random.randint(60, 100)
        temperature = round(random.uniform(36.0, 37.5), 1)
        blood_pressure = f"{random.randint(110, 130)}/{random.randint(70, 85)}"

    # Coordenadas de Porto Alegre - Faixa ajustada
    latitude = round(random.uniform(-30.15, -29.95), 6)
    longitude = round(random.uniform(-51.35, -51.05), 6)

    payload = {
        "device_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": "health_data",
        "sensor_data": {
            "heart_rate": heart_rate,
            "temperature": temperature,
            "blood_pressure": blood_pressure
        },
        "location": {
            "latitude": latitude,
            "longitude": longitude
        }
    }
    return json.dumps(payload), is_anomaly

def run_publisher():
    """
    Conecta ao broker e publica eventos continuamente, sem atrasos.
    """
    client = mqtt.Client()
    try:
        print(f"[{datetime.now()}] Conectando ao broker {BROKER}:{PORT} no tópico {TOPIC}...")
        client.connect(BROKER, PORT, 60)
        print(f"[{datetime.now()}] Conectado. Iniciando publicação de eventos (máxima velocidade).")

        i = 1
        while True:
            payload, is_anomaly = generate_payload(ANOMALY_CHANCE)
            client.publish(TOPIC, payload)
            print(f"[{datetime.now()}] Publicado: {payload}")

            i = i + 1

            if (i > 1000):
               sleep_interval = random.uniform(0.01,0.05)
               time.sleep(sleep_interval)
               i = 1

    except Exception as e:
        print(f"Erro na publicação: {e}")
        time.sleep(5) # Pequena espera em caso de erro antes de tentar novamente
    finally:
        client.disconnect()
        print(f"[{datetime.now()}] Desconectado do broker.")

if __name__ == "__main__":
    run_publisher()
