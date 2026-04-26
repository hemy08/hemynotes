# Linux容器基础

## 概述

容器是一种轻量级的虚拟化技术，提供进程级别的隔离，比传统虚拟机更高效、更快速。

## 容器vs虚拟机

| 特性 | 容器 | 虚拟机 |
|------|------|--------|
| 启动速度 | 秒级 | 分钟级 |
| 资源占用 | 低 | 高 |
| 隔离级别 | 进程级 | 系统级 |
| 性能 | 接近原生 | 有损耗 |
| 镜像大小 | MB级 | GB级 |

## Docker基础

### 安装Docker

```bash
# Ubuntu/Debian
apt update
apt install docker.io docker-compose

# CentOS/RHEL
yum install docker docker-compose

# 启动Docker
systemctl start docker
systemctl enable docker

# 查看版本
docker version
docker info
```

### 镜像管理

```bash
# 搜索镜像
docker search nginx

# 拉取镜像
docker pull nginx
docker pull nginx:1.20
docker pull ubuntu:20.04

# 查看镜像
docker images
docker image ls

# 删除镜像
docker rmi nginx:1.20
docker image prune    # 清理未使用镜像

# 导出导入镜像
docker save nginx > nginx.tar
docker load < nginx.tar

# 构建镜像
docker build -t myapp:v1 .
```

### 容器管理

```bash
# 运行容器
docker run -d --name web nginx
docker run -d --name web -p 80:80 nginx
docker run -d --name web -p 80:80 -v /data:/usr/share/nginx/html nginx

# 查看容器
docker ps            # 运行中的容器
docker ps -a         # 所有容器

# 启动停止
docker start web
docker stop web
docker restart web
docker kill web

# 删除容器
docker rm web
docker rm -f web     # 强制删除
docker container prune    # 清理已停止容器

# 进入容器
docker exec -it web bash
docker attach web

# 查看日志
docker logs web
docker logs -f web   # 实时查看
docker logs --tail 100 web

# 查看进程
docker top web

# 查看资源使用
docker stats web
```

### Dockerfile

```dockerfile
# Dockerfile示例
FROM ubuntu:20.04

LABEL maintainer="admin@example.com"

ENV APP_HOME /app
WORKDIR $APP_HOME

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "app.py"]
```

```bash
# 构建镜像
docker build -t myapp:v1 .
docker build -t myapp:v1 -f Dockerfile.prod .
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3'

services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
    depends_on:
      - app
  
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=db
      - DB_PORT=5432
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

```bash
# 启动服务
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs
docker-compose logs -f web

# 停止服务
docker-compose down
docker-compose down -v    # 同时删除卷

# 重启服务
docker-compose restart

# 扩展服务
docker-compose up -d --scale app=3
```

### 网络管理

```bash
# 查看网络
docker network ls

# 创建网络
docker network create mynet
docker network create --driver bridge mynet

# 连接容器到网络
docker network connect mynet web

# 断开网络
docker network disconnect mynet web

# 删除网络
docker network rm mynet
```

### 数据卷管理

```bash
# 查看卷
docker volume ls

# 创建卷
docker volume create mydata

# 查看卷详情
docker volume inspect mydata

# 删除卷
docker volume rm mydata
docker volume prune    # 清理未使用卷
```

## Podman（无守护进程容器）

### 基本使用

```bash
# Podman命令与Docker兼容
podman run -d --name web nginx
podman ps
podman images
podman exec -it web bash

# 无需root运行
podman run --user 1000 nginx
```

## 容器安全

### 安全配置

```bash
# 以非root用户运行
docker run -u 1000:1000 nginx

# 限制能力
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE nginx

# 只读根文件系统
docker run --read-only nginx

# 限制资源
docker run --memory 512m --cpus 1 nginx

# 安全选项
docker run --security-opt no-new-privileges nginx
```

## 容器监控

### 监控工具

```bash
# 查看资源使用
docker stats

# cAdvisor（Google）
docker run -d --name=cadvisor \
    -p 8080:8080 \
    -v /:/rootfs:ro \
    -v /var/run:/var/run:rw \
    google/cadvisor:latest
```

## 容器日志

### 日志驱动

```bash
# json-file（默认）
docker run --log-driver json-file nginx

# syslog
docker run --log-driver syslog nginx

# journald
docker run --log-driver journald nginx

# 限制日志大小
docker run --log-opt max-size=10m --log-opt max-file=3 nginx
```

## 常用容器镜像

### Web服务器

```bash
# Nginx
docker run -d -p 80:80 nginx

# Apache
docker run -d -p 80:80 httpd
```

### 数据库

```bash
# MySQL
docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password mysql:8

# PostgreSQL
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:13

# Redis
docker run -d -p 6379:6379 redis

# MongoDB
docker run -d -p 27017:27017 mongo
```

## 参考资料

- [Docker官方文档](https://docs.docker.com/)
- [Docker Compose文档](https://docs.docker.com/compose/)
- [Podman文档](https://podman.io/)
