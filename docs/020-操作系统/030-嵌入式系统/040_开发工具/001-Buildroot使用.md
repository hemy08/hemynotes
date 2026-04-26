# Buildroot使用

## 概述

Buildroot是一个用于自动化构建嵌入式Linux系统的工具，可以生成交叉编译工具链、根文件系统、内核镜像和引导加载程序。

## Buildroot特点

1. **自动化构建**：一键生成完整嵌入式系统
2. **高度可配置**：通过menuconfig灵活配置
3. **可重现性**：相同配置产生相同结果
4. **支持广泛**：大量官方包和开发板支持
5. **简单易用**：学习曲线相对平缓

## 安装Buildroot

### 获取源码

```bash
# 下载稳定版本
wget https://buildroot.org/downloads/buildroot-2023.11.tar.gz
tar xvf buildroot-2023.11.tar.gz
cd buildroot-2023.11

# 或使用Git
git clone https://git.buildroot.net/buildroot
cd buildroot
git checkout 2023.11
```

### 系统依赖

```bash
# Ubuntu/Debian
sudo apt install build-essential libncurses-dev \
    bison flex texinfo gzip patch rsync wget cpio unzip \
    bc git python3 python3-pip rsync

# Fedora/CentOS
sudo dnf install gcc gcc-c++ make ncurses-devel \
    bison flex texinfo gzip patch rsync wget cpio unzip \
    bc git python3 rsync
```

## 配置Buildroot

### 使用默认配置

```bash
# 列出支持的配置
make list-defconfigs

# 使用树莓派配置
make raspberrypi3_defconfig

# 使用STM32配置
make stm32f429_disco_defconfig

# 使用自定义配置
make myboard_defconfig
```

### 图形化配置

```bash
# 文本界面配置
make menuconfig

# Qt图形界面配置
make xconfig

# GTK图形界面配置
make gconfig
```

## 主要配置选项

### 目标架构配置

```
Target options  --->
    Target Architecture (ARM (little endian))
    Target Architecture Variant (cortex-A7)
    Target ABI (EABIhf)
    Floating point strategy (Hard float)
```

### 工具链配置

```
Toolchain  --->
    Toolchain type (External toolchain)
        [*] Use an external toolchain
        Toolchain (Custom toolchain)
        Toolchain path (/opt/toolchain/arm-linux-gnueabihf)
    
    或使用内部工具链：
    
    Toolchain type (Buildroot toolchain)
    (*) GCC compiler version (gcc 12.x)
    (*) C library (glibc)
    [*] Enable C++ support
    [*] Enable compiler cache support (ccache)
```

### 系统配置

```
System configuration  --->
    Root filesystem skeleton (default target skeleton)
    System hostname (buildroot)
    System banner (Welcome to Buildroot)
    Init system (BusyBox)
    /dev management (Dynamic using devtmpfs + mdev)
    Root login password (void)
    [*] Run a getty (login prompt) after boot
```

### 内核配置

```
Kernel  --->
    [*] Linux Kernel
    Kernel version (Custom Git repository)
    URL of custom Git repository (https://github.com/raspberrypi/linux.git)
    Custom Git repository version (rpi-5.10.y)
    Kernel configuration (Using a custom (def)config file)
    Path to the custom (def)config file (configs/rpi3_defconfig)
    [*] Build a Device Tree Blob (DTB)
```

### 文件系统镜像

```
Filesystem images  --->
    [*] ext2/3/4 root filesystem
        ext2/3/4 variant (ext4)
        exact size in MB (256)
    [*] cpio the root filesystem
        Compression method (gzip)
    [*] tar the root filesystem
        Compression method (gzip)
```

### 包选择

```
Target packages  --->
    Audio and video applications  --->
    Compressors and archivers  --->
    Development tools  --->
    Filesystem and flash utilities  --->
    Fonts, cursors, icons, sounds and themes  --->
    Graphic libraries and applications  --->
    Hardware handling  --->
    Interpreter languages and scripting  --->
    Libraries  --->
    Linux kernel utilities  --->
    Networking applications  --->
    Package managers  --->
    Real-Time  --->
    Security  --->
    Shell and utilities  --->
    System tools  --->
    Text editors and viewers  --->
```

## 构建系统

### 完整构建

```bash
# 构建所有组件
make

# 多核并行构建
make -j$(nproc)

# 仅构建某个组件
make toolchain    # 构建工具链
make linux        # 构建内核
make rootfs       # 构建根文件系统
```

### 单独重新构建

```bash
# 重新构建包
make <package>-rebuild

# 重新构建内核
make linux-rebuild

# 重新构建U-Boot
make uboot-rebuild

# 重新生成根文件系统
make target-finalize
```

### 清理构建

```bash
# 清理所有构建输出
make clean

# 完全清理（包括配置）
make distclean
```

## 输出目录结构

```
output/
├── build/          构建目录（各组件源码编译）
├── host/           主机工具（交叉编译器等）
├── images/         最终镜像文件
│   ├── rootfs.ext4
│   ├── rootfs.tar
│   ├── zImage
│   └── bcm2710-rpi-3-b.dtb
├── staging/        目标文件暂存
└── target/         目标根文件系统
```

## 自定义包

### 创建包目录

```bash
package/myapp/
├── Config.in       配置选项
├── myapp.hash      源码校验
├── myapp.mk        构建规则
└── myapp/          补丁文件
```

### Config.in

```bash
config BR2_PACKAGE_MYAPP
    bool "myapp"
    depends on BR2_PACKAGE_LIBFOO
    select BR2_PACKAGE_LIBBAR
    help
      This is my custom application.
      
      https://github.com/user/myapp
```

### myapp.mk

```makefile
MYAPP_VERSION = 1.0.0
MYAPP_SITE = https://github.com/user/myapp/releases/download/$(MYAPP_VERSION)
MYAPP_SOURCE = myapp-$(MYAPP_VERSION).tar.gz
MYAPP_LICENSE = MIT
MYAPP_LICENSE_FILES = LICENSE
MYAPP_DEPENDENCIES = libfoo libbar

define MYAPP_BUILD_CMDS
    $(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(@D)
endef

define MYAPP_INSTALL_TARGET_CMDS
    $(INSTALL) -D -m 0755 $(@D)/myapp $(TARGET_DIR)/usr/bin/myapp
endef

$(eval $(generic-package))
```

### 注册包

在 `package/Config.in` 中添加：

```bash
source "package/myapp/Config.in"
```

## 外部树（Out-of-tree）

### 创建外部树

```bash
my-board/
├── Config.in
├── external.mk
├── board/
│   └── mycompany/
│       └── myboard/
│           ├── linux.config
│           ├── uboot.config
│           ├── post-image.sh
│           └── rootfs-overlay/
└── configs/
    └── myboard_defconfig
```

### 使用外部树

```bash
make BR2_EXTERNAL=/path/to/my-board menuconfig
```

## 开发板定义

### 创建开发板配置

```bash
# configs/myboard_defconfig
BR2_arm=y
BR2_cortex_a7=y
BR2_TOOLCHAIN_EXTERNAL=y
BR2_LINUX_KERNEL=y
BR2_LINUX_KERNEL_CUSTOM_GIT=y
BR2_LINUX_KERNEL_CUSTOM_REPO_URL="https://github.com/mycompany/linux.git"
```

### Rootfs覆盖

```
board/mycompany/myboard/rootfs-overlay/
├── etc/
│   ├── init.d/
│   │   └── rcS
│   └── network/
│       └── interfaces
└── usr/
    └── local/
        └── bin/
            └── myapp
```

### 构建后脚本

```bash
# board/mycompany/myboard/post-image.sh
#!/bin/sh

# 创建SD卡镜像
BOARD_DIR=$(dirname $0)
GENIMAGE_CFG="${BOARD_DIR}/genimage.cfg"

genimage \
    --rootpath "${TARGET_DIR}" \
    --tmppath "${BINARIES_DIR}/tmp" \
    --inputpath "${BINARIES_DIR}" \
    --outputpath "${BINARIES_DIR}" \
    --config "${GENIMAGE_CFG}"
```

## 调试技巧

### 查看配置状态

```bash
# 显示当前配置
make show-config

# 显示包信息
make show-info

# 查看变量值
make print-VAR=BR2_PACKAGE_BUSYBOX
```

### 下载问题

```bash
# 设置下载镜像
BR2_PRIMARY_SITE = "https://my.mirror.com/"

# 或使用环境变量
export BR2_PRIMARY_SITE="https://my.mirror.com/"
```

### 构建问题

```bash
# 查看详细输出
make V=1

# 查看失败包
make <package>-show-depends

# 手动进入构建目录
make <package>-dirclean
make <package>-configure
```

## 常用场景

### 构建最小系统

```
# 精简配置
Target packages  --->
    [ ] BusyBox
    [ ] Dropbear SSH server
    
Kernel  --->
    [ ] Linux Kernel

Filesystem images  --->
    [*] cpio the root filesystem
```

### 添加Qt应用

```
Target packages  --->
    Graphic libraries and applications  --->
        [*] Qt5
        [*]   GUI module
        [*]   Widgets module
        Qt5 libraries available  --->
            [*]   Qt5 Charts
            [*]   Qt5 Multimedia
```

### 添加Python支持

```
Target packages  --->
    Interpreter languages and scripting  --->
        [*] python3
        External python modules  --->
            [*]   python-requests
            [*]   python-flask
```

## 参考资料

- [Buildroot官网](https://buildroot.org/)
- [Buildroot手册](https://buildroot.org/downloads/manual/manual.html)
- [Buildroot培训](https://bootlin.com/doc/training/buildroot/)
