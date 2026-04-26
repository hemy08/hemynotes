# Linux进程管理

## 概述

进程是Linux系统中正在运行的程序实例，进程管理是Linux系统管理的核心内容。

## 进程状态

| 状态 | 说明 |
|------|------|
| R | 运行或就绪 |
| S | 可中断睡眠 |
| D | 不可中断睡眠 |
| Z | 僵尸进程 |
| T | 停止 |
| I | 空闲 |

## 进程查看

### ps命令

```bash
# 查看当前用户进程
ps

# 查看所有进程
ps -e
ps aux

# 查看完整命令
ps -ef
ps auxf    # 显示进程树

# 按用户过滤
ps -u root

# 按进程名过滤
ps -C nginx

# 自定义输出
ps -eo pid,ppid,user,%cpu,%mem,cmd

# 查看进程线程
ps -eLf
ps -T -p <pid>
```

### top/htop命令

```bash
# 交互式进程查看
top

# 按CPU排序（交互中按P）
# 按内存排序（交互中按M）
# 按用户过滤（交互中按u）
# 显示线程（交互中按H）

# 批量模式
top -b -n 1 > top_output.txt

# 按用户过滤
top -u nginx

# 监控特定进程
top -p 1234,5678

# htop（需要安装）
htop
```

### pgrep/pkill命令

```bash
# 按名称查找进程ID
pgrep nginx
pgrep -l nginx    # 显示进程名

# 按用户查找
pgrep -u root nginx

# 按命令行匹配
pgrep -f "python script.py"

# 查找并显示详细信息
pgrep -a nginx

# 按名称杀死进程
pkill nginx

# 按用户杀死
pkill -u root

# 强制杀死
pkill -9 nginx
```

## 进程控制

### 启动进程

```bash
# 前台运行
./myprogram

# 后台运行
./myprogram &

# nohup（断开连接后继续运行）
nohup ./myprogram &
nohup ./myprogram > output.log 2>&1 &

# disown（从当前shell剥离作业)
./myprogram &
disown

# setsid（在新会话中运行）
setsid ./myprogram
```

### 停止进程

```bash
# 发送SIGTERM（15）
kill 1234
kill -15 1234

# 发送SIGKILL（9，强制）
kill -9 1234
kill -KILL 1234

# 发送SIGHUP（1，重载配置）
kill -HUP 1234
kill -1 1234

# 发送SIGSTOP（暂停）
kill -STOP 1234

# 发送SIGCONT（继续）
kill -CONT 1234

# 按进程名杀死
killall nginx
killall -9 nginx

# pkill（支持正则）
pkill -f "python.*script"
```

### 控制优先级

```bash
# 查看优先级
ps -eo pid,nice,cmd

# 以指定优先级启动
nice -n 10 ./myprogram    # 降低优先级
nice -n -10 ./myprogram   # 提高优先级（需要root）

# 修改运行中进程优先级
renice 10 -p 1234
renice -5 -p 1234         # 提高优先级需要root

# 按用户修改
renice 5 -u nginx
```

## 后台作业管理

### jobs命令

```bash
# 启动后台作业
sleep 100 &
sleep 200 &

# 查看作业
jobs
jobs -l    # 显示PID

# 前台恢复
fg %1

# 后台恢复
bg %1

# 等待作业完成
wait %1
wait       # 等待所有作业
```

## 进程监控

### watch命令

```bash
# 实时监控命令输出
watch -n 1 'ps aux | grep nginx'

# 高亮变化
watch -d 'free -m'

# 退出时不清屏
watch -n 1 -b 'date'
```

### pstree命令

```bash
# 显示进程树
pstree

# 显示PID
pstree -p

# 显示命令参数
pstree -a

# 指定进程
pstree -p 1234

# 按用户过滤
pstree -u nginx
```

## 孤儿进程

### 检查僵尸进程

```bash
# 查找僵尸进程
ps aux | awk '$8 ~ /Z/ {print}'

# 或
ps -eo pid,ppid,stat,cmd | grep Z
```

### 处理僵尸进程

```bash
# 僵尸进程的父进程需要调用wait()
# 或者杀死父进程，让init进程回收

# 找到父进程
ps -eo pid,ppid,stat,cmd | grep Z

# 杀死父进程（谨慎）
kill <ppid>
```

## 进程资源限制

### ulimit

```bash
# 查看所有限制
ulimit -a

# 文件描述符数量
ulimit -n
ulimit -n 65535    # 设置

# 最大内存
ulimit -v

# CPU时间
ulimit -t

# 栈大小
ulimit -s

# 核心转储大小
ulimit -c
ulimit -c unlimited
```

### /etc/security/limits.conf

```bash
# 永久设置限制
# /etc/security/limits.conf
*    soft    nofile    65535
*    hard    nofile    65535
root soft    nofile    65535
root hard    nofile    65535
```

## 进程间通信查看

### 查看共享内存

```bash
# 查看共享内存
ipcs -m

# 查看信号量
ipcs -s

# 查看消息队列
ipcs -q

# 查看所有
ipcs -a

# 删除共享内存
ipcrm -m <shmid>
```

## 进程诊断

### strace

```bash
# 跟踪系统调用
strace -p 1234

# 跟踪特定系统调用
strace -e open,read,write -p 1234

# 统计系统调用
strace -c -p 1234

# 跟踪新进程
strace ./myprogram
```

### ltrace

```bash
# 跟踪库函数调用
ltrace -p 1234

# 跟踪特定函数
ltrace -e malloc,free ./myprogram
```

## 参考资料

- [Linux进程管理](https://man7.org/linux/man-pages/man7/signal.7.html)
- [ps命令手册](https://man7.org/linux/man-pages/man1/ps.1.html)
