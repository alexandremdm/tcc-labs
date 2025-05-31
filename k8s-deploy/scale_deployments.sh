#!/bin/bash

# --- Script para escalar Deployments de IoT no Kubernetes ---

# --- Uso:
# ./scale_deployments.sh <replicas_producer> <replicas_bridge>

# Exemplo:
# ./scale_deployments.sh 5 10  # Escala producer para 5, bridge para 10
# ./scale_deployments.sh 0 1   # Escala producer para 0, bridge para 1

# --- Variáveis de Configuração (ajuste se necessário) ---
NAMESPACE="espfog-services"
PRODUCER_DEPLOYMENT="iot-producer"
BRIDGE_DEPLOYMENT="iot-events-bridge"

# --- Validação de Parâmetros ---
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Uso: $0 <replicas_producer> <replicas_bridge>"
  echo "  <replicas_producer>: Número de réplicas para o iot-producer"
  echo "  <replicas_bridge>: Número de réplicas para o iot-events-bridge"
  exit 1
fi

PRODUCER_REPLICAS=$1
BRIDGE_REPLICAS=$2

# --- Execução do Scaling ---

echo "---"
echo "Escalando o deployment '$PRODUCER_DEPLOYMENT' para $PRODUCER_REPLICAS réplicas na namespace '$NAMESPACE'..."
kubectl scale deployment/"$PRODUCER_DEPLOYMENT" --replicas="$PRODUCER_REPLICAS" -n "$NAMESPACE"

if [ $? -eq 0 ]; then # Verifica se o comando anterior foi bem-sucedido
  echo "Scaling do '$PRODUCER_DEPLOYMENT' solicitado com sucesso."
else
  echo "ERRO: Falha ao escalar o '$PRODUCER_DEPLOYMENT'. Verifique a saída acima."
  exit 1 # Sai com erro se o scaling do producer falhou
fi

echo "---"
echo "Escalando o deployment '$BRIDGE_DEPLOYMENT' para $BRIDGE_REPLICAS réplicas na namespace '$NAMESPACE'..."
kubectl scale deployment/"$BRIDGE_DEPLOYMENT" --replicas="$BRIDGE_REPLICAS" -n "$NAMESPACE"

if [ $? -eq 0 ]; then
  echo "Scaling do '$BRIDGE_DEPLOYMENT' solicitado com sucesso."
else
  echo "ERRO: Falha ao escalar o '$BRIDGE_DEPLOYMENT'. Verifique a saída acima."
  exit 1 # Sai com erro se o scaling do bridge falhou
fi

echo "---"
echo "Comandos de scaling executados."
echo "Monitore os pods com: kubectl get pods -n $NAMESPACE -w"
echo "Monitore os HPAs com: kubectl get hpa -n $NAMESPACE -w"
echo "---"
