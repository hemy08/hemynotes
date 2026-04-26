# find命令

## 概述

find命令是Linux下强大的文件查找工具，支持按名称、类型、大小、时间等多种条件搜索文件。

## 基本语法

```bash
find [路径] [选项] [操作]
```

## 常用选项

### 按名称查找

```bash
find /path -name "*.txt"           # 查找所有txt文件
find /path -iname "*.txt"          # 忽略大小写
find /path -name "file*"           # 查找以file开头的文件
```

### 按类型查找

```bash
find /path -type f                 # 普通文件
find /path -type d                 # 目录
find /path -type l                 # 符号链接
find /path -type b                 # 块设备
find /path -type c                 # 字符设备
find /path -type s                 # 套接字
find /path -type p                 # 管道
```

### 按大小查找

```bash
find /path -size 0                 # 空文件
find /path -size +100M             # 大于100MB
find /path -size -10k              # 小于10KB
find /path -size +1G               # 大于1GB
```

### 按时间查找

```bash
find /path -mtime -7               # 7天内修改过的文件
find /path -mtime +30              # 30天前修改过的文件
find /path -atime -1               # 1天内访问过的文件
find /path -ctime -1               # 1天内状态改变的文件
find /path -mmin -10               # 10分钟内修改过的文件
```

### 按权限查找

```bash
find /path -perm 755               # 权限为755的文件
find /path -perm -u=x              # 用户可执行
find /path -perm /u=s              # 设置了SUID
```

### 按用户/组查找

```bash
find /path -user root              # 属于root用户的文件
find /path -group users            # 属于users组的文件
find /path -nouser                 # 没有属主的文件
find /path -nogroup                # 没有属组的文件
```

## 常用操作

### exec执行命令

```bash
find /path -name "*.txt" -exec cat {} \;         # 显示所有txt文件内容
find /path -name "*.log" -exec rm {} \;          # 删除所有log文件
find /path -type d -exec chmod 755 {} \;         # 设置目录权限
find /path -type f -exec chmod 644 {} \;         # 设置文件权限
```

### ok执行命令（需确认）

```bash
find /path -name "*.tmp" -ok rm {} \;            # 删除前确认
```

### print打印路径

```bash
find /path -name "*.txt" -print                  # 打印路径
find /path -name "*.txt" -print0                 # 用null分隔（处理含空格文件名）
```

## 组合条件

### 与条件（-a）

```bash
find /path -name "*.txt" -a -size +1M            # txt文件且大于1MB
find /path -type f -a -mtime -7                  # 7天内修改的文件
```

### 或条件（-o）

```bash
find /path -name "*.txt" -o -name "*.md"         # txt或md文件
find /path -type f -o -type d                    # 文件或目录
```

### 非条件（!）

```bash
find /path ! -name "*.txt"                       # 不是txt文件
find /path ! -type d                             # 不是目录
```

## 实用示例

### 查找并删除文件

```bash
find /path -name "*.tmp" -delete                 # 删除所有tmp文件
find /path -type f -empty -delete                # 删除所有空文件
```

### 查找大文件

```bash
find /path -type f -size +100M -exec ls -lh {} \;
find / -type f -size +1G 2>/dev/null             # 查找全盘大于1GB的文件
```

### 查找最近修改的文件

```bash
find /path -type f -mtime -1                     # 最近24小时
find /path -type f -mmin -60                     # 最近60分钟
```

### 查找空目录

```bash
find /path -type d -empty                        # 查找空目录
find /path -type d -empty -delete                # 删除空目录
```

### 统计文件数量

```bash
find /path -type f | wc -l                       # 统计文件数
find /path -name "*.txt" | wc -l                 # 统计txt文件数
```

### 查找并打包

```bash
find /path -name "*.txt" | tar -czf texts.tar.gz -T -
```

## 性能优化

### 限制搜索深度

```bash
find /path -maxdepth 2 -name "*.txt"             # 最多搜索2层
find /path -mindepth 1 -maxdepth 3               # 搜索1-3层
```

### 排除目录

```bash
find /path -path "/path/dir" -prune -o -name "*.txt" -print
```

## 参考资料

- [find命令 - Linux man page](https://man7.org/linux/man-pages/man1/find.1.html)
