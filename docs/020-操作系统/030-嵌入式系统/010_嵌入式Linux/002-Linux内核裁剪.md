# Linux内核裁剪

## 概述

Linux内核裁剪是嵌入式开发的重要环节，通过移除不需要的功能和驱动，可以显著减小内核体积、降低内存占用、提高启动速度。

## 裁剪目标

1. **减小内核体积**：从数百MB减小到几MB
2. **降低内存占用**：减少运行时内存消耗
3. **加快启动速度**：减少初始化时间和模块加载
4. **提高安全性**：移除不必要的功能减少攻击面
5. **优化性能**：针对性优化关键功能

## 获取内核源码

### 官方内核

```bash
# 下载官方内核
wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.15.tar.xz
tar xvf linux-5.15.tar.xz
cd linux-5.15
```

### 厂商内核

```bash
# 树莓派内核
git clone --depth=1 https://github.com/raspberrypi/linux.git

# 全志内核
git clone https://github.com/linux-sunxi/linux-sunxi.git

# NXP i.MX内核
git clone https://source.codeaurora.org/external/imx/linux-imx.git
```

## 内核配置方法

### 使用默认配置

```bash
# 查看支持的架构
ls arch/

# 使用默认配置
make defconfig                        # 默认配置
make bcmrpi3_defconfig                # 树莓派3
make sun8i_h3_defconfig               # 全志H3
make imx_v7_defconfig                 # i.MX6/7
```

### 图形化配置

```bash
# 文本界面配置
make menuconfig

# Qt图形界面配置
make xconfig

# GTK图形界面配置
make gconfig

# 保存配置
cp .config arch/arm/configs/myboard_defconfig
```

### 从现有配置修改

```bash
# 加载现有配置
make myboard_defconfig

# 修改配置
make menuconfig

# 保存为新的默认配置
make savedefconfig
cp defconfig arch/arm/configs/myboard_defconfig
```

## 常用配置选项

### 通用设置

```
General setup  --->
    [ ] Configure standard kernel features (expert users)  ---> 
    [ ] Enable loadable module support                      # 禁用模块支持
    [ ] Enable the slab memory cache                        # 使用slab分配器
    (256) Initial RAM filesystem disk capacity (kB)         # 减小initramfs大小
```

### 处理器类型

```
System Type  --->
    [*] Support for the ARM EABI using binfmt_misc          # ARM EABI支持
    (3) Maximum number of CPUs (2-32)                       # CPU数量
    [*] SMP (Symmetric Multi-Processing) support            # 多核支持
```

### 调度器配置

```
General setup  --->
    [*] CPU/Task time and stats accounting  --->
        [*]   Export task/pid/cgroup time to user via /proc
    [ ] Support for hot-pluggable devices                   # 禁用热插拔
```

### 内存管理

```
General setup  --->
    [*] Enable VM event counters                           # VM事件计数
    [ ] Enable SLUB debugging support                      # 禁用SLUB调试
    [ ] Memory hotplug support                             # 禁用内存热插拔
```

### 驱动裁剪

```
Device Drivers  --->
    [ ] Multiple devices driver support (RAID and LVM)      # 禁用RAID
    [ ] IEEE 1394 (FireWire) support                       # 禁用FireWire
    [ ] I2C support  --->                                  # 按需启用
    [ ] SPI support  --->                                  # 按需启用
    [ ] GPIO Support  --->                                 # 按需启用
```

### 网络功能裁剪

```
Networking support  --->
    Networking options  --->
        [ ] Transformation user configuration interface     # 禁用IPsec
        [ ] TCP/IP networking                              # 按需启用
        [ ] The IPv6 protocol                              # 按需禁用IPv6
```

### 文件系统裁剪

```
File systems  --->
    [ ] Second extended fs support                         # ext2按需
    [*] The Extended 3 (ext3) filesystem support           # ext3
    [ ] The Extended 4 (ext4) filesystem support           # ext4按需
    [*] FUSE (Filesystem in Userspace) support            # FUSE支持
    [*] Pseudo filesystems  --->
        [*]   /proc file system support
        [*]   sysfs file system support
        [*]   Tmpfs virtual memory file system support
```

### 调试选项裁剪

```
Kernel hacking  --->
    [ ] Kernel debugging                                   # 禁用内核调试
    [ ] Magic SysRq keys                                   # 禁用SysRq
    [ ] Debug slab memory allocations                      # 禁用slab调试
```

## 驱动精简策略

### 按需选择驱动

```bash
# 只选择需要的驱动
Device Drivers  --->
    Character devices  --->
        [*] Serial drivers  --->
            [*] 8250/16550 serial support
    Block devices  --->
        [*] Loopback device support                        # 按需
    Network device support  --->
        [*] Ethernet driver support                        # 只选择需要网卡
```

### 移除不需要的驱动

```bash
# 移除不支持的硬件驱动
Device Drivers  --->
    [ ] Sound card support                                 # 无音频硬件
    [ ] USB support                                        # 无USB接口
    [ ] Bluetooth support                                  # 无蓝牙
    [ ] Multimedia support                                 # 无多媒体
```

## 内核编译

### 交叉编译设置

```bash
# 设置交叉编译工具链
export ARCH=arm
export CROSS_COMPILE=arm-linux-gnueabihf-

# 或使用make变量
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
```

### 编译流程

```bash
# 清理
make distclean

# 配置
make xxx_defconfig

# 编译内核
make zImage -j$(nproc)

# 编译设备树
make dtbs

# 编译模块（如果启用）
make modules -j$(nproc)
make modules_install INSTALL_MOD_PATH=/path/to/rootfs
```

### 输出文件

```bash
# 内核镜像
arch/arm/boot/zImage                      # 压缩内核
arch/arm/boot/uImage                      # U-Boot格式

# 设备树
arch/arm/boot/dts/*.dtb                   # 编译后的设备树

# 模块
/lib/modules/$(uname -r)/                 # 内核模块
```

## 内核大小优化

### 使用压缩

```bash
General setup  --->
    [*] Initial RAM filesystem and RAM disk (initramfs/initrd) support
    (gzip) Built-in initramfs compression mode
        ( ) gzip
        ( ) bzip2
        (X) LZMA                          # LZMA压缩率更高
        ( ) XZ
        ( ) lzo
        ( ) lz4
```

### 优化内核镜像

```bash
# 使用更小的内核格式
make xipImage                             # XIP内核（片上执行）

# 禁用符号表
Kernel hacking  --->
    [ ] Include debugging information in kernel binary

# 使用strip
arm-linux-gnueabihf-strip arch/arm/boot/zImage
```

## 设备树配置

### 设备树文件结构

```dts
/dts-v1/;
/plugin/;

/ {
    compatible = "vendor,board";
    model = "My Board";
    
    memory@40000000 {
        device_type = "memory";
        reg = <0x40000000 0x20000000>;    /* 512MB内存 */
    };
    
    chosen {
        bootargs = "console=ttyS0,115200 root=/dev/mmcblk0p2";
    };
};
```

### 编译设备树

```bash
# 编译dts为dtb
dtc -I dts -O dtb -o board.dtb board.dts

# 反编译dtb为dts
dtc -I dtb -O dts -o board.dts board.dtb
```

## 启动优化

### 减少启动时间

```
General setup  --->
    (0) Default boot command line arguments
    [ ] Support for hot-pluggable devices
    [ ] Mark the kernel read-only in rodata section

Power management options  --->
    [ ] Suspend to RAM and standby                          # 禁用休眠
    [ ] Hibernation (aka 'suspend to disk')
```

### 控制台优化

```
Device Drivers  --->
    Character devices  --->
        Serial drivers  --->
            [*] Console on 8250/16550 serial port
            (115200) Default Baud Rate
```

## 内核配置保存与恢复

### 保存配置

```bash
# 保存当前配置
make savedefconfig
cp defconfig arch/arm/configs/myboard_defconfig

# 或直接复制
cp .config arch/arm/configs/myboard_defconfig
```

### 恢复配置

```bash
# 从保存的配置恢复
make myboard_defconfig
```

## 调试与验证

### 检查内核大小

```bash
# 查看内核大小
ls -lh arch/arm/boot/zImage

# 查看内核符号大小
nm --size-sort vmlinux | tail -20

# 查看内核段大小
arm-linux-gnueabihf-size vmlinux
```

### 检查模块依赖

```bash
# 查看模块信息
modinfo xxx.ko

# 检查模块依赖
depmod -a
```

## 常见问题解决

### 编译错误处理

```bash
# 配置错误
make oldconfig                           # 更新配置
make menuconfig                          # 手动配置

# 依赖问题
make clean && make mrproper              # 清理
```

### 驱动加载问题

```bash
# 查看内核消息
dmesg | grep -i error

# 查看模块加载情况
lsmod
cat /proc/modules
```

## 参考资料

- [Linux内核文档](https://www.kernel.org/doc/)
- [Linux内核配置指南](https://www.kernel.org/doc/html/latest/kbuild/index.html)
- [嵌入式Linux开发](https://elinux.org/)
