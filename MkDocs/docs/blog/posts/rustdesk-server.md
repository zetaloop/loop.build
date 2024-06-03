---
date:
    created: 2024-06-03 03:31:47
authors:
    - fox
categories:
    - RustDesk
    - 远程控制
    - 服务
---
# Linux 如何搭建 RustDesk 服务器
有时候同学来找我解决电脑问题，我们身处异地，但各种远程连接软件又总是卡顿断联。怎么办呢？

RustDesk 是一个开源的远程控制软件。它的服务端可以部署到我们自己的服务器上，远程控制更加流畅稳定，也不用担心数据泄露。我们这里就尝试在这台服务器上部署 RustDesk 的服务端。
<!-- more -->

方便起见，我们采用 Docker 部署，主要参考这一份 [RustDesk 官网教程](https://rustdesk.com/docs/en/self-host/rustdesk-server-oss/docker)。

## 准备工作
需要在服务器上装好 Docker，操作步骤可参考本站服务器备忘录。

[:material-sticker-outline: 备忘录：Docker](../../apps/server/docker.md){ .md-button }

## 部署 RustDesk 服务端
`hbbs` 为管理服务器，`hbbr` 为中继服务端。

正常使用需要开放以下端口，如有防火墙需设置允许通过。

| 组件        | 端口  | 协议 | 用途           |
| ----------- | ----- | ---- | -------------- |
| hbbs 专业版 | 21114 | TCP  | 管理 API       |
| hbbs        | 21115 | TCP  | NAT 类型测试   |
| hbbs        | 21116 | TCP  | 直连打洞       |
| hbbs        | 21116 | UDP  | 心跳包 + ID    |
| hbbr        | 21117 | TCP  | 中继           |
| hbbs        | 21118 | TCP  | Web 客户端认证 |
| hbbr        | 21119 | TCP  | Web 客户端中继 |

然后，我们在服务器上创建一个目录，用于存放 RustDesk 的数据。

比如我选择放在 `~/apps/rustdesk` 里。
```bash title=""
cd ~/apps
mkdir rustdesk
cd rustdesk
```
然后根据教程创建一个 Docker Compose 配置文件。
```yaml title="YAML　　docker-compose.yml"
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
    command: hbbr -k _  # 强制使用密钥加密连接
    volumes:
      - ./data:/root
    network_mode: host
    restart: unless-stopped
```
将这个容器启动即可。
```bash title=""
docker compose up -d
```
然后，我们查看 `~/apps/rustdesk/data` 目录里的 `id_ed25519.pub` 文件。<br>
里面的内容是我们的连接密钥，这个需要先记下来。
```bash title=""
cat data/id_ed25519.pub  # 显示密钥
```
你的密钥应该大致长这个样子：`9tBI0BK0hUi5McRIADzyjsqvRxPgYD9X0WZpFPRRTXb=`（这个是假的）

## 设置 RustDesk 客户端

电脑端打开 `设置 -> 网络设置 -> ID/中继服务器`，手机端打开 `设置 -> ID/中继服务器`。

你应该可以看到以下设置：

| 设置          | 填写值                   | 举例                                         |
| ------------- | ------------------------ | -------------------------------------------- |
| ID 服务器地址 | 你的服务器域名或 IP 地址 | 114.5.1.4                                    |
| 中继服务器    | （不填，默认同上）       |                                              |
| API 服务器    | （不填，专业版才有）     |                                              |
| Key           | 刚才查看的密钥           | 9tBI0BK0hUi5McRIADzyjsqvRxPgYD9X0WZpFPRRTXb= |

在两台设备上都填写好后，你就可以愉快地远程控制啦。

 ---
[:material-sticker-outline: 备忘录：RustDesk Server](../../apps/server/rustdesk.md){ .md-button }
