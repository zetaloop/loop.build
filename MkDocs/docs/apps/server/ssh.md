# SSH

## 连接保活
来源：[知乎](https://zhuanlan.zhihu.com/p/664604642)
=== "手动编辑"
    编辑 `/etc/ssh/sshd_config` 文件
    ```bash
    nano /etc/ssh/sshd_config
    ```

    在末尾添加以下内容
    ```conf title=""
    TCPKeepAlive yes  # 向客户端发送保活包
    ClientAliveInterval 120  # 超时 120 秒则发送保活包
    ClientAliveCountMax 30  # 一小时 30 次保活包未收到则断开连接
    ```

    重启 SSH 服务
    ``` bash
    systemctl restart sshd
    ```
=== "一键设置"
    执行以下指令
    ```bash
    echo -e "TCPKeepAlive yes\nClientAliveInterval 120\nClientAliveCountMax 30" >> /etc/ssh/sshd_config
    systemctl restart sshd
    ```
