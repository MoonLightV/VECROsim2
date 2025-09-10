#!/usr/bin/env bash
set -euo pipefail

echo "===> Building jaeger-exporter..."
cd "$(dirname "$0")/jaeger-exporter"
go build -o jaeger-exporter ./cmd/jaeger-exporter
echo "Build finished: $(pwd)/jaeger-exporter"
cd - >/dev/null

echo "===> Applying manifests..."
kubectl apply --server-side -f manifests/setup

until kubectl get servicemonitors --all-namespaces ; do
  date
  sleep 1
  echo ""
done

kubectl apply -f manifests/