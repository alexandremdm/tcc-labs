import paho.mqtt.client as mqtt
import json
import uuid
import random
import time
import threading
from datetime import datetime

BROKER = 'mqtt-broker'
PORT = 1883
TOPIC = 'iot-events'

def generate_payload(anomaly_chance=0.1):
    is_anomaly = random.random() < anomaly_chance

    if is_anomaly:
        heart_rate = random.choice([random.randint(130, 180), random.randint(30, 50)])
        temperature = round(random.uniform(38.5, 41.0), 1)
        blood_pressure = f"{random.randint(150, 180)}/{random.randint(95, 120)}"
    else:
        heart_rate = random.randint(60, 100)
        temperature = round(random.uniform(36.0, 37.5), 1)
        blood_pressure = f"{random.randint(110, 130)}/{random.randint(70, 85)}"

    # Variação dentro de Porto Alegre
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

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

def publish_events(rate_per_sec, duration_sec, anomaly_chance=0.1):
    total_msgs = rate_per_sec * duration_sec
    interval = 1.0 / rate_per_sec
    anomaly_count = 0

    for _ in range(total_msgs):
        payload, is_anomaly = generate_payload(anomaly_chance)
        if is_anomaly:
            anomaly_count += 1
        client.publish(TOPIC, payload)
        print(f"[{datetime.now()}] Publicado: {payload}")
        time.sleep(interval)
    
    print(f"[{datetime.now()}] Cenário concluído. Total de mensagens: {total_msgs}, Anomalias: {anomaly_count}")

def cenario_estavel():
    print(f"[{datetime.now()}] Cenário 1 - Carga Estável")
    publish_events(rate_per_sec=10, duration_sec=60)

def cenario_variavel():
    print(f"[{datetime.now()}] Cenário 2 - Carga Variável")
    for i in range(3):
        rate = random.randint(5, 15)
        duration = 20
        print(f"[{datetime.now()}] Pico {i+1}: {rate} msg/s por {duration}s")
        publish_events(rate_per_sec=rate, duration_sec=duration)
        time.sleep(random.randint(5, 10))

def cenario_sobrecarga():
    print(f"[{datetime.now()}] Cenário 3 - Sobrecarga")
    publish_events(rate_per_sec=100, duration_sec=30)

def rodar_teste_temporizado(duracao_total=300):
    """
    Executa diferentes cenários de carga variando de forma contínua 
    até atingir a duração total especificada (em segundos).
    """
    print(f"[{datetime.now()}] Iniciando teste por {duracao_total} segundos...\n")
    inicio = time.time()
    
    cenarios = [cenario_estavel, cenario_variavel, cenario_sobrecarga]
    
    while (time.time() - inicio) < duracao_total:
        cenario = random.choice(cenarios)
        tempo_decorrido = time.time() - inicio
        tempo_restante = duracao_total - tempo_decorrido
        print(f"\n[{datetime.now()}] Tempo decorrido: {int(tempo_decorrido)}s, Tempo restante: {int(tempo_restante)}s")
        print(f"[{datetime.now()}] Executando: {cenario.__name__}")

        duracao_cenario = random.randint(30, 90)
        print(f"[{datetime.now()}] Duração planejada do cenário: {duracao_cenario} segundos")
        
        # Rodar o cenário numa thread
        thread = threading.Thread(target=cenario)
        thread.start()

        # Espera o tempo do cenário ou o tempo restante, o que for menor
        time.sleep(min(duracao_cenario, tempo_restante))
        
        print(f"[{datetime.now()}] Cenário {cenario.__name__} finalizado.\n")

    print(f"\n[{datetime.now()}] Teste finalizado após {duracao_total} segundos.")

if __name__ == "__main__":
    rodar_teste_temporizado(600)  # Rodar 5 minutos

