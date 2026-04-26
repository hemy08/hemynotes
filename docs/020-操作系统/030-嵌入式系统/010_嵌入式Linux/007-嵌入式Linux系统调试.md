# 嵌入式Linux系统调试

## 概述

嵌入式Linux系统调试涵盖内核调试、用户程序调试、系统性能分析等多个方面，掌握调试技术对嵌入式开发至关重要。

## 内核调试

### printk调试

```c
#include <linux/printk.h>

printk(KERN_INFO "Information message\n");
printk(KERN_ERR "Error message\n");
printk(KERN_DEBUG "Debug message\n");

// 动态调试
pr_debug("Dynamic debug message\n");
dev_info(dev, "Device info\n");
dev_err(dev, "Device error\n");
```

### 调整日志级别

```bash
# 查看当前日志级别
cat /proc/sys/kernel/printk

# 设置日志级别
echo "8 8 8 8" > /proc/sys/kernel/printk

# 在控制台输出所有消息
dmesg -n 8
```

### 动态调试（Dynamic Debug）

```bash
# 启用所有动态调试
echo 8 > /proc/sys/kernel/printk
mount -t debugfs none /sys/kernel/debug

# 启用特定文件的调试
echo "file mydriver.c +p" > /sys/kernel/debug/dynamic_debug/control

# 启用特定函数的调试
echo "func my_function +p" > /sys/kernel/debug/dynamic_debug/control

# 查看当前状态
cat /sys/kernel/debug/dynamic_debug/control
```

### KGDB内核调试

```bash
# 内核配置
CONFIG_KGDB=y
CONFIG_KGDB_SERIAL_CONSOLE=y

# 启动参数
kgdboc=ttyS0,115200 kgdbwait

# 在GDB中连接
gdb vmlinux
(gdb) target remote /dev/ttyS0
(gdb) break my_function
(gdb) continue
```

### Kdump内核崩溃分析

```bash
# 安装kdump工具
apt install kdump-tools

# 配置crashkernel参数
crashkernel=128M

# 查看崩溃转储
crash /usr/lib/debug/vmlinux /var/crash/vmcore
```

## GDB调试

### 交叉编译GDB

```bash
# 编译GDB
./configure --target=arm-linux-gnueabihf --prefix=/opt/arm-gdb
make && make install

# 启动GDB
arm-linux-gnueabihf-gdb ./myprogram
```

### 远程调试

目标机：
```bash
gdbserver :1234 ./myprogram
# 或附加到运行中的进程
gdbserver :1234 --attach <pid>
```

开发机：
```bash
arm-linux-gnueabihf-gdb ./myprogram
(gdb) target remote 192.168.1.100:1234
(gdb) break main
(gdb) continue
(gdb) step
(gdb) next
(gdb) print variable
(gdb) backtrace
```

### GDB常用命令

```bash
# 断点
break main                # 函数断点
break file.c:100          # 行号断点
break *0x400000           # 地址断点
delete 1                  # 删除断点
info breakpoints          # 查看断点

# 执行控制
run                       # 运行程序
continue                  # 继续执行
step                      # 单步进入
next                      # 单步跳过
finish                    # 执行到函数返回

# 查看信息
print var                 # 打印变量
print *ptr                # 打印指针内容
print array[0]@10         # 打印数组前10个元素
info registers            # 查看寄存器
backtrace                 # 查看调用栈
x/10x 0x400000            # 查看内存

# 监视
watch var                 # 监视变量变化
rwatch var                # 监视读
awatch var                # 监视读写
```

### GDB脚本

```bash
# .gdbinit文件
set auto-load safe-path /
set sysroot /path/to/sysroot

define my_macro
    break main
    run
    backtrace
end
```

## strace系统调用跟踪

### 基本使用

```bash
# 跟踪程序
strace ./myprogram

# 跟踪特定系统调用
strace -e open,read,write ./myprogram

# 跟踪网络相关
strace -e network ./myprogram

# 附加到进程
strace -p <pid>
```

### 输出选项

```bash
# 输出到文件
strace -o output.txt ./myprogram

# 显示时间戳
strace -t ./myprogram

# 显示相对时间
strace -r ./myprogram

# 显示执行时间
strace -T ./myprogram

# 显示进程ID
strace -f ./myprogram
```

### 分析示例

```bash
# 查看打开的文件
strace -e openat ./myprogram 2>&1 | grep openat

# 查看内存分配
strace -e brk,mmap ./myprogram

# 统计系统调用
strace -c ./myprogram
```

## ltrace库调用跟踪

```bash
# 跟踪库函数调用
ltrace ./myprogram

# 跟踪特定函数
ltrace -e malloc+free ./myprogram

# 跟踪系统调用和库调用
ltrace -S ./myprogram
```

## 系统性能分析

### top/htop

```bash
# 实时查看进程
top
htop

# 按CPU使用排序
top -o %CPU

# 按内存使用排序
top -o %MEM

# 查看特定进程
top -p <pid>
```

### vmstat

```bash
# 每秒显示一次
vmstat 1

# 查看10次
vmstat 1 10
```

输出说明：
- procs: 进程信息（r运行，b阻塞）
- memory: 内存信息（swpd交换，free空闲，buff缓冲，cache缓存）
- swap: 交换分区（si换入，so换出）
- io: IO信息（bi读入，bo写出）
- system: 系统信息（in中断，cs上下文切换）
- cpu: CPU信息（us用户，sy系统，id空闲，wa等待IO）

### iostat

```bash
# 查看IO统计
iostat

# 每秒更新
iostat 1

# 查看所有设备
iostat -x 1
```

### netstat/ss

```bash
# 查看网络连接
netstat -an
ss -an

# 查看监听端口
netstat -tlnp
ss -tlnp

# 查看统计信息
netstat -s
ss -s
```

### perf性能分析

```bash
# 记录性能数据
perf record ./myprogram

# 查看报告
perf report

# 实时查看
perf top

# 统计事件
perf stat ./myprogram

# 跟踪特定事件
perf record -e cycles,instructions ./myprogram
```

### ftrace内核跟踪

```bash
# 挂载tracefs
mount -t tracefs none /sys/kernel/tracing

# 跟踪函数
echo function > /sys/kernel/tracing/current_tracer
echo do_sys_open > /sys/kernel/tracing/set_ftrace_filter
cat /sys/kernel/tracing/trace

# 跟踪函数调用图
echo function_graph > /sys/kernel/tracing/current_tracer

# 跟踪事件
echo sched:sched_switch > /sys/kernel/tracing/set_event
```

## 内存调试

### valgrind内存检测

```bash
# 内存泄漏检测
valgrind --leak-check=full ./myprogram

# 检测未初始化的内存使用
valgrind --track-origins=yes ./myprogram

# 线程错误检测
valgrind --tool=helgrind ./myprogram

# 堆分析
valgrind --tool=massif ./myprogram
```

### AddressSanitizer

```c
// 编译时启用
gcc -fsanitize=address -g myprogram.c -o myprogram

// 运行程序
./myprogram
```

## 网络调试

### tcpdump抓包

```bash
# 抓取所有包
tcpdump -i eth0

# 抓取特定端口
tcpdump -i eth0 port 80

# 抓取TCP包
tcpdump -i eth0 tcp

# 保存到文件
tcpdump -i eth0 -w capture.pcap

# 读取文件
tcpdump -r capture.pcap

# 显示ASCII内容
tcpdump -A -i eth0 port 80
```

### wireshark分析

```bash
# 命令行分析
tshark -r capture.pcap

# 过滤显示
tshark -r capture.pcap -Y "http"
```

## 系统故障分析

### 内核崩溃分析

```bash
# 查看oops信息
dmesg | grep -i oops

# 使用crash工具分析
crash /usr/lib/debug/vmlinux /var/crash/vmcore

# crash常用命令
crash> bt              # 查看调用栈
crash> ps              # 查看进程
crash> files           # 查看打开的文件
crash> vm              # 查看内存信息
```

### 系统挂起分析

```bash
# 触发SysRq
echo t > /proc/sysrq-trigger    # 显示所有任务
echo m > /proc/sysrq-trigger    # 显示内存信息
echo w > /proc/sysrq-trigger    # 显示阻塞任务
echo c > /proc/sysrq-trigger    # 触发崩溃

# 启用SysRq
echo 1 > /proc/sys/kernel/sysrq
```

## 硬件调试

### JTAG调试

```bash
# 使用OpenOCD
openocd -f interface/jlink.cfg -f target/stm32f4x.cfg

# GDB连接
gdb-multiarch
(gdb) target remote localhost:3333
(gdb) monitor reset halt
(gdb) load
(gdb) continue
```

### 串口调试

```bash
# 使用minicom
minicom -D /dev/ttyUSB0

# 使用screen
screen /dev/ttyUSB0 115200

# 使用cu
cu -l /dev/ttyUSB0 -s 115200
```

## 参考资料

- [Linux内核调试](https://www.kernel.org/doc/html/latest/admin-guide/bug-hunting.html)
- [GDB手册](https://sourceware.org/gdb/current/onlinedocs/gdb/)
- [perf工具](https://perf.wiki.kernel.org/)
- [OpenOCD手册](http://openocd.org/documentation/)
