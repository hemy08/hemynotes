# Linux性能监控

## 概述

Linux性能监控帮助识别系统瓶颈，优化系统性能，确保系统稳定运行。

## CPU监控

### top命令

```bash
# 实时监控
top

# 批量输出
top -b -n 1

# 按CPU使用率排序
top -o %CPU

# 查看特定用户
top -u nginx

# 显示所有CPU核心
top -1
```

### mpstat

```bash
# 安装
apt install sysstat

# 查看CPU统计
mpstat

# 查看每个CPU核心
mpstat -P ALL

# 每秒更新
mpstat 1

# 指定间隔和次数
mpstat 1 10
```

### uptime

```bash
# 查看系统负载
uptime
# 输出: load average: 0.50, 0.70, 0.80
# 分别是1分钟、5分钟、15分钟平均负载
```

## 内存监控

### free命令

```bash
# 查看内存使用
free
free -h    # 人类可读格式
free -m    # MB单位
free -g    # GB单位

# 输出说明:
# total: 总内存
# used: 已使用
# free: 空闲
# shared: 共享内存
# buff/cache: 缓冲区/缓存
# available: 可用内存（估算）
```

### vmstat

```bash
# 查看内存统计
vmstat

# 每秒更新
vmstat 1

# 指定次数
vmstat 1 10

# 输出说明:
# si: 每秒从交换区读入内存
# so: 每秒从内存写入交换区
# bi: 每秒读取块设备
# bo: 每秒写入块设备
# us: 用户CPU时间
# sy: 系统CPU时间
# id: 空闲CPU时间
```

### 查看进程内存

```bash
# 按内存使用排序
ps aux --sort=-%mem | head

# 查看进程内存详情
pmap -x <pid>

# /proc/meminfo
cat /proc/meminfo
```

## 磁盘监控

### df命令

```bash
# 查看磁盘使用
df
df -h    # 人类可读格式
df -T    # 显示文件系统类型
df -i    # 显示inode使用
```

### du命令

```bash
# 查看目录大小
du -sh /path
du -h --max-depth=1 /path
du -sh * | sort -h    # 排序

# 查找大文件
find / -type f -size +100M 2>/dev/null
```

### iostat

```bash
# 查看IO统计
iostat
iostat -x    # 详细信息
iostat 1     # 每秒更新
iostat -x 1 10
```

### iotop

```bash
# 安装
apt install iotop

# 实时IO监控
iotop

# 只显示有IO的进程
iotop -o

# 批量模式
iotop -b -n 1
```

## 网络监控

### iftop

```bash
# 安装
apt install iftop

# 实时网络流量
iftop
iftop -i eth0    # 指定接口
iftop -P         # 显示端口
```

### nethogs

```bash
# 安装
apt install nethogs

# 按进程显示网络流量
nethogs
nethogs eth0
```

### netstat/ss

```bash
# 查看连接
netstat -an
ss -an

# 查看监听端口
netstat -tlnp
ss -tlnp

# 查看统计
netstat -s
ss -s
```

### sar

```bash
# 查看网络统计
sar -n DEV     # 网络设备
sar -n EDEV    # 网络错误
sar -n SOCK    # socket统计

# 查看历史数据
sar -n DEV -f /var/log/sa/sa01
```

## 综合监控工具

### htop

```bash
# 安装
apt install htop

# 运行
htop

# 快捷键:
# F1: 帮助
# F2: 设置
# F3: 搜索
# F4: 过滤
# F5: 树形视图
# F6: 排序
# F9: 杀死进程
# F10: 退出
```

### glances

```bash
# 安装
pip install glances

# 运行
glances
glances -w    # Web模式
```

### dstat

```bash
# 安装
apt install dstat

# 综合监控
dstat

# CPU和内存
dstat -cm

# 磁盘和网络
dstat -dn

# 完整输出
dstat -cdngy
```

## 性能分析

### perf

```bash
# 安装
apt install linux-perf

# 性能分析
perf top
perf record -g ./myapp
perf report

# 统计事件
perf stat ./myapp
```

### strace

```bash
# 跟踪系统调用
strace ./myapp
strace -p <pid>
strace -c ./myapp    # 统计
strace -e open,read ./myapp
```

### ltrace

```bash
# 跟踪库函数
ltrace ./myapp
ltrace -c ./myapp
```

## 系统调优

### 内核参数调优

```bash
# 查看参数
sysctl -a
sysctl net.ipv4.tcp_tw_reuse

# 临时修改
sysctl -w net.ipv4.tcp_tw_reuse=1

# 永久修改
# /etc/sysctl.conf
net.ipv4.tcp_tw_reuse = 1
net.ipv4.ip_local_port_range = 1024 65535
net.core.somaxconn = 65535

# 应用配置
sysctl -p
```

### 文件描述符限制

```bash
# 查看限制
ulimit -n

# 临时修改
ulimit -n 65535

# 永久修改
# /etc/security/limits.conf
* soft nofile 65535
* hard nofile 65535
```

## 监控告警脚本

```bash
#!/bin/bash
# 简单监控脚本

# CPU告警阈值
CPU_THRESHOLD=80

# 内存告警阈值
MEM_THRESHOLD=90

# 磁盘告警阈值
DISK_THRESHOLD=90

# 检查CPU
cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
if (( $(echo "$cpu_usage > $CPU_THRESHOLD" | bc -l) )); then
    echo "CPU使用率告警: $cpu_usage%"
fi

# 检查内存
mem_usage=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
if (( $(echo "$mem_usage > $MEM_THRESHOLD" | bc -l) )); then
    echo "内存使用率告警: $mem_usage%"
fi

# 检查磁盘
disk_usage=$(df -h / | grep '/' | awk '{print $5}' | cut -d'%' -f1)
if [ "$disk_usage" -gt "$DISK_THRESHOLD" ]; then
    echo "磁盘使用率告警: $disk_usage%"
fi
```

## 参考资料

- [Linux性能分析](https://www.brendangregg.com/linuxperf.html)
- [sysstat工具](https://github.com/sysstat/sysstat)
