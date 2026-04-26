# Yocto项目

## 概述

Yocto项目是一个开源协作项目，提供模板、工具和方法帮助开发者创建基于Linux的定制嵌入式系统，无论硬件架构如何。

## Yocto特点

1. **高度灵活**：完全定制每个组件
2. **分层架构**：通过Layer扩展功能
3. **BitBake构建**：类似Make的构建系统
4. **OpenEmbedded核心**：丰富的配方库
5. **工具链支持**：生成交叉编译SDK

## Yocto核心组件

| 组件 | 说明 |
|------|------|
| BitBake | 构建引擎 |
| OpenEmbedded-Core | 核心配方集 |
| Meta-* Layers | 功能扩展层 |
| Poky | 参考发行版 |
| Hob/Guibitbake | 图形界面 |

## 安装Yocto

### 系统依赖

```bash
# Ubuntu/Debian
sudo apt install gawk wget git diffstat unzip texinfo gcc \
    build-essential chrpath socat cpio python3 python3-pip \
    python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev \
    pylint3 xterm

# Fedora/CentOS
sudo dnf install gawk wget git diffstat unzip texinfo gcc \
    patch gcc-c++ chrpath socat cpio python3 python3-pip \
    python3-git python3-jinja2 SDL-devel xterm
```

### 获取Poky

```bash
# 克隆Poky仓库
git clone git://git.yoctoproject.org/poky
cd poky

# 切换到稳定版本
git checkout kirkstone
```

## 快速开始

### 初始化构建环境

```bash
# 初始化环境并创建构建目录
source oe-init-build-env build

# 这会自动设置环境变量并进入build目录
```

### 配置目标机器

编辑 `conf/local.conf`:

```bash
# 设置目标机器
MACHINE = "qemux86-64"
# 或
MACHINE = "raspberrypi3"
MACHINE = "beaglebone-yocto"

# 下载目录
DL_DIR = "/opt/yocto/downloads"

# 构建状态目录
SSTATE_DIR = "/opt/yocto/sstate-cache"

# 接受所有许可证
ACCEPT_FSL_EULA = "1"
```

### 构建镜像

```bash
# 构建最小镜像
bitbake core-image-minimal

# 构建基础镜像
bitbake core-image-base

# 构建完整镜像
bitbake core-image-sato

# 构建SDK镜像
bitbake core-image-minimal -c populate_sdk
```

### 运行QEMU

```bash
# 运行模拟器
runqemu qemux86-64 core-image-minimal

# 运行并启用图形
runqemu qemux86-64 core-image-sato
```

## Layer（层）管理

### Layer概念

Yocto通过Layer组织配方：

```
meta/                    # 核心层
meta-poky/              # Poky配置层
meta-yocto-bsp/         # Yocto BSP层
meta-openembedded/      # 附加包层
meta-raspberrypi/       # 树莓派层
meta-intel/             # Intel层
```

### 添加Layer

```bash
# 克隆Layer
git clone git://git.openembedded.org/meta-openembedded
git clone git://git.yoctoproject.org/meta-raspberrypi

# 添加到构建配置
bitbake-layers add-layer ../meta-openembedded/meta-oe
bitbake-layers add-layer ../meta-raspberrypi

# 或编辑 conf/bblayers.conf
```

### 查看Layer

```bash
# 列出所有Layer
bitbake-layers show-layers

# 显示Layer优先级
bitbake-layers show-layers
```

## 配方（Recipe）编写

### 基本配方结构

```
meta-myproject/recipes-example/myapp/
├── myapp_1.0.0.bb
└── files/
    └── myapp.service
```

### 简单配方示例

```bitbake
# myapp_1.0.0.bb
SUMMARY = "My custom application"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=xxxx"

SRC_URI = "git://github.com/user/myapp.git;protocol=https;branch=main"
SRCREV = "${AUTOREV}"

S = "${WORKDIR}/git"

do_compile() {
    oe_runmake
}

do_install() {
    install -d ${D}${bindir}
    install -m 0755 myapp ${D}${bindir}/myapp
}
```

### 使用autotools

```bitbake
SUMMARY = "My autotools application"
LICENSE = "GPL-2.0"
LIC_FILES_CHKSUM = "file://COPYING;md5=xxxx"

SRC_URI = "https://example.com/${BPN}-${PV}.tar.gz"
SRC_URI[sha256sum] = "xxxx"

inherit autotools

PACKAGECONFIG[foo] = "--enable-foo,--disable-foo,libfoo"
```

### 使用cmake

```bitbake
SUMMARY = "My cmake application"
LICENSE = "MIT"

SRC_URI = "git://github.com/user/myapp.git;protocol=https"

inherit cmake

EXTRA_OECMAKE = "-DENABLE_DEBUG=ON"
```

### 添加依赖

```bitbake
DEPENDS = "libfoo libbar"
RDEPENDS:${PN} = "libfoo libbar"

# 运行时推荐依赖
RRECOMMENDS:${PN} = "kernel-module-mymodule"
```

## 变量说明

### 常用变量

```bitbake
# 路径变量
${WORKDIR}      # 工作目录
${S}            # 源码目录
${D}            # 目标安装目录
${bindir}       # /usr/bin
${libdir}       # /usr/lib
${datadir}      # /usr/share
${sysconfdir}   # /etc

# 包变量
${PN}           # 包名
${PV}           # 包版本
${PR}           # 包修订
${BP}           # ${PN}-${PV}

# 目标变量
${TARGET_ARCH}  # 目标架构
${TARGET_OS}    # 目标OS
${MACHINE}      # 目标机器
```

## 镜像定制

### 镜像配方

```bitbake
# my-image.bb
SUMMARY = "My custom image"

inherit core-image

IMAGE_INSTALL = "packagegroup-core-boot \
                 ${ROOTFS_PKGMANAGE_BOOTSTRAP} \
                 myapp \
                 openssh \
                 "

IMAGE_FEATURES += "ssh-server-openssh"

# 添加调试工具
IMAGE_FEATURES += "tools-debug"

# 添加开发工具
IMAGE_FEATURES += "tools-sdk"
```

### 镜像特征

```bitbake
# 可用特征
IMAGE_FEATURES += "ssh-server-openssh"
IMAGE_FEATURES += "ssh-server-dropbear"
IMAGE_FEATURES += "package-management"
IMAGE_FEATURES += "debug-tweaks"
IMAGE_FEATURES += "tools-debug"
IMAGE_FEATURES += "tools-sdk"
IMAGE_FEATURES += "x11-base"
IMAGE_FEATURES += "x11-sato"
```

## 设备树和内核

### 配置内核

```bitbake
# conf/local.conf
PREFERRED_PROVIDER_virtual/kernel = "linux-yocto"
PREFERRED_VERSION_linux-yocto = "5.15%"

# 使用自定义内核配置
KERNEL_CONFIG = "my-custom.config"
```

### 修改设备树

```bitbake
# my-machine.conf
KERNEL_DEVICETREE = "my-board.dtb"

# 添加设备树覆盖
KERNEL_DEVICETREE:append = " my-overlay.dtbo"
```

## SDK生成

### 构建SDK

```bash
# 构建标准SDK
bitbake core-image-minimal -c populate_sdk

# 构建可扩展SDK
bitbake core-image-minimal -c populate_sdk_ext
```

### 安装和使用SDK

```bash
# 安装SDK
./tmp/deploy/sdk/poky-glibc-x86_64-core-image-minimal-qemux86-64.sh

# 设置环境
source /opt/poky/3.1/environment-setup-x86_64-poky-linux

# 使用SDK编译应用
$CC myapp.c -o myapp
```

## 调试技巧

### 查看任务

```bash
# 列出包的所有任务
bitbake -c listtasks myapp

# 执行特定任务
bitbake -c clean myapp
bitbake -c compile myapp
bitbake -c install myapp
```

### 调试配方

```bash
# 进入devshell
bitbake -c devshell myapp

# 显示变量值
bitbake -e myapp | grep ^SRC_URI

# 显示依赖
bitbake -g myapp
```

### 查看日志

```bash
# 构建日志位于
tmp/work/<arch>/<package>/<version>/temp/

# 主要日志
log.do_compile
log.do_install
log.do_package
```

## 常见问题

### 下载问题

```bash
# 设置镜像
PREMIRRORS:prepend = "\
    git://.*/.* http://my.mirror.com/ \n \
    ftp://.*/.* http://my.mirror.com/ \n \
"
```

### 许可问题

```bash
# 允许商业许可证
LICENSE_FLAGS_ACCEPTED = "commercial"
```

### 空间问题

```bash
# 设置下载缓存到共享位置
DL_DIR = "/opt/yocto/downloads"
SSTATE_DIR = "/opt/yocto/sstate-cache"
```

## 参考资料

- [Yocto官网](https://www.yoctoproject.org/)
- [Yocto文档](https://docs.yoctoproject.org/)
- [BitBake用户手册](https://docs.yoctoproject.org/bitbake/2.0/bitbake-user-manual.html)
- [开发手册](https://docs.yoctoproject.org/dev-manual/index.html)
