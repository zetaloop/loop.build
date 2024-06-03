# 日常维护

=== "APT"
    更新软件包
    ```bash title=""
    apt update
    apt upgrade
    ```
    清理下载缓存
    ```bash title=""
    apt clean
    ```
    删除不再使用的软件包
    ```bash title=""
    apt autoremove
    ```
    删除意外残留的配置文件
    ```bash title=""
    dpkg --purge $(dpkg -l | grep '^rc' | awk '{print $2}')
    ```
