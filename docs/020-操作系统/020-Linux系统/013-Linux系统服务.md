# Linux系统服务

## 概述

Linux系统服务是在后台运行的程序，通过systemd或传统init系统管理。

## systemd服务管理

### 基本操作

```bash
# 查看服务状态
systemctl status nginx
systemctl status sshd

# 启动服务
systemctl start nginx

# 停止服务
systemctl stop nginx

# 重启服务
systemctl restart nginx

# 重载配置
systemctl reload nginx

# 查看是否激活
systemctl is-active nginx

# 查看是否开机自启
systemctl is-enabled nginx
```

### 开机自启

```bash
# 启用开机自启
systemctl enable nginx

# 禁用开机自启
systemctl disable nginx

# 启用并立即启动
systemctl enable --now nginx

# 禁用并立即停止
systemctl disable --now nginx
```

### 服务列表

```bash
# 列出所有服务
systemctl list-units --type=service

# 列出运行中的服务
systemctl list-units --type=service --state=running

# 列出失败的服务
systemctl list-units --type=service --state=failed

# 列出所有单元文件
systemctl list-unit-files --type=service

# 列出已启用的服务
systemctl list-unit-files --type=service --state=enabled
```

## 编写systemd服务

### 简单服务文件

```bash
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=myapp
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/myapp
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### 服务类型

| 类型 | 说明 |
|------|------|
| simple | 主进程就是服务进程 |
| forking | 服务进程fork后退出 |
| oneshot | 执行一次后退出 |
| notify | 服务会发送通知 |
| dbus | D-Bus激活的服务 |

### 完整服务示例

```bash
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application Service
Documentation=https://example.com/docs
After=network.target remote-fs.target nss-lookup.target
Wants=network-online.target

[Service]
Type=notify
User=myapp
Group=myapp
WorkingDirectory=/opt/myapp

Environment="NODE_ENV=production"
EnvironmentFile=/opt/myapp/.env

ExecStart=/opt/myapp/bin/myapp --config /opt/myapp/config.yaml
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/bin/kill -WINCH $MAINPID

Restart=on-failure
RestartSec=5s

LimitNOFILE=65535
LimitNPROC=4096

PrivateTmp=true
ProtectSystem=strict
NoNewPrivileges=true

StandardOutput=journal
StandardError=journal
SyslogIdentifier=myapp

[Install]
WantedBy=multi-user.target
```

### 应用服务文件

```bash
# 重载systemd配置
systemctl daemon-reload

# 启用并启动
systemctl enable --now myapp

# 查看状态
systemctl status myapp

# 查看日志
journalctl -u myapp
```

## 服务依赖

```bash
[Unit]
Description=My Service
After=network.target        # 在network后启动
Requires=network.target     # 依赖network
Wants=network-online.target # 希望network在线
Conflicts=oldapp.service    # 与oldapp冲突
Before=otherapp.service     # 在otherapp之前启动
```

## 服务日志

### journalctl查看

```bash
# 查看服务日志
journalctl -u nginx

# 实时查看
journalctl -u nginx -f

# 限制行数
journalctl -u nginx -n 100

# 按时间过滤
journalctl -u nginx --since "1 hour ago"
journalctl -u nginx --since "2024-01-01"
journalctl -u nginx --since "2024-01-01 10:00:00" --until "2024-01-01 11:00:00"

# 按优先级过滤
journalctl -u nginx -p err
journalctl -u nginx -p warning

# 查看内核消息
journalctl -k

# 持续监控所有日志
journalctl -f
```

## 传统init脚本

### /etc/init.d脚本

```bash
#!/bin/bash
# /etc/init.d/myapp

case "$1" in
    start)
        echo "Starting myapp"
        /opt/myapp/bin/myapp &
        echo $! > /var/run/myapp.pid
        ;;
    stop)
        echo "Stopping myapp"
        kill $(cat /var/run/myapp.pid)
        rm /var/run/myapp.pid
        ;;
    restart)
        $0 stop
        $0 start
        ;;
    status)
        if [ -f /var/run/myapp.pid ]; then
            echo "myapp is running"
        else
            echo "myapp is not running"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0
```

```bash
# 使用service命令
service myapp start
service myapp stop
service myapp status
```

## 定时器服务

### 创建定时器

```bash
# /etc/systemd/system/mytask.service
[Unit]
Description=My Task

[Service]
Type=oneshot
ExecStart=/opt/scripts/mytask.sh
```

```bash
# /etc/systemd/system/mytask.timer
[Unit]
Description=My Task Timer

[Timer]
OnCalendar=*-*-* 02:00:00    # 每天凌晨2点
Persistent=true               # 错过时间后补执行

[Install]
WantedBy=timers.target
```

```bash
# 启用定时器
systemctl enable --now mytask.timer

# 查看定时器
systemctl list-timers
```

### 定时器配置

```bash
[Timer]
OnCalendar=*-*-* 02:00:00     # 每天2点
OnCalendar=*-*-* *:0:0        # 每小时
OnCalendar=Mon *-*-* 00:00:00 # 每周一
OnCalendar=*-*-01 00:00:00    # 每月1号

OnBootSec=5min                # 启动后5分钟
OnUnitActiveSec=1h            # 每小时执行

RandomizedDelaySec=300        # 随机延迟（分散负载）
```

## Socket激活

```bash
# /etc/systemd/system/myapp.socket
[Unit]
Description=My App Socket

[Socket]
ListenStream=8080

[Install]
WantedBy=sockets.target
```

```bash
# /etc/systemd/system/myapp@.service
[Unit]
Description=My App Instance

[Service]
ExecStart=/opt/myapp/bin/myapp
StandardInput=socket
```

## 服务资源限制

```bash
[Service]
# CPU限制
CPUQuota=50%
CPUShares=512

# 内存限制
MemoryLimit=1G
MemoryHigh=800M
MemoryLow=200M

# 进程数限制
LimitNPROC=100

# 文件描述符限制
LimitNOFILE=65535

# I/O限制
IOReadBandwidthMax=/dev/sda1 10M
IOWriteBandwidthMax=/dev/sda1 10M
```

## 参考资料

- [systemd文档](https://www.freedesktop.org/software/systemd/man/)
- [编写systemd服务](https://wiki.archlinux.org/title/Systemd)
