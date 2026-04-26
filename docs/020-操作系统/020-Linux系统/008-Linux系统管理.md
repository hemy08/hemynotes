# Linux系统管理

## 概述

Linux系统管理涵盖用户管理、服务管理、日志管理、定时任务等日常运维工作。

## 用户管理

### 用户操作

```bash
# 查看用户
cat /etc/passwd
id username
whoami

# 添加用户
useradd username
useradd -m username          # 创建主目录
useradd -m -s /bin/bash username  # 指定shell

# 设置密码
passwd username

# 删除用户
userdel username
userdel -r username          # 同时删除主目录

# 修改用户
usermod -l newname oldname   # 修改用户名
usermod -d /home/newdir username  # 修改主目录
usermod -s /bin/zsh username # 修改shell
usermod -L username          # 锁定用户
usermod -U username          # 解锁用户
```

### 组管理

```bash
# 查看组
cat /etc/group
groups username

# 添加组
groupadd groupname

# 删除组
groupdel groupname

# 修改组
groupmod -n newname oldname

# 添加用户到组
gpasswd -a username groupname
usermod -aG groupname username

# 从组中删除用户
gpasswd -d username groupname
```

### sudo配置

```bash
# 编辑sudo配置
visudo

# 添加用户sudo权限
username ALL=(ALL) ALL

# 免密码sudo
username ALL=(ALL) NOPASSWD: ALL

# 限制命令
username ALL=(ALL) /usr/bin/apt,/usr/bin/systemctl

# 用户组sudo
%wheel ALL=(ALL) ALL
```

## 服务管理

### systemctl命令

```bash
# 查看服务状态
systemctl status nginx

# 启动服务
systemctl start nginx

# 停止服务
systemctl stop nginx

# 重启服务
systemctl restart nginx

# 重载配置
systemctl reload nginx

# 开机自启
systemctl enable nginx

# 禁用开机自启
systemctl disable nginx

# 查看所有服务
systemctl list-units --type=service
systemctl list-units --type=service --state=running

# 查看失败的服务
systemctl --failed
```

### 服务文件

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
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

```bash
# 创建服务后重载
systemctl daemon-reload
systemctl enable myapp
systemctl start myapp
```

## 日志管理

### journalctl

```bash
# 查看所有日志
journalctl

# 实时查看
journalctl -f

# 查看服务日志
journalctl -u nginx

# 按时间过滤
journalctl --since "2024-01-01"
journalctl --since "1 hour ago"
journalctl --until "2024-01-01 12:00:00"

# 按优先级过滤
journalctl -p err
journalctl -p warning

# 查看内核日志
journalctl -k

# 限制行数
journalctl -n 100

# 详细输出
journalctl -o verbose

# 持久化日志存储
# 编辑 /etc/systemd/journald.conf
Storage=persistent
```

### 传统日志文件

```bash
# 系统日志
tail -f /var/log/syslog
tail -f /var/log/messages

# 认证日志
tail -f /var/log/auth.log

# 内核日志
dmesg
tail -f /var/log/kern.log

# 邮件日志
tail -f /var/log/mail.log

# 日志轮转配置
# /etc/logrotate.conf
# /etc/logrotate.d/
```

## 定时任务

### crontab

```bash
# 编辑当前用户的crontab
crontab -e

# 查看crontab
crontab -l

# 删除crontab
crontab -r

# 编辑其他用户的crontab
crontab -e -u username

# crontab格式
# 分 时 日 月 周 命令
# *  *  *  *  *  command

# 示例
# 每分钟执行
* * * * * /script.sh

# 每小时执行
0 * * * * /script.sh

# 每天凌晨2点执行
0 2 * * * /script.sh

# 每周一凌晨3点执行
0 3 * * 1 /script.sh

# 每月1号执行
0 0 1 * * /script.sh

# 每5分钟执行
*/5 * * * * /script.sh

# 工作日每小时执行
0 * * * 1-5 /script.sh
```

### systemd timer

```bash
# /etc/systemd/system/mytask.timer
[Unit]
Description=My Task Timer

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
# 启用定时器
systemctl enable mytask.timer
systemctl start mytask.timer

# 查看定时器
systemctl list-timers
```

## 网络配置

### 静态IP配置

```bash
# /etc/network/interfaces (Debian/Ubuntu)
auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8 8.8.4.4
```

```bash
# /etc/sysconfig/network-scripts/ifcfg-eth0 (RHEL/CentOS)
TYPE=Ethernet
BOOTPROTO=static
NAME=eth0
DEVICE=eth0
ONBOOT=yes
IPADDR=192.168.1.100
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
DNS1=8.8.8.8
```

### 网络命令

```bash
# 查看网络接口
ip addr
ip link

# 启用/禁用接口
ip link set eth0 up
ip link set eth0 down

# 添加IP地址
ip addr add 192.168.1.100/24 dev eth0

# 删除IP地址
ip addr del 192.168.1.100/24 dev eth0

# 查看路由
ip route
ip route show

# 添加路由
ip route add 192.168.2.0/24 via 192.168.1.1

# 删除路由
ip route del 192.168.2.0/24

# DNS配置
# /etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
```

## 防火墙

### firewalld

```bash
# 查看状态
firewall-cmd --state

# 查看所有规则
firewall-cmd --list-all

# 开放端口
firewall-cmd --add-port=80/tcp
firewall-cmd --add-port=80/tcp --permanent

# 关闭端口
firewall-cmd --remove-port=80/tcp
firewall-cmd --remove-port=80/tcp --permanent

# 开放服务
firewall-cmd --add-service=http
firewall-cmd --add-service=http --permanent

# 重载配置
firewall-cmd --reload

# 查看开放的端口
firewall-cmd --list-ports
```

### ufw

```bash
# 启用防火墙
ufw enable

# 禁用防火墙
ufw disable

# 查看状态
ufw status

# 允许端口
ufw allow 80
ufw allow 80/tcp

# 拒绝端口
ufw deny 80

# 允许IP
ufw allow from 192.168.1.100

# 删除规则
ufw delete allow 80
```

## 参考资料

- [Linux系统管理](https://www.linux.org/docs/)
- [systemd文档](https://www.freedesktop.org/software/systemd/man/)
