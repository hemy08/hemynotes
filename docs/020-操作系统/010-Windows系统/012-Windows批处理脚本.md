# Windows批处理脚本

## 概述

批处理脚本是Windows的自动化脚本，使用.bat或.cmd扩展名，可执行一系列命令。

## 基本语法

### 注释

```batch
@echo off
REM 这是单行注释
:: 这也是注释（更常用）
```

### 输出和变量

```batch
@echo off
echo Hello, World!

:: 设置变量
set name=Hello
echo %name%

:: 设置数值变量
set /a num=100
set /a sum=%num%+50
echo %sum%

:: 用户输入
set /p input=请输入:
echo 你输入了: %input%
```

### 环境变量

```batch
:: 查看所有环境变量
set

:: 查看特定变量
echo %PATH%
echo %USERPROFILE%
echo %TEMP%
echo %DATE%
echo %TIME%
echo %CD%

:: 设置环境变量（临时）
set MY_VAR=Hello

:: 设置系统环境变量（永久，需管理员）
setx MY_VAR "Hello"
setx MY_VAR "Hello" /M
```

## 流程控制

### if语句

```batch
@echo off
set num=10

:: 等于
if %num%==10 echo 等于10

:: 不等于
if not %num%==20 echo 不等于20

:: 大于
if %num% gtr 5 echo 大于5

:: 小于
if %num% lss 20 echo 小于20

:: 存在判断
if exist file.txt echo 文件存在

:: 目录判断
if exist mydir\ echo 目录存在

:: 定义判断
if defined MY_VAR echo 变量已定义
```

比较运算符：
- EQU 等于
- NEQ 不等于
- LSS 小于
- LEQ 小于等于
- GTR 大于
- GEQ 大于等于

### if-else

```batch
@echo off
set num=10

if %num%==10 (
    echo 等于10
) else (
    echo 不等于10
)

:: 嵌套if
if %num% geq 10 (
    if %num% leq 20 (
        echo 在10到20之间
    )
)
```

### for循环

```batch
@echo off

:: 遍历列表
for %%i in (1 2 3 4 5) do echo %%i

:: 遍历文件
for %%f in (*.txt) do echo %%f

:: 遍历目录
for /d %%d in (*) do echo %%d

:: 递归遍历
for /r %%f in (*.txt) do echo %%f

:: 数字范围
for /l %%i in (1,1,10) do echo %%i
:: (起始,步长,结束)

:: 读取文件内容
for /f "tokens=1,2" %%a in (file.txt) do (
    echo 第1列: %%a, 第2列: %%b
)

:: 读取命令输出
for /f "tokens=*" %%i in ('dir /b') do echo %%i
```

### goto和标签

```batch
@echo off
:start
echo 循环
goto start
```

### call调用

```batch
@echo off
call :myfunction 10 20
echo 返回值: %result%
goto :eof

:myfunction
set /a result=%1+%2
goto :eof
```

## 字符串操作

```batch
@echo off
set str=Hello World

:: 截取
echo %str:~0,5%       :: Hello
echo %str:~6%         :: World
echo %str:~-5%        :: World

:: 替换
echo %str:World=PowerShell%

:: 连接
set str1=Hello
set str2=World
set str3=%str1% %str2%
echo %str3%

:: 查找
echo %str:*l=%        :: lo World（第一个l之后的内容）
```

## 文件操作

```batch
@echo off

:: 创建文件
type nul > newfile.txt
echo Hello > file.txt
echo World >> file.txt

:: 复制文件
copy source.txt dest.txt
copy source.txt + another.txt merged.txt

:: 移动文件
move source.txt dest\
move source.txt newname.txt

:: 删除文件
del file.txt
del *.tmp
del /q /s *.log    :: 静默递归删除

:: 重命名
ren oldname.txt newname.txt

:: 创建目录
mkdir newdir
md dir1\dir2\dir3

:: 删除目录
rmdir emptydir
rd /s /q mydir     :: 递归删除

:: 查看文件内容
type file.txt
more file.txt
```

## 网络命令

```batch
@echo off

:: 查看IP配置
ipconfig
ipconfig /all
ipconfig /release
ipconfig /renew

:: 网络测试
ping 192.168.1.1
ping -n 10 192.168.1.1

:: 路由表
route print
route add 192.168.2.0 mask 255.255.255.0 192.168.1.1

:: DNS
nslookup www.example.com

:: 端口
netstat -an
netstat -ano | findstr :80

:: 网络共享
net share
net share myshare=C:\share
net use \\server\share
```

## 系统管理

```batch
@echo off

:: 查看服务
sc query
sc query wuauserv
sc start wuauserv
sc stop wuauserv

:: 任务列表
tasklist
tasklist | findstr notepad
taskkill /im notepad.exe
taskkill /pid 1234 /f

:: 系统信息
systeminfo

:: 关机重启
shutdown /s /t 60       :: 60秒后关机
shutdown /r /t 60       :: 60秒后重启
shutdown /a             :: 取消关机
shutdown /l             :: 注销

:: 用户管理
net user
net user newuser password /add
net user username /delete
net localgroup administrators username /add
```

## 常用脚本示例

### 备份脚本

```batch
@echo off
set source=C:\important
set dest=D:\backup\%DATE:/=-%
mkdir "%dest%"
xcopy "%source%" "%dest%" /e /i /y
echo 备份完成
pause
```

### 批量重命名

```batch
@echo off
setlocal enabledelayedexpansion
set count=1
for %%f in (*.txt) do (
    ren "%%f" "file_!count!.txt"
    set /a count+=1
)
```

### 自动清理临时文件

```batch
@echo off
echo 正在清理临时文件...
del /q /f "%TEMP%\*.*"
del /q /f "C:\Windows\Temp\*.*"
for /d %%d in ("%TEMP%\*") do rd /s /q "%%d"
echo 清理完成
pause
```

### 检测服务状态

```batch
@echo off
set service=wuauserv
sc query %service% | find "RUNNING" > nul
if errorlevel 1 (
    echo 服务未运行，正在启动...
    net start %service%
) else (
    echo 服务已运行
)
```

## 错误处理

```batch
@echo off

:: 使用errorlevel
copy file.txt dest\
if errorlevel 1 (
    echo 复制失败
) else (
    echo 复制成功
)

:: 错误重定向
dir file.txt 2>nul
if errorlevel 1 echo 文件不存在
```

## 参考资料

- [Windows批处理命令](https://docs.microsoft.com/windows-server/administration/windows-commands/)
