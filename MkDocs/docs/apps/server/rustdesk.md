# RustDesk 服务器

## 简介
RustDesk 是一个开源的远程控制软件。为了方便使用，我们将其服务端部署在服务器上。

- 21114：API，仅限专业版
- 21115：NAT 类型测试
- 21116：TCP 打洞，UDP 心跳包 + ID
- 21117：中继
- 21118、21119：Web 客户端用的

## 准备目录
``` bash
cd ~/apps
mkdir rustdesk
cd rustdesk
```

## 创建 Docker 配置文件
来源：[RustDesk 文档](https://rustdesk.com/docs/en/self-host/rustdesk-server-oss/docker/), [RustDesk 文档](https://rustdesk.com/docs/zh-cn/self-host/rustdesk-server-oss/install/)

``` bash
nano docker-compose.yml
```

``` yaml
services:
  hbbs:
    container_name: hbbs
    image: rustdesk/rustdesk-server:latest
    command: hbbs
    volumes:
      - ./data:/root
    network_mode: host
    depends_on:
      - hbbr
    restart: unless-stopped

  hbbr:
    container_name: hbbr
    image: rustdesk/rustdesk-server:latest
    command: hbbr -k _  # 强制使用密钥
    volumes:
      - ./data:/root
    network_mode: host
    restart: unless-stopped
```
由于这是我们自己私用的服务器，安全起见，禁止无密钥登录。

## 启动服务
``` bash
docker compose up -d
```

## 获取密钥
``` bash
cat data/id_ed25519.pub
```

## 填写软件设置
| RustDesk 设置 | 内容       |
| ------------- | ---------- |
| ID 服务器     | 服务器 IP  |
| 中继服务器    | 不填，自动 |
| API 服务器    | 不填，没钱 |
| Key           | 密钥       |

我们这里使用服务器 IP 地址而不是域名，因为我们域名是经过 CloudFlare 中转的。
