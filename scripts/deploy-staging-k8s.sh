#!/bin/bash

# Kubernetes 测试环境部署脚本
# 使用方法: ./scripts/deploy-staging-k8s.sh

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 配置变量
NAMESPACE="staging"
APP_NAME="llm-learn"
IMAGE="ghcr.io/zzyReal666/python"
TAG="develop"
REPLICAS=2

# 主函数
main() {
    log_info "开始 Kubernetes 测试环境部署..."
    
    # 1. 检查环境
    check_environment
    
    # 2. 创建命名空间
    create_namespace
    
    # 3. 创建 ConfigMap 和 Secret
    create_configs
    
    # 4. 部署应用
    deploy_application
    
    # 5. 创建服务
    create_service
    
    # 6. 创建 Ingress（如果需要）
    create_ingress
    
    # 7. 健康检查
    health_check
    
    log_success "Kubernetes 测试环境部署完成！"
}

# 检查环境
check_environment() {
    log_info "检查 Kubernetes 环境..."
    
    # 检查 kubectl 是否安装
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl 未安装，请先安装 kubectl"
        exit 1
    fi
    
    # 检查集群连接
    if ! kubectl cluster-info &> /dev/null; then
        log_error "无法连接到 Kubernetes 集群"
        exit 1
    fi
    
    # 检查当前上下文
    log_info "当前 Kubernetes 上下文: $(kubectl config current-context)"
    
    log_success "Kubernetes 环境检查通过"
}

# 创建命名空间
create_namespace() {
    log_info "创建命名空间: $NAMESPACE"
    
    kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -
    
    log_success "命名空间创建完成"
}

# 创建配置
create_configs() {
    log_info "创建 ConfigMap 和 Secret..."
    
    # 创建 ConfigMap
    cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: ${APP_NAME}-config
  namespace: ${NAMESPACE}
data:
  ENVIRONMENT: "staging"
  LOG_LEVEL: "DEBUG"
  GRADIO_SERVER_NAME: "0.0.0.0"
  GRADIO_SERVER_PORT: "7860"
EOF

    # 创建 Secret（如果需要敏感信息）
    cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: ${APP_NAME}-secret
  namespace: ${NAMESPACE}
type: Opaque
data:
  # 这里可以添加敏感信息，如 API 密钥等
  # api-key: <base64-encoded-value>
EOF

    log_success "配置创建完成"
}

# 部署应用
deploy_application() {
    log_info "部署应用到 Kubernetes..."
    
    cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app: ${APP_NAME}
    environment: staging
spec:
  replicas: ${REPLICAS}
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
        environment: staging
    spec:
      containers:
      - name: ${APP_NAME}
        image: ${IMAGE}:${TAG}
        ports:
        - containerPort: 7860
          name: http
        env:
        - name: ENVIRONMENT
          valueFrom:
            configMapKeyRef:
              name: ${APP_NAME}-config
              key: ENVIRONMENT
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: ${APP_NAME}-config
              key: LOG_LEVEL
        - name: GRADIO_SERVER_NAME
          valueFrom:
            configMapKeyRef:
              name: ${APP_NAME}-config
              key: GRADIO_SERVER_NAME
        - name: GRADIO_SERVER_PORT
          valueFrom:
            configMapKeyRef:
              name: ${APP_NAME}-config
              key: GRADIO_SERVER_PORT
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 7860
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 7860
          initialDelaySeconds: 5
          periodSeconds: 5
        command: ["python", "src/main.py", "run", "logging_demo"]
        volumeMounts:
        - name: logs
          mountPath: /app/logs
        - name: config
          mountPath: /app/config
      volumes:
      - name: logs
        emptyDir: {}
      - name: config
        configMap:
          name: ${APP_NAME}-config
EOF

    log_success "应用部署完成"
}

# 创建服务
create_service() {
    log_info "创建 Kubernetes 服务..."
    
    cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}-service
  namespace: ${NAMESPACE}
  labels:
    app: ${APP_NAME}
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 7860
    protocol: TCP
    name: http
  selector:
    app: ${APP_NAME}
EOF

    log_success "服务创建完成"
}

# 创建 Ingress（可选）
create_ingress() {
    log_info "创建 Ingress 规则..."
    
    cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ${APP_NAME}-ingress
  namespace: ${NAMESPACE}
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  rules:
  - host: staging.llm-learn.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ${APP_NAME}-service
            port:
              number: 80
EOF

    log_success "Ingress 创建完成"
}

# 健康检查
health_check() {
    log_info "执行健康检查..."
    
    # 等待部署完成
    log_info "等待部署完成..."
    kubectl rollout status deployment/${APP_NAME} -n ${NAMESPACE} --timeout=300s
    
    # 检查 Pod 状态
    log_info "检查 Pod 状态..."
    kubectl get pods -n ${NAMESPACE} -l app=${APP_NAME}
    
    # 检查服务状态
    log_info "检查服务状态..."
    kubectl get svc -n ${NAMESPACE} -l app=${APP_NAME}
    
    # 端口转发进行测试（可选）
    log_info "测试应用连接..."
    kubectl port-forward -n ${NAMESPACE} svc/${APP_NAME}-service 8080:80 &
    PF_PID=$!
    
    sleep 5
    
    if curl -f http://localhost:8080/health &> /dev/null; then
        log_success "应用健康检查通过"
    else
        log_warning "应用健康检查失败"
    fi
    
    kill $PF_PID 2>/dev/null || true
    
    log_success "健康检查完成"
}

# 回滚函数
rollback() {
    log_warning "开始回滚部署..."
    
    # 回滚到上一个版本
    kubectl rollout undo deployment/${APP_NAME} -n ${NAMESPACE}
    
    # 等待回滚完成
    kubectl rollout status deployment/${APP_NAME} -n ${NAMESPACE}
    
    log_success "回滚完成"
}

# 清理函数
cleanup() {
    log_warning "清理测试环境..."
    
    kubectl delete namespace ${NAMESPACE} --ignore-not-found=true
    
    log_success "清理完成"
}

# 显示帮助信息
show_help() {
    echo "Kubernetes 测试环境部署脚本"
    echo ""
    echo "使用方法:"
    echo "  $0              # 部署到测试环境"
    echo "  $0 rollback     # 回滚到上一个版本"
    echo "  $0 cleanup      # 清理测试环境"
    echo "  $0 help         # 显示帮助信息"
    echo ""
    echo "环境变量:"
    echo "  NAMESPACE       # Kubernetes 命名空间 (默认: staging)"
    echo "  APP_NAME        # 应用名称 (默认: llm-learn)"
    echo "  IMAGE           # Docker 镜像 (默认: ghcr.io/zzyReal666/python)"
    echo "  TAG             # 镜像标签 (默认: develop)"
    echo "  REPLICAS        # 副本数量 (默认: 2)"
}

# 脚本入口
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "rollback")
        rollback
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        log_error "未知参数: $1"
        show_help
        exit 1
        ;;
esac 