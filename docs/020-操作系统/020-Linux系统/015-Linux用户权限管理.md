# Linux用户权限管理

## 概述

Linux采用多用户、多组权限模型，通过用户、组、权限位实现文件和系统资源的访问控制。

## 用户管理

### 用户操作

```bash
# 添加用户
useradd username
useradd -m username          # 创建主目录
useradd -m -s /bin/bash username  # 指定shell
useradd -m -d /home/custom username  # 指定主目录

# 设置密码
passwd username

# 删除用户
userdel username
userdel -r username          # 同时删除主目录

# 修改用户
usermod -l newname oldname   # 修改用户名
usermod -d /home/new username    # 修改主目录
usermod -s /bin/zsh username # 修改shell
usermod -L username          # 锁定用户
usermod -U username          # 解锁用户
usermod -e 2024-12-31 username   # 设置过期日期
usermod -aG sudo username    # 添加到sudo组

# 查看用户
id username
w              # 当前登录用户
who            # 当前登录用户
whoami         # 当前用户名
```

### 用户配置文件

```bash
# /etc/passwd格式
username:x:uid:gid:comment:home:shell

# 示例
root:x:0:0:root:/root:/bin/bash
nginx:x:1000:1000::/home/nginx:/bin/false

# /etc/shadow格式
username:encrypted_password:lastchg:min:max:warn:inactive:expire:flag
```

## 组管理

### 组操作

```bash
# 创建组
groupadd groupname
groupadd -g 1001 groupname   # 指定GID

# 删除组
groupdel groupname

# 修改组
groupmod -n newname oldname  # 修改组名
groupmod -g 1002 groupname   # 修改GID

# 添加用户到组
gpasswd -a username groupname
usermod -aG groupname username

# 从组中删除用户
gpasswd -d username groupname

# 设置组管理员
gpasswd -A admin groupname

# 查看组
groups username    # 用户所属组
cat /etc/group
```

### 组配置文件

```bash
# /etc/group格式
groupname:x:gid:members

# 示例
sudo:x:27:username1,username2
docker:x:999:username
```

## 文件权限

### 权限说明

```
-rwxrwxrwx
│└──┴──┴── 权限
│   │  │  └─ 其他用户权限
│   │  └──── 组用户权限
│   └───────── 所有者权限
└──────────── 文件类型（-普通文件，d目录，l链接）
```

### 权限修改

```bash
# 字母方式
chmod u+x file          # 所有者添加执行权限
chmod g-w file          # 组用户移除写权限
chmod o=r file          # 其他用户只读
chmod a+x file          # 所有人添加执行权限
chmod u=rwx,g=rx,o=r file  # 同时设置

# 数字方式
chmod 755 file          # rwxr-xr-x
chmod 644 file          # rw-r--r--
chmod 600 file          # rw-------
chmod 777 file          # rwxrwxrwx（不推荐）

# 递归修改
chmod -R 755 directory
```

### 数字权限计算

| 权限 | 数值 |
|------|------|
| r | 4 |
| w | 2 |
| x | 1 |
| - | 0 |

```
rwx = 4+2+1 = 7
r-x = 4+0+1 = 5
rw- = 4+2+0 = 6
r-- = 4+0+0 = 4
```

### 特殊权限

```bash
# SUID（执行时获取所有者权限）
chmod u+s file    # 4xxx
chmod 4755 file

# SGID（执行时获取组权限，目录中新建文件继承组）
chmod g+s file    # 2xxx
chmod 2755 file

# Sticky Bit（目录中只能删除自己的文件）
chmod +t directory    # 1xxx
chmod 1777 directory

# 示例：/tmp目录
ls -ld /tmp    # drwxrwxrwt
```

## 文件所有权

```bash
# 修改所有者
chown user file
chown user:group file
chown :group file         # 只修改组

# 递归修改
chown -R user:group directory

# 修改组
chgrp group file
chgrp -R group directory
```

## ACL访问控制列表

### 启用ACL

```bash
# 挂载时启用
mount -o acl /dev/sda1 /mnt

# 或在/etc/fstab中
/dev/sda1  /mnt  ext4  defaults,acl  0  1
```

### ACL操作

```bash
# 查看ACL
getfacl file

# 设置ACL
setfacl -m u:username:rwx file    # 用户权限
setfacl -m g:groupname:rx file    # 组权限
setfacl -m o::r file              # 其他用户权限

# 删除ACL
setfacl -x u:username file        # 删除用户ACL
setfacl -b file                   # 删除所有ACL

# 默认ACL（目录）
setfacl -d -m u:username:rwx directory

# 递归设置
setfacl -R -m u:username:rwx directory
```

## sudo配置

### visudo编辑

```bash
# 编辑sudo配置
visudo

# 基本配置
username ALL=(ALL) ALL           # 用户sudo权限
%wheel ALL=(ALL) ALL             # 组sudo权限

# 免密码sudo
username ALL=(ALL) NOPASSWD: ALL

# 限制命令
username ALL=(ALL) /usr/bin/apt, /usr/bin/systemctl

# 限制特定主机
username server1=(ALL) ALL

# 允许以其他用户执行
username ALL=(postgres) /usr/bin/psql
```

### sudo使用

```bash
# 执行命令
sudo command

# 以指定用户执行
sudo -u username command

# 保存环境变量
sudo -E command

# 进入root shell
sudo -i
sudo su -

# 查看权限
sudo -l
```

## umask

### umask设置

```bash
# 查看umask
umask

# 设置umask
umask 022     # 创建文件：644，创建目录：755
umask 077     # 创建文件：600，创建目录：700

# 永久设置（~/.bashrc）
umask 022
```

### umask计算

```
文件默认权限：666 - umask
目录默认权限：777 - umask

umask 022:
文件：666 - 022 = 644 (rw-r--r--)
目录：777 - 022 = 755 (rwxr-xr-x)
```

## 参考资料

- [Linux权限管理](https://man7.org/linux/man-pages/man2/chmod.2.html)
- [sudo手册](https://www.sudo.ws/docs/man/)
