# Windows注册表详解

## 概述

Windows注册表是Windows系统的核心配置数据库，存储系统和应用程序的设置信息。

## 注册表结构

### 根键

| 根键 | 说明 |
|------|------|
| HKEY_CLASSES_ROOT | 文件关联和COM对象 |
| HKEY_CURRENT_USER | 当前用户设置 |
| HKEY_LOCAL_MACHINE | 本机系统设置 |
| HKEY_USERS | 所有用户配置 |
| HKEY_CURRENT_CONFIG | 硬件配置 |

### 数据类型

| 类型 | 说明 |
|------|------|
| REG_SZ | 字符串 |
| REG_EXPAND_SZ | 可扩展字符串 |
| REG_DWORD | 32位整数 |
| REG_QWORD | 64位整数 |
| REG_BINARY | 二进制数据 |
| REG_MULTI_SZ | 多字符串 |
| REG_NONE | 无类型 |

## reg命令操作

### 查询

```batch
:: 查询键值
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion"

:: 查询特定值
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion" /v ProductName

:: 查询所有子键
reg query "HKLM\SOFTWARE" /s

:: 使用通配符
reg query "HKCU\Software\Microsoft" /f "Office" /k
```

### 添加/修改

```batch
:: 添加字符串值
reg add "HKCU\Software\MyApp" /v Name /t REG_SZ /d "Value" /f

:: 添加DWORD值
reg add "HKCU\Software\MyApp" /v Count /t REG_DWORD /d 100 /f

:: 添加默认值
reg add "HKCU\Software\MyApp" /ve /d "Default" /f

:: 添加可扩展字符串
reg add "HKCU\Software\MyApp" /v Path /t REG_EXPAND_SZ /d "%USERPROFILE%\MyApp" /f
```

### 删除

```batch
:: 删除值
reg delete "HKCU\Software\MyApp" /v Name /f

:: 删除整个键
reg delete "HKCU\Software\MyApp" /f

:: 删除默认值
reg delete "HKCU\Software\MyApp" /ve /f
```

### 导出导入

```batch
:: 导出注册表
reg export "HKCU\Software\MyApp" backup.reg

:: 导入注册表
reg import backup.reg

:: 导出整个根键
reg export HKLM system.reg
```

## 常用注册表位置

### 系统启动

```
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
```

### 服务配置

```
HKLM\SYSTEM\CurrentControlSet\Services
```

### 环境变量

```
HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment
HKCU\Environment
```

### 网络配置

```
HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters
HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces
```

### 用户配置

```
HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer
HKCU\Control Panel\Desktop
```

## PowerShell操作注册表

### 查看注册表

```powershell
# 查看键
Get-ChildItem HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion

# 查看值
Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion

# 获取特定值
(Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion).ProductName
```

### 创建/修改

```powershell
# 创建键
New-Item -Path HKCU:\Software\MyApp -Force

# 创建值
New-ItemProperty -Path HKCU:\Software\MyApp -Name "Setting" -Value "Value" -PropertyType String

# 修改值
Set-ItemProperty -Path HKCU:\Software\MyApp -Name "Setting" -Value "NewValue"

# 创建DWORD值
New-ItemProperty -Path HKCU:\Software\MyApp -Name "Count" -Value 100 -PropertyType DWord
```

### 删除

```powershell
# 删除值
Remove-ItemProperty -Path HKCU:\Software\MyApp -Name "Setting"

# 删除键
Remove-Item -Path HKCU:\Software\MyApp -Recurse
```

## 注册表应用示例

### 禁用Windows Defender

```batch
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f
```

### 修改右键菜单

```batch
:: 添加"在此处打开命令提示符"
reg add "HKCR\Directory\Background\shell\cmd" /ve /d "在此处打开命令提示符" /f
reg add "HKCR\Directory\Background\shell\cmd\command" /ve /d "cmd.exe" /f
```

### 禁用自动更新

```batch
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v NoAutoUpdate /t REG_DWORD /d 1 /f
```

### 修改默认浏览器

```batch
reg add "HKCU\Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice" /v ProgId /t REG_SZ /d "ChromeHTML" /f
```

### 禁用休眠

```batch
powercfg /hibernate off
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v HibernateEnabled /t REG_DWORD /d 0 /f
```

## 注册表安全

### 权限设置

使用regedt32.exe设置权限：
1. 打开regedt32.exe
2. 选择要设置的键
3. 编辑 → 权限
4. 设置用户/组的权限

### 注册表保护

```powershell
# 检查键是否存在
Test-Path HKLM:\SOFTWARE\MyApp

# 备份重要键
$key = "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion"
reg export $key backup.reg
```

## 注意事项

1. **备份**：修改前先备份
2. **权限**：某些键需要管理员权限
3. **重启**：部分修改需要重启生效
4. **谨慎**：错误修改可能导致系统故障

## 参考资料

- [Windows注册表文档](https://docs.microsoft.com/windows/win32/sysinfo/registry)
