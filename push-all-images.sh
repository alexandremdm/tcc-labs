#!/bin/bash

set -e

echo "➡️  Login no Nexus Docker Registry (docker-vm:8085)"
docker login docker-vm:8085

echo "🚧 Buildando imagem do serviço: config-server"
cd config-server
./mvnw clean package -DskipTests
docker build -t config-server:latest .
docker tag config-server:latest docker-vm:8085/docker-hosted/config-server:latest
docker push docker-vm:8085/docker-hosted/config-server:latest
cd ..

echo "🚧 Buildando imagem do serviço: iot-events-bridge"
cd iot-events-bridge
./mvnw clean package -DskipTests
docker build -t iot-events-bridge:latest .
docker tag iot-events-bridge:latest docker-vm:8085/docker-hosted/iot-events-bridge:latest
docker push docker-vm:8085/docker-hosted/iot-events-bridge:latest
cd ..

echo "🚧 Buildando imagem do serviço: events-processor-service"
cd events-processor
./mvnw clean package -DskipTests
docker build -t events-processor:latest .
docker tag events-processor:latest docker-vm:8085/docker-hosted/events-processor:latest
docker push docker-vm:8085/docker-hosted/events-processor:latest
cd ..

echo "🚧 Buildando imagem do serviço: health-alert-manager"
cd health-alert-manager
./mvnw clean package -DskipTests
docker build -t health-alert-manager:latest .
docker tag health-alert-manager:latest docker-vm:8085/docker-hosted/health-alert-manager:latest
docker push docker-vm:8085/docker-hosted/health-alert-manager:latest
cd ..

echo "✅ Todas as imagens foram enviadas com sucesso para o Nexus."
