# Windows系统维护

## 概述

Windows系统维护包括磁盘清理、系统优化、故障排查等日常管理任务。

## 磁盘管理

### 磁盘清理

```batch
:: 运行磁盘清理工具
cleanmgr

:: 自动清理
cleanmgr /sagerun:1

:: 清理临时文件
del /q /f "%TEMP%\*.*"
del /q /f "C:\Windows\Temp\*.*"

:: 清理回收站
rd /s /q C:\$Recycle.Bin

:: 清理日志文件
forfiles /p "C:\Windows\Logs" /s /m *.log /d -30 /c "cmd /c del @path"
```

### 磁盘检查

```batch
:: 检查磁盘错误
chkdsk C: /f

:: 检查并修复
chkdsk C: /f /r

:: 离线检查
chkdsk C: /f /r /x
```

### 磁盘碎片整理

```batch
:: 分析磁盘
defrag C: /a

:: 整理磁盘
defrag C:

:: 优化SSD
defrag C: /o

:: 整理所有磁盘
defrag /c
```

### 磁盘空间分析

```powershell
# 查看磁盘使用
Get-Volume

# 查看文件夹大小
Get-ChildItem C:\ -Recurse | 
    Where-Object {$_.PSIsContainer} | 
    ForEach-Object {
        $size = (Get-ChildItem $_.FullName -Recurse -File | Measure-Object Length -Sum).Sum
        [PSCustomObject]@{
            Path = $_.FullName
            SizeMB = [math]::Round($size / 1MB, 2)
        }
    } | Sort-Object SizeMB -Descending | Select-Object -First 10
```

## 系统优化

### 禁用不必要的服务

```powershell
# 列出自动启动的服务
Get-Service | Where-Object {$_.StartType -eq "Automatic" -and $_.Status -eq "Running"}

# 禁用服务
Stop-Service -Name "ServiceName"
Set-Service -Name "ServiceName" -StartupType Disabled
```

### 禁用启动项

```batch
:: 查看启动项
wmic startup get caption,command

:: 通过注册表禁用
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "AppName" /f
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "AppName" /f
```

### 系统性能设置

```batch
:: 设置性能选项（调整为最佳性能）
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f

:: 禁用索引服务
sc stop WSearch
sc config WSearch start= disabled
```

### 电源管理

```batch
:: 查看电源方案
powercfg /list

:: 设置高性能模式
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c7354

:: 关闭休眠
powercfg /hibernate off

:: 查看电源设置
powercfg /query
```

## 系统修复

### 系统文件检查

```batch
:: 扫描系统文件
sfc /scannow

:: 验证系统文件
sfc /verifyonly

:: 修复指定文件
sfc /scanfile=C:\Windows\System32\kernel32.dll
```

### DISM修复

```batch
:: 检查系统镜像
DISM /Online /Cleanup-Image /CheckHealth

:: 扫描系统镜像
DISM /Online /Cleanup-Image /ScanHealth

:: 恢复系统镜像
DISM /Online /Cleanup-Image /RestoreHealth

:: 使用源文件恢复
DISM /Online /Cleanup-Image /RestoreHealth /Source:E:\sources\install.wim
```

### Windows更新修复

```batch
:: 重置Windows更新组件
net stop wuauserv
net stop cryptSvc
net stop bits
net stop msiserver

ren C:\Windows\SoftwareDistribution SoftwareDistribution.old
ren C:\Windows\System32\catroot2 catroot2.old

net start wuauserv
net start cryptSvc
net start bits
net start msiserver
```

### 网络重置

```batch
:: 重置网络适配器
netsh winsock reset
netsh int ip reset
ipconfig /flushdns

:: 重置防火墙
netsh advfirewall reset
```

## 事件日志

### 查看事件日志

```powershell
# 查看系统日志
Get-EventLog -LogName System -Newest 100

# 查看错误事件
Get-EventLog -LogName System -EntryType Error -Newest 50

# 查看应用程序日志
Get-EventLog -LogName Application -Newest 100

# 按时间过滤
Get-EventLog -LogName System -After (Get-Date).AddDays(-1)

# 按来源过滤
Get-EventLog -LogName System -Source "disk" -Newest 20

# 查看特定事件ID
Get-EventLog -LogName System -InstanceId 6005
```

### 清理事件日志

```batch
:: 清理日志
wevtutil el | for /f %x in ('wevtutil el') do wevtutil cl "%x"

:: 清理特定日志
wevtutil cl System
wevtutil cl Application
```

## 系统信息收集

```batch
:: 系统信息
systeminfo

:: 查看已安装补丁
wmic qfe list

:: 查看硬件信息
wmic computersystem get model,manufacturer
wmic cpu get name,numberofcores,numberoflogicalprocessors
wmic memorychip get capacity,speed
wmic diskdrive get model,size

:: 查看网络配置
ipconfig /all
netstat -an
route print
arp -a
```

## 故障排查

### 进程诊断

```batch
:: 查看进程
tasklist /v
tasklist /svc

:: 查看高CPU进程
wmic process get name,workingsetsize,pagefileusage /format:csv

:: 结束进程
taskkill /pid 1234 /f
taskkill /im process.exe /f
```

### 性能监控

```batch
:: 实时监控
typeperf "\Processor(_Total)\% Processor Time"
typeperf "\Memory\Available MBytes"
typeperf "\PhysicalDisk(_Total)\Disk Read Bytes/sec"

:: 使用性能监视器
perfmon
```

### 内存诊断

```batch
:: 运行内存诊断工具
mdsched

:: 查看内存信息
wmic memorychip get capacity,speed,manufacturer
```

## 备份与恢复

### 创建还原点

```powershell
# 启用系统保护
Enable-ComputerRestore -Drive "C:\"

# 创建还原点
Checkpoint-Computer -Description "Before Update" -RestorePointType MODIFY_SETTINGS
```

### 系统备份

```batch
:: 使用wbadmin备份
wbadmin start backup -backupTarget:D: -include:C: -allCritical

:: 查看备份
wbadmin get versions
```

## 参考资料

- [Windows系统管理](https://docs.microsoft.com/windows-server/administration/)
- [Windows故障排除](https://docs.microsoft.com/windows-client/troubleshoot/)
