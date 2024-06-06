# Watchtower

## 简介
自动更新 Docker 容器。

## 创建 Docker 配置文件
来源：[Watchtower](https://containrrr.dev/watchtower/)、[RustDesk](https://rustdesk.com/docs/en/self-host/rustdesk-server-oss/ubuntu-server/docker/)
```yaml title="~/apps/watchtower/docker-compose.yml"
version: "3"
services:
  watchtower:
    image: containrrr/watchtower:latest
    container_name: watchtower
    network_mode: bridge
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      TZ: Asia/Shanghai
    command: --cleanup --schedule "0 0 3 * * *"
    restart: always
```

## 启动
``` bash
cd ~/apps/watchtower
docker compose up -d
```
