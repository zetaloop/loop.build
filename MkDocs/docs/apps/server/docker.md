# Docker

## 安装 Docker Engine 套装
来源：[docs.docker.com](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

添加 Apt 源
```bash
# 添加 GPG 密钥
apt update
apt install ca-certificates curl
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

# 添加 Apt 源
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
```

安装软件包
```bash
apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

设定别名
```bash
echo 'alias docker-compose="docker compose"' >> ~/.bashrc
source ~/.bashrc
```

## 如何管理容器
我们使用 Docker Compose
```bash title="启动容器"
docker compose up -d
```
```bash title="停止容器"
docker compose down
```
```bash title="查看状态"
docker compose ps
```
```bash title="查看日志"
docker compose logs
```
