# Linux软件包管理

## 概述

Linux软件包管理系统用于安装、更新、卸载软件，不同发行版使用不同的包管理器。

## 包管理器对比

| 发行版 | 包管理器 | 格式 |
|--------|----------|------|
| Debian/Ubuntu | apt, dpkg | .deb |
| RHEL/CentOS/Fedora | yum, dnf, rpm | .rpm |
| SUSE/openSUSE | zypper, rpm | .rpm |
| Arch Linux | pacman | .pkg.tar.xz |
| Alpine | apk | .apk |

## APT（Debian/Ubuntu）

### 基本操作

```bash
# 更新软件源
apt update

# 升级所有软件
apt upgrade
apt full-upgrade    # 包含依赖关系处理

# 安装软件
apt install nginx
apt install nginx=1.18.0-0ubuntu1    # 指定版本

# 卸载软件
apt remove nginx
apt purge nginx        # 同时删除配置文件
apt autoremove         # 清理不需要的依赖

# 搜索软件
apt search nginx
apt show nginx         # 查看软件信息

# 查看已安装软件
apt list --installed
dpkg -l

# 查看文件属于哪个包
dpkg -S /usr/bin/nginx
apt-file search /usr/bin/nginx
```

### 软件源配置

```bash
# /etc/apt/sources.list
deb http://archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ focal-updates main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu/ focal-security main restricted universe multiverse

# 添加PPA
add-apt-repository ppa:nginx/stable
apt update
apt install nginx

# 删除PPA
add-apt-repository --remove ppa:nginx/stable
```

### 修复依赖

```bash
# 修复依赖
apt --fix-broken install
dpkg --configure -a

# 清理缓存
apt clean
apt autoclean
```

## YUM/DNF（RHEL/CentOS/Fedora）

### 基本操作

```bash
# 更新软件源
yum makecache

# 查看软件源
yum repolist

# 安装软件
yum install nginx
yum install nginx-1.18.0    # 指定版本

# 升级软件
yum update
yum update nginx

# 卸载软件
yum remove nginx

# 搜索软件
yum search nginx
yum info nginx

# 查看已安装软件
yum list installed
rpm -qa

# 查看文件属于哪个包
rpm -qf /usr/sbin/nginx
yum whatprovides /usr/sbin/nginx

# 软件组安装
yum groupinstall "Development Tools"
yum grouplist
```

### 软件源配置

```bash
# /etc/yum.repos.d/nginx.repo
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/centos/7/$basearch/
gpgcheck=0
enabled=1

# 添加EPEL源
yum install epel-release
```

## Zypper（openSUSE）

### 基本操作

```bash
# 更新软件源
zypper refresh

# 安装软件
zypper install nginx

# 升级软件
zypper update

# 卸载软件
zypper remove nginx

# 搜索软件
zypper search nginx
zypper info nginx

# 添加软件源
zypper addrepo http://download.opensuse.org/repositories/network/openSUSE_Leap_15.2/ network

# 删除软件源
zypper removerepo network
```

## Pacman（Arch Linux）

### 基本操作

```bash
# 更新系统
pacman -Syu

# 安装软件
pacman -S nginx

# 卸载软件
pacman -R nginx
pacman -Rs nginx    # 同时删除依赖
pacman -Rns nginx   # 删除依赖和配置

# 搜索软件
pacman -Ss nginx
pacman -Qi nginx    # 查看已安装软件信息

# 查看已安装软件
pacman -Q

# 清理缓存
pacman -Sc    # 清理旧版本
pacman -Scc   # 清理全部
```

## APK（Alpine）

### 基本操作

```bash
# 更新软件源
apk update

# 安装软件
apk add nginx

# 升级软件
apk upgrade

# 卸载软件
apk del nginx

# 搜索软件
apk search nginx
apk info nginx
```

## 源码编译安装

### 基本流程

```bash
# 下载源码
wget https://example.com/package-1.0.tar.gz
tar xzf package-1.0.tar.gz
cd package-1.0

# 配置
./configure --prefix=/usr/local

# 编译
make -j$(nproc)

# 安装
make install

# 卸载
make uninstall    # 需要源码目录
```

## Snap包

```bash
# 安装snapd
apt install snapd

# 安装软件
snap install nginx
snap install vlc --channel=stable

# 查看已安装
snap list

# 升级
snap refresh nginx

# 卸载
snap remove nginx

# 查看服务
snap services
```

## Flatpak包

```bash
# 安装flatpak
apt install flatpak

# 添加仓库
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# 安装软件
flatpak install flathub org.videolan.VLC

# 查看已安装
flatpak list

# 运行
flatpak run org.videolan.VLC

# 卸载
flatpak uninstall org.videolan.VLC
```

## 参考资料

- [APT手册](https://manpages.debian.org/apt/)
- [DNF文档](https://dnf.readthedocs.io/)
- [Pacman手册](https://wiki.archlinux.org/title/Pacman)
