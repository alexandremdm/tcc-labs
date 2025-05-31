#!/bin/bash
set -e

echo "🔧 Criando namespace espfog-services (se necessário)..."
kubectl create namespace espfog-services --dry-run=client -o yaml | kubectl apply -f -

echo "🚀 Aplicando manifestos na ordem:"
kubectl apply -f 00-namespace.yaml
kubectl apply -f 01-config-server.yaml
kubectl apply -f 02-iot-events-bridge.yaml
kubectl apply -f 03-events-processor.yaml
kubectl apply -f 04-health-alert-manager.yaml
kubectl apply -f 05-keda-scaledobject-events-processor.yaml
kubectl apply -f 06-iot-producer.yaml
echo '✅ Implantação completa.'
