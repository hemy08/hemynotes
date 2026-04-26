# Windows任务计划

## 概述

Windows任务计划程序允许自动执行计划任务，如定期备份、系统维护、脚本运行等。

## schtasks命令

### 创建任务

```batch
:: 创建基本任务
schtasks /create /tn "MyTask" /tr "C:\scripts\backup.bat" /sc daily /st 02:00

:: 创建每周任务
schtasks /create /tn "WeeklyBackup" /tr "C:\scripts\backup.bat" /sc weekly /d SUN /st 03:00

:: 创建每月任务
schtasks /create /tn "MonthlyTask" /tr "C:\scripts\cleanup.bat" /sc monthly /d 1 /st 04:00

:: 创建每小时任务
schtasks /create /tn "HourlyTask" /tr "C:\scripts\check.bat" /sc hourly /mo 1

:: 创建开机启动任务
schtasks /create /tn "StartupTask" /tr "C:\scripts\startup.bat" /sc onstart

:: 创建用户登录任务
schtasks /create /tn "LoginTask" /tr "C:\scripts\login.bat" /sc onlogon

:: 创建空闲任务
schtasks /create /tn "IdleTask" /tr "C:\scripts\idle.bat" /sc onidle /i 30

:: 创建一次性任务
schtasks /create /tn "OneTimeTask" /tr "C:\scripts\once.bat" /sc once /st 15:00 /sd 01/15/2024
```

### 高级任务创建

```batch
:: 以系统账户运行
schtasks /create /tn "SystemTask" /tr "C:\scripts\system.bat" /sc daily /st 01:00 /ru SYSTEM

:: 以特定用户运行
schtasks /create /tn "UserTask" /tr "C:\scripts\user.bat" /sc daily /st 02:00 /ru "DOMAIN\username" /rp password

:: 最高权限运行
schtasks /create /tn "AdminTask" /tr "C:\scripts\admin.bat" /sc daily /st 02:00 /rl HIGHEST

:: 多实例策略
:: 默认：不允许并行运行
schtasks /create /tn "Task" /tr "script.bat" /sc daily /st 02:00 /np
```

### 查看任务

```batch
:: 查看所有任务
schtasks /query

:: 查看特定任务
schtasks /query /tn "MyTask"

:: 详细查看
schtasks /query /tn "MyTask" /v

:: XML格式输出
schtasks /query /tn "MyTask" /xml

:: 查看某个文件夹下的任务
schtasks /query /fo LIST /v
```

### 运行和停止

```batch
:: 立即运行任务
schtasks /run /tn "MyTask"

:: 强制运行（忽略条件）
schtasks /run /tn "MyTask" /i

:: 结束任务
schtasks /end /tn "MyTask"
```

### 修改和删除

```batch
:: 修改任务
schtasks /change /tn "MyTask" /tr "C:\scripts\newscript.bat" /st 03:00

:: 修改运行用户
schtasks /change /tn "MyTask" /ru "DOMAIN\newuser" /rp newpassword

:: 启用任务
schtasks /change /tn "MyTask" /enable

:: 禁用任务
schtasks /change /tn "MyTask" /disable

:: 删除任务
schtasks /delete /tn "MyTask"

:: 删除时不确认
schtasks /delete /tn "MyTask" /f

:: 删除所有任务
schtasks /delete /tn * /f
```

## PowerShell任务计划

### 创建任务

```powershell
# 创建触发器
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 3am
$trigger = New-ScheduledTaskTrigger -AtLogon
$trigger = New-ScheduledTaskTrigger -AtStartup

# 创建操作
$action = New-ScheduledTaskAction -Execute "C:\scripts\backup.bat"
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\scripts\script.ps1"

# 创建设置
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd -AllowStartIfOnBatteries

# 创建主体（运行用户）
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

# 注册任务
Register-ScheduledTask -TaskName "MyTask" -Trigger $trigger -Action $action -Settings $settings -Principal $principal
```

### 管理任务

```powershell
# 查看任务
Get-ScheduledTask
Get-ScheduledTask -TaskName "MyTask"

# 启用/禁用
Enable-ScheduledTask -TaskName "MyTask"
Disable-ScheduledTask -TaskName "MyTask"

# 运行/停止
Start-ScheduledTask -TaskName "MyTask"
Stop-ScheduledTask -TaskName "MyTask"

# 删除
Unregister-ScheduledTask -TaskName "MyTask"

# 导出任务
Export-ScheduledTask -TaskName "MyTask" | Out-File "MyTask.xml"

# 导入任务
Register-ScheduledTask -Xml (Get-Content "MyTask.xml" | Out-String) -TaskName "ImportedTask"
```

## 任务触发器类型

| 类型 | 说明 |
|------|------|
| /sc daily | 每天 |
| /sc weekly | 每周 |
| /sc monthly | 每月 |
| /sc once | 一次 |
| /sc onstart | 开机启动 |
| /sc onlogon | 用户登录 |
| /sc onidle | 系统空闲 |
| /sc minute | 每分钟 |
| /sc hourly | 每小时 |

## 任务条件设置

通过GUI设置更复杂的条件：
1. 打开任务计划程序：taskschd.msc
2. 创建任务 → 条件选项卡
3. 设置空闲条件、电源条件、网络条件等

## 常用任务示例

### 每日备份

```batch
schtasks /create /tn "DailyBackup" /tr "C:\scripts\backup.bat" /sc daily /st 02:00 /ru SYSTEM /rl HIGHEST
```

### 每周清理临时文件

```batch
schtasks /create /tn "WeeklyCleanup" /tr "C:\scripts\cleanup.bat" /sc weekly /d SUN /st 04:00
```

### 开机启动服务检查

```batch
schtasks /create /tn "ServiceCheck" /tr "C:\scripts\check_services.bat" /sc onstart /ru SYSTEM
```

### 监控CPU使用率

```powershell
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\scripts\monitor_cpu.ps1"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)
Register-ScheduledTask -TaskName "CPUMonitor" -Action $action -Trigger $trigger
```

## 参考资料

- [schtasks命令](https://docs.microsoft.com/windows-server/administration/windows-commands/schtasks)
- [任务计划程序](https://docs.microsoft.com/windows/desktop/taskschd/task-scheduler-start-page)
