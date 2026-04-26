# gzip命令

## 概述

gzip是Linux下常用的压缩工具，使用Lempel-Ziv算法进行压缩。

## 基本语法

```bash
gzip [选项] 文件...
```

## 常用选项

| 选项 | 说明 |
|------|------|
| `-d` | 解压 |
| `-k` | 保留原文件 |
| `-v` | 显示详细信息 |
| `-l` | 显示压缩信息 |
| `-t` | 测试压缩文件完整性 |
| `-数字` | 压缩级别（1-9，默认6） |

## 基本用法

### 压缩文件

```bash
gzip file.txt                       # 压缩文件（原文件被删除）
gzip -k file.txt                    # 压缩并保留原文件
gzip -9 file.txt                    # 最大压缩率
gzip -1 file.txt                    # 最快压缩速度
```

### 解压文件

```bash
gzip -d file.txt.gz                 # 解压
gunzip file.txt.gz                  # 解压（另一种方式）
```

### 查看压缩信息

```bash
gzip -l file.txt.gz                 # 显示压缩信息
gzip -t file.txt.gz                 # 测试文件完整性
```

## 实用示例

### 批量压缩

```bash
gzip *.txt                          # 压缩所有txt文件
gzip -v *.log                       # 显示压缩过程
```

### 压缩目录

```bash
tar -czf archive.tar.gz dir/        # 配合tar压缩目录
```

### 管道压缩

```bash
cat file.txt | gzip > file.txt.gz
mysqldump db | gzip > db.sql.gz     # 压缩数据库备份
```

### 查看压缩文件内容

```bash
zcat file.txt.gz                    # 查看压缩文件内容
zless file.txt.gz                   # 分页查看
zgrep "pattern" file.txt.gz         # 在压缩文件中搜索
```

## 参考资料

- [gzip命令 - Linux man page](https://man7.org/linux/man-pages/man1/gzip.1.html)
