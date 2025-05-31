import paho.mqtt.client as mqtt
import json
import uuid
import random
import time
import sys # Importado para acessar os argumentos da linha de comando
from datetime import datetime

# Configurações do Broker - Fixas no código
BROKER = '192.168.122.81'  # IP fixo do seu broker MQTT
PORT = 1883               # Porta fixa do broker
TOPIC = 'iot-events'      # Tópico fixo
ANOMALY_CHANCE = 0.05     # Chance de anomalia fixa (5%)

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
        "timestamp": datetime.utcnow().isoformat() + "Z", # Timestamp de geração do evento
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

def run_publisher(num_events=None):
    """
    Conecta ao broker e publica eventos.
    Se 'num_events' for especificado, publica essa quantidade de eventos e encerra.
    Caso contrário, publica continuamente.
    """
    client = mqtt.Client()
    try:
        print(f"[{datetime.now()}] Conectando ao broker {BROKER}:{PORT} no tópico {TOPIC}...")
        client.connect(BROKER, PORT, 60)
        print(f"[{datetime.now()}] Conectado.")

        if num_events is None:
            print(f"[{datetime.now()}] Iniciando publicação contínua de eventos (máxima velocidade).")
            while True:
                payload, is_anomaly = generate_payload(ANOMALY_CHANCE)
                client.publish(TOPIC, payload)
                # print(f"[{datetime.now()}] Publicado: {payload}") # Removido para evitar muitos logs em produção
        else:
            print(f"[{datetime.now()}] Iniciando publicação de {num_events} eventos (máxima velocidade).")
            for i in range(num_events):
                payload, is_anomaly = generate_payload(ANOMALY_CHANCE)
                client.publish(TOPIC, payload)
                # print(f"[{datetime.now()}] Publicado [{i+1}/{num_events}]: {payload}") # Removido
            print(f"[{datetime.now()}] Publicação de {num_events} eventos concluída.")

    except Exception as e:
        print(f"[{datetime.now()}] Erro na publicação: {e}")
        time.sleep(5)  # Pequena espera em caso de erro antes de tentar novamente (se estiver em loop)
    finally:
        client.disconnect()
        print(f"[{datetime.now()}] Desconectado do broker.")

if __name__ == "__main__":
    # Verifica se um argumento foi passado na linha de comando
    if len(sys.argv) > 1:
        try:
            # Tenta converter o argumento para um inteiro
            events_to_generate = int(sys.argv[1])
            if events_to_generate < 0:
                print("Por favor, forneça um número de eventos não negativo.")
                sys.exit(1)
            run_publisher(num_events=events_to_generate)
        except ValueError:
            print(f"Erro: O argumento '{sys.argv[1]}' não é um número válido de eventos.")
            print("Uso: python producer.py [numero_de_eventos]")
            print("Ex: python producer.py 1000")
            print("Para publicação contínua: python producer.py")
            sys.exit(1)
    else:
        # Se nenhum argumento for passado, executa o modo contínuo
        run_publisher(num_events=None)
