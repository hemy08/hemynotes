# Windows安全设置

## 概述

Windows安全设置包括用户账户控制、防火墙、杀毒软件、安全策略等多个方面。

## 用户账户控制（UAC）

### 修改UAC级别

```batch
:: 通过注册表修改
:: 0: 从不通知
:: 1: 仅在程序尝试更改时通知
:: 2: 默认（程序尝试更改时通知）
:: 3: 始终通知

reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 1 /f
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 2 /f
```

### 以管理员身份运行

```batch
:: 使用runas
runas /user:Administrator cmd

:: 使用PowerShell
Start-Process powershell -Verb RunAs
```

## Windows Defender

### PowerShell管理

```powershell
# 查看Defender状态
Get-MpComputerStatus

# 更新病毒库
Update-MpSignature

# 扫描
Start-MpScan -ScanType QuickScan
Start-MpScan -ScanType FullScan

# 查看检测历史
Get-MpThreatDetection

# 移除威胁
Remove-MpThreat

# 排除路径
Add-MpPreference -ExclusionPath "C:\MyApp"

# 排除扩展名
Add-MpPreference -ExclusionExtension ".log"

# 禁用实时保护（不推荐）
Set-MpPreference -DisableRealtimeMonitoring $true

# 启用实时保护
Set-MpPreference -DisableRealtimeMonitoring $false
```

### 排除设置

```powershell
# 添加排除路径
Add-MpPreference -ExclusionPath "C:\Projects" -Force

# 添加排除进程
Add-MpPreference -ExclusionProcess "myapp.exe"

# 查看排除项
Get-MpPreference | Select-Object ExclusionPath, ExclusionProcess
```

## 本地安全策略

### secpol.msc

通过图形界面配置：
1. Win+R → secpol.msc
2. 配置账户策略、本地策略等

### 密码策略

```batch
:: 使用net accounts命令
net accounts                    :: 查看当前设置
net accounts /minpwlen:8        :: 最小密码长度
net accounts /maxpwage:90       :: 密码最大有效期（天）
net accounts /minpwage:1        :: 密码最小有效期（天）
net accounts /uniquepw:5        :: 密码历史记录数量
```

### 账户锁定策略

```batch
:: 设置锁定阈值
net accounts /lockoutthreshold:5    :: 5次失败后锁定

:: 设置锁定时间
net accounts /lockoutduration:30    :: 锁定30分钟

:: 设置重置时间
net accounts /lockoutwindow:30      :: 30分钟内失败计数
```

## BitLocker加密

### 启用BitLocker

```batch
:: 查看BitLocker状态
manage-bde -status

:: 启用BitLocker
manage-bde -on C:

:: 使用密码保护
manage-bde -on C: -pw

:: 使用恢复密钥
manage-bde -on C: -rk

:: 备份恢复密钥
manage-bde -backup C: -bk E:\

:: 暂停BitLocker
manage-bde -pause C:

:: 恢复BitLocker
manage-bde -resume C:

:: 禁用BitLocker
manage-bde -off C:
```

### PowerShell BitLocker

```powershell
# 查看状态
Get-BitLockerVolume

# 启用BitLocker
Enable-BitLocker -MountPoint "C:" -EncryptionMethod Aes256 -UsedSpaceOnly

# 添加密码保护
Add-BitLockerKeyProtector -MountPoint "C:" -PasswordProtector
```

## Windows更新

### PowerShell管理

```powershell
# 查看更新模块
Get-WindowsUpdate

# 安装更新
Install-WindowsUpdate -AcceptAll -AutoReboot

# 查看更新历史
Get-WUHistory

# 隐藏特定更新
Hide-WindowsUpdate -KBArticleID KB123456

# 查看隐藏更新
Get-WindowsUpdate -Hidden
```

### 命令行更新

```batch
:: 检查更新
usoclient StartScan

:: 下载更新
usoclient StartDownload

:: 安装更新
usoclient StartInstall

:: 重启设备
usoclient RestartDevice
```

## 远程桌面

### 启用远程桌面

```batch
:: 通过注册表启用
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f

:: 防火墙放行
netsh advfirewall firewall add rule name="RDP" dir=in action=allow protocol=tcp localport=3389
```

### PowerShell启用

```powershell
# 启用远程桌面
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 0

# 启用Network Level Authentication
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name "UserAuthentication" -Value 1
```

## 禁用不必要的服务

```powershell
# 查看自动启动服务
Get-Service | Where-Object {$_.StartType -eq "Automatic"}

# 禁用服务示例
Stop-Service -Name "DiagTrack"          # Connected User Experiences
Set-Service -Name "DiagTrack" -StartupType Disabled

Stop-Service -Name "WMPNetworkSvc"      # Windows Media Player Network
Set-Service -Name "WMPNetworkSvc" -StartupType Disabled
```

## 隐私设置

### 通过注册表

```batch
:: 禁用遥测
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f

:: 禁用广告ID
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo" /v Enabled /t REG_DWORD /d 0 /f

:: 禁用位置服务
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Location" /v DisableLocation /t REG_DWORD /d 1 /f

:: 禁用Cortana
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search" /v AllowCortana /t REG_DWORD /d 0 /f
```

## 安全审计

### 启用审计策略

```batch
:: 审核登录事件
auditpol /set /subcategory:"Logon" /success:enable /failure:enable

:: 审核对象访问
auditpol /set /subcategory:"Object Access" /success:enable /failure:enable

:: 审核策略更改
auditpol /set /subcategory:"Policy Change" /success:enable /failure:enable

:: 查看审计策略
auditpol /get /category:*
```

## 参考资料

- [Windows安全文档](https://docs.microsoft.com/windows/security/)
- [BitLocker文档](https://docs.microsoft.com/windows/security/information-protection/bitlocker/)
