# QEMU模拟器

## 概述

QEMU（Quick Emulator）是一个通用的开源模拟器和虚拟机，可以模拟多种处理器架构和硬件设备，常用于嵌入式开发测试。

## QEMU特点

1. **多架构支持**：ARM、MIPS、RISC-V、x86等
2. **全系统模拟**：模拟完整的计算机系统
3. **用户态模拟**：在x86上运行其他架构程序
4. **硬件虚拟化**：支持KVM加速
5. **设备模拟**：模拟各种外设

## 安装QEMU

### 包管理器安装

```bash
# Ubuntu/Debian
sudo apt install qemu-system-arm qemu-user-static

# Fedora
sudo dnf install qemu-system-arm qemu-user-static

# macOS
brew install qemu
```

### 从源码编译

```bash
git clone https://gitlab.com/qemu-project/qemu.git
cd qemu
./configure --target-list=arm-softmmu,aarch64-softmmu,arm-linux-user
make -j$(nproc)
sudo make install
```

## 系统模式模拟

### ARM Linux模拟

```bash
# 下载内核和根文件系统
wget https://releases.linaro.org/components/kernel/linaro-linux/latest/Image
wget https://releases.linaro.org/components/kernel/linaro-linux/latest/linaro-image-minimal-armhf.cpio.gz

# 启动ARM Linux
qemu-system-arm -M virt -cpu cortex-a15 -m 256 \
    -kernel Image \
    -initrd linaro-image-minimal-armhf.cpio.gz \
    -append "console=ttyAMA0" \
    -nographic
```

### ARM64 Linux模拟

```bash
qemu-system-aarch64 -M virt -cpu cortex-a57 -m 512 \
    -kernel Image \
    -initrd rootfs.cpio.gz \
    -append "console=ttyAMA0 root=/dev/ram" \
    -nographic
```

### RISC-V模拟

```bash
qemu-system-riscv64 -M virt -m 256 \
    -kernel opensbi-qemu-virt-riscv64.bin \
    -nographic
```

## 用户模式模拟

### 运行ARM程序

```bash
# 静态编译程序
arm-linux-gnueabihf-gcc -static -o hello hello.c

# 运行程序
qemu-arm-static ./hello

# 带调试运行
qemu-arm-static -g 1234 ./hello &
gdb-multiarch ./hello
(gdb) target remote :1234
```

### 使用sysroot

```bash
# 指定sysroot
qemu-arm-static -L /path/to/sysroot ./myapp

# 示例
qemu-arm-static -L /usr/arm-linux-gnueabihf ./myapp
```

## QEMU启动选项

### CPU和内存

```bash
# 指定CPU类型
-cpu cortex-a9
-cpu cortex-a53
-cpu max        # 支持所有特性

# 设置内存
-m 256          # 256MB内存
-m 1G           # 1GB内存
```

### 设备选项

```bash
# 串口
-serial stdio         # 标准输入输出
-serial mon:stdio     # 带监控器
-nographic            # 禁用图形，使用串口

# 网络设备
-netdev user,id=net0,hostfwd=tcp::2222-:22
-device virtio-net-pci,netdev=net0

# 块设备（磁盘）
-drive file=disk.img,format=raw,if=virtio

# USB设备
-usb
-usbdevice mouse
-usbdevice keyboard
```

### 调试选项

```bash
# 启用GDB服务器
-s                  # 等待GDB连接（端口1234）
-S                  # 启动时暂停

# 完整调试启动
qemu-system-arm -M virt -kernel zImage -s -S
gdb-multiarch vmlinux
(gdb) target remote localhost:1234
```

## 设备模拟

### 串口设备

```bash
# 标准串口
-serial stdio

# 多串口
-serial stdio -serial file:serial1.log

# 连接到伪终端
-serial pty
```

### 网络设备

```bash
# 用户模式网络
-netdev user,id=net0
-device virtio-net-device,netdev=net0

# 带端口转发
-netdev user,id=net0,hostfwd=tcp::8080-:80,hostfwd=tcp::2222-:22

# TAP网络（需要root权限）
-netdev tap,id=net0,ifname=tap0
-device virtio-net-pci,netdev=net0
```

### 存储设备

```bash
# 创建磁盘镜像
qemu-img create -f raw disk.img 1G
qemu-img create -f qcow2 disk.qcow2 1G

# 使用磁盘
-drive file=disk.img,format=raw,if=virtio

# SD卡模拟
-drive file=sd.img,format=raw,if=sd
```

## 嵌入式开发板模拟

### 树莓派

```bash
# 树莓派2
qemu-system-arm -M raspi2 -cpu cortex-a7 -m 1G \
    -kernel kernel7.img \
    -dtb bcm2709-rpi-2-b.dtb \
    -append "console=ttyAMA0 root=/dev/mmcblk0p2" \
    -drive file=raspbian.img,format=raw,if=sd \
    -nographic

# 树莓派3
qemu-system-aarch64 -M raspi3 -cpu cortex-a53 -m 1G \
    -kernel kernel8.img \
    -nographic
```

### STM32模拟

```bash
# 使用xPack QEMU ARM
qemu-system-gnu-mcu-eclipse -board nucleo-f401re \
    -image firmware.elf

# 或使用官方QEMU
qemu-system-arm -M netduino2 -kernel firmware.elf
```

### BeagleBone

```bash
qemu-system-arm -M beagle -m 256 \
    -kernel zImage \
    -dtb am335x-boneblack.dtb \
    -nographic
```

## GDB调试集成

### 启动调试会话

```bash
# 终端1：启动QEMU
qemu-system-arm -M virt -kernel zImage -s -S -nographic

# 终端2：启动GDB
gdb-multiarch vmlinux
(gdb) target remote localhost:1234
(gdb) break start_kernel
(gdb) continue
```

### 内核调试

```bash
(gdb) break schedule        # 调度函数断点
(gdb) break do_fork         # 进程创建断点
(gdb) info registers        # 查看寄存器
(gdb) backtrace             # 查看调用栈
```

### 应用程序调试

```bash
# 编译带调试信息的程序
arm-linux-gnueabihf-gcc -g -o myapp myapp.c

# 启动QEMU用户模式
qemu-arm-static -g 1234 ./myapp &

# GDB调试
gdb-multiarch ./myapp
(gdb) target remote :1234
(gdb) break main
(gdb) continue
```

## QEMU监控器

### 进入监控器

```bash
# Ctrl+A, C 切换到监控器
# 或使用 -monitor stdio

(qemu) info status          # 查看状态
(qemu) info cpus            # 查看CPU
(qemu) info block           # 查看块设备
(qemu) info network         # 查看网络
(qemu) savevm snapshot1     # 保存快照
(qemu) loadvm snapshot1     # 加载快照
(qemu) quit                 # 退出
```

## 性能分析

### TCG加速

```bash
# TCG（Tiny Code Generator）是QEMU默认的软件模拟
# 可以使用多线程加速
-accel tcg,thread=multi
```

### KVM加速（x86主机）

```bash
# 使用KVM加速
qemu-system-x86_64 -enable-kvm -m 1G -kernel bzImage
```

## 快照功能

```bash
# 启动时启用快照
qemu-system-arm ... -drive file=disk.qcow2,format=qcow2

# 在监控器中
(qemu) savevm my_snapshot
(qemu) loadvm my_snapshot
(qemu) delvm my_snapshot
(qemu) info snapshots
```

## 常用场景

### 测试内核模块

```bash
# 启动带调试的QEMU
qemu-system-arm -M virt -kernel zImage -s -S

# 加载模块
insmod mymodule.ko

# 测试功能
cat /proc/mymodule
```

### 交叉编译测试

```bash
# 编译ARM程序
arm-linux-gnueabihf-gcc -o test test.c

# 在QEMU中运行
qemu-arm-static -L /usr/arm-linux-gnueabihf ./test
```

### 系统启动测试

```bash
# 测试U-Boot
qemu-system-arm -M vexpress-a9 -kernel u-boot -nographic

# 在U-Boot中
=> bootm 0x42000000
```

## 参考资料

- [QEMU官网](https://www.qemu.org/)
- [QEMU文档](https://qemu.readthedocs.io/)
- [QEMU用户模式](https://qemu.readthedocs.io/en/latest/user/main.html)
