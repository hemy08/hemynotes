# Windows网络配置

## 概述

Windows网络配置包括IP地址设置、DNS配置、防火墙规则、网络共享等。

## IP地址配置

### 使用netsh命令

```batch
:: 查看网络接口
netsh interface show interface

:: 查看IP配置
netsh interface ip show config
netsh interface ip show address

:: 设置静态IP
netsh interface ip set address "以太网" static 192.168.1.100 255.255.255.0 192.168.1.1

:: 设置DNS
netsh interface ip set dns "以太网" static 8.8.8.8
netsh interface ip add dns "以太网" 8.8.4.4 index=2

:: 设置DHCP
netsh interface ip set address "以太网" dhcp
netsh interface ip set dns "以太网" dhcp
```

### 使用PowerShell

```powershell
# 查看网络适配器
Get-NetAdapter
Get-NetIPAddress

# 设置静态IP
New-NetIPAddress -InterfaceAlias "以太网" -IPAddress 192.168.1.100 -PrefixLength 24 -DefaultGateway 192.168.1.1

# 设置DNS
Set-DnsClientServerAddress -InterfaceAlias "以太网" -ServerAddresses 8.8.8.8,8.8.4.4

# 设置DHCP
Set-NetIPInterface -InterfaceAlias "以太网" -Dhcp Enabled
Set-DnsClientServerAddress -InterfaceAlias "以太网" -ResetServerAddresses

# 移除IP地址
Remove-NetIPAddress -InterfaceAlias "以太网" -IPAddress 192.168.1.100
```

## 防火墙配置

### netsh advfirewall

```batch
:: 查看防火墙状态
netsh advfirewall show allprofiles

:: 开放端口
netsh advfirewall firewall add rule name="HTTP" dir=in action=allow protocol=tcp localport=80

:: 开放端口范围
netsh advfirewall firewall add rule name="端口范围" dir=in action=allow protocol=tcp localport=8000-9000

:: 开放程序
netsh advfirewall firewall add rule name="MyApp" dir=in action=allow program="C:\app\myapp.exe"

:: 阻止端口
netsh advfirewall firewall add rule name="Block Telnet" dir=in action=block protocol=tcp localport=23

:: 删除规则
netsh advfirewall firewall delete rule name="HTTP"

:: 查看规则
netsh advfirewall firewall show rule name=all
```

### PowerShell防火墙

```powershell
# 查看防火墙状态
Get-NetFirewallProfile

# 开放端口
New-NetFirewallRule -DisplayName "HTTP" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 80

# 开放程序
New-NetFirewallRule -DisplayName "MyApp" -Direction Inbound -Action Allow -Program "C:\app\myapp.exe"

# 查看规则
Get-NetFirewallRule
Get-NetFirewallRule -DisplayName "HTTP"

# 禁用规则
Disable-NetFirewallRule -DisplayName "HTTP"

# 删除规则
Remove-NetFirewallRule -DisplayName "HTTP"
```

## 网络诊断

### ping和traceroute

```batch
:: ping测试
ping 192.168.1.1
ping -n 10 192.168.1.1
ping -l 1000 192.168.1.1    :: 发送1000字节

:: 路由追踪
tracert www.google.com
tracert -d www.google.com   :: 不解析主机名
```

### 端口测试

```batch
:: 使用telnet测试端口
telnet 192.168.1.1 80

:: PowerShell测试端口
powershell -Command "Test-NetConnection -ComputerName 192.168.1.1 -Port 80"
```

### 网络统计

```batch
:: 查看连接
netstat -an
netstat -ano    :: 显示进程ID

:: 查看监听端口
netstat -an | findstr LISTENING

:: 查看特定端口
netstat -an | findstr :80

:: 查看路由表
route print
route print -4
route print -6
```

## 路由配置

```batch
:: 查看路由表
route print

:: 添加静态路由
route add 192.168.2.0 mask 255.255.255.0 192.168.1.1

:: 添加永久路由
route add 192.168.2.0 mask 255.255.255.0 192.168.1.1 -p

:: 删除路由
route delete 192.168.2.0

:: 修改路由
route change 192.168.2.0 mask 255.255.255.0 192.168.1.2
```

## DNS配置

```batch
:: 查看DNS缓存
ipconfig /displaydns

:: 清除DNS缓存
ipconfig /flushdns

:: 使用nslookup
nslookup www.google.com
nslookup www.google.com 8.8.8.8    :: 使用指定DNS服务器
```

## 网络共享

### 共享文件夹

```batch
:: 创建共享
net share MyShare=C:\Share /grant:everyone,full

:: 查看共享
net share

:: 删除共享
net share MyShare /delete

:: 查看远程共享
net view \\server
```

### 访问共享

```batch
:: 映射网络驱动器
net use Z: \\server\share

:: 带认证映射
net use Z: \\server\share /user:username password

:: 断开映射
net use Z: /delete

:: 查看映射
net use
```

## 网络适配器管理

### PowerShell操作

```powershell
# 禁用适配器
Disable-NetAdapter -Name "以太网"

# 启用适配器
Enable-NetAdapter -Name "以太网"

# 重命名适配器
Rename-NetAdapter -Name "以太网" -NewName "LAN"

# 重置适配器
Restart-NetAdapter -Name "以太网"
```

## 代理设置

### 命令行设置

```batch
:: 设置代理
netsh winhttp set proxy proxy-server="http://proxy:8080" bypass-list="localhost;*.local"

:: 查看代理
netsh winhttp show proxy

:: 重置代理
netsh winhttp reset proxy
```

### 注册表设置

```batch
:: 启用IE代理
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d "proxy:8080" /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /t REG_SZ /d "localhost;*.local" /f
```

## 常见网络问题排查

### 重置网络

```batch
:: 重置Winsock
netsh winsock reset

:: 重置IP配置
netsh int ip reset

:: 重置防火墙
netsh advfirewall reset

:: 清除DNS缓存
ipconfig /flushdns

:: 释放并重新获取IP
ipconfig /release
ipconfig /renew
```

### 网络抓包

```powershell
# 使用pktmon（Windows 10+）
pktmon start --capture --etw -p Microsoft-Windows-TCPIP
pktmon stop
pktmon format PktMon.etl -o output.txt
```

## 参考资料

- [Windows网络命令](https://docs.microsoft.com/windows-server/administration/windows-commands/)
- [PowerShell网络模块](https://docs.microsoft.com/powershell/module/nettcpip/)
