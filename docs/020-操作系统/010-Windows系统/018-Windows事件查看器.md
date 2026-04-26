# Windows事件查看器

## 概述

Windows事件查看器记录系统、安全、应用程序等事件日志，用于故障排查和安全审计。

## 事件日志类型

| 日志类型 | 说明 |
|---------|------|
| Application | 应用程序事件 |
| System | 系统事件 |
| Security | 安全事件（需管理员权限） |
| Setup | 安装事件 |

## 事件级别

| 级别 | 说明 |
|------|------|
| Critical | 关键错误 |
| Error | 错误 |
| Warning | 警告 |
| Information | 信息 |
| Verbose | 详细信息 |

## wevtutil命令

### 查询事件

```batch
:: 查看所有日志
wevtutil el

:: 查询事件
wevtutil qe System /c:10
wevtutil qe Application /c:20 /rd:true

:: 查询特定事件ID
wevtutil qe System "/q:*[System[(EventID=6005)]]" /c:10

:: 查询错误级别事件
wevtutil qe System "/q:*[System[(Level=2)]]" /c:10

:: 格式化输出
wevtutil qe System /c:10 /f:text
wevtutil qe System /c:10 /f:xml
```

### 清理日志

```batch
:: 清理特定日志
wevtutil cl System
wevtutil cl Application

:: 清理所有日志
for /f %x in ('wevtutil el') do wevtutil cl "%x"
```

### 导出日志

```batch
:: 导出日志
wevtutil epl System system.evtx
wevtutil epl Application application.evtx

:: 导出特定时间范围
wevtutil epl System /query:"*[System[TimeCreated[timediff(@SystemTime) <= 86400000]]]" system_24h.evtx
```

## PowerShell事件日志

### 查看事件

```powershell
# 查看系统日志
Get-EventLog -LogName System -Newest 100
Get-EventLog -LogName Application -Newest 50

# 查看错误事件
Get-EventLog -LogName System -EntryType Error -Newest 20
Get-EventLog -LogName Application -EntryType Error,Warning -Newest 30

# 按事件ID查询
Get-EventLog -LogName System -InstanceId 6005 -Newest 10

# 按时间查询
Get-EventLog -LogName System -After (Get-Date).AddDays(-1)
Get-EventLog -LogName System -Before (Get-Date).AddHours(-12)

# 按来源查询
Get-EventLog -LogName System -Source "disk" -Newest 20

# 统计事件
Get-EventLog -LogName System | Group-Object Source | Sort-Object Count -Descending
```

### Write-EventLog

```powershell
# 写入事件日志
Write-EventLog -LogName Application -Source "MyApp" -EventId 1000 -Message "Application started"

# 写入错误事件
Write-EventLog -LogName Application -Source "MyApp" -EventId 1001 -EntryType Error -Message "An error occurred"

# 创建事件源（需管理员权限）
New-EventLog -LogName Application -Source "MyNewApp"
```

### 清除日志

```powershell
# 清除日志
Clear-EventLog -LogName Application
Limit-EventLog -LogName Application -OverflowAction OverwriteOlder
```

## 常用事件ID

### 系统启动事件

| 事件ID | 说明 |
|--------|------|
| 6005 | 事件日志服务启动（系统启动） |
| 6006 | 事件日志服务停止（系统关机） |
| 6008 | 非正常关机 |
| 6009 | 记录操作系统版本 |

### 服务事件

| 事件ID | 说明 |
|--------|------|
| 7036 | 服务进入运行/停止状态 |
| 7031 | 服务崩溃 |
| 7045 | 服务安装 |

### 安全事件

| 事件ID | 说明 |
|--------|------|
| 4624 | 登录成功 |
| 4625 | 登录失败 |
| 4634 | 注销 |
| 4648 | 使用显式凭据登录 |
| 4720 | 用户账户创建 |
| 4726 | 用户账户删除 |
| 4728 | 用户添加到安全组 |

## 事件日志监控脚本

```powershell
# 实时监控事件日志
$watcher = New-Object System.Diagnostics.EventLogWatcher("System")
$watcher.Enabled = $true

Register-ObjectEvent -InputObject $watcher -EventName EventRecordWritten -Action {
    $event = $EventArgs.NewEvent
    Write-Host "EventID: $($event.InstanceId)"
    Write-Host "Time: $($event.TimeCreated)"
    Write-Host "Message: $($event.Message)"
}
```

## WMI事件查询

```powershell
# 查询WMI事件
Get-WmiObject -Class Win32_NTLogEvent -Filter "LogFile='System' AND Type='Error'" | 
    Select-Object -First 10 TimeGenerated, SourceName, Message
```

## 事件订阅

```xml
<!-- 事件订阅示例 -->
<QueryList>
  <Query Id="0" Path="System">
    <Select Path="System">
      *[System[(Level=1  or Level=2 or Level=3)]]
    </Select>
  </Query>
</QueryList>
```

## 参考资料

- [Windows事件日志](https://docs.microsoft.com/windows/win32/eventlog/)
- [wevtutil命令](https://docs.microsoft.com/windows-server/administration/windows-commands/wevtutil)
