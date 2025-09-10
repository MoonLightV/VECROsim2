#!/bin/bash

# 设置命名空间
NAMESPACE="social"

# 创建日志目录
LOG_DIR="./vecro2/cpu-hog2"
mkdir -p $LOG_DIR

# 获取所有 Pod 名称
PODS=$(kubectl get pods -n $NAMESPACE --no-headers -o custom-columns=":metadata.name")

# 遍历所有 Pod，导出日志
for POD in $PODS; do
    # 输出日志文件名
    LOG_FILE="$LOG_DIR/${POD}.log"
    
    # 导出日志
    echo "Exporting logs for Pod: $POD"
    kubectl logs -n $NAMESPACE $POD > $LOG_FILE 2>&1

    # 检查是否有多个容器（Sidecar 情况）
    CONTAINERS=$(kubectl get pod -n $NAMESPACE $POD -o jsonpath='{.spec.containers[*].name}')
    if [[ $(echo $CONTAINERS | wc -w) -gt 1 ]]; then
        echo "Pod $POD has multiple containers. Exporting logs for each container."
        for CONTAINER in $CONTAINERS; do
            CONTAINER_LOG_FILE="$LOG_DIR/${POD}_${CONTAINER}.log"
            kubectl logs -n $NAMESPACE $POD -c $CONTAINER > $CONTAINER_LOG_FILE 2>&1
        done
    fi
done

echo "Logs exported to directory: $LOG_DIR"

