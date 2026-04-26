# Linux存储管理

## 概述

Linux存储管理包括磁盘分区、文件系统、LVM逻辑卷、RAID阵列、存储挂载等。

## 磁盘分区

### fdisk分区

```bash
# 查看磁盘
fdisk -l

# 分区操作
fdisk /dev/sdb

# fdisk交互命令:
# m: 帮助
# p: 查看分区表
# n: 新建分区
# d: 删除分区
# t: 修改分区类型
# w: 保存并退出
# q: 不保存退出
```

### gdisk分区（GPT）

```bash
# 查看磁盘
gdisk -l /dev/sdb

# GPT分区
gdisk /dev/sdb

# gdisk交互命令:
# m: 帮助
# p: 查看分区表
# n: 新建分区
# d: 删除分区
# t: 修改分区类型
# w: 保存并退出
# q: 不保存退出
```

### parted分区

```bash
# 查看分区
parted /dev/sdb print

# 创建GPT分区表
parted /dev/sdb mklabel gpt

# 创建MBR分区表
parted /dev/sdb mklabel msdos

# 创建分区
parted /dev/sdb mkpart primary ext4 1MiB 100GiB
parted /dev/sdb mkpart primary ext4 100GiB 200GiB

# 删除分区
parted /dev/sdb rm 1

# 调整分区大小
parted /dev/sdb resizepart 1 150GiB
```

## 文件系统

### 创建文件系统

```bash
# 创建ext4文件系统
mkfs.ext4 /dev/sdb1

# 创建xfs文件系统
mkfs.xfs /dev/sdb1

# 创建btrfs文件系统
mkfs.btrfs /dev/sdb1

# 创建ext4时指定标签
mkfs.ext4 -L "data" /dev/sdb1

# 创建ext4时指定预留空间
mkfs.ext4 -m 1 /dev/sdb1    # 1%预留

# 格式化swap分区
mkswap /dev/sdb2
swapon /dev/sdb2
swapoff /dev/sdb2
```

### 文件系统检查

```bash
# 检查ext4文件系统
e2fsck /dev/sdb1
e2fsck -f /dev/sdb1        # 强制检查

# 检查xfs文件系统
xfs_repair /dev/sdb1
```

### 文件系统调整

```bash
# 调整ext4大小
resize2fs /dev/sdb1

# 查看ext4信息
tune2fs -l /dev/sdb1

# 修改ext4标签
e2label /dev/sdb1 newlabel

# 修改ext4预留空间
tune2fs -m 1 /dev/sdb1
```

## LVM逻辑卷管理

### 物理卷（PV）

```bash
# 创建物理卷
pvcreate /dev/sdb1
pvcreate /dev/sdb2 /dev/sdc1

# 查看物理卷
pvdisplay
pvs

# 删除物理卷
pvremove /dev/sdb1
```

### 卷组（VG）

```bash
# 创建卷组
vgcreate vg01 /dev/sdb1 /dev/sdb2

# 查看卷组
vgdisplay
vgs

# 扩展卷组
vgextend vg01 /dev/sdc1

# 缩减卷组
vgreduce vg01 /dev/sdc1

# 删除卷组
vgremove vg01
```

### 逻辑卷（LV）

```bash
# 创建逻辑卷
lvcreate -L 50G -n lv01 vg01          # 指定大小
lvcreate -l 100%FREE -n lv02 vg01     # 使用所有空间

# 查看逻辑卷
lvdisplay
lvs

# 扩展逻辑卷
lvextend -L +10G /dev/vg01/lv01
lvextend -l +100%FREE /dev/vg01/lv01
resize2fs /dev/vg01/lv01              # 扩展文件系统

# 缩减逻辑卷
resize2fs /dev/vg01/lv01 40G          # 先缩减文件系统
lvreduce -L 40G /dev/vg01/lv01

# 删除逻辑卷
lvremove /dev/vg01/lv01
```

### LVM快照

```bash
# 创建快照
lvcreate -L 10G -s -n snap01 /dev/vg01/lv01

# 恢复快照
lvconvert --mergesnapshot /dev/vg01/snap01

# 删除快照
lvremove /dev/vg01/snap01
```

## RAID阵列

### 软RAID（mdadm）

```bash
# 安装
apt install mdadm

# 创建RAID0
mdadm --create /dev/md0 --level=0 --raid-devices=2 /dev/sdb1 /dev/sdc1

# 创建RAID1
mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1

# 创建RAID5
mdadm --create /dev/md0 --level=5 --raid-devices=3 /dev/sdb1 /dev/sdc1 /dev/sdd1

# 创建RAID10
mdadm --create /dev/md0 --level=10 --raid-devices=4 /dev/sdb1 /dev/sdc1 /dev/sdd1 /dev/sde1

# 查看RAID状态
cat /proc/mdstat
mdadm --detail /dev/md0

# 停止RAID
mdadm --stop /dev/md0

# 删除RAID
mdadm --zero-superblock /dev/sdb1

# 添加热备盘
mdadm --add /dev/md0 /dev/sdf1

# 移除故障盘
mdadm --remove /dev/md0 /dev/sdb1

# 标记故障盘
mdadm --fail /dev/md0 /dev/sdb1
```

## 挂载管理

### mount命令

```bash
# 挂载分区
mount /dev/sdb1 /mnt/data

# 挂载指定文件系统
mount -t ext4 /dev/sdb1 /mnt/data

# 挂载ISO
mount -o loop image.iso /mnt/iso

# 挂载NFS
mount -t nfs 192.168.1.1:/share /mnt/nfs

# 挂载CIFS/SMB
mount -t cifs //192.168.1.1/share /mnt/smb -o username=user,password=pass

# 重新挂载为读写
mount -o remount,rw /mnt/data

# 卸载
umount /mnt/data
umount -l /mnt/data    # 懒卸载
```

### /etc/fstab配置

```bash
# /etc/fstab格式
# 设备    挂载点    文件系统    选项    dump    fsck

/dev/sdb1    /mnt/data    ext4    defaults    0    2
/dev/vg01/lv01    /mnt/lvm    ext4    defaults    0    2
192.168.1.1:/share    /mnt/nfs    nfs    defaults    0    0

# 挂载选项说明
# defaults: rw,suid,dev,exec,auto,nouser,async
# noexec: 不允许执行
# nosuid: 不允许suid
# ro: 只读
# rw: 读写
# noauto: 不自动挂载
```

### 自动挂载

```bash
# 查看UUID
blkid

# 使用UUID挂载（推荐）
UUID=xxxx-xxxx    /mnt/data    ext4    defaults    0    2

# 使用标签挂载
LABEL=data    /mnt/data    ext4    defaults    0    2
```

## 磁盘配额

```bash
# 启用配额
mount -o usrquota,grpquota /dev/sdb1 /mnt/data

# 初始化配额
quotacheck -cug /mnt/data

# 启用配额
quotaon /mnt/data

# 设置用户配额
setquota -u username 10000 15000 100 150 /mnt/data

# 设置组配额
setquota -g groupname 50000 60000 500 600 /mnt/data

# 查看配额
repquota /mnt/data
quota -u username
```

## 参考资料

- [Linux存储管理](https://tldp.org/HOWTO/Storage-HOWTO/)
- [LVM管理指南](https://tldp.org/HOWTO/LVM-HOWTO/)
