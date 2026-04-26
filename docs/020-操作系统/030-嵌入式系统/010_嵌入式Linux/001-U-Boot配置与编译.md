# U-Boot配置与编译

## 概述

U-Boot（Universal Boot Loader）是嵌入式系统中最常用的引导加载程序，支持多种处理器架构。

## U-Boot功能

1. **硬件初始化**：初始化CPU、内存、外设
2. **内核加载**：从存储设备加载Linux内核
3. **设备树加载**：加载设备树文件
4. **环境变量管理**：管理启动参数
5. **命令行接口**：提供交互式命令行

## 获取U-Boot源码

```bash
# 从官方仓库获取
git clone https://source.denx.de/u-boot/u-boot.git

# 或使用特定版本
git clone -b v2023.10 https://source.denx.de/u-boot/u-boot.git
```

## 配置U-Boot

### 查看支持的板子

```bash
make list-configs                    # 列出所有支持的配置
```

### 选择默认配置

```bash
# 以树莓派为例
make rpi_3_32b_defconfig             # 树莓派3 32位
make rpi_4_32b_defconfig             # 树莓派4 32位

# 以全志芯片为例
make sun8i_h3_defconfig              # 全志H3
make sun50i_h6_defconfig             # 全志H6

# 以NXP芯片为例
make mx6sabresd_defconfig            # i.MX6
make imx8mm_evk_defconfig            # i.MX8M Mini
```

### 图形化配置

```bash
make menuconfig                      # ncurses图形界面
make xconfig                         # Qt图形界面
make gconfig                         # GTK图形界面
```

## 编译U-Boot

### 基本编译

```bash
make                                 # 编译
make -j$(nproc)                      # 多核编译
```

### 交叉编译

```bash
# 设置交叉编译工具链
export CROSS_COMPILE=arm-linux-gnueabihf-
export ARCH=arm

make                                 # 编译
```

### 完整编译流程

```bash
# 清理
make distclean

# 配置
make xxx_defconfig

# 编译
make -j$(nproc)
```

## 常用配置项

### 串口配置

```bash
# 在menuconfig中
Device Drivers  --->
    Serial drivers  --->
        [*] Support for a generic UART
        (0) UART base address
        (115200) Default baud rate
```

### 内存配置

```bash
# 设置内存大小
CONFIG_SYS_SDRAM_BASE=0x40000000
CONFIG_SYS_SDRAM_SIZE=0x40000000    # 1GB
```

### 启动参数

```bash
# 设置默认启动参数
CONFIG_BOOTCOMMAND="run distro_bootcmd"
CONFIG_BOOTDELAY=3                   # 启动延时3秒
```

## U-Boot命令

### 信息查看命令

```bash
printenv                             # 打印环境变量
version                              # 查看版本信息
bdinfo                               # 查看板级信息
```

### 内存操作命令

```bash
md 0x40000000 10                     # 显示内存（10个字）
mw 0x40000000 0x12345678             # 写入内存
cp 0x40000000 0x50000000 100         # 复制内存
```

### 存储设备命令

```bash
mmc info                             # MMC信息
mmc list                             # 列出MMC设备
mmc dev 0                            # 选择MMC设备0
mmc read 0x42000000 0 100            # 读取MMC
fatls mmc 0:1                        # 列出FAT分区文件
fatload mmc 0:1 0x42000000 zImage    # 加载文件
```

### 网络命令

```bash
dhcp                                 # DHCP获取IP
tftp 0x42000000 zImage               # TFTP下载文件
ping 192.168.1.1                     # ping测试
```

### 启动命令

```bash
bootz 0x42000000                     # 启动zImage内核
bootm 0x42000000                     # 启动uImage内核
boot                                 # 执行默认启动命令
```

## 环境变量配置

### 设置环境变量

```bash
setenv bootcmd 'fatload mmc 0:1 0x42000000 zImage; bootz 0x42000000'
setenv bootargs 'console=ttyS0,115200 root=/dev/mmcblk0p2 rootwait'
saveenv                              # 保存环境变量
```

### 常用环境变量

| 变量 | 说明 |
|------|------|
| bootcmd | 自动启动命令 |
| bootargs | 内核启动参数 |
| bootdelay | 启动延时（秒） |
| baudrate | 串口波特率 |
| ipaddr | 开发板IP地址 |
| serverip | 服务器IP地址 |

## 烧写U-Boot

### 烧写到SD卡

```bash
# 查看SD卡设备
lsblk

# 烧写U-Boot
dd if=u-boot-sunxi-with-spl.bin of=/dev/sdX bs=1024 seek=8
```

### 烧写到eMMC

```bash
# 在U-Boot命令行中
mmc dev 1                            # 选择eMMC
tftp 0x42000000 u-boot.bin           # 下载U-Boot
mmc write 0x42000000 0 100           # 写入eMMC
```

## 调试U-Boot

### 启用调试输出

```bash
# 在menuconfig中
Boot options  --->
    [*] Enable boot arguments
    (earlycon=uart8250,mmio32,0x21c0500 console=ttyS0,115200) Default boot arguments
```

### 使用JTAG调试

```bash
# 连接JTAG调试器
openocd -f interface/jlink.cfg -f target/imx6.cfg
```

## 参考资料

- [U-Boot官方文档](https://u-boot.readthedocs.io/)
- [U-Boot源码](https://source.denx.de/u-boot/u-boot.git)
