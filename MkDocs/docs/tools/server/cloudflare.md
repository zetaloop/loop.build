# 基于 Cloudflare 的服务器结构
日期：2024-04-21
 ---
## 结构图

```mermaid
flowchart LR
    server[服务器] <--->|自签名 https 证书\nmTLS 仅允许 Cloudflare 访问| cloudflare[Cloudflare CDN]
    cloudflare <--->|Cloudflare 的自动 https| user[用户]
```
<center>**图1** 外部结构</center>
```mermaid
flowchart LR
    nginx[Nginx]
    loop_main[loop.build]
    nginx_redirect[<b>www</b>.loop.build 🡒 loop.build\n直接访问 <b>/docs</b> 等内部路径 🡒 子域 docs.]
    docs[docs.loop.build]
    tools[tools.loop.build]
    blog[blog.loop.build]
    update[update.loop.build]
    about[about.loop.build]
    redirector[子域短网址跳转服务（举例）\ntorndown.loop.build 🡒 docs.loop.build/torndown\nbilibili.loop.build 🡒 space.bilibili.com/99583527]
    other_tools[其他服务与工具\n由 Nginx 代理或直接访问\n（举例）]
    gh-mirror[GitHub 镜像]
    gitea[自建 git]
    rustdesk-server[RustDesk 远程桌面服务器]

    nginx ---|MkDocs 静态主站| loop_main
    nginx ---|301| nginx_redirect
    loop_main ---|/docs 文档| docs
    loop_main ---|/tools 工具| tools
    loop_main ---|/blog 博客| blog
    loop_main ---|/update 更新| update
    loop_main ---|/about 关于| about
    nginx ---|其他子域| redirector
    nginx ---|其他部署| other_tools
    other_tools ---|gh-mirror| gh-mirror
    other_tools ---|gitea| gitea
    other_tools ---|rustdesk-server| rustdesk-server

    subgraph "地址通过代理转换"
        docs
        tools
        blog
        update
        about
    end
```
<center>**图2** 内部结构</center>

<!-- 服务器 <==自签名证书https+mTLS仅限CF访问==> Cloudflare CDN <==CF自动https==> 用户
    |
  nginx
    |- loop.build 主站（MkDocs静态，自动拉取github并编译）
    |- www.loop.build 301到主站
    |- docs.loop.build 文档（各项目说明）
    |- tools.loop.build 工具（服务器上部署的工具之类）
    |- blog.loop.build 博客
    |- update.loop.build 动态
    |- about.loop.build 关于页
    |   这五个内容站，内部实际上直接代理到loop.build/subdomain/*
    |   但是如果直接访问/subdomain，会被301到subdomain.loop.build
    |
    |- flask写的跳转器
    |       |- （举例）powertoys.loop.build -> docs.loop.build/powertoys
    |       |- （举例）among.loop.build -> docs.loop.build/among-python
    |
    | 其他部署（最好是docker）
    |- gh-mirror 镜像GitHub
    |- gitea 自建git
    ... -->
