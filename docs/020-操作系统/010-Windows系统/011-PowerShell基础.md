# PowerShell基础

## 概述

PowerShell是Windows的命令行Shell和脚本语言，基于.NET Framework，提供强大的系统管理能力。

## PowerShell特点

1. **面向对象**：命令输出为对象而非文本
2. **管道传递对象**：对象在管道中传递
3. **统一命令格式**：动词-名词格式（如Get-Process）
4. **强大的脚本语言**：支持变量、函数、类等
5. **跨平台**：PowerShell Core支持Linux和macOS

## 基本命令

### 获取帮助

```powershell
# 获取命令帮助
Get-Help Get-Process

# 详细帮助
Get-Help Get-Process -Full

# 示例
Get-Help Get-Process -Examples

# 更新帮助文档
Update-Help
```

### 常用命令

```powershell
# 进程管理
Get-Process                    # 获取所有进程
Get-Process -Name notepad      # 获取指定进程
Stop-Process -Name notepad     # 停止进程
Start-Process notepad          # 启动进程

# 服务管理
Get-Service                    # 获取所有服务
Get-Service -Name wuauserv     # 获取指定服务
Start-Service -Name wuauserv   # 启动服务
Stop-Service -Name wuauserv    # 停止服务
Restart-Service -Name wuauserv # 重启服务

# 文件操作
Get-ChildItem                  # 列出当前目录
Get-ChildItem -Path C:\ -Recurse -Depth 1
Copy-Item source.txt dest.txt  # 复制文件
Move-Item source.txt dest.txt  # 移动文件
Remove-Item file.txt           # 删除文件
New-Item -Type File file.txt   # 创建文件
New-Item -Type Directory dir   # 创建目录

# 文件内容
Get-Content file.txt           # 读取文件
Set-Content file.txt "Hello"   # 写入文件
Add-Content file.txt "World"   # 追加内容
Clear-Content file.txt         # 清空内容

# 系统信息
Get-ComputerInfo               # 计算机信息
Get-Host                       # PowerShell主机信息
$PSVersionTable                # PowerShell版本
```

## 变量

```powershell
# 定义变量
$name = "Hello"
$number = 100
$array = 1, 2, 3, 4, 5
$hash = @{Key1="Value1"; Key2="Value2"}

# 访问变量
$name
$array[0]
$hash["Key1"]

# 特殊变量
$_         # 当前管道对象
$args      # 脚本参数
$true      # 真
$false     # 假
$null      # 空值
$HOME      # 用户主目录
$PWD       # 当前目录
```

## 管道

```powershell
# 管道传递对象
Get-Process | Where-Object {$_.CPU -gt 100}
Get-Service | Where-Object {$_.Status -eq "Running"}
Get-ChildItem | Sort-Object Length -Descending | Select-Object -First 10

# 常用管道命令
Get-Process | Select-Object Name, CPU, WorkingSet
Get-Process | Sort-Object CPU -Descending
Get-Process | Where-Object {$_.Name -like "*note*"}
Get-Process | Group-Object Name
Get-Process | Measure-Object CPU -Sum
```

## 条件语句

```powershell
# if语句
if ($value -gt 10) {
    Write-Host "Greater than 10"
} elseif ($value -eq 10) {
    Write-Host "Equal to 10"
} else {
    Write-Host "Less than 10"
}

# switch语句
switch ($value) {
    1 { Write-Host "One" }
    2 { Write-Host "Two" }
    default { Write-Host "Other" }
}
```

## 循环语句

```powershell
# for循环
for ($i = 0; $i -lt 10; $i++) {
    Write-Host $i
}

# foreach循环
foreach ($item in $array) {
    Write-Host $item
}

# while循环
while ($i -lt 10) {
    Write-Host $i
    $i++
}

# do-while循环
do {
    Write-Host $i
    $i++
} while ($i -lt 10)
```

## 函数

```powershell
# 定义函数
function Get-Sum {
    param($a, $b)
    return $a + $b
}

# 调用函数
Get-Sum 1 2

# 带类型的参数
function Add-Numbers {
    param(
        [int]$a,
        [int]$b
    )
    return $a + $b
}

# 带帮助的函数
function Get-Hello {
    <#
    .SYNOPSIS
        输出问候语
    .DESCRIPTION
        输出个性化的问候语
    .PARAMETER Name
        用户名称
    #>
    param([string]$Name = "World")
    Write-Host "Hello, $Name!"
}
```

## 模块

```powershell
# 查看模块
Get-Module -ListAvailable

# 导入模块
Import-Module ActiveDirectory

# 查看模块命令
Get-Command -Module ActiveDirectory

# 安装模块
Install-Module -Name PSReadLine
```

## 远程执行

```powershell
# 启用远程
Enable-PSRemoting

# 远程执行
Invoke-Command -ComputerName Server01 -ScriptBlock {Get-Process}

# 进入远程会话
Enter-PSSession -ComputerName Server01
Exit-PSSession
```

## 常用操作示例

### 查找文件

```powershell
# 查找大文件
Get-ChildItem -Path C:\ -Recurse -File | 
    Where-Object {$_.Length -gt 100MB} | 
    Sort-Object Length -Descending | 
    Select-Object FullName, Length

# 查找特定扩展名
Get-ChildItem -Path C:\ -Recurse -Include *.log | 
    Select-Object FullName
```

### 进程监控

```powershell
# 监控CPU占用
while ($true) {
    Get-Process | 
        Where-Object {$_.CPU -gt 10} | 
        Select-Object Name, CPU
    Start-Sleep -Seconds 5
}
```

### 事件日志

```powershell
# 查看事件日志
Get-EventLog -LogName System -Newest 10

# 查看错误事件
Get-EventLog -LogName System -EntryType Error -Newest 10

# 写入事件日志
Write-EventLog -LogName Application -Source "MyApp" -EventId 1 -Message "Hello"
```

## 参考资料

- [PowerShell文档](https://docs.microsoft.com/powershell/)
- [PowerShell脚本中心](https://gallery.technet.microsoft.com/)
