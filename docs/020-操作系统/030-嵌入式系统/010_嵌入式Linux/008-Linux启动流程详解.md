# Linux启动流程详解

## 概述

Linux系统启动过程从上电到用户空间可用，经历多个阶段，理解每个阶段有助于系统优化和问题排查。

## 启动流程概览

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  上电复位   │ -> │  Bootloader │ -> │   内核启动  │
└─────────────┘    └─────────────┘    └─────────────┘
                                              │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 用户空间    │ <- │  init进程   │ <- │ 根文件系统  │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 第一阶段：Bootloader

### Bootloader功能

1. **硬件初始化**
   - CPU初始化
   - 内存控制器初始化
   - 串口初始化（调试输出）
   - 存储设备初始化

2. **加载内核**
   - 从存储设备读取内核镜像
   - 解压内核（如需要）
   - 加载设备树

3. **传递参数**
   - 内核启动参数（bootargs）
   - 设备树地址
   - initramfs地址

### U-Boot启动流程

```
_start (arch/arm/lib/vector.S)
    │
    ▼
reset (arch/arm/lib/start.S)
    │
    ├── CPU初始化
    ├── 板级初始化 (board_init_f)
    │       ├── 时钟初始化
    │       ├── 内存初始化
    │       └── 环境变量初始化
    │
    ├── 重定位到RAM
    │
    └── 板级初始化 (board_init_r)
            ├── 设备初始化
            ├── 环境变量加载
            └── 进入主循环 (main_loop)
                    ├── 处理命令
                    └── 自动启动 (bootm)
```

### U-Boot环境变量

```bash
# 查看环境变量
printenv

# 设置启动命令
setenv bootcmd 'fatload mmc 0:1 0x42000000 zImage; fatload mmc 0:1 0x43000000 dtb; bootz 0x42000000 - 0x43000000'

# 设置启动参数
setenv bootargs 'console=ttyS0,115200 root=/dev/mmcblk0p2 rootwait'

# 保存环境变量
saveenv
```

## 第二阶段：内核启动

### 内核入口

```c
// arch/arm/kernel/head.S
ENTRY(stext)
    // 检查处理器ID
    bl  __lookup_processor_type
    // 检查机器类型
    bl  __lookup_machine_type
    // 创建页表
    bl  __create_page_tables
    // 启用MMU
    b   __enable_mmu
    // 跳转到C代码
    b   __mmap_switched
ENDPROC(stext)
```

### start_kernel流程

```c
// init/main.c
asmlinkage __visible void __init start_kernel(void)
{
    // 早期设置
    setup_arch(&command_line);      // 架构相关初始化
    setup_log_buf(0);               // 日志缓冲区
    setup_nr_cpu_ids();             // CPU数量
    smp_prepare_boot_cpu();         // SMP准备
    
    // 内存管理初始化
    setup_per_cpu_areas();          // per-cpu区域
    build_all_zonelists(NULL);      // 内存区域
    page_alloc_init();              // 页分配器
    
    // 中断和时间初始化
    trap_init();                    // 陷阱门
    early_irq_init();               // 中断控制器
    tick_init();                    // 时钟
    init_timers();                  // 定时器
    hrtimers_init();                // 高精度定时器
    timekeeping_init();             // 时间保持
    time_init();                    // 架构时间初始化
    
    // 进程调度初始化
    sched_init();                   // 调度器
    
    // 工作队列和RCU
    workqueue_init_early();         // 工作队列
    rcu_init();                     // RCU
    
    // 中断后期初始化
    init_IRQ();                     // 中断
    softirq_init();                 // 软中断
    timekeeping_init();             // 时间
    
    // 进程1初始化
    rest_init();                    // 启动init进程
}
```

### rest_init

```c
static noinline void __ref rest_init(void)
{
    // 创建内核线程init（PID 1）
    kernel_thread(kernel_init, NULL, CLONE_FS);
    
    // 创建内核线程kthreadd（PID 2）
    pid = kernel_thread(kthreadd, NULL, CLONE_FS | CLONE_FILES);
    
    // 启用调度
    schedule_preempt_disabled();
    
    // idle循环
    cpu_startup_entry(CPUHP_AP_ONLINE_IDLE);
}
```

### kernel_init

```c
static int __ref kernel_init(void *unused)
{
    // 等待kthreadd完成
    wait_for_completion(&kthreadd_done);
    
    // 初始化驱动
    do_basic_setup();
    
    // 挂载根文件系统
    if (!ramdisk_execute_command)
        ramdisk_execute_command = "/init";
    
    if (sys_access((const char __user *) ramdisk_execute_command, 0) != 0) {
        ramdisk_execute_command = NULL;
        prepare_namespace();
    }
    
    // 执行init程序
    if (ramdisk_execute_command) {
        run_init_process(ramdisk_execute_command);
    }
    
    if (execute_command) {
        run_init_process(execute_command);
    }
    
    // 尝试标准init路径
    run_init_process("/sbin/init");
    run_init_process("/etc/init");
    run_init_process("/bin/init");
    run_init_process("/bin/sh");
    
    panic("No init found.  Try passing init= option to kernel.");
}
```

## 第三阶段：init进程

### init程序功能

1. **系统服务启动**
   - 启动系统服务
   - 管理运行级别
   - 进程监控和重启

2. **用户登录**
   - 启动getty
   - 处理用户登录

### SysV init

```bash
# /etc/inittab
::sysinit:/etc/init.d/rcS
::respawn:-/bin/sh
::askfirst:-/bin/sh
::ctrlaltdel:/bin/umount -a -r
::shutdown:/bin/umount -a -r
```

### systemd

```bash
# 查看启动服务
systemctl list-units --type=service

# 启动服务
systemctl start myservice

# 开机自启
systemctl enable myservice

# 查看启动耗时
systemd-analyze
systemd-analyze blame
```

### BusyBox init

```bash
# /etc/inittab
::sysinit:/etc/init.d/rcS
ttyS0::askfirst:-/bin/sh
::ctrlaltdel:/bin/umount -a -r
```

## initramfs

### initramfs作用

1. 加载必要的驱动模块
2. 挂载真正的根文件系统
3. 切换到根文件系统

### initramfs结构

```
initramfs/
├── bin/          基本命令
├── sbin/         系统命令
├── lib/          库文件
├── lib/modules/  内核模块
├── etc/          配置文件
├── dev/          设备节点
├── init          初始化脚本
└── usr/          用户程序
```

### init脚本示例

```bash
#!/bin/sh

# 挂载虚拟文件系统
mount -t proc none /proc
mount -t sysfs none /sys
mount -t devtmpfs none /dev

# 加载必要的模块
modprobe mmc_core
modprobe mmc_block
modprobe sdhci

# 挂载根文件系统
mkdir /mnt/root
mount -t ext4 /dev/mmcblk0p2 /mnt/root

# 切换到根文件系统
exec switch_root /mnt/root /sbin/init
```

## 启动时间优化

### 测量启动时间

```bash
# 使用systemd-analyze
systemd-analyze time
systemd-analyze blame
systemd-analyze critical-chain

# 使用bootgraph
dmesg | perl scripts/bootgraph.pl > boot.svg
```

### 优化方法

1. **内核优化**
   ```bash
   # 禁用不需要的驱动
   # 使用内置驱动代替模块
   # 压缩内核
   ```

2. **Bootloader优化**
   ```bash
   # 减少启动延时
   setenv bootdelay 0
   
   # 使用更快的存储设备
   ```

3. **文件系统优化**
   ```bash
   # 使用更快的文件系统
   # 减少启动服务
   # 并行启动服务
   ```

## 启动问题排查

### 内核启动失败

```bash
# 检查内核消息
dmesg

# 检查内核 panic
# 常见原因：
# - 根文件系统挂载失败
# - 缺少驱动
# - 内存不足
```

### 根文件系统挂载失败

```bash
# 检查启动参数
cat /proc/cmdline

# 检查设备节点
ls /dev

# 检查文件系统类型
file -s /dev/mmcblk0p2
```

### init失败

```bash
# 检查init程序
ls -la /sbin/init

# 检查依赖库
ldd /sbin/init

# 尝试手动启动
init=/bin/sh
```

## 参考资料

- [Linux内核启动](https://www.kernel.org/doc/html/latest/x86/boot.html)
- [U-Boot文档](https://u-boot.readthedocs.io/)
- [systemd手册](https://www.freedesktop.org/software/systemd/man/)
