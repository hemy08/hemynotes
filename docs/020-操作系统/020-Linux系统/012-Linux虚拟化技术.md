# Linux虚拟化技术

## 概述

Linux虚拟化技术允许在单个物理主机上运行多个虚拟机，提高硬件利用率，简化系统管理。

## 虚拟化类型

| 类型 | 说明 | 代表 |
|------|------|------|
| 全虚拟化 | 完全模拟硬件 | KVM、VMware、VirtualBox |
| 半虚拟化 | 修改客户系统 | Xen |
| 容器虚拟化 | 进程级隔离 | Docker、LXC |

## KVM虚拟化

### 安装KVM

```bash
# Ubuntu/Debian
apt install qemu-kvm libvirt-daemon-system libvirt-clients virt-manager

# CentOS/RHEL
yum install qemu-kvm libvirt virt-install virt-manager

# 启动libvirtd
systemctl start libvirtd
systemctl enable libvirtd

# 检查KVM支持
egrep -c '(vmx|svm)' /proc/cpuinfo    # 检查CPU虚拟化支持
kvm-ok                                # Ubuntu检查命令
```

### virsh命令

```bash
# 查看虚拟机
virsh list --all

# 启动虚拟机
virsh start vm1

# 关闭虚拟机
virsh shutdown vm1
virsh destroy vm1    # 强制关闭

# 重启虚拟机
virsh reboot vm1

# 暂停/恢复
virsh suspend vm1
virsh resume vm1

# 删除虚拟机
virsh undefine vm1

# 查看虚拟机信息
virsh dominfo vm1

# 查看虚拟机状态
virsh domstate vm1

# 控制台连接
virsh console vm1
```

### 创建虚拟机

```bash
# 使用virt-install创建
virt-install \
  --name vm1 \
  --ram 2048 \
  --vcpus 2 \
  --disk path=/var/lib/libvirt/images/vm1.qcow2,size=20 \
  --os-variant ubuntu20.04 \
  --network bridge=virbr0 \
  --graphics vnc,listen=0.0.0.0 \
  --cdrom /path/to/ubuntu.iso

# 使用现有磁盘
virt-install \
  --name vm2 \
  --ram 4096 \
  --vcpus 4 \
  --disk /var/lib/libvirt/images/vm2.qcow2 \
  --import
```

### 虚拟机克隆

```bash
# 克隆虚拟机
virt-clone --original vm1 --name vm1-clone --file /var/lib/libvirt/images/vm1-clone.qcow2
```

### 快照管理

```bash
# 创建快照
virsh snapshot-create-as vm1 snap1 "Before update"

# 查看快照
virsh snapshot-list vm1

# 恢复快照
virsh snapshot-revert vm1 snap1

# 删除快照
virsh snapshot-delete vm1 snap1

# 查看快照信息
virsh snapshot-info vm1 snap1
```

## QEMU命令行

### 直接使用QEMU

```bash
# 创建磁盘镜像
qemu-img create -f qcow2 disk.qcow2 20G
qemu-img create -f raw disk.raw 20G

# 启动虚拟机
qemu-system-x86_64 \
  -m 2048 \
  -smp 2 \
  -drive file=disk.qcow2,format=qcow2 \
  -cdrom ubuntu.iso \
  -boot d \
  -netdev user,id=net0 -device e1000,netdev=net0

# 启用KVM加速
qemu-system-x86_64 -enable-kvm -m 2048 disk.qcow2

# 查看镜像信息
qemu-img info disk.qcow2

# 转换镜像格式
qemu-img convert -f raw -O qcow2 disk.raw disk.qcow2
qemu-img convert -f qcow2 -O vmdk disk.qcow2 disk.vmdk
```

## 网络配置

### 网络模式

```bash
# NAT模式（默认）
virsh net-start default
virsh net-autostart default

# 查看网络
virsh net-list --all
virsh net-info default

# 创建桥接网络
# /etc/network/interfaces
auto br0
iface br0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
    bridge_ports eth0
    bridge_stp off
    bridge_fd 0
```

## 存储池管理

```bash
# 查看存储池
virsh pool-list --all

# 创建目录存储池
virsh pool-define-as --name local --type dir --target /var/lib/libvirt/images
virsh pool-build local
virsh pool-start local
virsh pool-autostart local

# 查看存储池信息
virsh pool-info local

# 查看存储卷
virsh vol-list local
```

## VirtualBox

### 命令行管理

```bash
# 查看虚拟机
VBoxManage list vms
VBoxManage list runningvms

# 启动虚拟机
VBoxManage startvm vm1 --type headless

# 关闭虚拟机
VBoxManage controlvm vm1 poweroff
VBoxManage controlvm vm1 acpipowerbutton

# 创建虚拟机
VBoxManage createvm --name vm1 --register
VBoxManage modifyvm vm1 --memory 2048 --cpus 2
VBoxManage createhd --filename vm1.vdi --size 20480

# 快照
VBoxManage snapshot vm1 take snap1
VBoxManage snapshot vm1 restore snap1
VBoxManage snapshot vm1 delete snap1
```

## Vagrant

### 基本使用

```ruby
# Vagrantfile
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.hostname = "myvm"
  config.vm.network "private_network", ip: "192.168.33.10"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = 2048
    vb.cpus = 2
  end
  config.vm.provision "shell", inline: <<-SHELL
    apt update
    apt install -y nginx
  SHELL
end
```

```bash
# 启动虚拟机
vagrant up

# 连接虚拟机
vagrant ssh

# 查看状态
vagrant status

# 停止虚拟机
vagrant halt

# 删除虚拟机
vagrant destroy

# 重新加载
vagrant reload

# 查看SSH配置
vagrant ssh-config
```

## 资源监控

### 查看虚拟机资源

```bash
# CPU使用
virsh vcpuinfo vm1

# 内存使用
virsh dommemstat vm1

# 磁盘I/O
virsh domblkstat vm1

# 网络I/O
virsh domifstat vm1 vnet0

# 综合监控
virt-top
```

## 迁移

### 在线迁移

```bash
# 迁移到另一台主机
virsh migrate --live vm1 qemu+ssh://dest-host/system

# 离线迁移
virsh migrate vm1 qemu+ssh://dest-host/system
```

## 参考资料

- [KVM文档](https://www.linux-kvm.org/)
- [libvirt文档](https://libvirt.org/)
- [QEMU文档](https://www.qemu.org/)
- [Vagrant文档](https://www.vagrantup.com/docs/)
