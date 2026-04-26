# Linux Shell脚本编程

## 概述

Shell脚本是Linux系统的自动化脚本，使用.sh扩展名，可以执行一系列命令和控制流程。

## 基本语法

### 脚本结构

```bash
#!/bin/bash
# 这是一个Shell脚本示例

echo "Hello, World!"
```

### 注释

```bash
# 单行注释
echo "Hello"

: '
多行注释
第二行
第三行
'
```

### 执行脚本

```bash
# 添加执行权限
chmod +x script.sh

# 直接执行
./script.sh

# 用bash执行
bash script.sh

# 用source执行（在当前shell中）
source script.sh
. script.sh
```

## 变量

### 定义和使用

```bash
#!/bin/bash

# 定义变量（等号两边不能有空格）
name="Hello"
age=100

# 使用变量
echo $name
echo ${name}
echo "My name is $name, age is $age"

# 只读变量
readonly PI=3.14

# 删除变量
unset name
```

### 特殊变量

```bash
#!/bin/bash

echo "脚本名: $0"           # 脚本名称
echo "参数个数: $#"         # 参数数量
echo "所有参数: $*"         # 所有参数
echo "所有参数: $@"         # 所有参数（数组形式）
echo "第一个参数: $1"       # 第一个参数
echo "第二个参数: $2"       # 第二个参数
echo "上一命令退出码: $?"   # 上一个命令的退出码
echo "当前进程ID: $$"       # 当前进程ID
```

### 环境变量

```bash
#!/bin/bash

echo $HOME          # 用户主目录
echo $PWD           # 当前目录
echo $USER          # 当前用户
echo $PATH          # PATH环境变量
echo $LANG          # 语言设置
echo $SHELL         # 当前Shell
```

## 字符串操作

```bash
#!/bin/bash

str="Hello World"

# 字符串长度
echo ${#str}                # 11

# 截取子串
echo ${str:0:5}             # Hello
echo ${str:6}               # World
echo ${str: -5}             # orld

# 查找替换
echo ${str/World/Linux}     # Hello Linux（替换第一个）
echo ${str//o/O}            # HellO WOrld（替换所有）

# 删除匹配
echo ${str#Hello }          # World（删除开头匹配）
echo ${str%World}           # Hello （删除结尾匹配）

# 大小写转换
echo ${str^^}               # HELLO WORLD（大写）
echo ${str,,}               # hello world（小写）

# 默认值
unset var
echo ${var:-"default"}      # default
echo ${var:="default"}      # default（并赋值）
```

## 数组

```bash
#!/bin/bash

# 定义数组
arr=(1 2 3 4 5)
arr2=([0]=a [1]=b [2]=c)

# 访问元素
echo ${arr[0]}              # 1
echo ${arr[-1]}             # 5（最后一个）

# 所有元素
echo ${arr[@]}
echo ${arr[*]}

# 数组长度
echo ${#arr[@]}             # 5
echo ${#arr[0]}             # 1（第一个元素的长度）

# 添加元素
arr+=(6 7)

# 删除元素
unset arr[2]

# 遍历数组
for i in ${arr[@]}; do
    echo $i
done

# 遍历索引
for i in ${!arr[@]}; do
    echo "$i: ${arr[$i]}"
done
```

## 条件判断

### if语句

```bash
#!/bin/bash

num=10

# 基本if
if [ $num -eq 10 ]; then
    echo "等于10"
fi

# if-else
if [ $num -gt 10 ]; then
    echo "大于10"
else
    echo "小于等于10"
fi

# if-elif-else
if [ $num -gt 20 ]; then
    echo "大于20"
elif [ $num -gt 10 ]; then
    echo "大于10"
else
    echo "小于等于10"
fi

# 逻辑运算
if [ $num -gt 5 ] && [ $num -lt 15 ]; then
    echo "在5到15之间"
fi

if [ $num -lt 5 ] || [ $num -gt 15 ]; then
    echo "不在5到15之间"
fi
```

### 条件测试

```bash
#!/bin/bash

# 数值比较
[ $a -eq $b ]   # 等于
[ $a -ne $b ]   # 不等于
[ $a -gt $b ]   # 大于
[ $a -ge $b ]   # 大于等于
[ $a -lt $b ]   # 小于
[ $a -le $b ]   # 小于等于

# 字符串比较
[ "$str1" = "$str2" ]      # 相等
[ "$str1" != "$str2" ]     # 不相等
[ -z "$str" ]              # 空字符串
[ -n "$str" ]              # 非空字符串

# 文件测试
[ -e file ]      # 存在
[ -f file ]      # 是普通文件
[ -d dir ]       # 是目录
[ -r file ]      # 可读
[ -w file ]      # 可写
[ -x file ]      # 可执行
[ -s file ]      # 非空文件
[ file1 -nt file2 ]  # file1比file2新
[ file1 -ot file2 ]  # file1比file2旧
```

## 循环

### for循环

```bash
#!/bin/bash

# 列表循环
for i in 1 2 3 4 5; do
    echo $i
done

# 范围循环
for i in {1..5}; do
    echo $i
done

# 步长循环
for i in {1..10..2}; do
    echo $i
done

# C风格for循环
for ((i=1; i<=5; i++)); do
    echo $i
done

# 遍历文件
for file in *.txt; do
    echo $file
done

# 遍历命令输出
for line in $(cat file.txt); do
    echo $line
done
```

### while循环

```bash
#!/bin/bash

# 基本while
i=1
while [ $i -le 5 ]; do
    echo $i
    ((i++))
done

# 读取文件
while read line; do
    echo $line
done < file.txt

# 无限循环
while true; do
    echo "Press Ctrl+C to exit"
    sleep 1
done
```

### until循环

```bash
#!/bin/bash

i=1
until [ $i -gt 5 ]; do
    echo $i
    ((i++))
done
```

### 循环控制

```bash
#!/bin/bash

# break
for i in {1..10}; do
    if [ $i -eq 5 ]; then
        break
    fi
    echo $i
done

# continue
for i in {1..10}; do
    if [ $i -eq 5 ]; then
        continue
    fi
    echo $i
done
```

## 函数

### 定义和调用

```bash
#!/bin/bash

# 定义函数
hello() {
    echo "Hello, World!"
}

# 调用函数
hello

# 带参数的函数
greet() {
    echo "Hello, $1!"
    echo "You are $2 years old"
}

greet "Alice" 25

# 返回值
add() {
    echo $(($1 + $2))
}

result=$(add 10 20)
echo $result

# 返回退出码
check_file() {
    if [ -f "$1" ]; then
        return 0
    else
        return 1
    fi
}

check_file "test.txt"
if [ $? -eq 0 ]; then
    echo "File exists"
fi
```

### 局部变量

```bash
#!/bin/bash

func() {
    local local_var="I'm local"
    echo $local_var
}

func
echo $local_var    # 空，因为局部变量在外部不可见
```

## 输入输出

### read命令

```bash
#!/bin/bash

# 读取输入
echo "Enter your name:"
read name
echo "Hello, $name!"

# 读取多个变量
read -p "Enter name and age: " name age
echo "Name: $name, Age: $age"

# 读取密码（不显示）
read -s -p "Enter password: " password
echo

# 读取到数组
read -a arr -p "Enter numbers: "
echo "First: ${arr[0]}"

# 限制输入长度
read -n 1 -p "Continue? (y/n): " answer
echo
```

### printf格式化

```bash
#!/bin/bash

printf "Hello, %s!\n" "World"
printf "%d + %d = %d\n" 10 20 $((10+20))
printf "%-10s %5d\n" "Name" 100
printf "%.2f\n" 3.14159
```

## 信号处理

```bash
#!/bin/bash

# 捕获信号
trap 'echo "Interrupted!"; exit 1' INT
trap 'echo "Terminated!"; exit 1' TERM

echo "PID: $$"
echo "Press Ctrl+C to exit"

while true; do
    sleep 1
done
```

## 调试

```bash
# 检查语法
bash -n script.sh

# 调试模式（显示执行的命令）
bash -x script.sh

# 在脚本中启用调试
#!/bin/bash
set -x    # 开启调试
set +x    # 关闭调试

# 遇到错误立即退出
set -e

# 使用未定义变量时报错
set -u
```

## 参考资料

- [Bash手册](https://www.gnu.org/software/bash/manual/)
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
